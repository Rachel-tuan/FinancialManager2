"""报表导出层：负责 matplotlib Figure 的导出保存。

只接收 Figure 与目标路径，不依赖 tkinter；
失败时抛出原始异常，由调用方（UI 层）处理交互与提示。
"""


def export_figure_png(fig, file_path, dpi=300):
    """将 Figure 保存为 PNG 文件。"""
    fig.savefig(file_path, dpi=dpi, bbox_inches='tight')


def export_figure_pdf(fig, file_path, dpi=300):
    """将 Figure 保存为 PDF 文件。"""
    fig.savefig(file_path, dpi=dpi, format='pdf', bbox_inches='tight')