import pygame
import sys
import imageio
from button import Button
# from pgu import gui

pygame.init()

WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pomodoro Timer")

CLOCK = pygame.time.Clock()

# Load a backdrop image with transparency
BACKDROP = pygame.image.load("assets/backdrop.png").convert_alpha()

# Background GIF
gif = imageio.get_reader("gif.gif")
target_width, target_height = 900, 600
frames = [
    pygame.transform.scale(pygame.image.fromstring(frame.tobytes(), frame.shape[1::-1], "RGB"), (target_width, target_height))
    for frame in gif
]

# Additional GIF-related variables
gif_frame_index = 0
gif_fps = 30

WHITE_BUTTON = pygame.image.load("assets/button.png")

FONT = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 120)
timer_text_rect = FONT.render("25:00", True, "white").get_rect(center=(WIDTH / 2, HEIGHT / 2 - 25))

# Button
START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH / 2, HEIGHT / 2 + 100), 170, 60, "START",
                           pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
RESET_BUTTON = Button(None, (WIDTH / 2 + 160, HEIGHT / 2 + 100), 120, 30, "Reset",
                          pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
MUSIC_BUTTON = Button(None, (WIDTH / 2 - 180, HEIGHT / 2 + 100), 120, 30, "Music",
                          pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
POMODORO_BUTTON = Button(None, (WIDTH / 2 - 150, HEIGHT / 2 - 140), 120, 30, "Pomodoro",
                          pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
SHORT_BREAK_BUTTON = Button(None, (WIDTH / 2, HEIGHT / 2 - 140), 120, 30, "Short Break",
                            pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
LONG_BREAK_BUTTON = Button(None, (WIDTH / 2 + 150, HEIGHT / 2 - 140), 120, 30, "Long Break",
                           pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
# Time length
POMODORO_LENGTH = 1500  # 1500 secs = 25 mins
SHORT_BREAK_LENGTH = 300  # 300 secs = 5 mins
LONG_BREAK_LENGTH = 900  # 900 secs = 15 mins

current_seconds = POMODORO_LENGTH
pygame.time.set_timer(pygame.USEREVENT, 1000)
started = False

# Initial alpha value (0-255)
current_alpha = 255

# Load music
pygame.mixer.music.load("D:\Pomodoro-Timer-PyGame-main\LofiMusic.mp3")
music_playing = False
    
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if START_STOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                if started:
                    started = False
                else:
                    started = True
            if POMODORO_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = POMODORO_LENGTH
                started = False
            if RESET_BUTTON.check_for_input(pygame.mouse.get_pos()):
                if LONG_BREAK_LENGTH < current_seconds <= POMODORO_LENGTH:
                    current_seconds = POMODORO_LENGTH
                    started = False
                elif SHORT_BREAK_LENGTH < current_seconds <= LONG_BREAK_LENGTH:
                    current_seconds = LONG_BREAK_LENGTH
                    started = False
                elif current_seconds <= SHORT_BREAK_LENGTH:
                    current_seconds = SHORT_BREAK_LENGTH
                    started = False
            if SHORT_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = SHORT_BREAK_LENGTH    
                started = False
            if LONG_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = LONG_BREAK_LENGTH
                started = False
            if started:
                START_STOP_BUTTON.text_input = "STOP"
                START_STOP_BUTTON.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                    START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
            else:
                START_STOP_BUTTON.text_input = "START"
                START_STOP_BUTTON.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                    START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
            
            # Check if the Music button is clicked
            if MUSIC_BUTTON.check_for_input(pygame.mouse.get_pos()):
                music_playing = not music_playing  # Toggle music state
                if music_playing:
                    pygame.mixer.music.play(-1)  # -1 means play on loop
                else:
                    pygame.mixer.music.pause()
            if music_playing:
                MUSIC_BUTTON.text_input = "Music: ON"
                MUSIC_BUTTON.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                    MUSIC_BUTTON.text_input, True, MUSIC_BUTTON.base_color)
            else:
                MUSIC_BUTTON.text_input = "Music: OFF"
                MUSIC_BUTTON.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                    MUSIC_BUTTON.text_input, True, MUSIC_BUTTON.base_color)
        if event.type == pygame.USEREVENT and started:
            current_seconds -= 1

    # Display frame of the GIF
    SCREEN.blit(frames[gif_frame_index], (0, 0))
    gif_frame_index = (gif_frame_index + 1) % len(frames)

    # Set the alpha value for the backdrop
    BACKDROP.set_alpha(current_alpha)
    
    SCREEN.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

    START_STOP_BUTTON.update(SCREEN)
    START_STOP_BUTTON.change_color(pygame.mouse.get_pos())

    RESET_BUTTON.update(SCREEN)
    RESET_BUTTON.change_color(pygame.mouse.get_pos())

    MUSIC_BUTTON.update(SCREEN)
    MUSIC_BUTTON.change_color(pygame.mouse.get_pos())

    POMODORO_BUTTON.update(SCREEN)
    POMODORO_BUTTON.change_color(pygame.mouse.get_pos())

    SHORT_BREAK_BUTTON.update(SCREEN)
    SHORT_BREAK_BUTTON.change_color(pygame.mouse.get_pos())

    LONG_BREAK_BUTTON.update(SCREEN)
    LONG_BREAK_BUTTON.change_color(pygame.mouse.get_pos())

    if current_seconds >= 0:
        display_seconds = current_seconds % 60
        display_minutes = int(current_seconds / 60) % 60

    timer_text = FONT.render(f"{display_minutes:2}:{display_seconds:02}", True, "white")
    SCREEN.blit(timer_text, timer_text_rect)

    pygame.display.update()
    CLOCK.tick(gif_fps)  # Adjust the frame rate based on GIF's frame rate

    # Gradually decrease the alpha value
    current_alpha = max(150, current_alpha - 1)