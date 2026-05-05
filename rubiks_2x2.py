import random

COLORS = ['W', 'Y', 'R', 'O', 'G', 'B']  # 白 黄 红 橙 绿 蓝
SIDES = ['U', 'D', 'F', 'B', 'L', 'R']   # 上 下 前 后 左 右

# 2x2x2 魔方状态：每一面是2x2
class Cube2x2:
    # 每一面 0:U, 1:D, 2:F, 3:B, 4:L, 5:R
    def __init__(self):
        # 初始化6个面的颜色
        self.faces = [[c] * 4 for c in COLORS]
    
    def is_solved(self):
        return all(all(sticker == face[0] for sticker in face) for face in self.faces)
    
    # 展示魔方
    def show(self):
        f = self.faces
        print(f"      {f[0][0]} {f[0][1]}\n      {f[0][2]} {f[0][3]}")
        print(f"{f[4][0]} {f[4][1]} {f[2][0]} {f[2][1]} {f[5][0]} {f[5][1]} {f[3][0]} {f[3][1]}")
        print(f"{f[4][2]} {f[4][3]} {f[2][2]} {f[2][3]} {f[5][2]} {f[5][3]} {f[3][2]} {f[3][3]}")
        print(f"      {f[1][0]} {f[1][1]}\n      {f[1][2]} {f[1][3]}\n")

    # 单面顺时针旋转(面索引)
    def rotate_face(self, idx):
        f = self.faces[idx]
        self.faces[idx] = [f[2], f[0], f[3], f[1]]

    # 单步操作
    def move(self, op):
        # 旋转操作，包括 U, U', F, F', R, R', ...
        # 定义各面的相邻边 sticker 索引变化
        # 注意：简明起见，本实现直接暴力实现各操作的 sticker 变换
        rotate_map = {
            'U': (0, [(2,4,0),(3,4,1),(0,5,0),(1,5,1),(0,2,0),(1,2,1),(0,3,1),(1,3,0)]),
            'D': (1, [(2,2,2),(3,2,3),(0,5,2),(1,5,3),(0,4,2),(1,4,3),(0,3,2),(1,3,3)]),
            'F': (2, [(2,0,2),(3,0,3),(0,5,0),(2,5,2),(3,1,0),(2,1,1),(3,4,3),(2,4,1)]),
            'B': (3, [(0,0,0),(1,0,1),(2,5,1),(3,5,3),(2,1,2),(3,1,3),(2,4,0),(3,4,2)]),
            'L': (4, [(2,0,0),(3,0,2),(0,2,0),(2,2,2),(3,1,0),(2,1,2),(3,3,0),(2,3,2)]),
            'R': (5, [(2,0,1),(3,0,3),(0,2,1),(2,2,3),(3,1,1),(2,1,3),(3,3,1),(2,3,3)]),
        }
        is_ccw = op.endswith("'")
        face = op[0]
        if face not in rotate_map:
            print("无效操作！")
            return
        face_idx, adj = rotate_map[face]
        # 旋转自身
        if is_ccw:
            for _ in range(3): self.rotate_face(face_idx)
        else:
            self.rotate_face(face_idx)
        # 邻角交换(这里用了暴力交换，实际魔方更复杂，但2x2可简化)
        if is_ccw:
            # 逆时针
            v = [self.faces[side][sticker] for _,side,sticker in adj]
            for i,(p,side,sticker) in enumerate(adj):
                self.faces[side][sticker] = v[(i+2)%8]
        else:
            # 顺时针
            v = [self.faces[side][sticker] for _,side,sticker in adj]
            for i,(p,side,sticker) in enumerate(adj):
                self.faces[side][sticker] = v[(i-2)%8]
    
    # 打乱
    def scramble(self, n=10):
        ops = ['U', "U'", 'D', "D'", 'L', "L'", 'R', "R'", 'F', "F'", 'B', "B'"]
        for _ in range(n):
            self.move(random.choice(ops))
    
def main():
    cube = Cube2x2()
    cube.scramble(15)
    print("欢迎来到2x2魔方小游戏！\n输入 U, U', D, D', L, L', R, R', F, F', B, B' 来操作，输入 q 退出")
    while True:
        cube.show()
        if cube.is_solved():
            print("恭喜你还原魔方！")
            break
        cmd = input("请输入操作：").strip().upper()
        if cmd == 'Q':
            print("退出游戏。")
            break
        cube.move(cmd)

if __name__ == '__main__':
    main()