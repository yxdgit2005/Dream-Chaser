import tkinter as tk
from tkinter import messagebox
import math
import time
from datetime import datetime
import pygame
import threading

# 初始化pygame用于音效
pygame.mixer.init()
# 可自定义找到合适的wav文件，示例用系统自带的beep声音
TONE_FILE = None  # 若有自定义音效wav文件, 设置成路径，如'tone.wav'

def play_tone():
    def run():
        if TONE_FILE:
            pygame.mixer.music.load(TONE_FILE)
            pygame.mixer.music.play()
        else:
            # 没有自定义音效时用beep实现（需要Windows）
            try:
                import winsound
                winsound.Beep(1000, 120)  # 1000Hz, 120ms
            except:
                pass
    threading.Thread(target=run).start()

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("科学计算器")
        self.geometry("470x610")
        self.resizable(False, False)

        # 显示文本
        self.expression = ""
        self.input_text = tk.StringVar()

        # 显示框
        self.input_frame = tk.Frame(self, width=312, height=50, bd=0)
        self.input_frame.pack(side=tk.TOP)

        self.input_field = tk.Entry(self.input_frame, font=('Arial', 22), textvariable=self.input_text, width=35, bg="#eee", bd=5, justify=tk.RIGHT)
        self.input_field.grid(row=0, column=0)
        self.input_field.pack(ipady=15)

        # 日期显示
        self.date_label = tk.Label(self, text="", font=('Arial', 13), anchor='e')
        self.date_label.pack()
        self.update_date()

        # 时钟显示
        self.clock_label = tk.Label(self, text="", font=('Arial', 13), anchor='e')
        self.clock_label.pack()
        self.update_clock()

        # 按键
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack()

        self.buttons = [
            ['(', ')', 'π', 'e', 'C', '⌫'],
            ['sin', 'cos', 'tan', '√', '^', '/'],
            ['asin', 'acos', 'atan', 'log', 'ln', '*'],
            ['7', '8', '9', '!', '%', '-'],
            ['4', '5', '6', 'exp', '1/x', '+'],
            ['1', '2', '3', '.', 'Ans', '='],
            ['0']
        ]

        self.ans = ''

        # 按键布局
        for r, row in enumerate(self.buttons):
            for c, btn_text in enumerate(row):
                if btn_text == '0':
                    btn = tk.Button(self.buttons_frame, text=btn_text,
                                    width=41, height=2, bd=0, fg='black', bg='#ccc',
                                    font=('Arial', 14),
                                    command=lambda x=btn_text: self.button_click(x))
                    btn.grid(row=r, column=c, columnspan=6, padx=1, pady=1)
                else:
                    btn = tk.Button(self.buttons_frame, text=btn_text,
                                    width=6, height=2, bd=0, fg='black', bg='#fff',
                                    font=('Arial', 14),
                                    command=lambda x=btn_text: self.button_click(x))
                    btn.grid(row=r, column=c, padx=1, pady=1)

    def update_date(self):
        self.date_label.config(text=f"今日日期: {datetime.today().strftime('%Y-%m-%d')}")
        self.after(1000 * 60, self.update_date)  # 每分钟刷新一次

    def update_clock(self):
        self.clock_label.config(text=f"当前时间: {time.strftime('%H:%M:%S')}")
        self.after(1000, self.update_clock)  # 每秒刷新一次

    def button_click(self, item):
        play_tone()
        if item == 'C':
            self.expression = ""
            self.input_text.set("")
        elif item == '⌫':
            self.expression = self.expression[:-1]
            self.input_text.set(self.expression)
        elif item == '=':
            try:
                result = self.evaluate()
                self.input_text.set(result)
                self.ans = result
                self.expression = str(result)
            except Exception as e:
                self.input_text.set("错误")
                self.expression = ""
        elif item == 'Ans':
            self.expression += self.ans
            self.input_text.set(self.expression)
        elif item in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'ln', 'sqrt', '√', 'exp', '!', '^', 'π', 'e', '1/x', '%']:
            self.expression = self.handle_scientific(item)
            self.input_text.set(self.expression)
        else:
            self.expression += item
            self.input_text.set(self.expression)

    def evaluate(self):
        # 替换常用的科学记号
        exp = self.expression.replace('π', str(math.pi)).replace('e', str(math.e)).replace('^', '**')
        exp = exp.replace('ln', 'math.log').replace('log', 'math.log10').replace('√', 'math.sqrt')
        exp = exp.replace('exp', 'math.exp')
        exp = exp.replace('%', '/100')
        # 阶乘
        if '!' in exp:
            nums = exp.split('!')
            exp = f"{math.factorial(int(eval(nums[0])))}"
        # 倒数
        if '1/x' in exp:
            nums = exp.split('1/x')
            exp = f"1/({nums[0]})"
        # 替换三角函数
        exp = exp.replace('asin', 'math.asin').replace('acos', 'math.acos').replace('atan', 'math.atan')
        exp = exp.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
        # 支持deg(角度)
        # 支持ans
        exp = exp.replace('Ans', self.ans)
        result = eval(exp)
        # 弧度结果转换
        if 'asin' in self.expression or 'acos' in self.expression or 'atan' in self.expression:
            result = math.degrees(result)  # 逆三角以角度显示
        return result

    def handle_scientific(self, item):
        if item == 'π':
            return self.expression + str(math.pi)
        elif item == 'e':
            return self.expression + str(math.e)
        elif item == 'sin':
            return self.expression + 'sin('
        elif item == 'cos':
            return self.expression + 'cos('
        elif item == 'tan':
            return self.expression + 'tan('
        elif item == 'asin':
            return self.expression + 'asin('
        elif item == 'acos':
            return self.expression + 'acos('
        elif item == 'atan':
            return self.expression + 'atan('
        elif item == 'log':
            return self.expression + 'log('
        elif item == 'ln':
            return self.expression + 'ln('
        elif item == '√' or item == 'sqrt':
            return self.expression + '√('
        elif item == 'exp':
            return self.expression + 'exp('
        elif item == '!':
            return self.expression + '!'
        elif item == '^':
            return self.expression + '^'
        elif item == '1/x':
            return self.expression + '1/x'
        elif item == '%':
            return self.expression + '%'
        return self.expression

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()