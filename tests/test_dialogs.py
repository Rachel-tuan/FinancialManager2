"""dialogs 层测试：保存回调、校验失败、查询流程。

基于 tests/stubs 中的 tkinter / matplotlib 桩运行，无需真实 GUI。
"""

import json
import os

import tkinter as tk
import 记账程序 as fm
from dialogs import AddRecordDialog, SetGoalDialog, SummaryDialog


def _root_and_app(data_dir):
    root = tk.Tk()
    app = fm.FinanceApp(root)
    return root, app


def test_add_record_dialog_save_callback_and_persist(data_dir):
    calls = []
    root, app = _root_and_app(data_dir)
    dlg = AddRecordDialog(root, on_saved=lambda: calls.append('saved'))
    dlg.date_var.set('2026-08-01')
    dlg.type_var.set('支出')
    dlg.amount_var.set('88.5')
    dlg.note_var.set('测试备注')
    dlg._save()
    assert calls == ['saved'], f"成功保存后 on_saved 未被调用: {calls}"
    assert os.path.exists('records.json'), "未写入 records.json"
    data = json.load(open('records.json', encoding='utf-8'))
    assert data[0] == {'date': '2026-08-01', 'category': '支出', 'amount': 88.5, 'note': '测试备注'}


def test_add_record_dialog_validation_failure(data_dir):
    calls = []
    root, app = _root_and_app(data_dir)
    dlg = AddRecordDialog(root, on_saved=lambda: calls.append('saved'))
    dlg.amount_var.set('abc')
    dlg._save()
    assert calls == [], f"校验失败不应触发 on_saved: {calls}"
    assert not os.path.exists('records.json'), "校验失败却写入了数据"


def test_set_goal_dialog_save_callback_and_persist(data_dir):
    calls = []
    root, app = _root_and_app(data_dir)
    dlg = SetGoalDialog(root, on_saved=lambda: calls.append('saved'))
    dlg.month_var.set('2026-08')
    dlg.amount_var.set('2000')
    dlg._save()
    assert calls == ['saved'], "SetGoal 成功后 on_saved 未被调用"
    goals = json.load(open('goals.json', encoding='utf-8'))
    assert goals == {'2026-08': 2000.0}


def test_summary_dialog_query_flow(data_dir):
    root, app = _root_and_app(data_dir)
    dlg = SummaryDialog(root)
    dlg.month_var.set('2026-08')
    dlg._query()


def test_finance_app_entry_passthrough(data_dir):
    root, app = _root_and_app(data_dir)
    app.open_add_record_window()
    app.open_set_goal_window()
    app.show_month_summary_ui()
    app.refresh_views()