from idlelib.debugobj_r import remote_object_tree_item

import pygame
import random

pygame.init()
resolution = [1270, 720]
window = pygame.display.set_mode(resolution)
pygame.display.update()
#background = pygame.image.load("art/environment/background.png")

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
        self.actual_tick = pygame.time.get_ticks()
        self.last_tick = 0
        self.i = 0

    def physic_tick(self):
        self.vertical_current_speed += self.vertical_acc
        #odswiezanie hitboxa playable object
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

class Background:
    def __init__(self):
        self.x_cord = 0
        self.y_cord = 0
        self.wide_background = pygame.image.load("art/environment/wide_background.png")
        self.width = self.wide_background.get_width()

    #przekazujemy playable_object aby można było pobrać od niego wartości zmiennych
    def draw(self, playable_object):
        if playable_object.x_cord < resolution[0]/2:
            self.x_cord = 0
        elif playable_object.x_cord >= resolution[0]/2:
            self.x_cord -= playable_object.horizontal_current_speed
            if playable_object.x_cord > self.width - resolution[0]/2:
                self.x_cord = resolution[0] - self.width

        window.blit(self.wide_background, (self.x_cord, self.y_cord))

    def tick(self, x, y):
        self.x_cord = x
        self.y_cord = y

class PlayableObject(Physic):
    def __init__ (self, beams):
        self.default_playable_obj = pygame.image.load("art/playable_object/playable_object.png").convert_alpha()
        #ponizej zastosowano technike list comprehension do skrocenia tworzenia listy
        self.walk_pics = [pygame.image.load(f"art/playable_object/walk/{x}.png").convert_alpha() for x in range(3)]
        width = self.default_playable_obj.get_width()
        height = self.default_playable_obj.get_height()
        super().__init__(200, 647, width, height, 15, 10, 1, 10, 0, beams)
        self.x_screen = 0
    def calculate_acceleration(self, speed1, speed2):
        if speed1 < speed2:
            return self.horizontal_acc
        else:
            return 0

    def tick(self, keys):
        #tick do animacji, moze pozniej warto to wrzucic do jakiejs metody dedykowanej dla animacji?
        self.actual_tick = pygame.time.get_ticks()
        self.prev_x_cord = self.x_cord
        self.prev_y_cord = self.y_cord

        if keys[pygame.K_w] and self.jumping == False:
            self.vertical_current_speed -= 30
            self.jumping = True
        if keys[pygame.K_a]:
            self.horizontal_current_speed -= self.calculate_acceleration(self.horizontal_max_speed*-1, self.horizontal_current_speed)
            self.x_cord += self.horizontal_current_speed
            print(self.x_cord)
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

    def draw(self, background):
        if self.x_cord < resolution[0]/2:
            self.x_screen = self.x_cord
        elif resolution[0]/2 <= self.x_cord <= background.width - resolution[0]/2:
            self.x_screen = resolution[0]/2
        else:
            self.x_screen += self.horizontal_current_speed

        if self.horizontal_current_speed != 0:
            window.blit(self.walk_pics[self.i], (self.x_screen, self.y_cord))
            if self.actual_tick - self.last_tick >= 50:
                self.update_animation()
        else:
            self.i = 0
            window.blit(self.default_playable_obj, (self.x_screen, self.y_cord))

    def update_animation(self):
        if self.i < 2:
            self.i += 1
            self.last_tick = self.actual_tick
        else:
            self.i = 0
            self.last_tick = self.actual_tick

class Beam:
    def __init__(self, x, y, width, height):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, win, x_background):
        pygame.draw.rect(win, (128, 128, 128), pygame.Rect(self.x_cord + x_background, self.y_cord, self.width, self.height))

def main():
    run = True
    beams = [
        Beam(0, 710, 3000, 10), #floor
        Beam(950, 610, 10, 100)  #wall
    ]
    playable_object = PlayableObject(beams)
    background = Background()
    while run:
        pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        playable_object.tick(keys)
        #window.blit(background, (0, 0))
        background.draw(playable_object) #najpierw rysujemy tlo, w innym wypadku tlo zasloni obiekty wygenerowane wczesniej
        playable_object.draw(background)
        for beam in beams:
            beam.draw(window, background.x_cord)
        pygame.display.update()

if __name__ == "__main__":
    main()