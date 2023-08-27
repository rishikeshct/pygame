import pygame, random
import sys
from pygame.locals import *

pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

again_rect = Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 180, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Project")

bg = pygame.image.load("./assets/bg.png")

clock = pygame.time.Clock()
running = True

pygame.mixer.music.load('./assets/gunshot.wav')

basic_font = pygame.font.Font('freesansbold.ttf', 32)


green = (0, 255, 0)
light_grey = (200,200,200)

class Player():
    def __init__(self, screen, path, w, h, x, y):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  
        screen.blit(self.image, (x, y))      


def check_shot(x, y):
    global player_1, player_2, player_1_win, player_2_win, player_1_score, player_2_score, total_games, shown_word, ticks
    ticks = pygame.time.get_ticks()
    if not player_1_win and not player_2_win and total_games != 0 and shown_word:
        pygame.mixer.music.play()
        if x > 0 and x < SCREEN_WIDTH // 2:
            if word == "shoot":
                player_1_win = True
                player_1_score += 1
            else:
                player_2_win = True
                player_1_score -= 1
        if x > SCREEN_WIDTH//2 and x < SCREEN_WIDTH:
            if word == "shoot":
                player_2_win = True
                player_2_score += 1
            else:
                player_1_win = True
                player_2_score -= 1
        total_games -= 1

def draw_game_over():
    global player_1_score, player_2_score
    if player_1_score > player_2_score:
        end_text = "Player 1 won"
    else:
        end_text = "Player 2 won" 

    end_img = basic_font.render(end_text, True, (200, 0, 0))
    pygame.draw.rect(screen, green, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50))
    screen.blit(end_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

    again_text = 'Play Again?'
    again_img = basic_font.render(again_text, True,  (200, 0, 0))
    pygame.draw.rect(screen, green, again_rect)
    screen.blit(again_img, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10))

player_1_win = False
player_2_win = False

player_1 = {}
player_2 = {}
player_1_score = 0
player_2_score = 0
word = ""
total_games = 3
ticks = pygame.time.get_ticks()
word_ticks = pygame.time.get_ticks()
current_ticks = pygame.time.get_ticks()
words = ["soccer", "sit", "socks", "shoot"]
show_word = False
shown_word = False
while running:
    if pygame.time.get_ticks() - ticks > 3000 and (player_2_win or  player_1_win):
        player_2_win = False
        player_1_win = False
        shown_word = False
        ticks = pygame.time.get_ticks()
        word_ticks = ticks
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            check_shot(pos[0], pos[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                check_shot(SCREEN_WIDTH // 2 - 10, 0)
            if event.key == pygame.K_RIGHT:
                check_shot(SCREEN_WIDTH // 2 + 10, 0)


    screen.blit(bg, (0, 0))
    pygame.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    if not shown_word and pygame.time.get_ticks() - word_ticks > 5000:
        word = random.choice(words)
        shown_word = True

    if word != "" and shown_word:
        font = basic_font.render(f"{word}", True, (200, 0 , 0))
        word_rect = pygame.draw.rect(screen, light_grey, (SCREEN_WIDTH // 2 - font.get_width() // 2, SCREEN_HEIGHT // 2, font.get_width(),50))
        screen.blit(font, word_rect)

    player_1_score_rect = pygame.draw.rect(screen, (255,255,255), (0, 0, 150,50))
    player_2_score_rect = pygame.draw.rect(screen, (255,255,255), (SCREEN_WIDTH - 150, 0, 150, 50))
    
    basic_font.render(f"Score {player_2_score}", True, (200, 0 , 0))

    screen.blit(basic_font.render(f"Score {player_1_score}", True, (200, 0 , 0)), player_1_score_rect)
    screen.blit(basic_font.render(f"Score {player_2_score}", True, (200, 0 , 0)), player_2_score_rect)

    if not player_1_win and not player_2_win:
        player_1 = Player(screen, "./assets/player.jpeg", 100, 100, 0, SCREEN_HEIGHT // 2 - 50)
        player_2 = Player(screen, "./assets/player_2.jpg", 100, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2 - 50)
    elif not player_1_win and player_2_win: 
        player_1 = Player(screen, "./assets/player_shot.jpeg", 100, 100, 0, SCREEN_HEIGHT // 2 - 50)
        player_2 = Player(screen, "./assets/player_2.jpg", 100, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2 - 50)
    elif player_1_win and not player_2_win:
        player_1 = Player(screen, "./assets/player.jpeg", 100, 100, 0, SCREEN_HEIGHT // 2 - 50)
        player_2 = Player(screen, "./assets/player_2_shot.jpg", 100, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2 - 50)

    if total_games == 0:
        draw_game_over()
        pos = pygame.mouse.get_pos() 
        if again_rect.collidepoint(pos):
                player_1_score = 0
                player_2_score = 0
                player_1_win = False
                player_2_win = False
                total_games = 3
    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()
sys.exit()
