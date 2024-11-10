import pygame
import random

pygame.init()
window = pygame.display.set_mode((1280, 720))
pygame.display.update()
background = pygame.image.load("background.png")

class Physic:
    def __init__ (self, horizontal_max_speed, vertical_max_speed, vertical_acc, horizontal_acc, horizontal_no_speed):
        self.horizontal_current_speed = 0
        self.vertical_current_speed = 0
        self.horizontal_max_speed = horizontal_max_speed
        self.vertical_max_speed = vertical_max_speed
        self.horizontal_acc = horizontal_acc
        self.horizontal_no_speed = horizontal_no_speed

    def physic_tick(self):
        self.vertical_current_speed += 0.3

class PlayableObject(Physic):
    def __init__ (self):
        super().__init__(10, 10, 0.6, 0.6, 0)
        self.x_cord = 0
        self.y_cord = 657
        self.image = pygame.image.load("playable_object.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.tmp = 0.0


    def calculate_acceleration(self, speed1, speed2):
        if speed1 < speed2:
            return self.horizontal_acc
        else:
            return 0

    def tick(self, keys):
        self.physic_tick()
        if keys[pygame.K_a]:
            self.horizontal_current_speed -= self.calculate_acceleration(self.horizontal_max_speed*-1, self.horizontal_current_speed)
            self.x_cord += self.horizontal_current_speed
        if keys[pygame.K_d]:
            self.horizontal_current_speed += self.calculate_acceleration(self.horizontal_current_speed, self.horizontal_max_speed)
            self.x_cord += self.horizontal_current_speed

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            if abs(self.horizontal_current_speed) < 1e-10 and abs(self.horizontal_current_speed) != 0:
                self.horizontal_current_speed = 0
            if self.horizontal_current_speed < self.horizontal_no_speed:
                self.horizontal_current_speed += self.calculate_acceleration(self.horizontal_current_speed, self.horizontal_no_speed)
                self.x_cord += self.horizontal_current_speed
            elif self.horizontal_current_speed > self.horizontal_no_speed:
                self.horizontal_current_speed -= self.calculate_acceleration(self.horizontal_no_speed, self.horizontal_current_speed)
                self.x_cord += self.horizontal_current_speed

        self.y_cord += self.vertical_current_speed

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))

def main():
    run = True
    playable_object = PlayableObject()
    while run:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        playable_object.tick(keys)
        window.blit(background, (0, 0)) #najpierw rysujemy tlo, w innym wypadku tlo zasloni obiekty wygenerowane wczesniej
        playable_object.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()