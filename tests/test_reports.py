"""reports 层测试：PNG/PDF 导出参数与异常传递。"""

import re
import inspect

import pytest

from reports import export_figure_png, export_figure_pdf


class FakeFig:
    def __init__(self):
        self.calls = []

    def savefig(self, *args, **kwargs):
        self.calls.append((args, kwargs))


class BoomFig:
    def savefig(self, *args, **kwargs):
        raise PermissionError('denied')


def test_export_png_passes_correct_args():
    fig = FakeFig()
    export_figure_png(fig, '/tmp/x.png')
    expected = [(('/tmp/x.png',), {'dpi': 300, 'bbox_inches': 'tight'})]
    assert fig.calls == expected, f"PNG 导出参数不符: {fig.calls}"


def test_export_pdf_passes_correct_args():
    fig = FakeFig()
    export_figure_pdf(fig, '/tmp/x.pdf')
    expected = (('/tmp/x.pdf',), {'dpi': 300, 'format': 'pdf', 'bbox_inches': 'tight'})
    assert fig.calls[-1] == expected, f"PDF 导出参数不符: {fig.calls[-1]}"


def test_exception_propagates():
    with pytest.raises(PermissionError) as ei:
        export_figure_png(BoomFig(), '/tmp/y.png')
    assert str(ei.value) == 'denied', "异常信息被篡改"


def test_no_tkinter_dependency():
    src = inspect.getsource(__import__('reports'))
    for line in src.splitlines():
        if re.match(r'\s*(import|from)\s', line):
            assert 'tkinter' not in line, f"意外依赖: {line}"