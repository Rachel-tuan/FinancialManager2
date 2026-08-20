import tkinter as tk
from tkinter import messagebox, ttk, font,filedialog
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from decimal import Decimal, ROUND_HALF_UP
from services import format_decimal
from controller import get_monthly_summary, get_monthly_records, get_usage_breakdown
from dialogs import AddRecordDialog, SetGoalDialog, SummaryDialog

matplotlib.use('TkAgg')  # 确保使用正确的后端

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.create_widgets()
        self.update_summary()
        self.update_table()
        self.update_chart()

    def open_add_record_window(self):
        AddRecordDialog(self.root, on_saved=self.refresh_views)

    def open_set_goal_window(self):
        SetGoalDialog(self.root, on_saved=self.refresh_views)

    def show_month_summary_ui(self):
        SummaryDialog(self.root)

    def refresh_views(self):
        self.update_summary()
        self.update_table()
        self.update_chart()

    def update_summary(self):
        month = self.selected_month.get().strip()
        if not month:
            month = datetime.now().strftime('%Y-%m')
            self.selected_month.set(month)

        summary = get_monthly_summary(month)
        income, expense, balance = summary['income'], summary['expense'], summary['balance']
        goal_info = summary['goal']

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

        self.summary_var.set(summary)

    def show_month_summary_ui(self):
        SummaryDialog(self.root)

    def update_table(self):
        # 清空表格
        for row in self.table.get_children():
            self.table.delete(row)

        # 获取选择的月份
        month = self.selected_month.get().strip()
        if not month:
            month = datetime.now().strftime('%Y-%m')
            self.selected_month.set(month)

        # 获取当前月份数据并按日期降序排序
        sorted_data = sorted(get_monthly_records(month), key=lambda x: x['date'], reverse=True)

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
            item_id = self.table.insert('', 'end', values=(r['date'], r['category'], amount_str, r['note']))

            # 设置金额列的颜色
            self.table.tag_configure(f'amount_{item_id}', foreground=amount_color)
            self.table.item(item_id, tags=(f'amount_{item_id}',))

    def export_chart_png(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG 文件", "*.png"), ("所有文件", "*.*")],
                                                 title="保存图表为 PNG")
        if file_path:
            self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
            messagebox.showinfo("导出成功", f"图表已成功保存为 PNG 文件：\n{file_path}")

    def export_chart_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF 文件", "*.pdf"), ("所有文件", "*.*")],
                                                 title="保存图表为 PDF")
        if file_path:
            self.fig.savefig(file_path, dpi=300, format='pdf', bbox_inches='tight')
            messagebox.showinfo("导出成功", f"图表已成功保存为 PDF 文件：\n{file_path}")


    def create_widgets(self):
        self.root.title('个人记账管理系统')
        self.root.geometry('1000x700')  # 更大窗口
        self.root.configure(bg='#f5f6fa')  # 柔和背景色
        self.root.resizable(True, True)  # 允许调整窗口大小

        # 创建自定义字体
        title_font = ('微软雅黑', 18, 'bold')
        header_font = ('微软雅黑', 14, 'bold')
        normal_font = ('微软雅黑', 12)

        # 创建主标题
        title_frame = tk.Frame(self.root, bg='#273c75', height=60)
        title_frame.pack(fill='x')
        title_label = tk.Label(title_frame, text='个人记账管理系统', font=title_font, bg='#273c75', fg='white')
        title_label.pack(pady=10)

        # 创建主布局框架
        main_frame = tk.Frame(self.root, bg='#f5f6fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # 左侧面板 - 包含摘要和按钮
        left_panel = tk.Frame(main_frame, bg='#f5f6fa', width=300)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)  # 防止框架缩小

        # 摘要信息
        summary_frame = tk.LabelFrame(left_panel, text='本月摘要', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=10)
        summary_frame.pack(fill='x', pady=10)

        self.summary_var = tk.StringVar()
        summary_label = tk.Label(summary_frame, textvariable=self.summary_var, justify='left', font=normal_font, bg='#f5f6fa', fg='#273c75')
        summary_label.pack(pady=10, anchor='w')

        # 按钮区域
        btn_frame = tk.LabelFrame(left_panel, text='操作', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=10)
        btn_frame.pack(fill='x', pady=10)

        # 设置按钮样式
        add_btn = tk.Button(btn_frame, text='添加账单', width=14, height=2, font=normal_font, bg='#00b894', fg='white', command=self.open_add_record_window, relief='flat')
        add_btn.pack(fill='x', pady=5)

        goal_btn = tk.Button(btn_frame, text='设置月目标', width=14, height=2, font=normal_font, bg='#0984e3', fg='white', command=self.open_set_goal_window, relief='flat')
        goal_btn.pack(fill='x', pady=5)

        stat_btn = tk.Button(btn_frame, text='月度统计', width=14, height=2, font=normal_font, bg='#fdcb6e', fg='#2d3436', command=self.show_month_summary_ui, relief='flat')
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
        self.selected_month = tk.StringVar(value=datetime.now().strftime('%Y-%m'))
        month_entry = tk.Entry(month_select_frame, textvariable=self.selected_month, font=('微软雅黑', 12), width=10)
        month_entry.pack(side='left', padx=5)

        # 查询按钮
        query_btn = tk.Button(month_select_frame, text='查询', font=('微软雅黑', 10), bg='#0984e3', fg='white', 
                              command=lambda: [self.update_summary(), self.update_table(), self.update_chart()], relief='flat')
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
        self.table = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

        # 设置表头
        self.table.heading('日期', text='日期')
        self.table.heading('类型', text='类型')
        self.table.heading('金额', text='金额')
        self.table.heading('用途', text='用途/备注')

        # 设置列宽
        self.table.column('日期', width=100, anchor='center')
        self.table.column('类型', width=80, anchor='center')
        self.table.column('金额', width=100, anchor='e')  # 右对齐
        self.table.column('用途', width=200)

        self.table.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # 消费分析区域
        chart_frame = tk.LabelFrame(right_panel, text='消费分析', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=10)
        chart_frame.pack(fill='both', expand=True, pady=10)

        # 添加导出按钮区域
        export_btn_frame = tk.Frame(chart_frame, bg='#f5f6fa')
        export_btn_frame.pack(pady=5)

        png_btn = tk.Button(export_btn_frame, text="导出为 PNG", command=self.export_chart_png,
                            bg="#0984e3", fg="white", font=("微软雅黑", 10), padx=10, pady=5)
        png_btn.pack(side='left', padx=10)

        pdf_btn = tk.Button(export_btn_frame, text="导出为 PDF", command=self.export_chart_pdf,
                            bg="#6c5ce7", fg="white", font=("微软雅黑", 10), padx=10, pady=5)
        pdf_btn.pack(side='left', padx=10)


        # 创建一个带滚动条的框架来容纳图表
        chart_canvas_frame = tk.Frame(chart_frame, bg='#f5f6fa')
        chart_canvas_frame.pack(fill='both', expand=True)

        # 创建画布和滚动条
        self.chart_canvas = tk.Canvas(chart_canvas_frame, bg='#f5f6fa', highlightthickness=0)
        self.chart_scrollbar = ttk.Scrollbar(chart_canvas_frame, orient='vertical', command=self.chart_canvas.yview)
        self.chart_canvas.configure(yscrollcommand=self.chart_scrollbar.set)

        # 添加水平滚动条
        self.chart_h_scrollbar = ttk.Scrollbar(chart_canvas_frame, orient='horizontal', command=self.chart_canvas.xview)
        self.chart_canvas.configure(yscrollcommand=self.chart_scrollbar.set, xscrollcommand=self.chart_h_scrollbar.set)

        # 放置画布和滚动条
        self.chart_scrollbar.pack(side='right', fill='y')
        self.chart_canvas.pack(side='left', fill='both', expand=True)
        self.chart_h_scrollbar.pack(side='bottom', fill='x')

        # 创建一个框架放在画布上
        self.chart_inner_frame = tk.Frame(self.chart_canvas, bg='#f5f6fa')
        self.chart_canvas.create_window((0, 0), window=self.chart_inner_frame, anchor='nw')

        # 创建图表
        self.fig = plt.Figure(figsize=(12, 16), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_inner_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

        # 鼠标横向滚动（Shift+滚轮）
        self.chart_canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

    def _on_shift_mousewheel(self, event):
        self.chart_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    # 更新图表函数
    def update_chart(self):
        month = self.selected_month.get().strip()
        if not month:
            month = datetime.now().strftime('%Y-%m')
            self.selected_month.set(month)

        usage = get_usage_breakdown(month)

        self.ax.clear()
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
            bars = self.ax.barh(labels, sizes, color=colors[:len(labels)], height=1)

            # 在条形上添加数值和百分比标签
            for i, bar in enumerate(bars):
                width = bar.get_width()
                percentage = width / total * 100
                self.ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                       f'{width:.2f}元 ({percentage:.1f}%)',
                       va='center', fontsize=11, fontfamily='SimHei')

            # 设置图表标题和标签
            self.ax.set_title(f'{month} 用途消费分布', fontsize=16, fontweight='bold', pad=20, fontfamily='SimHei')
            self.ax.set_xlabel('支出金额 (元)', fontsize=12, fontfamily='SimHei')

            # 设置Y轴标签字体大小和字体
            self.ax.tick_params(axis='y', labelsize=10)
            for label in self.ax.get_yticklabels():
                label.set_fontfamily('SimHei')

            # 根据条目数量调整图表高度
            self.fig.set_figheight(max(5, len(labels) * 0.6))
            self.fig.set_figwidth(12)  # 加宽
        else:
            self.ax.text(0.5, 0.5, '本月暂无支出', ha='center', va='center', fontsize=14, fontweight='bold', fontfamily='SimHei')

        # 自动调整布局
        self.fig.tight_layout()
        self.canvas.draw()

        # 更新滚动区域
        self.chart_inner_frame.update_idletasks()
        self.chart_canvas.config(scrollregion=self.chart_canvas.bbox('all'))
        self.chart_canvas.configure(yscrollcommand=self.chart_scrollbar.set, xscrollcommand=self.chart_h_scrollbar.set)

        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            self.chart_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.chart_canvas.bind_all("<MouseWheel>", _on_mousewheel)



if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
