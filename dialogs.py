"""UI 弹窗层：记账程序的三个模态对话框。

只负责控件布局、输入校验与结果展示；
业务操作调用 controller，保存成功后的刷新由调用方（on_saved）处理。
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from controller import add_record, set_goal, get_monthly_summary
from services import format_decimal
from config import INCOME, EXPENSE, MONTH_FORMAT, DATE_FORMAT


class AddRecordDialog:
    """添加账单弹窗。"""

    def __init__(self, parent, on_saved=None):
        self.parent = parent
        self.on_saved = on_saved

        self.window = tk.Toplevel(parent)
        self.window.title('添加账单')
        self.window.geometry('400x300')
        self.window.configure(bg='#f5f6fa')
        self.window.resizable(False, False)
        self.window.transient(parent)  # 设置为主窗口的子窗口
        self.window.grab_set()  # 模态窗口

        # 设置窗口样式
        title_label = tk.Label(self.window, text='添加新账单', font=('微软雅黑', 16, 'bold'), bg='#f5f6fa', fg='#273c75')
        title_label.pack(pady=10)

        # 创建表单框架
        form_frame = tk.Frame(self.window, bg='#f5f6fa')
        form_frame.pack(pady=5, fill='both', expand=True)

        # 日期输入
        date_frame = tk.Frame(form_frame, bg='#f5f6fa')
        date_frame.pack(fill='x', pady=5)
        date_label = tk.Label(date_frame, text='日期:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
        date_label.pack(side='left', padx=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime(DATE_FORMAT))
        self.date_entry = tk.Entry(date_frame, textvariable=self.date_var, font=('微软雅黑', 12), width=20)
        self.date_entry.pack(side='left', padx=5)

        # 类型选择
        type_frame = tk.Frame(form_frame, bg='#f5f6fa')
        type_frame.pack(fill='x', pady=5)
        type_label = tk.Label(type_frame, text='类型:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
        type_label.pack(side='left', padx=5)
        self.type_var = tk.StringVar(value=EXPENSE)
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, values=(EXPENSE, INCOME), font=('微软雅黑', 12), width=18, state='readonly')
        type_combo.pack(side='left', padx=5)

        # 金额输入
        amount_frame = tk.Frame(form_frame, bg='#f5f6fa')
        amount_frame.pack(fill='x', pady=5)
        amount_label = tk.Label(amount_frame, text='金额:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
        amount_label.pack(side='left', padx=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = tk.Entry(amount_frame, textvariable=self.amount_var, font=('微软雅黑', 12), width=20)
        self.amount_entry.pack(side='left', padx=5)

        # 用途/备注输入
        note_frame = tk.Frame(form_frame, bg='#f5f6fa')
        note_frame.pack(fill='x', pady=5)
        note_label = tk.Label(note_frame, text='用途/备注:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
        note_label.pack(side='left', padx=5)
        self.note_var = tk.StringVar()
        self.note_entry = tk.Entry(note_frame, textvariable=self.note_var, font=('微软雅黑', 12), width=20)
        self.note_entry.pack(side='left', padx=5)

        # 按钮框架
        btn_frame = tk.Frame(self.window, bg='#f5f6fa')
        btn_frame.pack(pady=10)

        save_btn = tk.Button(btn_frame, text='保存', width=10, font=('微软雅黑', 12), bg='#00b894', fg='white', command=self._save, relief='flat')
        save_btn.pack(side='left', padx=10)

        # 取消按钮
        cancel_btn = tk.Button(btn_frame, text='取消', width=10, font=('微软雅黑', 12), bg='#d63031', fg='white', command=self.window.destroy, relief='flat')
        cancel_btn.pack(side='left', padx=10)

        # 设置初始焦点
        self.date_entry.focus_set()

    def _save(self):
        try:
            ok, message = add_record(self.date_var.get(), self.type_var.get(),
                                     self.amount_var.get(), self.note_var.get())
            if not ok:
                messagebox.showwarning('提示', message, parent=self.window)
                return

            messagebox.showinfo('成功', message, parent=self.window)
            if self.on_saved is not None:
                self.on_saved()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror('错误', f'保存失败: {str(e)}', parent=self.window)


class SetGoalDialog:
    """设置月度目标弹窗。"""

    def __init__(self, parent, on_saved=None):
        self.parent = parent
        self.on_saved = on_saved

        self.window = tk.Toplevel(parent)
        self.window.title('设置月度目标')
        self.window.geometry('400x200')
        self.window.configure(bg='#f5f6fa')
        self.window.resizable(False, False)
        self.window.transient(parent)  # 设置为主窗口的子窗口
        self.window.grab_set()  # 模态窗口

        # 设置窗口样式
        title_label = tk.Label(self.window, text='设置月度支出目标', font=('微软雅黑', 16, 'bold'), bg='#f5f6fa', fg='#273c75')
        title_label.pack(pady=10)

        # 创建表单框架
        form_frame = tk.Frame(self.window, bg='#f5f6fa')
        form_frame.pack(pady=5, fill='both', expand=True)

        # 月份输入
        month_frame = tk.Frame(form_frame, bg='#f5f6fa')
        month_frame.pack(fill='x', pady=5)
        month_label = tk.Label(month_frame, text='月份:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
        month_label.pack(side='left', padx=5)
        self.month_var = tk.StringVar(value=datetime.now().strftime(MONTH_FORMAT))
        self.month_entry = tk.Entry(month_frame, textvariable=self.month_var, font=('微软雅黑', 12), width=20)
        self.month_entry.pack(side='left', padx=5)

        # 目标金额输入
        amount_frame = tk.Frame(form_frame, bg='#f5f6fa')
        amount_frame.pack(fill='x', pady=5)
        amount_label = tk.Label(amount_frame, text='目标金额:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
        amount_label.pack(side='left', padx=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = tk.Entry(amount_frame, textvariable=self.amount_var, font=('微软雅黑', 12), width=20)
        self.amount_entry.pack(side='left', padx=5)

        # 按钮框架
        btn_frame = tk.Frame(self.window, bg='#f5f6fa')
        btn_frame.pack(pady=10)

        save_btn = tk.Button(btn_frame, text='保存', width=10, font=('微软雅黑', 12), bg='#00b894', fg='white', command=self._save, relief='flat')
        save_btn.pack(side='left', padx=10)

        # 取消按钮
        cancel_btn = tk.Button(btn_frame, text='取消', width=10, font=('微软雅黑', 12), bg='#d63031', fg='white', command=self.window.destroy, relief='flat')
        cancel_btn.pack(side='left', padx=10)

        # 设置初始焦点
        self.month_entry.focus_set()

    def _save(self):
        try:
            ok, message = set_goal(self.month_var.get(), self.amount_var.get())
            if not ok:
                messagebox.showwarning('提示', message, parent=self.window)
                return

            messagebox.showinfo('成功', message, parent=self.window)
            if self.on_saved is not None:
                self.on_saved()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror('错误', f'保存失败: {str(e)}', parent=self.window)


class SummaryDialog:
    """月度统计查询弹窗。"""

    def __init__(self, parent):
        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title('月度统计')
        self.window.geometry('400x300')
        self.window.configure(bg='#f5f6fa')
        self.window.resizable(False, False)
        self.window.transient(parent)  # 设置为主窗口的子窗口
        self.window.grab_set()  # 模态窗口

        # 设置窗口样式
        title_label = tk.Label(self.window, text='月度收支统计', font=('微软雅黑', 16, 'bold'), bg='#f5f6fa', fg='#273c75')
        title_label.pack(pady=10)

        # 创建表单框架
        form_frame = tk.Frame(self.window, bg='#f5f6fa')
        form_frame.pack(pady=5, fill='x')

        # 月份输入
        month_frame = tk.Frame(form_frame, bg='#f5f6fa')
        month_frame.pack(fill='x', pady=5)
        month_label = tk.Label(month_frame, text='月份:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
        month_label.pack(side='left', padx=5)
        self.month_var = tk.StringVar(value=datetime.now().strftime(MONTH_FORMAT))
        self.month_entry = tk.Entry(month_frame, textvariable=self.month_var, font=('微软雅黑', 12), width=15)
        self.month_entry.pack(side='left', padx=5)

        # 结果显示框架
        result_frame = tk.Frame(self.window, bg='#f5f6fa')
        result_frame.pack(pady=10, fill='both', expand=True)

        # 结果文本框
        self.result_text = tk.Text(result_frame, font=('微软雅黑', 12), width=35, height=8, bg='white', relief='flat')
        self.result_text.pack(padx=20, pady=5, fill='both', expand=True)

        # 按钮框架
        btn_frame = tk.Frame(self.window, bg='#f5f6fa')
        btn_frame.pack(pady=10)

        query_btn = tk.Button(btn_frame, text='查询', width=10, font=('微软雅黑', 12), bg='#00b894', fg='white', command=self._query, relief='flat')
        query_btn.pack(side='left', padx=10)

        close_btn = tk.Button(btn_frame, text='关闭', width=10, font=('微软雅黑', 12), bg='#d63031', fg='white', command=self.window.destroy, relief='flat')
        close_btn.pack(side='left', padx=10)

        # 初始查询
        self._query()

        # 设置初始焦点
        self.month_entry.focus_set()

    def _query(self):
        month = self.month_var.get().strip()
        if not month:
            month = datetime.now().strftime(MONTH_FORMAT)

        summary = get_monthly_summary(month)
        income, expense, balance = summary['income'], summary['expense'], summary['balance']
        goal_info = summary['goal']

        self.result_text.delete(1.0, tk.END)

        self.result_text.insert(tk.END, f"月份: {month}\n\n")
        self.result_text.insert(tk.END, f"总收入: {format_decimal(income)} 元\n")
        self.result_text.insert(tk.END, f"总支出: {format_decimal(expense)} 元\n")
        self.result_text.insert(tk.END, f"结余: {format_decimal(balance)} 元\n\n")

        if goal_info is not None:
            self.result_text.insert(tk.END, f"本月目标: {format_decimal(goal_info.goal)} 元\n")
            self.result_text.insert(tk.END, f"剩余额度: {format_decimal(goal_info.remaining)} 元 ({goal_info.status})")
        else:
            self.result_text.insert(tk.END, "本月未设置支出目标")

        self.result_text.config(state='disabled')