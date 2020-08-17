import pygame, sys, random

class Missile:
    def __init__(self, screen, x):
        self.screen = screen
        self.x = x
        self.y = 591
        self.has_exploded = False

    def move(self):
        self.y -= 5

    def draw(self):
        pygame.draw.line(self.screen, (0, 255, 0), (self.x, self.y),(self.x, self.y + 8), 4)



class Spaceship:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load("Spaceship.png")
        self.image.set_colorkey((255,255,255))
        self.missiles = []
        self.fire_sound = pygame.mixer.Sound("pew.wav")


    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def fire(self):
        new_missile = Missile(self.screen, self.x + self.image.get_width() // 2)
        self.missiles.append(new_missile)
        self.fire_sound.play()

    def remove_exploded_missiles(self):
        for k in range(len(self.missiles) - 1, -1, -1):
            if self.missiles[k].has_exploded or self.missiles[k].y < 0:
                del self.missiles[k]