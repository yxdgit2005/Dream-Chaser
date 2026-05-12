import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 定义鲁班锁的六块积木的数据（长方体）
blocks = [
    # (x, y, z, color)
    ((-1, 0, 0), (1, 0.3, 0.3), (1,0,0)), # 红
    ((0, -1, 0), (0.3, 1, 0.3), (0,1,0)), # 绿
    ((0, 0, -1), (0.3, 0.3, 1), (0,0,1)), # 蓝
    ((1, 0, 0), (1, 0.3, 0.3), (1,1,0)),  # 黄
    ((0, 1, 0), (0.3, 1, 0.3), (0,1,1)),  # 青
    ((0, 0, 1), (0.3, 0.3, 1), (1,0,1)),  # 紫
]

def draw_block(center, size, color):
    glPushMatrix()
    glTranslatef(*center)
    glColor3f(*color)
    # 拉伸长方体
    sx, sy, sz = size
    glScalef(sx, sy, sz)
    glutSolidCube(1.0)
    glPopMatrix()

def draw_lock(is_locked):
    # 锁紧状态时在中心堆叠，解除状态时各自偏移
    offset = [0, 2, 4] if not is_locked else [0, 0, 0]
    for i, (center, size, color) in enumerate(blocks):
        if not is_locked:
            # 让每个木条按不同方向散开
            shift = [0,0,0]
            shift[i//2] = offset[i//2]*(1 if i%2==0 else -1)
            real_center = tuple(c+s for c, s in zip(center, shift))
        else:
            real_center = center
        draw_block(real_center, size, color)

def main():
    from OpenGL.GLUT import glutInit  # 避免GLUT初始化报错
    glutInit()

    pygame.init()
    screen = pygame.display.set_mode((800,600), DOUBLEBUF|OPENGL)
    pygame.display.set_caption("鲁班锁3D锁紧与解除模拟")

    gluPerspective(45, (800/600), 0.1, 50.0)
    glTranslatef(0.0,0.0,-12)

    # 控制旋转和状态
    rot_x, rot_y = 30, 30
    is_locked = True

    font = pygame.font.SysFont("SimHei", 30)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_l:  # L键锁紧
                    is_locked = True
                elif event.key==pygame.K_u:  # U键解除
                    is_locked = False
            elif event.type==pygame.MOUSEMOTION:
                # 鼠标右键旋转
                if event.buttons[2]:
                    dx, dy = event.rel
                    rot_x += dy
                    rot_y += dx

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glPushMatrix()
        glRotatef(rot_x, 1,0,0)
        glRotatef(rot_y, 0,1,0)
        draw_lock(is_locked)
        glPopMatrix()

        # 画按钮文本
        # 用pygame画文本需要用blit到surface，然后再转为OpenGL纹理。这里简单跳过，直接依赖按键
        # 见提示

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()

# 提示：
# - 运行程序后按L锁紧、U解除，鼠标右键拖动旋转视角。
# - 你可进一步增加鼠标点击界面按钮，或者加入木条拆解动画等。
