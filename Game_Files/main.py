import pygame
import random
from squirrel import Squirrel
from wood import Wood
from score import read_score
from score import update_text


#Author: AnubiX

# Játék beállításai
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
FPS = 60

icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

# Restart Gomb
class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x,y)
        
        def draw(self):
            clicked = False  
            #eger helye
            mouse_pos = pygame.mouse.get_pos()
             #eger a gombon van-e  
            if self.rect.collidepoint(mouse_pos):
                #Kattintás vizsgálat
                if pygame.mouse.get_pressed()[0] == 1:
                  clicked = True  
                
            screen.blit(self.image, (self.rect.x, self.rect.y))
            return clicked
        
def reset():
    wood_group.empty()
    squirrel.rect.x = 130
    squirrel.rect.y = SCREEN_HEIGHT // 2
    score = 0 #másik score, nem a fo
    return score
    
def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flying Squirrel")

    global wood_group # hogy elerje a reset function
    # Sprite csoportok
    squirrel_group = pygame.sprite.Group()
    wood_group = pygame.sprite.Group()

    global squirrel # hogy elerje a reset function
    # Mókus létrehozása
    squirrel = Squirrel(130, SCREEN_HEIGHT // 2)
    squirrel_group.add(squirrel)

    # Betűtípus
    font = pygame.font.SysFont("Bradley Hand", 50)
    font2 = pygame.font.SysFont("Bradley Hand", 30)
    white = (255, 255, 255)
    
    # Képek betöltése
    background = pygame.image.load("images/background.png")
    ground = pygame.image.load("images/ground.png")
    button_image = pygame.image.load("images/button.png")
    
    # Változók
    clock = pygame.time.Clock()
    ground_move = 0
    move_speed = 4
    score = 0
    pass_wood = False
    start = False
    game_over = False
    running = True
    wood_timer = pygame.time.get_ticks()

    
    #Restart gomb
    button = Button(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 50, button_image)
    
    while running:
        clock.tick(FPS)
        screen.blit(background, (0, 0))
        best_score = read_score()
        best_score_title = f"Eddigi legjobb pontszám: {best_score}" 

        # Mókus és fatörzs rajzolása
        squirrel_group.draw(screen)
        squirrel_group.update(start, game_over)
        wood_group.draw(screen)

        # Mozgó talaj
        screen.blit(ground, (ground_move, 600))
        if start and not game_over:
            ground_move -= move_speed
            if abs(ground_move) > 40:
                ground_move = 0

        # Új fatörzsek generálása
        if start and not game_over:
            if pygame.time.get_ticks() - wood_timer > 1200:
                wood_height = random.randint(-100, 100)
                wood_group.add(Wood(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + wood_height, -1))
                wood_group.add(Wood(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + wood_height, 1))
                wood_timer = pygame.time.get_ticks()
            wood_group.update(move_speed)
            
        #Mókus ütközik egy fával
        if pygame.sprite.spritecollide(squirrel, wood_group, False, pygame.sprite.collide_mask) or squirrel.rect.top < 0:
              game_over = True
              
        #Mókus leesika  földre
        if squirrel.rect.bottom > 670:
            game_over = True
            start = False
        
        #Pontszám növelése, ha a mókus áthalad egy fatörzsön
        if len(wood_group) > 0:
            if squirrel.rect.centerx < wood_group.sprites()[0].rect.right and not pass_wood:
                pass_wood = True
                
        if pass_wood == True:
            if len(wood_group) > 0 and squirrel_group.sprites()[0].rect.left > wood_group.sprites()[0].rect.right:
                score += 1
                pass_wood = False
                      
        #Pontszam vizsgálat/text update
        if score > best_score:
           update_text(score)
           
        # Pontszám megjelenítés
        score_text = font.render(str(score), True, white)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 30))

        best_score_text = font2.render(str(best_score_title), True, white)
        if game_over == True:    
            screen.blit(best_score_text, (SCREEN_WIDTH // 2 - best_score_text.get_width() // 2, 250))
        
        
        # Restart
        if game_over == True:
            if button.draw():
                game_over = False
                score = reset()
                
        # Kilépés
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not start and not game_over:
                start = True    
                      
        pygame.display.update()

    pygame.quit()

main()
