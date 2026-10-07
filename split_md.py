#!/usr/bin/env python3
"""Split gview6官方说明书.md into chapters by page markers."""
import re, os, pathlib

SRC = "gview6官方说明书.md"
OUT_DIR = "chapters"
os.makedirs(OUT_DIR, exist_ok=True)

CHAPTERS = [
    # (filename, title, page_start, page_end_inclusive, description)
    ("01_界面与基础操作.md", "界面与基础操作", 5, 15, "主界面、工具栏、分子/视图、多视图窗口、鼠标、菜单、偏好设置、Tips"),
    ("02_构建与编辑分子.md", "构建与编辑分子", 16, 46, "元素/基团/环/生物片段、编辑、Clean、 symmetry、键角二面角、显示格式、坐标轴"),
    ("03_高斯计算设置与提交.md", "高斯计算设置与提交", 47, 87, "Calculation Setup 各面板、Checkpoint 读取、各类任务特殊设置、Scan、提交与任务控制、执行方式"),
    ("04_绘图与光谱.md", "绘图与光谱（Plots & Spectra）", 88, 135, "3D Scan 图、Plot 各面板、自定义、右键菜单、参考数据、位移模式、同位素、线型、Spectra 菜单与数据保存"),
    ("05_Cube与表面体积数据.md", "Cube 与表面/体积数据", 136, 149, "Cubes 生成与操作、Surfaces、Contours、等值面平面定义"),
    ("06_选择与原子编辑.md", "选择与原子编辑", 150, 193, "选择工具栏/快捷键、Atom List Editor、原子群组、MO 相关、构象/Grid 搜索、PBC 搭建与文件类型"),
    ("07_文件与分子列表.md", "文件与分子列表", 194, 206, "File List、分子去向、Molecule List、命名、排序、保存操作"),
    ("08_动画与电影.md", "动画与电影", 207, 213, "初始设置、简正振动动画、多视图动画、导出电影"),
    ("09_任务管理与脚本.md", "任务管理与脚本（SC Job Manager）", 214, 226, "提交任务、SC Job Manager 各面板、Job Types、启用配置、命令行变量、自带脚本"),
    ("10_附录.md", "附录", 227, 266, "图标与菜单总表、计算关键词与选项、FAQ、Clean 技巧、表面配色、Windows 文件关联、命令行变量、脚本"),
    ("11_教程.md", "教程（Tutorials）", 267, 332, "多视图/振动动画、建模实例（吡啶、金属羰基物、ONIOM 等）、构象搜索+VCD、PBC 建晶胞系列教程"),
]

with open(SRC, encoding="utf-8") as f:
    text = f.read()

# split by <!-- p.N -->
parts = re.split(r"<!-- p\.(\d+) -->", text)
# parts[0] = header (title+TOC), then pairs (pageno, content)
header = parts[0]
pages = {}
for i in range(1, len(parts), 2):
    pno = int(parts[i])
    content = parts[i+1] if i+1 < len(parts) else ""
    pages[pno] = content

# fix image paths for chapters/ (imgs -> ../imgs)
def fix_imgs(s):
    return s.replace("](imgs/", "](../imgs/")

for fname, title, pstart, pend, desc in CHAPTERS:
    chunks = []
    for p in range(pstart, pend+1):
        if p in pages:
            chunks.append(f"<!-- p.{p} -->\n" + pages[p])
    body = "".join(chunks).strip()
    body = fix_imgs(body)
    out = f"# GaussView 6：{title}（p.{pstart}–{pend}）\n\n> {desc}\n\n> 原文件：`../gview6官方说明书.md`（全量单文件存档）｜图片目录：`../imgs/`\n\n---\n\n" + body + "\n"
    with open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"{fname}: pages {pstart}-{pend}, chars {len(out)}")

# README index
idx = ["# GaussView 6 官方说明书 · 分章索引\n",
       "\n> PDF 共 332 页，已转为 Markdown。单文件全量存档见 `../gview6官方说明书.md`（381KB）；本目录为按主题拆分的 11 章，便于检索与维护。图片统一存放在 `../imgs/`（373 张）。\n",
       "\n## 章节\n"]
for fname, title, pstart, pend, desc in CHAPTERS:
    idx.append(f"- [{title}（p.{pstart}–{pend}）](./{fname})：{desc}\n")
idx.append("\n## 说明\n- 每章内保留 `<!-- p.N -->` 页标记，可回溯 PDF 原页。\n- 标题层级：`#`=一级节（16pt）、`##`=子节（13pt）、`###`=三级（11pt）。\n- 表格已转为 Markdown 表格，图片为 PNG（小图标已过滤）。\n")
with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.writelines(idx)
print("README done")
