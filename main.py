import sys
import pygame
from but_cass import All_Buttons
from board import boards
import math
import copy

pygame.init()
WIGHT = 900
HEIGHT = 800
color = "purple"
screen = pygame.display.set_mode((WIGHT, HEIGHT))
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("carbona.ttf", 20)
level = copy.deepcopy(boards)
PI = math.pi

players_im = []
turn = [False, False, False, False]

players_im.append(pygame.transform.scale(pygame.image.load("1.png"), (43, 43)))
players_im.append(pygame.transform.scale(pygame.image.load("2.png"), (43, 43)))
players_im.append(pygame.transform.scale(pygame.image.load("3.png"), (43, 43)))
players_im.append(pygame.transform.scale(pygame.image.load("4.png"), (43, 43)))

blinky_i = pygame.transform.scale(pygame.image.load("slime_3.png"), (43, 43))
blinky_x = 56
blinky_y = 48
blinky_direction = 0
blinky_dead = False
blinky_bo = False

inky_i = pygame.transform.scale(pygame.image.load("slime_1.png"), (43, 43))
inky_x = 440
inky_y = 340
inky_direction = 2
inky_dead = False
inky_bo = False

pinky_i = pygame.transform.scale(pygame.image.load("slime_2.png"), (43, 43))
pinky_x = 440
pinky_y = 340
pinky_direction = 2
pinky_dead = False
pinky_bo = False

clyde_i = pygame.transform.scale(pygame.image.load("slime_4.png"), (43, 43))
clyde_x = 440
clyde_y = 340
clyde_direction = 2
clyde_dead = False
clyde_bo = False

dead = pygame.transform.scale(pygame.image.load("dead.png"), (43, 43))
power_go = pygame.transform.scale(pygame.image.load("powerup.png"), (43, 43))
speed = 2

x_play = 450
y_play = 546
direction = 0
cou = 0
flicker = False
direction_command = 0
player_speed = 2

score = 0
powup = False
pow_cou = 0
eat_go = [False, False, False, False]
ghost_speeds = [2, 2, 2, 2]
target = [(x_play, y_play), (x_play, y_play), (x_play, y_play), (x_play, y_play)]
startup_counter = 0
lives = 3
game_over = False
game_won = False
main_back = pygame.image.load("IMG_6659.jpg")
sett_back = pygame.image.load("sett.jpg")
new_cursor = pygame.image.load("curcur.png")
pygame.mouse.set_visible(False)


def draw_board(lev):
    num_1 = ((HEIGHT - 50) // 32)
    num_2 = (WIGHT // 30)
    for i in range(len(lev)):
        for j in range(len(lev[i])):
            if lev[i][j] == 1:
                pygame.draw.circle(screen, (255, 255, 255), (j * num_2 + (0.5 * num_2), i * num_1 + (0.5 * num_1)), 4)
            if lev[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, (255, 255, 255), (j * num_2 + (0.5 * num_2), i * num_1 + (0.5 * num_1)), 11)
            if lev[i][j] == 3:
                pygame.draw.line(screen, color, (j * num_2 + (0.5 * num_2), i * num_1),
                                 (j * num_2 + (0.5 * num_2), i * num_1 + num_1), 3)
            if lev[i][j] == 4:
                pygame.draw.line(screen, color, (j * num_2, i * num_1 + (0.5 * num_1)),
                                 (j * num_2 + num_2, i * num_1 + (0.5 * num_1)), 3)
            if lev[i][j] == 5:
                pygame.draw.arc(screen, color,
                                [(j * num_2 - (num_2 * 0.4)) - 2, (i * num_1 + (0.5 * num_1)), num_2, num_1],
                                0, PI / 2, 3)
            if lev[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num_2 + (num_2 * 0.5)), (i * num_1 + (0.5 * num_1)), num_2, num_1],
                                PI / 2, PI, 3)
            if lev[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num_2 + (num_2 * 0.5)), (i * num_1 - (0.4 * num_1)), num_2, num_1],
                                PI, 3 * PI / 2, 3)
            if lev[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num_2 - (num_2 * 0.4)) - 2, (i * num_1 - (0.4 * num_1)), num_2, num_1],
                                3 * PI / 2, 2 * PI, 3)
            if lev[i][j] == 9:
                pygame.draw.line(screen, (255, 255, 255), (j * num_2, i * num_1 + (0.5 * num_1)),
                                 (j * num_2 + num_2, i * num_1 + (0.5 * num_1)), 3)


def draw_player():
    # 0 - ПРАВО, 1 - ЛЕВО, 2 - ВНИЗ, 3 - ВВЕРХ
    if direction == 0:
        screen.blit(players_im[cou // 5], (x_play, y_play))
    elif direction == 1:
        screen.blit(pygame.transform.flip(players_im[cou // 5], True, False), (x_play, y_play))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(players_im[cou // 5], 90), (x_play, y_play))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(players_im[cou // 5], 270), (x_play, y_play))


def check_pos(x_c, y_c):
    af_turn = [False, False, False, False]
    num_1 = (HEIGHT - 50) // 32
    num_2 = WIGHT // 30
    num_3 = 15
    if x_c // 30 < 29:
        if level[y_c // num_1][(x_c - num_3) // num_2] < 3:
            af_turn[1] = True
        if level[y_c // num_1][(x_c + num_3) // num_2] < 3:
            af_turn[0] = True
        if level[(y_c + num_3) // num_1][x_c // num_2] < 3:
            af_turn[3] = True
        if level[(y_c - num_3) // num_1][x_c // num_2] < 3:
            af_turn[2] = True

        if direction == 2 or direction == 3:
            if 12 <= x_c % num_2 <= 18:
                if level[(y_c + num_3) // num_1][x_c // num_2] < 3:
                    af_turn[3] = True
                if level[(y_c - num_3) // num_1][x_c // num_2] < 3:
                    af_turn[2] = True
            if 12 <= y_c % num_1 <= 18:
                if level[y_c // num_1][(x_c - num_2) // num_2] < 3:
                    af_turn[1] = True
                if level[y_c // num_1][(x_c + num_2) // num_2] < 3:
                    af_turn[0] = True
        if direction == 0 or direction == 1:
            if 12 <= x_c % num_2 <= 18:
                if level[(y_c + num_1) // num_1][x_c // num_2] < 3:
                    af_turn[3] = True
                if level[(y_c - num_1) // num_1][x_c // num_2] < 3:
                    af_turn[2] = True
            if 12 <= y_c % num_1 <= 18:
                if level[y_c // num_1][(x_c - num_3) // num_2] < 3:
                    af_turn[1] = True
                if level[y_c // num_1][(x_c + num_3) // num_2] < 3:
                    af_turn[0] = True
    else:
        af_turn[0] = True
        af_turn[1] = True
    return af_turn


def move_player(x_go, y_go):
    if direction == 0 and turn[0]:
        x_go += player_speed
    elif direction == 1 and turn[1]:
        x_go -= player_speed
    if direction == 2 and turn[2]:
        y_go -= player_speed
    elif direction == 3 and turn[3]:
        y_go += player_speed
    return x_go, y_go


def check_collision(sco, powup, pow_cou, eat_go):
    num_1 = (HEIGHT - 50) // 32
    num_2 = WIGHT // 30
    if 0 < x_play < 870:
        if level[y_center // num_1][x_center // num_2] == 1:
            level[y_center // num_1][x_center // num_2] = 0
            sco += 10
        if level[y_center // num_1][x_center // num_2] == 2:
            level[y_center // num_1][x_center // num_2] = 0
            sco += 50
            powup = True
            pow_cou = 0
            eat_go = [False, False, False, False]

    return sco, powup, pow_cou, eat_go


def draw_misc():
    score_te = font.render(f'SCORE: {score}', True, (255, 255, 255))
    screen.blit(score_te, (10, 770))
    if powup:
        pygame.draw.circle(screen, "blue", (140, 780), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(players_im[0], (30, 30)), (650 + i * 40, 765))

    if game_over:
        pygame.draw.rect(screen, 'white', [180, 100, 500, 300], 0, 10)
        pygame.draw.rect(screen, 'dark blue', [200, 120, 460, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'white', 1000)
        screen.blit(gameover_text, (250, 220))

    if game_won:
        pygame.draw.rect(screen, 'white', [180, 100, 500, 300], 0, 10)
        pygame.draw.rect(screen, 'dark blue', [200, 120, 460, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green', 200)
        screen.blit(gameover_text, (250, 220))


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powup and not self.dead) or (eat_go[self.id] and powup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powup and not self.dead and not eat_go[self.id]:
            screen.blit(power_go, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIGHT // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if x_play < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if y_play < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powup:
        if not blinky.dead and not eat_go[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eat_go[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (x_play, y_play)
        else:
            blink_target = return_target
        if not inky.dead and not eat_go[1]:
            ink_target = (runaway_x, y_play)
        elif not inky.dead and eat_go[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (x_play, y_play)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (x_play, runaway_y)
        elif not pinky.dead and eat_go[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (x_play, y_play)
        else:
            pink_target = return_target
        if not clyde.dead and not eat_go[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eat_go[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (x_play, y_play)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (x_play, y_play)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (x_play, y_play)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (x_play, y_play)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (x_play, y_play)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]


def main_menu():
    start_but = All_Buttons(500, 130, 400, 100, "START", "start_1.png", "lets_play.png", "pac-man-startup.mp3")
    set_but = All_Buttons(600, 650, 250, 100, "SETTINGS", "start_1.png", "start.png", "click.mp3")
    exit_but = All_Buttons(35, 650, 250, 100, "EXIT", "start_1.png", "lets_exit.png", "click.mp3")
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_back, (0, 0))

        font = pygame.font.Font("carbona.ttf", 72)
        pygame.draw.rect(screen, (0, 0, 0), [95, 30, 705, 80], 0, 10)
        text_appere = font.render("MY LOVELY PACMAN", True, (255, 255, 255))
        text_rect = text_appere.get_rect(center=(450, 70))
        screen.blit(text_appere, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == set_but:
                print("settings were put")
                settings()

            if event.type == pygame.USEREVENT and event.button == start_but:
                new_ga()

            if event.type == pygame.USEREVENT and event.button == exit_but:
                running = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()

            for btn in [start_but, set_but, exit_but]:
                btn.al_event(event)

        for btn in [start_but, set_but, exit_but]:
            btn.check_mos(pygame.mouse.get_pos())
            btn.drow_but(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(new_cursor, (x - 2, y - 2))
        pygame.display.flip()


def settings():
    running = True
    audio = All_Buttons(350, 150, 250, 100, "AUDIO", "start_1.png", "start.png", "click.mp3")
    volume = All_Buttons(350, 250, 250, 100, "VOLUME", "start_1.png", "start.png", "click.mp3")
    exit_intomenu = All_Buttons(350, 350, 250, 100, "EXIT", "start_1.png", "lets_exit.png", "click.mp3")
    while running:
        screen.fill((0, 0, 0))
        screen.blit(sett_back, (0, 0))

        font = pygame.font.Font("carbona.ttf", 72)
        text_appere = font.render("SETTINGS", True, (255, 255, 255))
        text_rect = text_appere.get_rect(center=(470, 70))
        screen.blit(text_appere, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.USEREVENT and event.button == exit_intomenu:
                running = False

            for btn in [audio, volume, exit_intomenu]:
                btn.al_event(event)

        for btn in [audio, volume, exit_intomenu]:
            btn.check_mos(pygame.mouse.get_pos())
            btn.drow_but(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(new_cursor, (x - 2, y - 2))
        pygame.display.flip()


def new_ga():
    global x_center
    global y_center
    global blinky
    global inky
    global clyde
    global pinky
    global flicker
    global cou
    global powup
    global startup_counter
    global game_over
    global game_won
    global level
    global pow_cou
    global x_play
    global y_play
    global eat_go
    global blinky_dead
    global inky_dead
    global pinky_dead
    global clyde_dead
    global blinky_x
    global blinky_y
    global target
    global blinky_direction
    global inky_x
    global inky_y
    global inky_direction
    global pinky_x
    global pinky_y
    global pinky_direction
    global clyde_y
    global clyde_x
    global clyde_direction
    global score
    global lives
    global direction_command
    global direction
    global moving
    global turn
    global ghost_speeds

    running = True
    while running:
        timer.tick(fps)
        if cou < 19:
            cou += 1
            if cou > 3:
                flicker = False
        else:
            cou = 0
            flicker = True

        if powup and pow_cou < 600:
            pow_cou += 1
        elif powup and pow_cou >= 600:
            pow_cou = 0
            powup = False
            eat_go = [False, False, False, False]

        if startup_counter < 180 and not game_over and not game_won:
            moving = False
            startup_counter += 1
        else:
            moving = True

        screen.fill((0, 0, 0))
        draw_board(level)
        draw_player()

        x_center = x_play + 21
        y_center = y_play + 18

        if powup:
            ghost_speeds = [1, 1, 1, 1]
        else:
            ghost_speeds = [2, 2, 2, 2]
        if eat_go[0]:
            ghost_speeds[0] = 2
        if eat_go[1]:
            ghost_speeds[1] = 2
        if eat_go[2]:
            ghost_speeds[2] = 2
        if eat_go[3]:
            ghost_speeds[3] = 2
        if blinky_dead:
            ghost_speeds[0] = 4
        if inky_dead:
            ghost_speeds[1] = 4
        if pinky_dead:
            ghost_speeds[2] = 4
        if clyde_dead:
            ghost_speeds[3] = 4

        game_won = True
        for i in range(len(level)):
            if 1 in level[i] or 2 in level[i]:
                game_won = False

        player_circle = pygame.draw.circle(screen, 'black', (x_center, y_center), 20, 2)
        draw_player()

        blinky = Ghost(blinky_x, blinky_y, target[0], ghost_speeds[0], blinky_i, blinky_direction, blinky_dead,
                       blinky_bo,
                       0)
        inky = Ghost(inky_x, inky_y, target[1], ghost_speeds[1], inky_i, inky_direction, inky_dead, inky_bo, 1)
        pinky = Ghost(pinky_x, pinky_y, target[2], ghost_speeds[2], pinky_i, pinky_direction, pinky_dead, pinky_bo, 2)
        clyde = Ghost(clyde_x, clyde_y, target[3], ghost_speeds[3], clyde_i, clyde_direction, clyde_dead, clyde_bo, 3)

        draw_misc()
        target = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
        turn = check_pos(x_center, y_center)

        if moving:
            x_play, y_play = move_player(x_play, y_play)
            if not blinky_dead and not blinky.in_box:
                blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
            else:
                blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
            if not pinky_dead and not pinky.in_box:
                pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
            else:
                pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
            if not inky_dead and not inky.in_box:
                inky_x, inky_y, inky_direction = inky.move_inky()
            else:
                inky_x, inky_y, inky_direction = inky.move_clyde()
            clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
        score, powup, pow_cou, eat_go = check_collision(score, powup, pow_cou, eat_go)

        if not powup:
            if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                    (player_circle.colliderect(inky.rect) and not inky.dead) or \
                    (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                    (player_circle.colliderect(clyde.rect) and not clyde.dead):
                if lives > 0:
                    lives -= 1
                    startup_counter = 0
                    powup = False
                    cou = 0
                    x_play = 450
                    y_play = 546
                    direction = 0
                    direction_command = 0
                    blinky_x = 56
                    blinky_y = 48
                    blinky_direction = 0
                    inky_x = 440
                    inky_y = 290
                    inky_direction = 2
                    pinky_x = 440
                    pinky_y = 340
                    pinky_direction = 2
                    clyde_x = 440
                    clyde_y = 340
                    clyde_direction = 2
                    eat_go = [False, False, False, False]
                    blinky_dead = False
                    inky_dead = False
                    clyde_dead = False
                    pinky_dead = False
                else:
                    game_over = True
                    moving = False
                    startup_counter = 0
        if powup and player_circle.colliderect(blinky.rect) and eat_go[0] and not blinky.dead:
            if lives > 0:
                powup = False
                cou = 0
                lives -= 1
                startup_counter = 0
                x_play = 450
                y_play = 546
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 48
                blinky_direction = 0
                inky_x = 440
                inky_y = 290
                inky_direction = 2
                pinky_x = 440
                pinky_y = 340
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 340
                clyde_direction = 2
                eat_go = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powup and player_circle.colliderect(inky.rect) and eat_go[1] and not inky.dead:
            if lives > 0:
                powup = False
                cou = 0
                lives -= 1
                startup_counter = 0
                x_play = 450
                y_play = 546
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 48
                blinky_direction = 0
                inky_x = 440
                inky_y = 290
                inky_direction = 2
                pinky_x = 440
                pinky_y = 340
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 340
                clyde_direction = 2
                eat_go = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powup and player_circle.colliderect(pinky.rect) and eat_go[2] and not pinky.dead:
            if lives > 0:
                powup = False
                cou = 0
                lives -= 1
                startup_counter = 0
                x_play = 450
                y_play = 546
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 48
                blinky_direction = 0
                inky_x = 440
                inky_y = 290
                inky_direction = 2
                pinky_x = 440
                pinky_y = 340
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 340
                clyde_direction = 2
                eat_go = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powup and player_circle.colliderect(clyde.rect) and eat_go[3] and not clyde.dead:
            if lives > 0:
                powup = False
                cou = 0
                lives -= 1
                startup_counter = 0
                x_play = 450
                y_play = 546
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 48
                blinky_direction = 0
                inky_x = 440
                inky_y = 290
                inky_direction = 2
                pinky_x = 440
                pinky_y = 340
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 340
                clyde_direction = 2
                eat_go = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eat_go[0]:
            blinky_dead = True
            eat_go[0] = True
            score += (2 ** eat_go.count(True)) * 100
        if powup and player_circle.colliderect(inky.rect) and not inky.dead and not eat_go[1]:
            inky_dead = True
            eat_go[1] = True
            score += (2 ** eat_go.count(True)) * 100
        if powup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eat_go[2]:
            pinky_dead = True
            eat_go[2] = True
            score += (2 ** eat_go.count(True)) * 100
        if powup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eat_go[3]:
            clyde_dead = True
            eat_go[3] = True
            score += (2 ** eat_go.count(True)) * 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction_command = 0
                if event.key == pygame.K_LEFT:
                    direction_command = 1
                if event.key == pygame.K_UP:
                    direction_command = 2
                if event.key == pygame.K_DOWN:
                    direction_command = 3
                if event.key == pygame.K_SPACE and (game_over or game_won):
                    powup = False
                    cou = 0
                    lives -= 1
                    startup_counter = 0
                    x_play = 450
                    y_play = 546
                    direction = 0
                    direction_command = 0
                    blinky_x = 56
                    blinky_y = 48
                    blinky_direction = 0
                    inky_x = 440
                    inky_y = 290
                    inky_direction = 2
                    pinky_x = 440
                    pinky_y = 340
                    pinky_direction = 2
                    clyde_x = 440
                    clyde_y = 340
                    clyde_direction = 2
                    eat_go = [False, False, False, False]
                    blinky_dead = False
                    inky_dead = False
                    clyde_dead = False
                    pinky_dead = False
                    score = 0
                    lives = 3
                    level = copy.deepcopy(boards)
                    game_over = False
                    game_won = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and direction_command == 0:
                    direction_command = direction
                if event.key == pygame.K_LEFT and direction_command == 1:
                    direction_command = direction
                if event.key == pygame.K_UP and direction_command == 2:
                    direction_command = direction
                if event.key == pygame.K_DOWN and direction_command == 3:
                    direction_command = direction
        if direction_command == 0 and turn[0]:
            direction = 0
        if direction_command == 1 and turn[1]:
            direction = 1
        if direction_command == 2 and turn[2]:
            direction = 2
        if direction_command == 3 and turn[3]:
            direction = 3

        if x_play > 900:
            x_play = -47
        elif x_play < -50:
            x_play = 897

        if blinky.in_box and blinky_dead:
            blinky_dead = False
        if inky.in_box and inky_dead:
            inky_dead = False
        if pinky.in_box and pinky_dead:
            pinky_dead = False
        if clyde.in_box and clyde_dead:
            clyde_dead = False

        x, y = pygame.mouse.get_pos()
        screen.blit(new_cursor, (x - 2, y - 2))
        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
