import tkinter as tk
from tkinter import messagebox, ttk, font,filedialog
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from decimal import Decimal, ROUND_HALF_UP
from services import monthly_totals, monthly_goal, format_decimal
from storage import load_records, save_records, load_goals, save_goals
from controller import add_record

matplotlib.use('TkAgg')  # 确保使用正确的后端

def open_add_record_window():
    # 创建新窗口
    add_window = tk.Toplevel(root)
    add_window.title('添加账单')
    add_window.geometry('400x300')
    add_window.configure(bg='#f5f6fa')
    add_window.resizable(False, False)
    add_window.transient(root)  # 设置为主窗口的子窗口
    add_window.grab_set()  # 模态窗口
    
    # 设置窗口样式
    title_label = tk.Label(add_window, text='添加新账单', font=('微软雅黑', 16, 'bold'), bg='#f5f6fa', fg='#273c75')
    title_label.pack(pady=10)
    
    # 创建表单框架
    form_frame = tk.Frame(add_window, bg='#f5f6fa')
    form_frame.pack(pady=5, fill='both', expand=True)
    
    # 日期输入
    date_frame = tk.Frame(form_frame, bg='#f5f6fa')
    date_frame.pack(fill='x', pady=5)
    date_label = tk.Label(date_frame, text='日期:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
    date_label.pack(side='left', padx=5)
    date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
    date_entry = tk.Entry(date_frame, textvariable=date_var, font=('微软雅黑', 12), width=20)
    date_entry.pack(side='left', padx=5)
    
    # 类型选择
    type_frame = tk.Frame(form_frame, bg='#f5f6fa')
    type_frame.pack(fill='x', pady=5)
    type_label = tk.Label(type_frame, text='类型:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
    type_label.pack(side='left', padx=5)
    type_var = tk.StringVar(value='支出')
    type_combo = ttk.Combobox(type_frame, textvariable=type_var, values=('支出', '收入'), font=('微软雅黑', 12), width=18, state='readonly')
    type_combo.pack(side='left', padx=5)
    
    # 金额输入
    amount_frame = tk.Frame(form_frame, bg='#f5f6fa')
    amount_frame.pack(fill='x', pady=5)
    amount_label = tk.Label(amount_frame, text='金额:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
    amount_label.pack(side='left', padx=5)
    amount_var = tk.StringVar()
    amount_entry = tk.Entry(amount_frame, textvariable=amount_var, font=('微软雅黑', 12), width=20)
    amount_entry.pack(side='left', padx=5)
    
    # 用途/备注输入
    note_frame = tk.Frame(form_frame, bg='#f5f6fa')
    note_frame.pack(fill='x', pady=5)
    note_label = tk.Label(note_frame, text='用途/备注:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
    note_label.pack(side='left', padx=5)
    note_var = tk.StringVar()
    note_entry = tk.Entry(note_frame, textvariable=note_var, font=('微软雅黑', 12), width=20)
    note_entry.pack(side='left', padx=5)
    
    # 按钮框架
    btn_frame = tk.Frame(add_window, bg='#f5f6fa')
    btn_frame.pack(pady=10)
    
    # 保存按钮
    def save_record():
        try:
            ok, message = add_record(date_var.get(), type_var.get(), amount_var.get(), note_var.get())
            if not ok:
                messagebox.showwarning('提示', message, parent=add_window)
                return
            
            messagebox.showinfo('成功', message, parent=add_window)
            update_summary()
            update_table()
            update_chart()
            add_window.destroy()
        except Exception as e:
            messagebox.showerror('错误', f'保存失败: {str(e)}', parent=add_window)
    
    save_btn = tk.Button(btn_frame, text='保存', width=10, font=('微软雅黑', 12), bg='#00b894', fg='white', command=save_record, relief='flat')
    save_btn.pack(side='left', padx=10)
    
    # 取消按钮
    cancel_btn = tk.Button(btn_frame, text='取消', width=10, font=('微软雅黑', 12), bg='#d63031', fg='white', command=add_window.destroy, relief='flat')
    cancel_btn.pack(side='left', padx=10)
    
    # 设置初始焦点
    date_entry.focus_set()

def open_set_goal_window():
    # 创建新窗口
    goal_window = tk.Toplevel(root)
    goal_window.title('设置月度目标')
    goal_window.geometry('400x200')
    goal_window.configure(bg='#f5f6fa')
    goal_window.resizable(False, False)
    goal_window.transient(root)  # 设置为主窗口的子窗口
    goal_window.grab_set()  # 模态窗口
    
    # 设置窗口样式
    title_label = tk.Label(goal_window, text='设置月度支出目标', font=('微软雅黑', 16, 'bold'), bg='#f5f6fa', fg='#273c75')
    title_label.pack(pady=10)
    
    # 创建表单框架
    form_frame = tk.Frame(goal_window, bg='#f5f6fa')
    form_frame.pack(pady=5, fill='both', expand=True)
    
    # 月份输入
    month_frame = tk.Frame(form_frame, bg='#f5f6fa')
    month_frame.pack(fill='x', pady=5)
    month_label = tk.Label(month_frame, text='月份:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
    month_label.pack(side='left', padx=5)
    month_var = tk.StringVar(value=datetime.now().strftime('%Y-%m'))
    month_entry = tk.Entry(month_frame, textvariable=month_var, font=('微软雅黑', 12), width=20)
    month_entry.pack(side='left', padx=5)
    
    # 目标金额输入
    amount_frame = tk.Frame(form_frame, bg='#f5f6fa')
    amount_frame.pack(fill='x', pady=5)
    amount_label = tk.Label(amount_frame, text='目标金额:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
    amount_label.pack(side='left', padx=5)
    amount_var = tk.StringVar()
    amount_entry = tk.Entry(amount_frame, textvariable=amount_var, font=('微软雅黑', 12), width=20)
    amount_entry.pack(side='left', padx=5)
    
    # 按钮框架
    btn_frame = tk.Frame(goal_window, bg='#f5f6fa')
    btn_frame.pack(pady=10)
    
    # 保存按钮
    def save_goal():
        try:
            month = month_var.get().strip()
            amount_str = amount_var.get().strip()
            
            if not month or not amount_str:
                messagebox.showwarning('提示', '月份和目标金额不能为空！', parent=goal_window)
                return
                
            try:
                amount = float(amount_str)
            except ValueError:
                messagebox.showwarning('提示', '目标金额必须是数字！', parent=goal_window)
                return
            
            if amount <= 0:
                messagebox.showwarning('提示', '目标金额必须为正数！', parent=goal_window)
                return
            
            goals = load_goals()
            goals[month] = amount
            save_goals(goals)
            
            messagebox.showinfo('成功', f'{month} 月支出目标已设置为 {amount:.2f}！', parent=goal_window)
            update_summary()
            update_table()
            update_chart()
            goal_window.destroy()
        except Exception as e:
            messagebox.showerror('错误', f'保存失败: {str(e)}', parent=goal_window)
    
    save_btn = tk.Button(btn_frame, text='保存', width=10, font=('微软雅黑', 12), bg='#00b894', fg='white', command=save_goal, relief='flat')
    save_btn.pack(side='left', padx=10)
    
    # 取消按钮
    cancel_btn = tk.Button(btn_frame, text='取消', width=10, font=('微软雅黑', 12), bg='#d63031', fg='white', command=goal_window.destroy, relief='flat')
    cancel_btn.pack(side='left', padx=10)
    
    # 设置初始焦点
    month_entry.focus_set()

def update_summary():
    month = selected_month.get().strip()
    if not month:
        month = datetime.now().strftime('%Y-%m')
        selected_month.set(month)
    
    data = load_records()
    income, expense, balance = monthly_totals(data, month)
    goal_info = monthly_goal(load_goals(), month, expense)
    
    # 格式化摘要信息
    summary = f"当前月份: {month}\n\n"
    summary += f"本月收入: {format_decimal(income)} 元\n"
    summary += f"本月支出: {format_decimal(expense)} 元\n"
    summary += f"当前结余: {format_decimal(balance)} 元\n\n"
    
    if goal_info is not None:
        summary += f"本月目标: {format_decimal(goal_info.goal)} 元\n"
        summary += f"剩余额度: {format_decimal(goal_info.remaining)} 元\n"
        summary += f"状态: {goal_info.status}"
    else:
        summary += "本月未设置支出目标\n"
        summary += "请点击'设置月目标'按钮"
    
    summary_var.set(summary)

def show_month_summary_ui():
    # 创建新窗口
    summary_window = tk.Toplevel(root)
    summary_window.title('月度统计')
    summary_window.geometry('400x300')
    summary_window.configure(bg='#f5f6fa')
    summary_window.resizable(False, False)
    summary_window.transient(root)  # 设置为主窗口的子窗口
    summary_window.grab_set()  # 模态窗口
    
    # 设置窗口样式
    title_label = tk.Label(summary_window, text='月度收支统计', font=('微软雅黑', 16, 'bold'), bg='#f5f6fa', fg='#273c75')
    title_label.pack(pady=10)
    
    # 创建表单框架
    form_frame = tk.Frame(summary_window, bg='#f5f6fa')
    form_frame.pack(pady=5, fill='x')
    
    # 月份输入
    month_frame = tk.Frame(form_frame, bg='#f5f6fa')
    month_frame.pack(fill='x', pady=5)
    month_label = tk.Label(month_frame, text='月份:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
    month_label.pack(side='left', padx=5)
    month_var = tk.StringVar(value=datetime.now().strftime('%Y-%m'))
    month_entry = tk.Entry(month_frame, textvariable=month_var, font=('微软雅黑', 12), width=15)
    month_entry.pack(side='left', padx=5)
    
    # 结果显示框架
    result_frame = tk.Frame(summary_window, bg='#f5f6fa')
    result_frame.pack(pady=10, fill='both', expand=True)
    
    # 结果文本框
    result_text = tk.Text(result_frame, font=('微软雅黑', 12), width=35, height=8, bg='white', relief='flat')
    result_text.pack(padx=20, pady=5, fill='both', expand=True)
    
    # 查询按钮
    def query_summary():
        month = month_var.get().strip()
        if not month:
            month = datetime.now().strftime('%Y-%m')
            
        data = load_records()
        income, expense, balance = monthly_totals(data, month)
        goal_info = monthly_goal(load_goals(), month, expense)
        
        result_text.delete(1.0, tk.END)
        
        result_text.insert(tk.END, f"月份: {month}\n\n")
        result_text.insert(tk.END, f"总收入: {format_decimal(income)} 元\n")
        result_text.insert(tk.END, f"总支出: {format_decimal(expense)} 元\n")
        result_text.insert(tk.END, f"结余: {format_decimal(balance)} 元\n\n")
        
        if goal_info is not None:
            result_text.insert(tk.END, f"本月目标: {format_decimal(goal_info.goal)} 元\n")
            result_text.insert(tk.END, f"剩余额度: {format_decimal(goal_info.remaining)} 元 ({goal_info.status})")
        else:
            result_text.insert(tk.END, "本月未设置支出目标")
            
        result_text.config(state='disabled')
    
    # 按钮框架
    btn_frame = tk.Frame(summary_window, bg='#f5f6fa')
    btn_frame.pack(pady=10)
    
    query_btn = tk.Button(btn_frame, text='查询', width=10, font=('微软雅黑', 12), bg='#00b894', fg='white', command=query_summary, relief='flat')
    query_btn.pack(side='left', padx=10)
    
    close_btn = tk.Button(btn_frame, text='关闭', width=10, font=('微软雅黑', 12), bg='#d63031', fg='white', command=summary_window.destroy, relief='flat')
    close_btn.pack(side='left', padx=10)
    
    # 初始查询
    query_summary()
    
    # 设置初始焦点
    month_entry.focus_set()

def update_table():
    # 清空表格
    for row in table.get_children():
        table.delete(row)
        
    # 获取选择的月份
    month = selected_month.get().strip()
    if not month:
        month = datetime.now().strftime('%Y-%m')
        selected_month.set(month)
    
    # 加载数据
    data = load_records()
    
    # 过滤当前月份的数据并按日期降序排序
    filtered_data = [r for r in data if r['date'].startswith(month)]
    sorted_data = sorted(filtered_data, key=lambda x: x['date'], reverse=True)
    
    # 填充表格
    for r in sorted_data:
        # 格式化金额，收入为正数，支出为负数
        amount = r['amount']
        if r['category'] == '支出':
            amount_str = f"-{amount:.2f}"
            amount_color = '#d63031'  # 支出用红色
        else:
            amount_str = f"+{amount:.2f}"
            amount_color = '#00b894'  # 收入用绿色
            
        # 插入数据行
        item_id = table.insert('', 'end', values=(r['date'], r['category'], amount_str, r['note']))
        
        # 设置金额列的颜色
        table.tag_configure(f'amount_{item_id}', foreground=amount_color)
        table.item(item_id, tags=(f'amount_{item_id}',))

def export_chart_png():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG 文件", "*.png"), ("所有文件", "*.*")],
                                             title="保存图表为 PNG")
    if file_path:
        fig.savefig(file_path, dpi=300, bbox_inches='tight')
        messagebox.showinfo("导出成功", f"图表已成功保存为 PNG 文件：\n{file_path}")

def export_chart_pdf():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF 文件", "*.pdf"), ("所有文件", "*.*")],
                                             title="保存图表为 PDF")
    if file_path:
        fig.savefig(file_path, dpi=300, format='pdf', bbox_inches='tight')
        messagebox.showinfo("导出成功", f"图表已成功保存为 PDF 文件：\n{file_path}")


root = tk.Tk()
root.title('个人记账管理系统')
root.geometry('1000x700')  # 更大窗口
root.configure(bg='#f5f6fa')  # 柔和背景色
root.resizable(True, True)  # 允许调整窗口大小

# 创建自定义字体
title_font = ('微软雅黑', 18, 'bold')
header_font = ('微软雅黑', 14, 'bold')
normal_font = ('微软雅黑', 12)

# 创建主标题
title_frame = tk.Frame(root, bg='#273c75', height=60)
title_frame.pack(fill='x')
title_label = tk.Label(title_frame, text='个人记账管理系统', font=title_font, bg='#273c75', fg='white')
title_label.pack(pady=10)

# 创建主布局框架
main_frame = tk.Frame(root, bg='#f5f6fa')
main_frame.pack(fill='both', expand=True, padx=20, pady=10)

# 左侧面板 - 包含摘要和按钮
left_panel = tk.Frame(main_frame, bg='#f5f6fa', width=300)
left_panel.pack(side='left', fill='y', padx=(0, 10))
left_panel.pack_propagate(False)  # 防止框架缩小

# 摘要信息
summary_frame = tk.LabelFrame(left_panel, text='本月摘要', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=10)
summary_frame.pack(fill='x', pady=10)

summary_var = tk.StringVar()
summary_label = tk.Label(summary_frame, textvariable=summary_var, justify='left', font=normal_font, bg='#f5f6fa', fg='#273c75')
summary_label.pack(pady=10, anchor='w')

# 按钮区域
btn_frame = tk.LabelFrame(left_panel, text='操作', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=10)
btn_frame.pack(fill='x', pady=10)

# 设置按钮样式
add_btn = tk.Button(btn_frame, text='添加账单', width=14, height=2, font=normal_font, bg='#00b894', fg='white', command=open_add_record_window, relief='flat')
add_btn.pack(fill='x', pady=5)

goal_btn = tk.Button(btn_frame, text='设置月目标', width=14, height=2, font=normal_font, bg='#0984e3', fg='white', command=open_set_goal_window, relief='flat')
goal_btn.pack(fill='x', pady=5)

stat_btn = tk.Button(btn_frame, text='月度统计', width=14, height=2, font=normal_font, bg='#fdcb6e', fg='#2d3436', command=show_month_summary_ui, relief='flat')
stat_btn.pack(fill='x', pady=5)

# 右侧面板 - 
right_panel = tk.Frame(main_frame, bg='#f5f6fa')
right_panel.pack(side='right', fill='both', expand=True)

# 月份选择框架
month_select_frame = tk.Frame(right_panel, bg='#f5f6fa')
month_select_frame.pack(fill='x', padx=10, pady=5)

# 月份选择标签和输入框
month_label = tk.Label(month_select_frame, text='选择月份:', font=('微软雅黑', 12), bg='#f5f6fa', fg='#273c75')
month_label.pack(side='left', padx=5)

# 创建全局月份变量
selected_month = tk.StringVar(value=datetime.now().strftime('%Y-%m'))
month_entry = tk.Entry(month_select_frame, textvariable=selected_month, font=('微软雅黑', 12), width=10)
month_entry.pack(side='left', padx=5)

# 查询按钮
query_btn = tk.Button(month_select_frame, text='查询', font=('微软雅黑', 10), bg='#0984e3', fg='white', 
                      command=lambda: [update_summary(), update_table(), update_chart()], relief='flat')
query_btn.pack(side='left', padx=5)

# 表格区域
table_frame = tk.LabelFrame(right_panel, text='账单记录', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=10)
table_frame.pack(fill='both', expand=True, pady=10)

# 设置表格样式
style = ttk.Style()
style.theme_use('default')
style.configure('Treeview', font=normal_font, rowheight=32, background='#ffffff', fieldbackground='#ffffff')
style.configure('Treeview.Heading', font=('微软雅黑', 13, 'bold'), background='#dff9fb', foreground='#273c75')
style.map('Treeview', background=[('selected', '#0984e3')])

# 创建表格和滚动条
columns = ('日期', '类型', '金额', '用途')
table = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

# 设置表头
table.heading('日期', text='日期')
table.heading('类型', text='类型')
table.heading('金额', text='金额')
table.heading('用途', text='用途/备注')

# 设置列宽
table.column('日期', width=100, anchor='center')
table.column('类型', width=80, anchor='center')
table.column('金额', width=100, anchor='e')  # 右对齐
table.column('用途', width=200)

table.pack(side='left', fill='both', expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')

# 消费分析区域
chart_frame = tk.LabelFrame(right_panel, text='消费分析', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=10)
chart_frame.pack(fill='both', expand=True, pady=10)

# 添加导出按钮区域
export_btn_frame = tk.Frame(chart_frame, bg='#f5f6fa')
export_btn_frame.pack(pady=5)

png_btn = tk.Button(export_btn_frame, text="导出为 PNG", command=export_chart_png,
                    bg="#0984e3", fg="white", font=("微软雅黑", 10), padx=10, pady=5)
png_btn.pack(side='left', padx=10)

pdf_btn = tk.Button(export_btn_frame, text="导出为 PDF", command=export_chart_pdf,
                    bg="#6c5ce7", fg="white", font=("微软雅黑", 10), padx=10, pady=5)
pdf_btn.pack(side='left', padx=10)


# 创建一个带滚动条的框架来容纳图表
chart_canvas_frame = tk.Frame(chart_frame, bg='#f5f6fa')
chart_canvas_frame.pack(fill='both', expand=True)

# 创建画布和滚动条
chart_canvas = tk.Canvas(chart_canvas_frame, bg='#f5f6fa', highlightthickness=0)
chart_scrollbar = ttk.Scrollbar(chart_canvas_frame, orient='vertical', command=chart_canvas.yview)
chart_canvas.configure(yscrollcommand=chart_scrollbar.set)

# 添加水平滚动条
chart_h_scrollbar = ttk.Scrollbar(chart_canvas_frame, orient='horizontal', command=chart_canvas.xview)
chart_canvas.configure(yscrollcommand=chart_scrollbar.set, xscrollcommand=chart_h_scrollbar.set)

# 放置画布和滚动条
chart_scrollbar.pack(side='right', fill='y')
chart_canvas.pack(side='left', fill='both', expand=True)
chart_h_scrollbar.pack(side='bottom', fill='x')

# 创建一个框架放在画布上
chart_inner_frame = tk.Frame(chart_canvas, bg='#f5f6fa')
chart_canvas.create_window((0, 0), window=chart_inner_frame, anchor='nw')

# 创建图表
fig = plt.Figure(figsize=(12, 16), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=chart_inner_frame)
canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)


# 鼠标横向滚动（Shift+滚轮）
def _on_shift_mousewheel(event):
    chart_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
chart_canvas.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

# 更新图表函数
def update_chart():
    month = selected_month.get().strip()
    if not month:
        month = datetime.now().strftime('%Y-%m')
        selected_month.set(month)

    data = load_records()
    usage = {}
    for r in data:
        if r['category'] == '支出' and r['date'].startswith(month):
            usage[r['note']] = usage.get(r['note'], 0) + r['amount']

    ax.clear()
    if usage:
        # 设置中文字体，解决方框显示问题
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False

        # 按金额从大到小排序
        sorted_usage = sorted(usage.items(), key=lambda x: x[1], reverse=True)
        labels = [item[0] for item in sorted_usage]
        sizes = [item[1] for item in sorted_usage]

        # 计算总支出
        total = sum(sizes)

        # 使用更好看的颜色方案
        colors = ['#00b894', '#00cec9', '#0984e3', '#6c5ce7', '#fdcb6e', '#e84393', '#d63031', '#e17055', '#74b9ff']
        # 如果颜色不够，循环使用
        if len(labels) > len(colors):
            colors = colors * (len(labels) // len(colors) + 1)

        # 创建水平条形图
        bars = ax.barh(labels, sizes, color=colors[:len(labels)], height=1)

        # 在条形上添加数值和百分比标签
        for i, bar in enumerate(bars):
            width = bar.get_width()
            percentage = width / total * 100
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{width:.2f}元 ({percentage:.1f}%)',
                   va='center', fontsize=11, fontfamily='SimHei')

        # 设置图表标题和标签
        ax.set_title(f'{month} 用途消费分布', fontsize=16, fontweight='bold', pad=20, fontfamily='SimHei')
        ax.set_xlabel('支出金额 (元)', fontsize=12, fontfamily='SimHei')

        # 设置Y轴标签字体大小和字体
        ax.tick_params(axis='y', labelsize=10)
        for label in ax.get_yticklabels():
            label.set_fontfamily('SimHei')

        # 根据条目数量调整图表高度
        fig.set_figheight(max(5, len(labels) * 0.6))
        fig.set_figwidth(12)  # 加宽
    else:
        ax.text(0.5, 0.5, '本月暂无支出', ha='center', va='center', fontsize=14, fontweight='bold', fontfamily='SimHei')

    # 自动调整布局
    fig.tight_layout()
    canvas.draw()

    # 更新滚动区域
    chart_inner_frame.update_idletasks()
    chart_canvas.config(scrollregion=chart_canvas.bbox('all'))
    chart_canvas.configure(yscrollcommand=chart_scrollbar.set, xscrollcommand=chart_h_scrollbar.set)

    # 绑定鼠标滚轮事件
    def _on_mousewheel(event):
        chart_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    chart_canvas.bind_all("<MouseWheel>", _on_mousewheel)



update_summary()
update_table()
update_chart()

root.mainloop()