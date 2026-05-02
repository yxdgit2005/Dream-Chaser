import tkinter as tk
from tkinter import messagebox
import random, copy

# 棋子定义：(名字, 宽, 高, 编号)
pieces = [
    ("曹操", 2, 2, 1),
    ("关羽", 2, 1, 2),
    ("张飞", 1, 2, 3),
    ("赵云", 1, 2, 4),
    ("马超", 1, 2, 5),
    ("黄忠", 1, 2, 6),
    ("兵A", 1, 1, 7),
    ("兵B", 1, 1, 8),
    ("兵C", 1, 1, 9),
    ("兵D", 1, 1, 10),
]

# 经典布局
init_layout = [
    [ 3, 1, 1, 4 ],
    [ 3, 1, 1, 4 ],
    [ 5, 2, 2, 6 ],
    [ 5, 7, 8, 6 ],
    [ 9, 0,10, 0 ],
]

ROWS, COLS = 5, 4
TILE = 80

class HuarongDao:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, bg='white', width=COLS*TILE, height=ROWS*TILE)
        self.canvas.pack()
        self.move_count = 0
        self.move_label = tk.Label(master, text='步数: 0')
        self.move_label.pack()
        self.reset_btn = tk.Button(master, text="重置", command=self.reset)
        self.reset_btn.pack()
        self.master.title('华容道 by Copilot')
        self.selected_piece = None  # 用于自主方向选择
        self.reset()

        self.canvas.bind("<Button-1>", self.on_click)

    def reset(self):
        self.layout = copy.deepcopy(init_layout)
        self.selected_piece = None
        self.move_count = 0
        self.move_label['text'] = f"步数: {self.move_count}"
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        # 绘制棋盘及棋子
        drawn = set()
        for r in range(ROWS):
            for c in range(COLS):
                val = self.layout[r][c]
                if val and val not in drawn:
                    self.draw_piece(r, c, val)
                    drawn.add(val)
        # 画网格
        for i in range(COLS+1):
            self.canvas.create_line(i*TILE, 0, i*TILE, ROWS*TILE, fill="#AAA")
        for i in range(ROWS+1):
            self.canvas.create_line(0, i*TILE, COLS*TILE, i*TILE, fill="#AAA")

    def draw_piece(self, r, c, piece_id):
        name, w, h, p = pieces[piece_id-1]
        # 检查左上角
        for i in range(r+1):
            if self.layout[i][c]==piece_id and (i < r):
                return
        for j in range(c+1):
            if self.layout[r][j]==piece_id and (j < c):
                return
        x1 = c*TILE
        y1 = r*TILE
        x2 = (c+w)*TILE
        y2 = (r+h)*TILE
        colors = ['#FFD700', '#FF6347', '#ADFF2F', '#20B2AA', '#87CEFA', '#9370DB', '#CD853F', '#BDB76B', '#008B8B', '#483D8B']
        color = colors[piece_id % len(colors)]
        # 高亮选中
        outline_color = "red" if self.selected_piece and self.selected_piece[4] == piece_id else "black"
        outline_width = 5 if self.selected_piece and self.selected_piece[4] == piece_id else 2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline_color, width=outline_width)
        self.canvas.create_text(
            (x1+x2)//2, (y1+y2)//2, text=name, font=("黑体", int(26-5*(max(w,h)-1)), 'bold')
        )

    def on_click(self, event):
        c, r = event.x // TILE, event.y // TILE
        if not (0 <= r < ROWS and 0 <= c < COLS):
            self.selected_piece = None
            self.draw()
            return

        val = self.layout[r][c]
        if self.selected_piece is None:
            # 第一次点击 —— 棋子
            if val == 0:
                self.selected_piece = None
                self.draw()
                return
            name, w, h, p = pieces[val-1]
            # 找左上角
            sr, sc = r, c
            while sr > 0 and self.layout[sr-1][sc] == val: sr -= 1
            while sc > 0 and self.layout[sr][sc-1] == val: sc -= 1
            self.selected_piece = (sr, sc, w, h, val)
            self.draw()
        else:
            # 第二次点击 —— 尝试移动
            sr, sc, w, h, val = self.selected_piece
            # 判断目标格是否为紧邻的空白
            if self.layout[r][c] != 0:
                # 点到非空白格，则取消高亮，重新选择
                self.selected_piece = None
                self.draw()
                return

            # 检查点击的空格是否为选中棋子的某个一边（上下左右）
            dr = dc = None
            if sr <= r < sr+h and (c == sc-1 or c == sc+w):  # 左或右
                if c == sc-1:
                    dr, dc = 0, -1
                elif c == sc+w:
                    dr, dc = 0, 1
            elif sc <= c < sc+w and (r == sr-1 or r == sr+h):  # 上或下
                if r == sr-1:
                    dr, dc = -1, 0
                elif r == sr+h:
                    dr, dc = 1, 0

            if dr is not None and dc is not None and self.can_move(sr, sc, w, h, dr, dc):
                # 合法移动
                self.move_piece(sr, sc, w, h, dr, dc)
                self.move_count += 1
                self.move_label['text'] = f"步数: {self.move_count}"
                self.selected_piece = None  # 一次一步，移动后取消选择
                self.draw()
                if self.check_win():
                    messagebox.showinfo('恭喜', f'你赢了！总步数：{self.move_count}')
            else:
                # 非法移动，取消选择
                self.selected_piece = None
                self.draw()

    def can_move(self, r, c, w, h, dr, dc):
        nr, nc = r+dr, c+dc
        if nr<0 or nc<0 or nr+h>ROWS or nc+w>COLS:
            return False
        # 检查目标区是否都为空或本身
        for i in range(h):
            for j in range(w):
                tr, tc = nr+i, nc+j
                # 原位置覆盖新位置时不应判断为阻挡
                if not (self.layout[tr][tc]==0 or self.layout[r+i][c+j]==self.layout[tr][tc]):
                    return False
        return True

    def move_piece(self, r, c, w, h, dr, dc):
        val = self.layout[r][c]
        # 先清空原区
        for i in range(h):
            for j in range(w):
                self.layout[r+i][c+j] = 0
        # 赋值到新区
        for i in range(h):
            for j in range(w):
                self.layout[r+i+dr][c+j+dc] = val

    def check_win(self):
        # "曹操"到目标
        idx = None
        for r in range(ROWS-1):
            for c in range(COLS-1):
                if self.layout[r][c]==1 and self.layout[r][c+1]==1 and self.layout[r+1][c]==1 and self.layout[r+1][c+1]==1:
                    idx = (r, c)
        return idx == (3,1)

if __name__=="__main__":
    root = tk.Tk()
    hr = HuarongDao(root)
    root.mainloop()