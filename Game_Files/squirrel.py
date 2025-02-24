import pygame

class Squirrel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("images/squirrel4.png")
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.gravity = 0
        self.click = False
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, start, game_over):
        if start == True:
            # Gravitáció
            self.gravity += 0.5
            if self.gravity > 10:
                self.gravity = 10
            self.rect.y += int(self.gravity)

            # Ugrás
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.gravity = -10
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

            # Forgás
            rotation_angle = self.gravity * -2
            self.image = pygame.transform.rotate(self.original_image, rotation_angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = pygame.mask.from_surface(self.image)
