#!/usr/bin/env python3
"""Convert gview6官方说明书.pdf (text-based, 332 pages) to Markdown."""
import fitz, re, os, pathlib

SRC = "gview6官方说明书.pdf"
OUT_MD = "gview6官方说明书.md"
IMG_DIR = "imgs"

os.makedirs(IMG_DIR, exist_ok=True)
doc = fitz.open(SRC)
toc = doc.get_toc()  # [level, title, page]

def clean_text(t):
    t = t.replace("\u00a0", " ")
    return t

def is_footer_line(s):
    s = s.strip()
    if s in ("GV6 Help",):
        return True
    if re.fullmatch(r"\d{1,3}", s):
        return True
    return False

md = []
md.append("# GaussView 6 官方说明书（PDF 转 Markdown）\n")
md.append(f"> 来源：`{SRC}`，共 {len(doc)} 页，目录 {len(toc)} 条，由 PyMuPDF 直接提取（可复制文本，无需 OCR）。\n")
md.append("## 目录（来自 PDF 书签）\n")
for level, title, pageno in toc:
    indent = "  " * (level - 1)
    md.append(f"{indent}- {title}（p.{pageno}）\n")
md.append("\n---\n")

img_count = 0
# TOC pages are 1-4 (index 0-3); body starts index 4
for pno in range(4, len(doc)):
    page = doc[pno]
    # --- extract images ---
    pix_imgs = []
    for img in page.get_images(full=True):
        xref = img[0]
        try:
            pix = fitz.Pixmap(doc, xref)
        except Exception:
            continue
        if pix.n - pix.alpha > 3:
            try:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            except Exception:
                continue
        # skip tiny icons (<80px)
        if pix.w < 80 or pix.h < 25:
            continue
        img_count += 1
        fname = f"p{pno+1}_{img_count:03d}.png"
        fpath = os.path.join(IMG_DIR, fname)
        try:
            pix.save(fpath)
            # image bbox for ordering
            try:
                bboxes = page.get_image_bbox(img)
                y = bboxes[0].y0 if isinstance(bboxes, list) else bboxes.y0
                if not isinstance(y, (int, float)):
                    y = 1e9
            except Exception:
                y = 1e9
            pix_imgs.append((y, fname))
        except Exception:
            continue
    pix_imgs.sort()

    # --- tables via find_tables ---
    tables_md = []
    table_bboxes = []
    try:
        tabs = page.find_tables()
        for t in tabs:
            try:
                data = t.extract()
            except Exception:
                continue
            if not data or len(data) < 2:
                continue
            # filter empty tables
            nonEmpty = sum(1 for row in data for c in row if str(c).strip())
            if nonEmpty < 4:
                continue
            table_bboxes.append(fitz.Rect(t.bbox))
            rows = []
            ncol = max(len(r) for r in data)
            for r in data:
                cells = [clean_text(str(c or "")).replace("|", "\\|").replace("\n", "<br/>").strip() for c in r]
                cells += [""] * (ncol - len(cells))
                rows.append("| " + " | ".join(cells) + " |")
            sep = "| " + " | ".join(["---"] * ncol) + " |"
            tables_md.append("\n".join([rows[0], sep] + rows[1:]) + "\n")
    except Exception:
        pass

    def in_table(rect):
        for tb in table_bboxes:
            if rect.intersects(tb):
                # block center inside table bbox
                cx = (rect.x0 + rect.x1) / 2
                cy = (rect.y0 + rect.y1) / 2
                if tb.x0 - 2 <= cx <= tb.x1 + 2 and tb.y0 - 2 <= cy <= tb.y1 + 2:
                    return True
        return False

    d = page.get_text("dict")
    blocks = [b for b in d["blocks"] if b["type"] == 0]
    blocks.sort(key=lambda b: (round(b["bbox"][1]), b["bbox"][0]))

    page_lines = []
    for b in blocks:
        rect = fitz.Rect(b["bbox"])
        if in_table(rect):
            continue
        # gather lines
        lines = []
        for l in b["lines"]:
            segs = []
            for s in l["spans"]:
                t = clean_text(s["text"])
                if t.strip() == "":
                    continue
                segs.append((s, t))
            if not segs:
                continue
            line_text = "".join(t for _, t in segs)
            if is_footer_line(line_text):
                continue
            lines.append((segs, line_text))
        if not lines:
            continue
        # heading detection: single-line block, all spans bold & big
        if len(lines) == 1:
            segs, lt = lines[0]
            sizes = {round(s["size"]) for s, _ in segs}
            fonts = {s["font"] for s, _ in segs}
            txt = lt.strip()
            if len(sizes) == 1 and len(txt) >= 3 and not is_footer_line(txt):
                sz = sizes.pop()
                is_bold = any("Bold" in f for f in fonts)
                if is_bold and sz >= 16 and len(txt) < 120:
                    # skip figure-caption junk in toolbar pages? keep as heading if long enough
                    page_lines.append(("h1", "# " + txt + "\n"))
                    continue
                if is_bold and sz == 13 and len(txt) < 150:
                    # filter table-header-like single words inside tables (already skipped by bbox),
                    # keep genuine subheadings: length>8 or multiword
                    if len(txt) > 8 or " " in txt:
                        page_lines.append(("h2", "## " + txt + "\n"))
                        continue
                if is_bold and sz == 11 and len(txt) < 150 and len(txt) > 5:
                    page_lines.append(("h3", "### " + txt + "\n"))
                    continue
        # normal paragraph block: join lines, handle hyphenation
        paras = []
        buf = ""
        for _, lt in lines:
            s = lt.strip()
            if not s or is_footer_line(s):
                continue
            if s.startswith("◦"):
                if buf.strip():
                    paras.append(buf.strip())
                    buf = ""
                paras.append("- " + s[1:].strip())
                continue
            if buf.endswith("-") and len(buf) > 2 and not buf.endswith(" -"):
                # hyphenated line break: remove hyphen, join directly
                buf = buf[:-1] + s.split()[0] + " " + " ".join(s.split()[1:]) if s.split() else buf[:-1]
                # simpler: handled below; redo cleanly
                pass
            if buf == "":
                buf = s
            else:
                if buf.endswith("-"):
                    buf = buf[:-1] + s
                else:
                    buf = buf + " " + s
        if buf.strip():
            paras.append(buf.strip())
        for p in paras:
            # skip dotted TOC leaders if any leaked into body
            if re.search(r"\.{6,}", p) and len(p) > 100:
                continue
            page_lines.append(("p", p + "\n"))

    if not page_lines and not tables_md and not pix_imgs:
        continue
    # page anchor (only add separator, headings come from content)
    md.append(f"\n<!-- p.{pno+1} -->\n")
    for kind, text in page_lines:
        md.append(text + "\n")
    for tmd in tables_md:
        md.append("\n" + tmd + "\n")
    for _, fname in pix_imgs:
        md.append(f"\n![]({IMG_DIR}/{fname})\n")

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.writelines(md)
print(f"done: {OUT_MD}, images: {img_count}")
