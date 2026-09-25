import tkinter as tk
from tkinter import messagebox, ttk, font,filedialog, simpledialog
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from decimal import Decimal, ROUND_HALF_UP
import uuid

matplotlib.use('TkAgg')  # 确保使用正确的后端

CATEGORY_FILE = 'categories.json'
RULES_FILE = 'rules.json'
DATA_FILE = 'records.json'
GOAL_FILE = 'goals.json'
CATEGORY_FILE = 'categories.json'

def _safe_read_json(file_path, default):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, type(default)) else default
    except Exception:
        return default
    return default

def _safe_write_json(file_path, data):
    tmp_path = file_path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, file_path)

def load_data():
    data = _safe_read_json(DATA_FILE, [])
    changed = False
    normalized = []
    for r in data:
        if isinstance(r, dict):
            if not str(r.get('id', '')).strip():
                r['id'] = uuid.uuid4().hex
                changed = True
            normalized.append(r)
    if changed:
        _safe_write_json(DATA_FILE, normalized)
    return normalized

def save_data(data):
    _safe_write_json(DATA_FILE, data)

def load_goals():
    return _safe_read_json(GOAL_FILE, {})

def save_goals(goals):
    _safe_write_json(GOAL_FILE, goals)

SETTINGS_FILE = 'settings.json'
def load_settings():
    return _safe_read_json(SETTINGS_FILE, {})
def save_settings(s):
    _safe_write_json(SETTINGS_FILE, s)
def get_setting(key, default=None):
    s = load_settings()
    return s.get(key, default) if isinstance(s, dict) else default
def set_setting(key, value):
    s = load_settings()
    if not isinstance(s, dict):
        s = {}
    s[key] = value
    save_settings(s)

def load_categories():
    cats = _safe_read_json(CATEGORY_FILE, [])
    if not isinstance(cats, list):
        cats = []
    cats = [str(c).strip() for c in cats if isinstance(c, str)]
    if '未分类' not in cats:
        cats.append('未分类')
    return sorted(set(cats))

def save_categories(categories):
    cats = [str(c).strip() for c in categories if str(c).strip()]
    _safe_write_json(CATEGORY_FILE, sorted(set(cats)))

def load_rules():
    rules = _safe_read_json(RULES_FILE, [])
    if not isinstance(rules, list):
        rules = []
    cleaned = []
    for r in rules:
        if isinstance(r, dict):
            kw = str(r.get('keyword', '')).strip()
            cat = str(r.get('category', '')).strip()
            if kw and cat:
                cleaned.append({'keyword': kw, 'category': cat})
    return cleaned

def save_rules(rules):
    _safe_write_json(RULES_FILE, rules)

def suggest_tag(note):
    note = (note or '').strip()
    if not note:
        return '未分类'
    for r in load_rules():
        if r['keyword'] and r['keyword'] in note:
            return r['category']
    data = load_data()
    freq = {}
    for r in data:
        n = (r.get('note') or '').strip()
        t = (r.get('tag') or '').strip()
        if n == note and t:
            freq[t] = freq.get(t, 0) + 1
    if freq:
        return max(freq.items(), key=lambda x: x[1])[0]
    return '未分类'


# ============ 预置智能分类规则（基于历史记账习惯归纳） ============
PRESET_RULES = [
    # 交通
    {'keyword': '车费', 'category': '交通'},
    {'keyword': '公交', 'category': '交通'},
    {'keyword': '地铁', 'category': '交通'},
    {'keyword': '打车', 'category': '交通'},
    {'keyword': '滴滴', 'category': '交通'},
    {'keyword': '高铁', 'category': '交通'},
    {'keyword': '火车', 'category': '交通'},
    {'keyword': '车票', 'category': '交通'},
    {'keyword': '共享单车', 'category': '交通'},
    {'keyword': '单车', 'category': '交通'},
    {'keyword': '哈啰', 'category': '交通'},
    {'keyword': '摩的', 'category': '交通'},
    {'keyword': '加油', 'category': '交通'},
    {'keyword': '停车', 'category': '交通'},
    # 学习
    {'keyword': '打印', 'category': '学习'},
    {'keyword': '资料', 'category': '学习'},
    {'keyword': '学费', 'category': '学习'},
    {'keyword': '教材', 'category': '学习'},
    {'keyword': '网课', 'category': '学习'},
    {'keyword': '考试', 'category': '学习'},
    {'keyword': '六级', 'category': '学习'},
    {'keyword': '成绩单', 'category': '学习'},
    {'keyword': '文具', 'category': '学习'},
    {'keyword': '书本', 'category': '学习'},
    {'keyword': '买书', 'category': '学习'},
    {'keyword': '《', 'category': '学习'},
    {'keyword': '本子', 'category': '学习'},
    {'keyword': 'APP', 'category': '学习'},
    # 话费 / 电费 / 会员
    {'keyword': '话费', 'category': '话费'},
    {'keyword': '流量', 'category': '话费'},
    {'keyword': '电费', 'category': '电费'},
    {'keyword': '会员', 'category': '会员'},
    {'keyword': 'VIP', 'category': '会员'},
    {'keyword': 'vip', 'category': '会员'},
    {'keyword': '续费', 'category': '会员'},
    {'keyword': '订阅', 'category': '会员'},
    # 生活用品（具体词在前，避免被泛词误判）
    {'keyword': '卫生巾', 'category': '生活用品'},
    {'keyword': '内衣', 'category': '生活用品'},
    {'keyword': '洗衣', 'category': '生活用品'},
    {'keyword': '抽纸', 'category': '生活用品'},
    {'keyword': '纸巾', 'category': '生活用品'},
    {'keyword': '卫生纸', 'category': '生活用品'},
    {'keyword': '牙膏', 'category': '生活用品'},
    {'keyword': '牙刷', 'category': '生活用品'},
    {'keyword': '毛巾', 'category': '生活用品'},
    {'keyword': '手机壳', 'category': '生活用品'},
    {'keyword': '袜子', 'category': '生活用品'},
    {'keyword': '洗发', 'category': '生活用品'},
    {'keyword': '沐浴', 'category': '生活用品'},
    {'keyword': '垃圾袋', 'category': '生活用品'},
    {'keyword': '洗衣粉', 'category': '生活用品'},
    {'keyword': '衣架', 'category': '生活用品'},
    {'keyword': '衣服', 'category': '生活用品'},
    {'keyword': '内裤', 'category': '生活用品'},
    {'keyword': '拖鞋', 'category': '生活用品'},
    {'keyword': '卷纸', 'category': '生活用品'},
    {'keyword': '洗浴', 'category': '生活用品'},
    {'keyword': '置物架', 'category': '生活用品'},
    {'keyword': '水杯', 'category': '生活用品'},
    {'keyword': '伞', 'category': '生活用品'},
    {'keyword': '梯子', 'category': '生活用品'},
    {'keyword': '鼠标', 'category': '生活用品'},
    {'keyword': '耳机', 'category': '生活用品'},
    {'keyword': '手环', 'category': '生活用品'},
    {'keyword': '手表', 'category': '生活用品'},
    {'keyword': '凉席', 'category': '生活用品'},
    {'keyword': '太阳镜', 'category': '生活用品'},
    {'keyword': '收纳袋', 'category': '生活用品'},
    {'keyword': '防尘膜', 'category': '生活用品'},
    {'keyword': '创口贴', 'category': '生活用品'},
    {'keyword': '排插', 'category': '生活用品'},
    {'keyword': '洗洁精', 'category': '生活用品'},
    {'keyword': '短裤', 'category': '生活用品'},
    # 其他
    {'keyword': '理发', 'category': '其他'},
    {'keyword': '剪头发', 'category': '其他'},
    {'keyword': '看电影', 'category': '其他'},
    # 饮食（具体在前，泛词兜底在后）
    {'keyword': '自选餐', 'category': '饮食'},
    {'keyword': '减脂餐', 'category': '饮食'},
    {'keyword': '小碗菜', 'category': '饮食'},
    {'keyword': '一荤', 'category': '饮食'},
    {'keyword': '两荤', 'category': '饮食'},
    {'keyword': '早餐', 'category': '饮食'},
    {'keyword': '午餐', 'category': '饮食'},
    {'keyword': '晚餐', 'category': '饮食'},
    {'keyword': '夜宵', 'category': '饮食'},
    {'keyword': '自助餐', 'category': '饮食'},
    {'keyword': '聚餐', 'category': '饮食'},
    {'keyword': '外卖', 'category': '饮食'},
    {'keyword': '煎饼', 'category': '饮食'},
    {'keyword': '包子', 'category': '饮食'},
    {'keyword': '馒头', 'category': '饮食'},
    {'keyword': '花卷', 'category': '饮食'},
    {'keyword': '烧麦', 'category': '饮食'},
    {'keyword': '小笼包', 'category': '饮食'},
    {'keyword': '饭团', 'category': '饮食'},
    {'keyword': '玉米', 'category': '饮食'},
    {'keyword': '饺子', 'category': '饮食'},
    {'keyword': '馄饨', 'category': '饮食'},
    {'keyword': '拌面', 'category': '饮食'},
    {'keyword': '拉面', 'category': '饮食'},
    {'keyword': '汤面', 'category': '饮食'},
    {'keyword': '炒粉', 'category': '饮食'},
    {'keyword': '拌粉', 'category': '饮食'},
    {'keyword': '土豆粉', 'category': '饮食'},
    {'keyword': '土豆泥', 'category': '饮食'},
    {'keyword': '米粉', 'category': '饮食'},
    {'keyword': '米线', 'category': '饮食'},
    {'keyword': '鸡公煲', 'category': '饮食'},
    {'keyword': '麻辣香锅', 'category': '饮食'},
    {'keyword': '石锅', 'category': '饮食'},
    {'keyword': '烤肉', 'category': '饮食'},
    {'keyword': '火锅', 'category': '饮食'},
    {'keyword': '塔斯汀', 'category': '饮食'},
    {'keyword': '汉堡', 'category': '饮食'},
    {'keyword': '烤鸭', 'category': '饮食'},
    {'keyword': '鸭腿', 'category': '饮食'},
    {'keyword': '鸡腿', 'category': '饮食'},
    {'keyword': '牛肉', 'category': '饮食'},
    {'keyword': '炸鸡', 'category': '饮食'},
    {'keyword': '烧烤', 'category': '饮食'},
    {'keyword': '烤串', 'category': '饮食'},
    {'keyword': '零食', 'category': '饮食'},
    {'keyword': '辣条', 'category': '饮食'},
    {'keyword': '坚果', 'category': '饮食'},
    {'keyword': '瓜子', 'category': '饮食'},
    {'keyword': '水果', 'category': '饮食'},
    {'keyword': '葡萄', 'category': '饮食'},
    {'keyword': '柚子', 'category': '饮食'},
    {'keyword': '甜瓜', 'category': '饮食'},
    {'keyword': '蓝莓', 'category': '饮食'},
    {'keyword': '果粒茶', 'category': '饮食'},
    {'keyword': '沙拉', 'category': '饮食'},
    {'keyword': '牛奶', 'category': '饮食'},
    {'keyword': '酸奶', 'category': '饮食'},
    {'keyword': '豆浆', 'category': '饮食'},
    {'keyword': '奶茶', 'category': '饮食'},
    {'keyword': '饮料', 'category': '饮食'},
    {'keyword': '咖啡', 'category': '饮食'},
    {'keyword': '鸡蛋', 'category': '饮食'},
    {'keyword': '卤蛋', 'category': '饮食'},
    {'keyword': '西兰花', 'category': '饮食'},
    {'keyword': '空心菜', 'category': '饮食'},
    {'keyword': '蔬菜', 'category': '饮食'},
    {'keyword': '青菜', 'category': '饮食'},
    {'keyword': '买菜', 'category': '饮食'},
    {'keyword': '面包', 'category': '饮食'},
    {'keyword': '蛋糕', 'category': '饮食'},
    {'keyword': '泡面', 'category': '饮食'},
    {'keyword': '方便面', 'category': '饮食'},
    {'keyword': '小米粥', 'category': '饮食'},
    {'keyword': '粥', 'category': '饮食'},
    {'keyword': '米饭', 'category': '饮食'},
    {'keyword': '快餐', 'category': '饮食'},
    {'keyword': '油条', 'category': '饮食'},
    {'keyword': '凉皮', 'category': '饮食'},
    {'keyword': '西瓜', 'category': '饮食'},
    {'keyword': '手抓饼', 'category': '饮食'},
    {'keyword': '西红柿', 'category': '饮食'},
    {'keyword': '蛋堡', 'category': '饮食'},
    {'keyword': '柠檬水', 'category': '饮食'},
    {'keyword': '红枣', 'category': '饮食'},
    {'keyword': '红薯干', 'category': '饮食'},
    {'keyword': '苹果醋', 'category': '饮食'},
    {'keyword': '烤红薯', 'category': '饮食'},
    {'keyword': '螺狮粉', 'category': '饮食'},
    {'keyword': '馅饼', 'category': '饮食'},
    {'keyword': '黄瓜', 'category': '饮食'},
    {'keyword': '圣女果', 'category': '饮食'},
    {'keyword': '香蕉', 'category': '饮食'},
    {'keyword': '菠萝', 'category': '饮食'},
    {'keyword': '酱香饼', 'category': '饮食'},
    {'keyword': '土豆卷', 'category': '饮食'},
    {'keyword': '韭菜盒子', 'category': '饮食'},
    {'keyword': '烧饼', 'category': '饮食'},
    {'keyword': '卷饼', 'category': '饮食'},
    {'keyword': '便当', 'category': '饮食'},
    {'keyword': '奶', 'category': '饮食'},
    {'keyword': '素', 'category': '饮食'},
    {'keyword': '餐', 'category': '饮食'},
    {'keyword': '面', 'category': '饮食'},
    {'keyword': '饭', 'category': '饮食'},
]

# 这些类别若不存在，预置时一并补齐
PRESET_CATEGORIES = sorted(set([r['category'] for r in PRESET_RULES]))


def ensure_preset_rules():
    """首次使用（rules.json 为空）时自动灌入基于历史习惯归纳的智能分类规则。"""
    try:
        rules = load_rules()
        if not rules:
            save_rules([dict(r) for r in PRESET_RULES])
        # 同时补齐类别列表
        cats = load_categories()
        changed = False
        for c in PRESET_CATEGORIES:
            if c not in cats:
                cats.append(c)
                changed = True
        if changed:
            save_categories(cats)
    except Exception:
        pass


def apply_rules_to_all_records():
    """把关键词规则应用到历史记录中尚未分类（无 tag 或为'未分类'）的条目，
    不覆盖用户手动标注过的类别。返回本次补全的条数。"""
    data = load_data()
    rules = load_rules()
    if not rules:
        return 0
    changed = 0
    for r in data:
        note = (r.get('note') or '').strip()
        if not note:
            continue
        old_tag = (r.get('tag') or '').strip()
        if old_tag and old_tag != '未分类':
            continue
        new_tag = None
        for rule in rules:
            kw = (rule.get('keyword') or '').strip()
            if kw and kw in note:
                new_tag = rule['category']
                break
        if new_tag and new_tag != old_tag:
            r['tag'] = new_tag
            changed += 1
    if changed:
        save_data(data)
    return changed


# ============ 月份与累计结余工具（需求1：余额跨月滚动累积） ============
def _next_month_first(month):
    """返回 month('YYYY-MM') 下一个月的 1 号日期字符串，作为累计的开区间边界。"""
    y, m = int(month[:4]), int(month[5:7])
    if m == 12:
        return f"{y + 1:04d}-01-01"
    return f"{y:04d}-{m + 1:02d}-01"


def previous_month(month):
    y, m = int(month[:4]), int(month[5:7])
    if m == 1:
        return f"{y - 1:04d}-12"
    return f"{y:04d}-{m - 1:02d}"


def record_months():
    """所有有记录的月份('YYYY-MM')升序列表。"""
    data = load_data()
    return sorted(set(r['date'][:7] for r in data if r.get('date') and len(r['date']) >= 7))


def restart_point():
    """断档重算模式下，当前连续记账段的起始月。
    从最新有记录的月往回走，前一个月也有记录就继续，直到遇到没记录的月。
    例如记录为 2025-05~2026-01、2026-08~2026-09，则返回 '2026-08'。"""
    months = set(record_months())
    if not months:
        return None
    cur = max(months)
    while previous_month(cur) in months:
        cur = previous_month(cur)
    return cur


def cumulative_balance_until(month):
    """累计结余。
    - 断档重算模式（默认）：只从当前连续记账段的起始月累计；查询月若在断档期内则返回0。
    - 一直累计模式：从最早记录开始累计，空月贡献0，负数照常结转。"""
    boundary = _next_month_first(month)
    data = load_data()
    start_date = ''
    if get_setting('restart_on_gap', True):
        rp = restart_point()
        if rp:
            if month < rp:
                return Decimal('0')
            start_date = rp + '-01'
    inc = sum((Decimal(str(r['amount'])) for r in data
               if r['category'] == '收入' and start_date <= r['date'] < boundary), Decimal('0'))
    exp = sum((Decimal(str(r['amount'])) for r in data
               if r['category'] == '支出' and start_date <= r['date'] < boundary), Decimal('0'))
    return inc - exp


def calc_investment(month):
    """计算某月建议定投金额 = (上月结转正数 + 本月收入) × 20%。
    返回 dict: carried_raw, carry, month_income, base, invest"""
    data = load_data()
    month_income = sum((Decimal(str(r['amount'])) for r in data
                        if r['category'] == '收入' and r['date'].startswith(month)), Decimal('0'))
    carried_raw = cumulative_balance_until(previous_month(month))
    carry = max(carried_raw, Decimal('0'))
    base = carry + month_income
    invest = (base * Decimal('0.20')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return {'carried_raw': carried_raw, 'carry': carry,
            'month_income': month_income, 'base': base, 'invest': invest}


def _is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except Exception:
        return False

def _is_valid_month(month_str):
    try:
        datetime.strptime(month_str, '%Y-%m')
        return True
    except Exception:
        return False

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

    tag_frame = tk.Frame(form_frame, bg='#f5f6fa')
    tag_frame.pack(fill='x', pady=5)
    tag_label = tk.Label(tag_frame, text='类别:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa')
    tag_label.pack(side='left', padx=5)
    tag_var = tk.StringVar()
    tag_combo = ttk.Combobox(tag_frame, textvariable=tag_var, values=load_categories(), font=('微软雅黑', 12), width=18, state='normal')
    tag_combo.pack(side='left', padx=5)

    def _update_tag_suggestion():
        # 随备注实时自动建议类别；用户一旦点进类别框手动选择，则不再覆盖。
        # （旧逻辑只在类别框为空时建议，导致输入"零"时先被设成"未分类"，
        #   再输入"食"就停住了，"零食"无法自动归类。）
        try:
            if root.focus_get() is tag_combo:
                return
        except Exception:
            pass
        tag_var.set(suggest_tag(note_var.get()))
    note_var.trace_add('write', lambda *a: _update_tag_suggestion())
    
    # 按钮框架
    btn_frame = tk.Frame(add_window, bg='#f5f6fa')
    btn_frame.pack(pady=10)
    
    # 保存按钮
    def save_record():
        try:
            date = date_var.get()
            category = type_var.get()
            amount_str = amount_var.get().strip()
            note = note_var.get().strip()

            if not amount_str or not category:
                messagebox.showwarning('提示', '类型和金额不能为空！', parent=add_window)
                return
            if not _is_valid_date(date):
                messagebox.showwarning('提示', '日期格式需为 YYYY-MM-DD！', parent=add_window)
                return
                
            try:
                amount_dec = Decimal(amount_str)
            except ValueError:
                messagebox.showwarning('提示', '金额必须是数字！', parent=add_window)
                return
            
            if amount_dec <= 0:
                messagebox.showwarning('提示', '金额必须为正数！', parent=add_window)
                return
            
            amount_dec = abs(amount_dec).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            amount = float(amount_dec)
            
            tag = (tag_var.get() or '').strip()
            if not tag:
                tag = suggest_tag(note)
            record = {'date': date, 'category': category, 'tag': tag, 'amount': amount, 'note': note}
            data = load_data()
            data.append(record)
            save_data(data)
            cats = load_categories()
            if tag and tag != '未分类' and tag not in cats:
                cats.append(tag)
                save_categories(cats)
            
            messagebox.showinfo('成功', '账单已添加！', parent=add_window)
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
    elif not _is_valid_month(month):
        messagebox.showwarning('提示', '月份格式需为 YYYY-MM！')
        return
    
    data = load_data()
    income = sum((Decimal(str(r['amount'])) for r in data if r['category'] == '收入' and r['date'].startswith(month)), Decimal('0'))
    expense = sum((Decimal(str(r['amount'])) for r in data if r['category'] == '支出' and r['date'].startswith(month)), Decimal('0'))
    month_balance = income - expense

    # 跨月滚动累积：上月末累计结余（负数也结转），再加本月即当前累计结余
    prev_month = previous_month(month)
    carried = cumulative_balance_until(prev_month)      # 历史结转（到上月末）
    cumulative = carried + month_balance                # 累计结余（到本月末）

    q = lambda x: x.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    goals = load_goals()
    goal = goals.get(month, None)

    # 格式化摘要信息
    summary = f"当前月份: {month}\n\n"
    summary += f"本月收入: {q(income)} 元\n"
    summary += f"本月支出: {q(expense)} 元\n"
    summary += f"本月结余: {q(month_balance)} 元\n"
    summary += f"历史结转(上月末): {q(carried)} 元\n"
    summary += f"累计结余: {q(cumulative)} 元\n\n"

    if goal is not None:
        goal_dec = Decimal(str(goal))
        remaining = goal_dec - expense
        status = "达标" if remaining >= 0 else "超支"
        summary += f"本月目标: {goal_dec.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)} 元\n"
        summary += f"剩余额度: {remaining.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)} 元\n"
        summary += f"状态: {status}"
    else:
        summary += "本月未设置支出目标\n"
        summary += "请点击'设置月目标'按钮"
    
    summary_var.set(summary)
    update_investment()

def update_investment():
    """刷新左上角定投卡片：显示当前选中月份的建议定投金额。"""
    try:
        month = selected_month.get().strip() or datetime.now().strftime('%Y-%m')
        if not _is_valid_month(month):
            return
        data = calc_investment(month)
        invest_var.set(f"¥ {data['invest']}")
    except Exception:
        invest_var.set('—')

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
        elif not _is_valid_month(month):
            messagebox.showwarning('提示', '月份格式需为 YYYY-MM！', parent=summary_window)
            return
            
        data = load_data()
        income = sum((Decimal(str(r['amount'])) for r in data if r['category'] == '收入' and r['date'].startswith(month)), Decimal('0'))
        expense = sum((Decimal(str(r['amount'])) for r in data if r['category'] == '支出' and r['date'].startswith(month)), Decimal('0'))
        goals = load_goals()
        goal = goals.get(month, None)
        
        result_text.delete(1.0, tk.END)
        
        result_text.insert(tk.END, f"月份: {month}\n\n")
        result_text.insert(tk.END, f"总收入: {income.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)} 元\n")
        result_text.insert(tk.END, f"总支出: {expense.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)} 元\n")
        result_text.insert(tk.END, f"结余: {(income - expense).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)} 元\n\n")
        
        if goal is not None:
            goal_dec = Decimal(str(goal))
            remaining = goal_dec - expense
            status = "达标" if remaining >= 0 else "超支"
            result_text.insert(tk.END, f"本月目标: {goal_dec.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)} 元\n")
            result_text.insert(tk.END, f"剩余额度: {remaining.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)} 元 ({status})")
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

def open_investment_window():
    """定投计划界面：每月自动计算可投资金额 = (上月结转正数 + 本月收入) × 20%。"""
    win = tk.Toplevel(root)
    win.title('定投计划')
    win.geometry('460x520')
    win.configure(bg='#f5f6fa')
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()

    tk.Label(win, text='每月定投计划', font=('微软雅黑', 16, 'bold'), bg='#f5f6fa', fg='#273c75').pack(pady=10)

    # 月份选择
    month_frame = tk.Frame(win, bg='#f5f6fa')
    month_frame.pack(pady=5)
    tk.Label(month_frame, text='月份:', font=('微软雅黑', 12), bg='#f5f6fa').pack(side='left', padx=5)
    month_var = tk.StringVar(value=datetime.now().strftime('%Y-%m'))
    month_entry = tk.Entry(month_frame, textvariable=month_var, font=('微软雅黑', 12), width=12)
    month_entry.pack(side='left', padx=5)

    # 大字结果区
    result_big = tk.Label(win, text='', font=('微软雅黑', 22, 'bold'), bg='#f5f6fa', fg='#d63031')
    result_big.pack(pady=15)

    detail_label = tk.Label(win, text='', font=('微软雅黑', 11), bg='#f5f6fa', fg='#2d3436', justify='left')
    detail_label.pack(pady=5, padx=20, anchor='w')

    def calc():
        month = month_var.get().strip()
        if not month:
            month = datetime.now().strftime('%Y-%m')
            month_var.set(month)
        elif not _is_valid_month(month):
            messagebox.showwarning('提示', '月份格式需为 YYYY-MM！', parent=win)
            return

        data = calc_investment(month)
        carried_raw = data['carried_raw']
        carry = data['carry']
        month_income = data['month_income']
        base = data['base']
        invest = data['invest']
        q = lambda x: x.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        result_big.config(text=f'本月建议定投\n¥ {q(invest)}')
        neg_note = '（上月为负，按 0 计入）' if carried_raw < 0 else ''
        detail = (
            f"计算月份：{month}\n"
            f"上月结转余额：{q(carried_raw)} 元 {neg_note}\n"
            f"计入投资的结转：{q(carry)} 元\n"
            f"本月收入合计：{q(month_income)} 元\n"
            f"──────────────────\n"
            f"计算基数：{q(base)} 元\n"
            f"定投比例：20%\n"
            f"建议定投金额：{q(invest)} 元"
        )
        detail_label.config(text=detail)

    tk.Button(win, text='计算', width=12, font=('微软雅黑', 12), bg='#00b894', fg='white',
              relief='flat', command=calc).pack(pady=10)
    tk.Button(win, text='关闭', width=12, font=('微软雅黑', 12), bg='#d63031', fg='white',
              relief='flat', command=win.destroy).pack()

    calc()
    month_entry.focus_set()


def open_category_manager_window():
    win = tk.Toplevel(root)
    win.title('类别与规则管理')
    win.geometry('700x420')
    win.configure(bg='#f5f6fa')
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()

    left = tk.LabelFrame(win, text='类别', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=10)
    left.pack(side='left', fill='both', expand=True, padx=10, pady=10)
    right = tk.LabelFrame(win, text='关键词规则', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=10)
    right.pack(side='right', fill='both', expand=True, padx=10, pady=10)

    cat_list = tk.Listbox(left, font=normal_font, height=10)
    cat_list.pack(fill='both', expand=True)

    def refresh_cats():
        cat_list.delete(0, tk.END)
        for c in load_categories():
            cat_list.insert(tk.END, c)

    add_cat_frame = tk.Frame(left, bg='#f5f6fa')
    add_cat_frame.pack(fill='x', pady=5)
    new_cat_var = tk.StringVar()
    new_cat_entry = tk.Entry(add_cat_frame, textvariable=new_cat_var, font=normal_font)
    new_cat_entry.pack(side='left', padx=5)
    def add_cat():
        name = new_cat_var.get().strip()
        if not name:
            return
        cats = load_categories()
        if name not in cats:
            cats.append(name)
            save_categories(cats)
            refresh_cats()
            new_cat_var.set('')
    tk.Button(add_cat_frame, text='新增', font=normal_font, bg='#00b894', fg='white', relief='flat', command=add_cat).pack(side='left', padx=5)

    def rename_cat():
        sel = cat_list.curselection()
        if not sel:
            return
        old = cat_list.get(sel[0])
        if old == '未分类':
            return
        new = simpledialog.askstring('重命名类别', '新的类别名称：', parent=win)
        if not new:
            return
        new = new.strip()
        if not new:
            return
        cats = load_categories()
        if new in cats:
            return
        cats = [new if c == old else c for c in cats]
        save_categories(cats)
        data = load_data()
        for r in data:
            if (r.get('tag') or '') == old:
                r['tag'] = new
        save_data(data)
        rules = load_rules()
        for rr in rules:
            if rr['category'] == old:
                rr['category'] = new
        save_rules(rules)
        refresh_cats()

    def delete_cat():
        sel = cat_list.curselection()
        if not sel:
            return
        name = cat_list.get(sel[0])
        if name == '未分类':
            return
        if not messagebox.askyesno('确认', f'删除类别 {name} 并将相关记录设为未分类？', parent=win):
            return
        data = load_data()
        for r in data:
            if (r.get('tag') or '') == name:
                r['tag'] = '未分类'
        save_data(data)
        rules = [rr for rr in load_rules() if rr['category'] != name]
        save_rules(rules)
        cats = [c for c in load_categories() if c != name]
        save_categories(cats)
        refresh_cats()

    op_frame = tk.Frame(left, bg='#f5f6fa')
    op_frame.pack(fill='x', pady=5)
    tk.Button(op_frame, text='重命名', font=normal_font, bg='#fdcb6e', fg='#2d3436', relief='flat', command=rename_cat).pack(side='left', padx=5)
    tk.Button(op_frame, text='删除', font=normal_font, bg='#d63031', fg='white', relief='flat', command=delete_cat).pack(side='left', padx=5)

    rules_cols = ('关键词', '类别')
    rules_tree = ttk.Treeview(right, columns=rules_cols, show='headings', height=10)
    rules_tree.heading('关键词', text='关键词')
    rules_tree.heading('类别', text='类别')
    rules_tree.column('关键词', width=180)
    rules_tree.column('类别', width=120)
    rules_tree.pack(fill='both', expand=True)

    def refresh_rules():
        for i in rules_tree.get_children():
            rules_tree.delete(i)
        for rr in load_rules():
            rules_tree.insert('', 'end', values=(rr['keyword'], rr['category']))

    add_rule_frame = tk.Frame(right, bg='#f5f6fa')
    add_rule_frame.pack(fill='x', pady=5)
    kw_var = tk.StringVar()
    kw_entry = tk.Entry(add_rule_frame, textvariable=kw_var, font=normal_font, width=20)
    kw_entry.pack(side='left', padx=5)
    cat_var2 = tk.StringVar()
    cat_combo2 = ttk.Combobox(add_rule_frame, textvariable=cat_var2, values=load_categories(), font=normal_font, width=18, state='normal')
    cat_combo2.pack(side='left', padx=5)
    def add_rule():
        kw = kw_var.get().strip()
        cat = cat_var2.get().strip() or '未分类'
        if not kw:
            return
        rules = load_rules()
        rules.append({'keyword': kw, 'category': cat})
        save_rules(rules)
        if cat not in load_categories():
            cats = load_categories()
            cats.append(cat)
            save_categories(cats)
        kw_var.set('')
        refresh_rules()
        cat_combo2.config(values=load_categories())
    tk.Button(add_rule_frame, text='新增规则', font=normal_font, bg='#00b894', fg='white', relief='flat', command=add_rule).pack(side='left', padx=5)

    def delete_rule():
        sel = rules_tree.selection()
        if not sel:
            return
        vals = rules_tree.item(sel[0], 'values')
        kw = vals[0]
        cat = vals[1]
        rules = [rr for rr in load_rules() if not (rr['keyword'] == kw and rr['category'] == cat)]
        save_rules(rules)
        refresh_rules()
    tk.Button(add_rule_frame, text='删除规则', font=normal_font, bg='#d63031', fg='white', relief='flat', command=delete_rule).pack(side='left', padx=5)

    refresh_cats()
    refresh_rules()
    def _apply_rules():
        changed = apply_rules_to_all_records()
        if changed:
            update_table()
            update_chart()
            messagebox.showinfo('完成', '已应用规则到历史记录')
        else:
            messagebox.showinfo('提示', '当前无可应用的规则或记录')
    tk.Button(right, text='应用规则到历史记录', font=normal_font, bg='#fdcb6e', fg='#2d3436', relief='flat', command=_apply_rules).pack(fill='x', pady=5)

def update_table():
    # 清空表格
    for row in table.get_children():
        table.delete(row)
        
    # 获取选择的月份
    month = selected_month.get().strip()
    if not month:
        month = datetime.now().strftime('%Y-%m')
        selected_month.set(month)
    elif not _is_valid_month(month):
        messagebox.showwarning('提示', '月份格式需为 YYYY-MM！')
        return
    
    # 加载数据
    data = load_data()
    
    # 过滤当前月份的数据并按日期降序排序
    filtered_data = [r for r in data if r['date'].startswith(month)]
    sorted_data = sorted(filtered_data, key=lambda x: x['date'], reverse=True)
    
    # 填充表格
    for r in sorted_data:
        amount = r['amount']
        if r['category'] == '支出':
            amount_str = f"-{amount:.2f}"
            amount_color = '#d63031'
        else:
            amount_str = f"+{amount:.2f}"
            amount_color = '#00b894'
        tag_val = (r.get('tag') or '').strip() or '未分类'
        item_id = table.insert('', 'end', iid=str(r.get('id')), values=(r['date'], r['category'], tag_val, amount_str, r['note']))
        
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


def get_selected_record_id():
    sel = table.selection()
    if not sel:
        return None
    return sel[0]

def open_edit_record_window():
    rec_id = get_selected_record_id()
    if not rec_id:
        messagebox.showwarning('提示', '请先在表格中选择一条记录')
        return
    data = load_data()
    target = None
    for r in data:
        if str(r.get('id')) == rec_id:
            target = r
            break
    if not target:
        messagebox.showerror('错误', '未找到选中记录')
        return
    win = tk.Toplevel(root)
    win.title('编辑记录')
    win.geometry('420x320')
    win.configure(bg='#f5f6fa')
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()

    form = tk.Frame(win, bg='#f5f6fa')
    form.pack(pady=10, fill='both', expand=True)

    date_var = tk.StringVar(value=target.get('date'))
    type_var = tk.StringVar(value=target.get('category'))
    amount_var = tk.StringVar(value=f"{float(target.get('amount', 0)):.2f}")
    note_var = tk.StringVar(value=target.get('note', ''))
    tag_var = tk.StringVar(value=target.get('tag', ''))

    tk.Label(form, text='日期:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa').grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(form, textvariable=date_var, font=('微软雅黑', 12), width=20).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(form, text='类型:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa').grid(row=1, column=0, padx=5, pady=5)
    ttk.Combobox(form, textvariable=type_var, values=('支出','收入'), font=('微软雅黑', 12), width=18, state='readonly').grid(row=1, column=1, padx=5, pady=5)
    tk.Label(form, text='金额:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa').grid(row=2, column=0, padx=5, pady=5)
    tk.Entry(form, textvariable=amount_var, font=('微软雅黑', 12), width=20).grid(row=2, column=1, padx=5, pady=5)
    tk.Label(form, text='用途/备注:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa').grid(row=3, column=0, padx=5, pady=5)
    tk.Entry(form, textvariable=note_var, font=('微软雅黑', 12), width=20).grid(row=3, column=1, padx=5, pady=5)
    tk.Label(form, text='类别:', width=10, anchor='e', font=('微软雅黑', 12), bg='#f5f6fa').grid(row=4, column=0, padx=5, pady=5)
    ttk.Combobox(form, textvariable=tag_var, values=load_categories(), font=('微软雅黑', 12), width=18, state='normal').grid(row=4, column=1, padx=5, pady=5)

    def save_edit():
        date = date_var.get().strip()
        if not _is_valid_date(date):
            messagebox.showwarning('提示', '日期格式需为 YYYY-MM-DD！', parent=win)
            return
        t = type_var.get().strip()
        amt_str = amount_var.get().strip()
        try:
            amt_dec = Decimal(amt_str)
        except Exception:
            messagebox.showwarning('提示', '金额必须是数字！', parent=win)
            return
        if amt_dec <= 0:
            messagebox.showwarning('提示', '金额必须为正数！', parent=win)
            return
        amt_dec = abs(amt_dec).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        tag = (tag_var.get() or '').strip() or '未分类'
        note = (note_var.get() or '').strip()
        for r in data:
            if str(r.get('id')) == rec_id:
                r['date'] = date
                r['category'] = t
                r['amount'] = float(amt_dec)
                r['note'] = note
                r['tag'] = tag
                break
        save_data(data)
        cats = load_categories()
        if tag and tag not in cats:
            cats.append(tag)
            save_categories(cats)
        update_summary()
        update_table()
        update_chart()
        win.destroy()

    btns = tk.Frame(win, bg='#f5f6fa')
    btns.pack(pady=10)
    tk.Button(btns, text='保存', width=10, font=('微软雅黑', 12), bg='#00b894', fg='white', relief='flat', command=save_edit).pack(side='left', padx=10)
    tk.Button(btns, text='取消', width=10, font=('微软雅黑', 12), bg='#d63031', fg='white', relief='flat', command=win.destroy).pack(side='left', padx=10)

def delete_selected_record():
    rec_id = get_selected_record_id()
    if not rec_id:
        messagebox.showwarning('提示', '请先在表格中选择一条记录')
        return
    if not messagebox.askyesno('确认', '确定删除选中记录？'):
        return
    data = load_data()
    data = [r for r in data if str(r.get('id')) != rec_id]
    save_data(data)
    update_summary()
    update_table()
    update_chart()
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

# 信念横幅（需求4：醒目突出）
banner = tk.Label(root,
                  text='我是有能力把握将来十倍甚至百倍资产增长的人。',
                  font=('微软雅黑', 15, 'bold'), bg='#273c75', fg='#fdcb6e')
banner.pack(fill='x')

# 创建主布局框架
main_frame = tk.Frame(root, bg='#f5f6fa')
main_frame.pack(fill='both', expand=True, padx=20, pady=10)

# 左侧面板 - 包含摘要和按钮（可滚动）
left_outer = tk.Frame(main_frame, bg='#f5f6fa', width=300)
left_outer.pack(side='left', fill='y', padx=(0, 10))
left_canvas = tk.Canvas(left_outer, bg='#f5f6fa', width=280, highlightthickness=0)
left_scroll = ttk.Scrollbar(left_outer, orient='vertical', command=left_canvas.yview)
left_canvas.configure(yscrollcommand=left_scroll.set)
left_scroll.pack(side='right', fill='y')
left_canvas.pack(side='left', fill='both', expand=True)
left_panel = tk.Frame(left_canvas, bg='#f5f6fa')
_left_win = left_canvas.create_window((0, 0), window=left_panel, anchor='nw')

def _on_left_inner_config(e):
    left_canvas.configure(scrollregion=left_canvas.bbox('all'))
left_panel.bind('<Configure>', _on_left_inner_config)
def _on_left_canvas_config(e):
    left_canvas.itemconfigure(_left_win, width=e.width)
left_canvas.bind('<Configure>', _on_left_canvas_config)

def _on_left_wheel(e):
    left_canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units')
def _on_left_enter(e):
    # 鼠标进入左侧时，滚轮交给左侧；离开时恢复图表滚轮
    try:
        chart_canvas.unbind_all('<MouseWheel>')
    except Exception:
        pass
    left_canvas.bind_all('<MouseWheel>', _on_left_wheel)
def _on_left_leave(e):
    left_canvas.unbind_all('<MouseWheel>')
    try:
        chart_canvas.bind_all('<MouseWheel>', _on_mousewheel)
    except Exception:
        pass
left_canvas.bind('<Enter>', _on_left_enter)
left_canvas.bind('<Leave>', _on_left_leave)

# 定投金额卡片（左上角，醒目显示本月建议定投）
invest_frame = tk.LabelFrame(left_panel, text='本月定投', font=header_font, bg='#f5f6fa', fg='#273c75', padx=10, pady=6)
invest_frame.pack(fill='x', pady=(10, 0))
invest_var = tk.StringVar(value='—')
invest_label = tk.Label(invest_frame, textvariable=invest_var, font=('微软雅黑', 16, 'bold'), bg='#f5f6fa', fg='#d63031')
invest_label.pack(pady=4)

# 断档重算开关：停记一段时间后重新开始记账时，旧结余不再结转
restart_var = tk.BooleanVar(value=bool(get_setting('restart_on_gap', True)))
def on_restart_toggle():
    set_setting('restart_on_gap', restart_var.get())
    update_summary()
    update_investment()
restart_chk = tk.Checkbutton(left_panel, text='停记后重新累计', variable=restart_var,
                             command=on_restart_toggle, font=('微软雅黑', 10, 'bold'),
                             bg='#f5f6fa', fg='#c0392b', anchor='w')
restart_chk.pack(fill='x', padx=5, pady=(4, 0))

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

category_btn = tk.Button(btn_frame, text='类别管理', width=14, height=2, font=normal_font, bg='#a29bfe', fg='white', command=lambda: open_category_manager_window(), relief='flat')
category_btn.pack(fill='x', pady=5)

invest_btn = tk.Button(btn_frame, text='定投计划', width=14, height=2, font=normal_font, bg='#e17055', fg='white', command=lambda: open_investment_window(), relief='flat')
invest_btn.pack(fill='x', pady=5)

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

edit_btn = tk.Button(month_select_frame, text='编辑选中', font=('微软雅黑', 10), bg='#6c5ce7', fg='white', 
                     command=lambda: open_edit_record_window(), relief='flat')
edit_btn.pack(side='left', padx=5)

del_btn = tk.Button(month_select_frame, text='删除选中', font=('微软雅黑', 10), bg='#d63031', fg='white', 
                    command=lambda: delete_selected_record(), relief='flat')
del_btn.pack(side='left', padx=5)

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
columns = ('日期', '类型', '类别', '金额', '用途')
table = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)

# 设置表头
table.heading('日期', text='日期')
table.heading('类型', text='类型')
table.heading('类别', text='类别')
table.heading('金额', text='金额')
table.heading('用途', text='用途/备注')

# 设置列宽
table.column('日期', width=100, anchor='center')
table.column('类型', width=80, anchor='center')
table.column('类别', width=100, anchor='center')
table.column('金额', width=100, anchor='e')
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

# 鼠标纵向滚动（只绑定一次，避免 update_chart 反复叠加 handler）
def _on_mousewheel(event):
    chart_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
chart_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# 更新图表函数
def update_chart():
    month = selected_month.get().strip()
    if not month:
        month = datetime.now().strftime('%Y-%m')
        selected_month.set(month)
    elif not _is_valid_month(month):
        messagebox.showwarning('提示', '月份格式需为 YYYY-MM！')
        return

    data = load_data()
    usage = {}
    for r in data:
        if r['category'] == '支出' and r['date'].startswith(month):
            key = (r.get('tag') or '').strip() or '未分类'
            usage[key] = usage.get(key, 0) + r['amount']

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
        ax.set_title(f'{month} 类别消费分布', fontsize=16, fontweight='bold', pad=20, fontfamily='SimHei')
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



ensure_preset_rules()

update_summary()
update_table()
update_chart()

root.mainloop()
