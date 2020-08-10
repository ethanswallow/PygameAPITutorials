import pygame
import sys
import random


# You will implement this module ENTIRELY ON YOUR OWN!
class Ball:
    def __init__(self, screen, color, x, y):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = random.randint(5,20)
        self.speed_x = random.randint(100,150)
        self.speed_y = random.randint(100,150)

    def draw(self):
        pygame.draw.circle(self.screen, self.color,(5,5),self.radius,self.radius)

    def move(self):
        if self.x > self.screen.get_width():
            self.x -= self.speed_x
        else:
            self.x += self.speed_x
        if self.y > self.screen.get_height():
            self.y -= self.speed_y
        else:
            self.y += self.speed_y
# done: Create a Ball class.
# done: Possible member variables: screen, color, x, y, radius, speed_x, speed_y
# done: Methods: __init__, draw, move


def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Bouncing Ball')
    screen.fill(pygame.Color('gray'))
    clock = pygame.time.Clock()

    # done: Create an instance of the Ball class called ball1
    ball1 = Ball(screen,pygame.Color('red'),200, 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(60)
        screen.fill(pygame.Color('gray'))

        # done: Move the ball
        # done: Draw the ball
        ball1.move()
        ball1.draw()

        pygame.display.update()


main()


# Optional challenges (if you finish and want do play a bit more):
#   After you get 1 ball working make a few balls (ball2, ball3, etc) that start in different places.
#   Make each ball a different color
#   Make the screen 1000 x 800 to allow your balls more space (what needs to change?)
#   Make the speed of each ball randomly chosen (1 to 5)
#   After you get that working try making a list of balls to have 100 balls (use a loop)!
#   Use random colors for each ball
