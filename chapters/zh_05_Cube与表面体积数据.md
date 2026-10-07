# GaussView 6：Cube 与表面/体积数据（p.136–149）

> Cube 的生成与操作、表面（Surfaces）、等值线（Contours）、等值面平面定义

> 原文件：`../gview6官方说明书.md`（全量单文件存档）｜图片目录：`../imgs/`

---

<!-- p.136 -->

## 表面与等值线（Surfaces and Contours）

结果（Results）=>表面/等值线（Surfaces/Contours）菜单项用于打开 GaussView 表面与等值线（Surfaces and Contours）对话框（如下图所示）。它允许您以三维形式显示各种化学数据。体积数据可以由 Gaussian 检查点（checkpoint）文件生成，也可以从 Cube 文件中读入。请注意，实际显示一个表面（surface）包括两个步骤：

- 通过生成或读入获得一个 Cube。

- 生成用于显示的实际表面或等值线。

该对话框允许您选择 Cube 以显示为表面和/或等值线，也可对当前已显示的表面和等值线进行操作。

表面与等值线对话框（Surfaces and Contours Dialog）

该对话框的三个区域分别控制 Cube（体积数据集，例如分子轨道和电子密度）、表面（叠加在分子显示上的 Cube 数据三维图）、等值线（投影到某一平面上的 Cube 数据）。

## Cube

Cube 操作（Cube Actions）菜单包含以下项目：

- 新建 Cube（New Cube）：打开生成 Cube（Generate Cube）对话框，您可在此选择要为该文件创建的 Cube 类型并指定其属性。新 Cube 随后会被加入可用 Cube 列表，可用于生成表面和等值线。

- 载入 Cube（Load Cube）：从外部文件读入 Cube 数据。该 Cube 可以是先前由 GaussView 保存的，也可以是由 cubegen 工具独立生成的。

- 保存 Cube（Save Cube）：允许您保存 Cube 以供日后使用。


![](../imgs/p136_142.png)

<!-- p.137 -->

- 删除 Cube（Remove Cube）：从列表中删除一项。如果该 Cube 是从外部文件载入或已保存的，则文件不受影响。如果该 Cube 是在本次会话中生成的且未保存，则数据将被丢弃，日后查看时必须重新生成。

## 体积数据的可视化（Visualizing Volumetric Data）

表面操作（Surface Actions）和等值线操作（Contour Actions）菜单上的新建…（New …）项目作用于当前选中的 Cube。其他项目作用于当前表面/等值线（即当前视图窗口（view window）中的那一个）。

该对话框底部的复选框同时适用于表面和等值线：

- 为新表面/等值线添加视图（Add views for new surfaces/contours）：（源文无说明）

- 将操作应用于分子组（Apply actions to molecule group）：（源文无说明）

## 表面（Surfaces）

表面操作（Surface Actions）菜单包含以下项目：

- 新建表面（New Surface）：由当前选中的 Cube 生成一个新表面，并将其加入可查看的可用表面列表。

- 新建映射表面（New Mapped Surface）：打开表面映射（Surface Mapping）对话框，您可在此决定要生成的表面类型以及由哪个 Cube 生成。所生成的表面是指定属性的按比例缩放的热图。创建后，它会被加入可显示的表面列表。

- 显示表面（Show Surface）：显示被隐藏的表面。

- 隐藏表面（Hide Surface）：隐藏一个表面。

- 删除表面（Remove Surface）：从可显示的表面列表中删除一个表面。若要再次查看，必须重新生成。

表面列表下方的新表面的等值（Isovalue）字段控制所生成表面的特征。修改其数值将应用于随后生成的表面，但不影响已有表面。一般不应更改这些数值。注意：比较来自不同分子但使用了不同等值（isovalue）的表面通常会产生误导。

## 等值线（Contours）

等值线操作（Contour Actions）菜单包含以下项目：

- 新建等值线（New Contour）：打开生成等值线（Generate Contours）窗口。用于创建新的等值线。

- 显示等值线（Show Contour）：显示被隐藏的等值线。

- 隐藏等值线（Hide Contour）：隐藏一条等值线。

- 删除等值线（Remove Contour）：从可显示的等值线列表中删除一条等值线。若要再次查看，必须重新生成。

## Cube 的生成与操作（Generating and Manipulating Cubes）

表面与等值线对话框中 Cube 操作（Cube Actions）菜单上的新建 Cube（New Cube）选项将弹出下图所示的对话框。它用于由检查点（checkpoint）文件中的电子密度和其他数据生成新的 Cube。GaussView 会自动调用 CubeGen 工具。


<!-- p.138 -->

类型（Type）弹出菜单用于选择要生成 Cube 的分子属性。对于大多数选项，还会出现附加字段以进一步指定所需数据。例如，在下图中，可以选择生成静电势 Cube 时使用的密度矩阵。类似地，对于分子轨道，通过附加字段指明要生成的具体轨道。

生成 Cube 对话框（Generate Cubes Dialog）

该对话框将生成类型（Type）字段中指定的 Cube 类型。这里，我们正在由 SCF 电子密度（默认冻芯）计算生成静电势的 Cube。

网格（Grid）字段用于指定 Cube 的密度。密度越高，计算量越大。一般来说，默认的粗（Coarse）设置足以满足大多数可视化目的；中（Medium）足以满足大多数打印和展示目的。粗（Coarse）、中（Medium）、细（Fine）每种选项对应的每“边”等效点数显示在该行第二个字段中。使用自定义（Custom）项可指定不同的数值。

单击确定（Ok）按钮将生成该 Cube（作为后台计算）并退出对话框。新 Cube 将在计算完成后出现在可用 Cube（Cubes Available）列表中。您可以通过计算（Calculate）=>当前任务（Current Jobs）菜单项或等效的当前任务（Current Jobs）按钮查看该任务。注意：以这种方式即时生成的 Cube 除非您明确保存，否则不会保存到磁盘；否则 GaussView 退出时它们将丢失。

类型（Type）弹出菜单中有若干项目允许您对一个或多个 Cube 进行变换：您可以对 Cube 进行缩放和平方，以及对两个 Cube 相加或相减。例如，如果您想显示差分密度，可以载入两个 Cube 文件（例如在气相和溶液中计算的密度）。载入后，您可以创建一个新 Cube（通过 Cube 操作（Cube Actions）=>新建 Cube（New Cube）），然后从类型（Type）菜单中选择减去两个 Cube（Subtract Two Cubes）。

创建作为两个密度之差的 Cube（Creating a Cube as the Difference of Two Densities）

该对话框创建的新 Cube 是两个源 Cube 对应数值之差。


![](../imgs/p138_143.png)

![](../imgs/p138_144.png)

<!-- p.139 -->

## 生成映射表面（Generating Mapped Surfaces）

GaussView 还允许您将一种属性的值映射到另一种属性的等值面上，换句话说，创建一个其着色由第二种属性值决定的表面。下面右侧窗口显示了按静电势数值着色的甲醛电子密度表面。

创建映射表面（Creating a Mapped Surface）

该对话框中各字段的用途如下：

- 使用现有 Cube（Use an existing cube）：将当前 Cube 之一用作着色数据。当选中此项时，从出现的列表中选择所需的表面。

- 仅在表面点处生成数值（Generate values only at surface points）：在每个表面点处即时生成着色数据。这通常是更快的选择。在弹出菜单和其他字段中指定所需的着色数据表面。

视图窗口（view window）显示映射表面，并在顶部包含颜色映射工具栏（如上图中右侧窗口所示）。映射表面渲染所用的颜色基于最小值与最大值之间的均匀缩放，如光谱（spectrum）左右两侧文本框中的数值所指定（分别为最小值和最大值）。更改这些框中的数值将改变颜色标尺，并相应改变映射表面上的着色。与其他工具栏一样，该颜色映射工具栏可通过单击握柄条并按住拖动，在窗口内移动。


![](../imgs/p139_145.png)

<!-- p.140 -->

## 自定义表面显示（Customizing Surface Displays）

表面可以实心、透明和线框网格形式显示。表面显示可通过显示格式（Display Format）对话框的表面（Surface）面板进行修改（通过视图（View）=>显示格式（Display Format）菜单项及工具栏上等效的显示格式（Display Format）按钮进入）。下图所示为透明表面的对话框格式。

自定义表面显示（Customizing a Surface Display）这里我们正在修改一个透明表面。

对于透明表面，透明选项（Transparent Options）滑块用于改变透明表面的不透明度，淡化映射表面数值（Fade mapped surface value）复选框可使光谱（spectrum）中段范围的数值变为透明（即接近零的那些数值）。

其余控件在所有表面类型的对话框中都存在。

- 等值（IsoValues）弹出菜单控制显示正值、负值还是两者（默认）。

- 隐藏背面（Hide backside）复选框控制是否显示表面的背面。选中后，透明表面的透明度会提高。尝试在格式（Format）设为网格（Mesh）时打开和关闭它，以确切了解被隐藏或显示的内容。

- Z 裁剪（Z-Clip）滑块可用于去除图像最前面的部分，以便观察分子显示的内部。

表面属性的默认值可通过显示格式首选项（Display Format Preferences）的表面（Surface）面板设置，其中包含相同的控件。


![](../imgs/p140_146.png)

<!-- p.141 -->

## 生成等值线（Generating Contours）

等值线（contour）是 Cube 数据在某一平面上的二维投影。它们同样使用在表面与等值线对话框中生成的 Cube。您可以使用等值线操作（Contour Actions）菜单上的项目创建新等值线（新建等值线（New Contour））、显示或隐藏等值线（显示等值线（Show Contour）和隐藏等值线（Hide Contour）），以及删除等值线（删除等值线（Remove Contour））。下图显示了一个等值线显示示例。

等值线图示例（Example Contour Plot）该等值线将 HOMO 投影到 垂直于 C=O 键的平面上。

下图显示了选择等值线操作（Contour Actions）=>新建等值线（New Contour）后出现的对话框。


![](../imgs/p141_147.png)

<!-- p.142 -->

生成等值线对话框（Generate Contours Dialog）

该对话框将由先前通过表面与等值线对话框中 Cube 操作（Cube Actions）菜单创建或载入的现有 Cube 生成等值线。它包含四个子区域：

- 二维网格（2-D Grid）：指定用于计算等值线点的网格特征。您用弹出菜单指定该区域中数值的单位。U 和 V 字段指定两个网格方向上的最小值和最大值，分辨率（Resolution）字段指定网格点之间的距离。

- 平面（Plane）：指定绘制等值线的平面。该项在下文讨论。

- Cube：选择等值线数据的来源：现有 Cube（从列表中选择）或为平面网格明确生成数值。后者在上图中示出；后者类似于映射表面的对应功能。

- 等值（IsoValues）：指定计算等值线所用的一系列等值。在此列表中可根据需要添加或删除项目。

## 定义等值线平面（Defining the Contour Plane）

默认情况下，等值线平面定义为视图的 XY 平面。平面可在等值线对话框的平面（Plane）区域中定义。它被定义为垂直于对话框中指定的法线（Normal）和原点（Origin）两点所定义的矢量的平面。默认原点为 (0,0,0)，定义法向矢量的默认点为 (0,0,1)。

单击定义平面（Define Plane）按钮可指定更复杂的平面定义，将弹出下图所示的对话框。定义平面有两种方法：法向量（Normal Vector）（如上所述）和三点（Three Points）（如图所示）。在后一种方法中，您定义原点和其他两点来定义等值线平面（传统上称为 O、P 和 Q）。最简便的方法是为这些点指定原子，也可以输入原子列表（此时将使用其坐标的平均值）或完全任意的笛卡尔坐标。


![](../imgs/p142_148.png)

<!-- p.143 -->

指定所需的等值线平面（Specifying the Desired Contour Plane）

在本例中，我们使用三点定义法，将等值线平面定义为包含碳原子的平面。视图窗口（view window）中的绿色线条表示在原点（O）处的法向量（标记为 N）以及 OQ 连线。OP 连线在此视图中不可见，因为它与原子 1 和 5 之间的 C-C 键重合。

定义等值线平面后，您可以使用对话框底部区域的弹出菜单和其他控件进一步移动它。平面可以沿各种已定义的轴平移或旋转。


![](../imgs/p143_149.png)

<!-- p.144 -->

## PCM 溶剂化空腔（PCM Solvation Cavity）

PCM 溶剂化显示对话框（PCM Solvation Display Dialog）

PCM 溶剂化显示（PCM Solvation Display）显示由 SCRF=Read 功能的 PrintSpheres 附加关键字计算的溶剂化空腔。

选中显示表面（Show Surface）按钮时，将激活分子的整体表面。其格式可通过下方的三个复选框指定。

选中显示实心（Show Solid）按钮时，将表面显示为实心，遮住分子。选中显示网格（Show Mesh）按钮时，将表面显示为网格，仍可看到表面之下的原子和化学键。选中显示点（Show Points）按钮时，将表面显示为一系列点，比显示网格（Show Mesh）显示能更好地观察原子和化学键。可以同时使用多种显示类型。

颜色（Color）菜单允许您选择表面显示的颜色。如果选中按原子着色（Color by Atom）按钮，则此功能不可用，该按钮将使用生成表面各部分的原子的颜色对表面的不同部分着色。

剔除背面（Cull Backside）按钮可去除分子“背后”的那部分表面。这有时可以改善显示效果。

剔除背面（Cull Backside）按钮下方的下拉菜单仅在选中显示网格（Show Mesh）和显示点（Show Points）按钮时可用。其选项有小（Small）、中（Medium）和大（Large）。它们控制围绕分子的网格线或点的大小。

实心不透明度（Solid Opacity）滑块仅在选中显示实心（Show Solid）或显示网格（Show Mesh）时可用。该滑块控制表面的不透明/透明程度。滑块左端对应完全透明的表面（不可见），右端对应完全不透明的表面。


![](../imgs/p144_150.png)

<!-- p.145 -->

## 原子属性（Atom Properties）

原子属性对话框（Atom Properties dialog）

原子属性（Atom Properties）对话框用于可视化已完成的 Gaussian 计算中的原子属性。名称（Name）菜单允许您选择要显示的原子属性（仅 Gaussian 日志/检查点（checkpoint）文件中存在的项目可用）。此处的示例将使用 Mulliken 电荷属性进行演示。

颜色范围（Color Range）字段指定用于按属性值给原子着色的颜色范围的端点值。默认情况下，范围取自数据中存在的最小值和最大值。

对称颜色范围（Symmetric Range for Color）复选框将强制颜色范围（Color Range）输入对最小值和最大值使用相同的绝对值。默认值为 ±max(|data_max|,|data_min|)。

固定颜色范围（Fixed Range for Color）复选框允许您在颜色范围（Color Range）输入中输入自己的数值。

显示颜色（Show Colors）复选框按颜色范围（Color Range）字段中的设置给原子着色：

原子着色（Atom Coloring）原子按其预测的 Mulliken 电荷着色。

显示数值（Show Numbers）复选框在视图窗口（view window）中显示每个原子的数值型属性值：


![](../imgs/p145_151.png)

![](../imgs/p145_152.png)

<!-- p.146 -->

属性值显示（Property Value Display）每个原子标注其预测的 Mulliken 电荷。

您可以用关闭（Close）或取消（Cancel）按钮退出对话框。关闭（Close）在对话框关闭后保持原子属性显示，而取消（Cancel）则恢复正常的视图（View）显示。


![](../imgs/p146_153.png)

<!-- p.147 -->

## 键属性（Bond Properties）

键属性（Bond Properties）对话框用于直观显示预测的键长和键级。名称（Name）菜单控制当前激活的属性显示。

显示数值（Show Numbers）复选框显示每条键的所选属性：

键长数值显示（Bond Lengths Numeric Display）本例显示以 Å 为单位的键长。

显示颜色（Show Colors）复选框按颜色范围（Color Range）字段中的设置给原子着色。颜色范围（Color Range）字段指定用于按属性值给原子着色的颜色范围的端点值。默认情况下，范围取自数据中存在的最小值和最大值。对称颜色范围（Symmetric Range for Color）复选框将强制颜色范围（Color Range）输入对最小值和最大值使用相同的绝对值。默认值为 ±max(|data_max|,|data_min|)。

固定颜色范围（Fixed Range for Color）复选框允许您在颜色范围（Color Range）输入中输入自己的数值。


![](../imgs/p147_154.png)

<!-- p.148 -->

按键级着色（Coloring by Bond Order）本例在球棍显示模式下按键级 给键着色：红色=单键，绿色=双键，黑色=共振键。

您可以用关闭（Close）或取消（Cancel）按钮退出对话框。关闭（Close）在对话框关闭后保持原子属性显示，而取消（Cancel）则恢复正常的视图（View）显示。


![](../imgs/p148_155.png)

<!-- p.149 -->

## 显示 Gaussian 中计算的原子电荷（Displaying Atomic Charges Computed in Gaussian）

结果（Results）=>电荷分布（Charge Distribution）菜单项用于打开显示原子电荷（Display Atomic Charges）对话框（见下图）。该工具管理 Gaussian 中各种方法计算的部分电荷密度的显示。在对话框的原子电荷（Atomic Charges）区域中，可显示默认的 Mulliken 电荷以及该任务可用的其他计算电荷。类型（Type）菜单列出可用的选项。

显示原子电荷（Displaying Atomic Charges）左侧对话框用于控制显示哪些电荷以及如何显示。中间窗口显示数值型电荷数显示，右侧窗口显示 按电荷着色的原子（反映左侧对话框中的设置），以及偶极矩矢量。

默认情况下，电荷显示的颜色光谱（spectrum）通过读取为该分子计算的最大电荷并设置范围与之匹配来设定。也可以通过在颜色范围（Color Range）字段中输入数值手动调整范围。

该对话框上部其余复选框的含义如下：

- 显示数值（Show Numbers）：在每个原子旁放置原子电荷值。

- 按电荷给原子着色（Color Atoms by Charge）：按颜色范围（Color Range）字段和对称颜色范围（Symmetric Color Range）复选框的规定，按原子电荷给每个原子重新着色。

- 对称颜色范围（Symmetric Color Range）：强制电荷范围的正负限具有相同的绝对大小（无论原子电荷值的实际范围如何）。

- 固定颜色范围（Fixed Color Range）：强制电荷显示使用默认固定范围。该范围默认设为 -1.0 到 1.0，可在电荷分布首选项（Charge Distribution Preferences）中修改。

对话框的偶极矩（Dipole Moment）区域控制显示中是否包含表示偶极矩的矢量。显示该矢量时，可以指定矢量长度的缩放因子（默认约为 1.0）及其原点。后者的可用取值如前图所示。

显示电荷分布（Display Charge Distribution）对话框底部的按钮控制对话框关闭后显示是否保留。单击关闭（Close）将保留原子电荷（Atomic Charges）显示，而单击取消（Cancel）将使视图窗口（view window）恢复正常状态。


![](../imgs/p149_156.png)
