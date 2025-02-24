import pygame

class Wood(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        super().__init__()
        self.image = pygame.image.load("images/wood1.png")
        self.rect = self.image.get_rect()
        wood_space = 175

        if pos == 1:  # First Log
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - wood_space // 2)
        elif pos == -1:  # Lower Log
            self.rect.topleft = (x, y + wood_space // 2)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, move_speed):
        self.rect.x -= move_speed
        if self.rect.right < 0:
            self.kill()
