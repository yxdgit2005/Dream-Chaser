import pygame
import sys

# 游戏参数
WIDTH, HEIGHT = 800, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 20
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("乒乓球 Pong Game")

left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH-30-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]
score = [0, 0]
font = pygame.font.SysFont('Arial', 36)
big_font = pygame.font.SysFont('Arial', 60)

clock = pygame.time.Clock()

# AI不得分计时器
no_ai_score_timer = 0    # 秒
game_over = False
result = ""

while True:
    dt = clock.tick(60)   # 每帧毫秒

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_over:
        # 游戏结束什么都不动，只显示分数结果
        screen.fill(BLACK)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        score_text = font.render(f"{score[0]}   {score[1]}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
        msg = big_font.render(result, True, WHITE)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
        pygame.display.flip()
        continue

    # 玩家球拍：键盘
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    # 玩家球拍：鼠标
    mouse_y = pygame.mouse.get_pos()[1]
    if 0 <= mouse_y - PADDLE_HEIGHT//2 <= HEIGHT - PADDLE_HEIGHT:
        left_paddle.y = mouse_y - PADDLE_HEIGHT//2

    # AI 控制
    if right_paddle.centery < ball.centery and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED
    elif right_paddle.centery > ball.centery and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED

    # 球移动
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # 碰撞检测
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]
    if ball.colliderect(left_paddle) and ball_speed[0] < 0:
        ball_speed[0] = -ball_speed[0]
    if ball.colliderect(right_paddle) and ball_speed[0] > 0:
        ball_speed[0] = -ball_speed[0]

    # AI不得分计时
    no_ai_score_timer += dt / 1000.0 # 秒

    # AI得分（玩家丢分）
    if ball.left <= 0:
        score[1] += 1
        ball.x, ball.y = WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2
        ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]
        no_ai_score_timer = 0  # 重置计时器

    # 玩家得分
    if ball.right >= WIDTH:
        score[0] += 1
        ball.x, ball.y = WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2
        ball_speed = [-BALL_SPEED_X, BALL_SPEED_Y]
        no_ai_score_timer = 0  # 也要重置，因为有人得分

    # 30秒AI不得分，玩家得1分，球重置，计时器重置
    if 30 <= no_ai_score_timer < 180: # 切勿180秒后重复触发
        score[0] += 1
        ball.x, ball.y = WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2
        ball_speed = [-BALL_SPEED_X, BALL_SPEED_Y]
        no_ai_score_timer = 0

    # 谁先得6分
    if score[0] >= 6: # 玩家胜
        result = "YOU WIN!"
        game_over = True
    elif score[1] >= 6: # AI胜
        result = "COMPUTER WINS!"
        game_over = True

    # AI连续3分钟不得分，玩家获胜
    if no_ai_score_timer >= 180:
        result = "YOU WIN! (AI 3min No Score)"
        game_over = True

    # 画面
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    score_text = font.render(f"{score[0]}   {score[1]}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    # 显示AI 30秒计时
    timer_text = font.render(f"AI 30s: {int(30 - (no_ai_score_timer % 30))}", True, WHITE)
    screen.blit(timer_text, (10, 10))

    # 还可以提示AI 3分钟不得分剩余时间
    remain3min = max(0, 180 - int(no_ai_score_timer))
    timer3_text = font.render(f"AI 3min: {remain3min}s", True, WHITE)
    screen.blit(timer3_text, (10, 45))

    pygame.display.flip()