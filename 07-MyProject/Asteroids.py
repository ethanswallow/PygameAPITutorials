import pygame, sys, random

class Missile:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.location = Location(self.x,self.y)
        self.has_exploded = False

    def move(self):
        if self.location.y > self.screen.get_height()// 2:
            self.y -= 5
        else:
            self.y += 5

    def draw(self):
        pygame.draw.line(self.screen, (0, 255, 0), (self.x, self.y),(self.x, self.y + 8), 4)


class Spaceship:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.location = Location(500, 500)
        self.image = pygame.image.load("ship.png")
        self.image.set_colorkey((0,0,0))
        self.missiles = []
        self.fire_sound = pygame.mixer.Sound("pew.wav")


    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def fire(self):
        new_missile = Missile(self.screen, self.x + self.image.get_width() // 2, self.y )
        self.missiles.append(new_missile)
        self.fire_sound.play()

    def remove_exploded_missiles(self):
        for k in range(len(self.missiles) - 1, -1, -1):
            if self.missiles[k].has_exploded or self.missiles[k].y < 0:
                del self.missiles[k]

    def reset(self):
        self.destroy()

    def destroy(self):
        self.location.x = 500
        self.location.y = 500

class Asteroid:
    def __init__(self, screen, x, y, speed):
        self.screen = screen
        self.x = x
        self.original_x = x
        self.location = Location(0,0)
        self.y = y
        self.speed_x = random.randint(1, 5)
        self.speed_y = random.randint(1, 5)
        self.is_dead = False
        self.image = pygame.image.load("Rocks.png")


    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x > 1000 or self.x < 10:
            self.speed_x = -self.speed_x
        if self.y > 750 or self.y < 10:
            self.speed_y = -self.speed_y

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def reset(self):
        self.location.y = random.randint(0,750)
        self.location.x = random.randint(0, 1000)

    def hit_by(self, missile):
        hitbox = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        return hitbox.collidepoint(missile.x, missile.y)

class Rocks:
    def __init__(self, screen, number_rocks):
        self.screen = screen
        self.asteroids = []
        self.explosion_sound = pygame.mixer.Sound("explosion.wav")
        for j in range(number_rocks):
            for k in range(5):
                self.asteroids.append(Asteroid(screen, 80 * k, 50 * j + 20, number_rocks))

    @property
    def is_defeated(self):
        return len(self.asteroids) == 0

    def move(self):
        for asteriod in self.asteroids:
            asteriod.move()

    def draw(self):
        for asteroid in self.asteroids:
            asteroid.draw()

    def remove_dead_badguys(self):
        for k in range(len(self.asteroids) - 1, -1, -1):
            if self.asteroids[k].is_dead:
                del self.asteroids[k]
                self.explosion_sound.play()
class Scoreboard:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.font = pygame.font.Font(None, 30)

    def draw(self):
        score_string = "Score: " + str(self.score)
        score_image = self.font.render(score_string, True, (255, 255, 255))
        self.screen.blit(score_image, (5,5))
class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_loc(self):
        return [self.x, self.y]

def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("ASTERIODS!")
    screen = pygame.display.set_mode((1000, 750))
    is_game_over = False
    spaceship = Spaceship(screen, screen.get_width() // 2, screen.get_height() // 2)
    number_rocks = 5
    rocks = Rocks(screen, number_rocks)
    scoreboard = Scoreboard(screen)
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                spaceship.fire()
            if event.type == pygame.QUIT:
                sys.exit()

        scoreboard.draw()
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT] and spaceship.x > -spaceship.image.get_width() / 2:
            spaceship.x -= 5
        if pressed_keys[pygame.K_RIGHT] and spaceship.x < screen.get_width() -spaceship.image.get_width() / 2:
            spaceship.x += 5
        if pressed_keys[pygame.K_UP] and spaceship.x > -spaceship.image.get_width() / 2:
            spaceship.y -= 5
        if pressed_keys[pygame.K_DOWN] and spaceship.x < screen.get_width() -spaceship.image.get_width() / 2:
            spaceship.y += 5

        spaceship.draw()
        rocks.draw()
        pygame.display.update()
        for missile in spaceship.missiles:
            missile.move()
            missile.draw()

        rocks.move()

        spaceship.remove_exploded_missiles()
        rocks.remove_dead_badguys()
        for asteroid in rocks.asteroids:
            for missile in spaceship.missiles:
                if asteroid.hit_by(missile):
                    scoreboard.score += 100
                    asteroid.is_dead = True
                    missile.has_exploded = True

        if rocks.is_defeated:
            number_rocks += 2
            rocks = Rocks(screen, number_rocks)

        pygame.display.update()

main()