# Make it all object oriented by converting the code in various classes

from tkinter import font
import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)


class Apple:
    def __init__(self, surface):
        self.parent_screen = surface
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24)*SIZE
        self.y = random.randint(0, 18)*SIZE

class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'


    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)



    # def move_left(self):
    #     self.x -= 10
    #     self.draw()
    #
    # def move_right(self):
    #     self.x += 10
    #     self.draw()
    #
    # def move_up(self):
    #     self.y -= 10
    #     self.draw()
    #
    # def move_down(self):
    #     self.y += 10
    #     self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")
        self.surface = pygame.display.set_mode((1000,800))
        pygame.mixer.init()
        self.play_background_music()
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"score : {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (888, 10))

    def is_collision(self,x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()


        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")

                raise "Game Over"

         # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"The game is over, Your score is : {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To play again press enter, To exit press escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()


    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)






    def run(self):
        running = True
        pouse = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pouse = False

                    if not pouse:

                        if event.key == K_LEFT:
                            if self.snake.direction == 'right':
                                pass
                            else:
                                self.snake.direction  = 'left'

                        if event.key == K_RIGHT:
                            if self.snake.direction == 'left':
                                pass
                            else:
                                self.snake.direction = 'right'

                        if event.key == K_UP:
                            if self.snake.direction == 'down':
                                pass
                            else:
                                self.snake.direction = 'up'

                        if event.key == K_DOWN:
                            if self.snake.direction == 'up':
                                pass
                            else:
                                self.snake.direction = 'down'

                elif event.type == QUIT:
                    running = False
            try:
                if not pouse:
                    self.play()


            except Exception as e:
                self.show_game_over()
                pouse = True
                self.reset()
            time.sleep(.1)



if __name__ == '__main__':
    game = Game()
    game.run()


