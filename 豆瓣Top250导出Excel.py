"""
豆瓣电影 Top250 → 导出 Excel
用法：
1. 把本脚本放在存放 1.html ~ 10.html 的同一个文件夹里
2. 先安装依赖：pip install lxml openpyxl
3. 运行：python 豆瓣Top250导出Excel.py
4. 同目录会生成 豆瓣Top250.xlsx
"""

import os
from lxml import html
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter


def clean(s):
    """去掉不换行空格、首尾斜杠和多余空白"""
    return s.replace('\xa0', ' ').strip().lstrip('/').strip()


def clean_count(s):
    """只提取字符串里的数字，去掉括号、“人评价”"""
    if not s:
        return ""
    return ''.join(ch for ch in s if ch.isdigit())


def pick(lst, idx=0):
    """安全取值：列表长度不够就返回空字符串，避免 IndexError"""
    return clean(lst[idx]) if len(lst) > idx else ''


rows = []

# 遍历 1.html ~ 10.html，每页 25 条，共 250 条
for page in range(1, 11):
    filename = f'{page}.html'
    if not os.path.exists(filename):
        print(f'[跳过] 找不到 {filename}')
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        doc = html.fromstring(f.read())

    items = doc.xpath('//ol[@class="grid_view"]/li')
    print(f'{filename}：解析到 {len(items)} 条')

    for item in items:
        rank_res = item.xpath('.//div[@class="pic"]/em/text()')            # 排名
        title_res = item.xpath('.//span[@class="title"]/text()')           # 中文名 + 外文名
        other_res = item.xpath('.//span[@class="other"]/text()')           # 别名
        bd_res = item.xpath('.//div[@class="bd"]/p/text()')                # 导演主演 / 年份地区类型
        rating_res = item.xpath('.//span[@class="rating_num"]/text()')     # 评分
        store_res = item.xpath('.//span[contains(text(), "人评价")]/text()')  # 评价人数（形如“3363381人评价”）

        rows.append([
            pick(rank_res, 0),      # 排名
            pick(title_res, 0),     # 中文名
            pick(title_res, 1),     # 外文名
            pick(other_res, 0),     # 别名
            pick(bd_res, 0),        # 导演/主演
            pick(bd_res, 1),        # 年份/地区/类型
            pick(rating_res, 0),    # 评分
            clean_count(pick(store_res, 0)),     # 评价人数
        ])

# ---------- 写入 Excel ----------
wb = Workbook()
ws = wb.active
ws.title = '豆瓣Top250'

headers = ['排名', '中文名', '外文名', '别名', '导演/主演', '年份/地区/类型', '评分', '评价人数']
ws.append(headers)

# 表头样式
head_font = Font(name='微软雅黑', bold=True, size=11, color='FFFFFF')
head_fill = PatternFill('solid', fgColor='4E79A7')
thin = Side(style='thin', color='D9D9D9')
border = Border(left=thin, right=thin, top=thin, bottom=thin)

for col in range(1, len(headers) + 1):
    c = ws.cell(row=1, column=col)
    c.font = head_font
    c.fill = head_fill
    c.alignment = Alignment(horizontal='center', vertical='center')
    c.border = border

# 数据行
for r in rows:
    ws.append(r)

# 数据行样式：自动换行 + 细边框
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(headers)):
    for c in row:
        c.alignment = Alignment(vertical='center', wrap_text=True)
        c.border = border

# 列宽
widths = [6, 22, 32, 30, 48, 30, 7, 14]
for i, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[1].height = 24

# 冻结表头 + 筛选
ws.freeze_panes = 'A2'
ws.auto_filter.ref = f'A1:{get_column_letter(len(headers))}{ws.max_row}'

out = '豆瓣Top250.xlsx'
wb.save(out)
print(f'\n完成：{out}，共写入 {len(rows)} 条数据')
