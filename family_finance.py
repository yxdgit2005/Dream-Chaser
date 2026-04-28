import csv
import os
from datetime import datetime

CSV_FILE = 'family_finance.csv'
FIELDS = ['date', 'type', 'category', 'amount', 'note']

INCOME_CATEGORIES = ['工资', '理财']
EXPENSE_CATEGORIES = ['水费', '电费', '燃气费', '物业费', '食品', '交通', '娱乐', '其他']

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

def add_record():
    date = input("日期（YYYY-MM-DD，留空则为今天）：").strip()
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    r_type = input("类型（1-收入，2-支出）：").strip()
    if r_type == '1':
        r_type = '收入'
        print(f"收入分类：{INCOME_CATEGORIES}")
        category = input("请选择收入分类：").strip()
        if category not in INCOME_CATEGORIES:
            category = '其他'
    elif r_type == '2':
        r_type = '支出'
        print(f"支出分类：{EXPENSE_CATEGORIES}")
        category = input("请选择支出分类：").strip()
        if category not in EXPENSE_CATEGORIES:
            category = '其他'
    else:
        print("类型输入错误")
        return

    amount = input("金额：").strip()
    try:
        amount = float(amount)
    except:
        print("金额输入错误")
        return

    note = input("备注（可空）：").strip()

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({
            'date': date,
            'type': r_type,
            'category': category,
            'amount': amount,
            'note': note
        })
    print("记录添加成功！")

def show_records():
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print(f"{'日期':<12}{'类型':<8}{'分类':<8}{'金额':<10}{'备注'}")
        for row in reader:
            print(f"{row['date']:<12}{row['type']:<8}{row['category']:<8}{row['amount']:<10}{row['note']}")

def summary():
    income_total = 0.0
    expense_total = 0.0
    income_by_cat = {}
    expense_by_cat = {}

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            amt = float(row['amount'])
            if row['type'] == '收入':
                income_total += amt
                income_by_cat[row['category']] = income_by_cat.get(row['category'], 0) + amt
            else:
                expense_total += amt
                expense_by_cat[row['category']] = expense_by_cat.get(row['category'], 0) + amt

    print(f"总收入：{income_total:.2f}")
    for k, v in income_by_cat.items():
        print(f"   {k}：{v:.2f}")
    print(f"总支出：{expense_total:.2f}")
    for k, v in expense_by_cat.items():
        print(f"   {k}：{v:.2f}")
    print(f"结余：{income_total - expense_total:.2f}")

def main():
    init_csv()
    while True:
        print("\n======== 家庭理财账本 ========")
        print("1. 添加记录")
        print("2. 查看所有记录")
        print("3. 汇总收支情况")
        print("0. 退出")
        choice = input("请选择操作：").strip()
        if choice == '1':
            add_record()
        elif choice == '2':
            show_records()
        elif choice == '3':
            summary()
        elif choice == '0':
            break
        else:
            print("选择有误，请重新输入。")

if __name__ == '__main__':
    main()