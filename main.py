import pygame
import random

pygame.init()
window = pygame.display.set_mode((1280, 720))
pygame.display.update()
background = pygame.image.load("art/environment/background.png")

class Physic:
    def __init__ (self, x, y, width, height, horizontal_max_speed, vertical_max_speed, vertical_acc, horizontal_acc, horizontal_no_speed, beams):
        self.x_cord = x
        self.y_cord = y
        self.prev_x_cord = x
        self.prev_y_cord = y
        self.width = width
        self.height = height
        self.horizontal_current_speed = 0
        self.vertical_current_speed = 0
        self.horizontal_max_speed = horizontal_max_speed
        self.vertical_max_speed = vertical_max_speed
        self.vertical_acc = vertical_acc
        self.horizontal_acc = horizontal_acc
        self.horizontal_no_speed = horizontal_no_speed
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        self.beams = beams
        self.jumping = False

    def physic_tick(self):
        self.vertical_current_speed += self.vertical_acc
        #odswiezanie hitboxa
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)
        for beam in self.beams:
            if beam.hitbox.colliderect(self.hitbox):
                if self.prev_y_cord + self.height < beam.y_cord + 1 <= self.y_cord + self.height:
                    self.y_cord = self.prev_y_cord
                    self.vertical_current_speed = 0
                    self.jumping = False
                if self.prev_x_cord + self.width < beam.x_cord + 1 <= self.x_cord + self.width:
                    self.x_cord = self.prev_x_cord
                    self.horizontal_current_speed = 0
                if self.prev_x_cord > beam.x_cord + beam.width - 1 >= self.x_cord:
                    self.x_cord = self.prev_x_cord
                    self.horizontal_current_speed = 0
                if self.prev_y_cord > beam.y_cord + beam.height - 1 >= self.y_cord:
                    self.y_cord = self.prev_y_cord
                    self.vertical_current_speed = 0


class PlayableObject(Physic):
    def __init__ (self, beams):
        self.image = pygame.image.load("art/playable_object/playable_object.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        super().__init__(200, 647, width, height, 10, 10, 1, 0.6, 0, beams)

    def calculate_acceleration(self, speed1, speed2):
        if speed1 < speed2:
            return self.horizontal_acc
        else:
            return 0

    def tick(self, keys):

        self.prev_x_cord = self.x_cord
        self.prev_y_cord = self.y_cord

        if keys[pygame.K_w] and self.jumping == False:
            self.vertical_current_speed -= 30
            self.jumping = True
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

        self.physic_tick()


    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))

class Beam:
    def __init__(self, x, y, width, height):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, (128, 128, 128), self.hitbox)

def main():
    run = True
    beams = [
        Beam(100, 710, 300, 10), #floor
        Beam(100, 400, 300, 10), #ceiling
        Beam(100, 410, 10, 300), #left wall
        Beam(390, 610, 10, 100)  #right wall

    ]
    playable_object = PlayableObject(beams)
    while run:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        playable_object.tick(keys)
        window.blit(background, (0, 0)) #najpierw rysujemy tlo, w innym wypadku tlo zasloni obiekty wygenerowane wczesniej
        playable_object.draw()
        for beam in beams:
            beam.draw(window)
        pygame.display.update()

if __name__ == "__main__":
    main()