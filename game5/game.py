import time
import datetime
import pygame
import sys
import os
import webbrowser
import random
from screeninfo import get_monitors
from main import run

# переменные для звука и таймера
VOLUME = 0.4
SOUND_EFFECT = True

START_TIME = 0
FINISH_TIME = 0

pygame.init()


# класс для создания кнопок
class Button:

    def __init__(self, x, y, width, height, image, sound=None):
        global SOUND_EFFECT

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fon = False
        if width > 100:
            if "value" not in image and "select" not in image and "used" not in image:
                self.background_button = pygame.image.load("data/neon_eff.png")
                self.background_button = pygame.transform.scale(self.background_button, (
                    width + 20 if width < 140 else width + 50, height + 10))
                self.fon = True
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        if sound:
            self.sound = pygame.mixer.Sound(sound)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.ishovered = False

        if SOUND_EFFECT:
            self.volume = 1
        else:
            self.volume = 0

    def draw(self, screen):
        if self.ishovered:
            if self.fon:
                screen.blit(self.background_button, self.rect.topleft)
        screen.blit(self.image, self.rect.topleft)

    def homing(self, mouse_pos):
        self.ishovered = self.rect.collidepoint(mouse_pos)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.ishovered:
            if self.sound:
                self.sound.play()
                self.sound.set_volume(self.volume)
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


# основное меню
class Menu:

    def __init__(self):
        for m in get_monitors():
            self.x = m.width / 1920
            self.y = m.height / 1080
        size = self.width, self.height = 1920, 1080
        pygame.display.set_caption("GOLF")
        self.window = True
        if self.window:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)
        pygame.mixer.music.load("music/music_fon7.mp3")

        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(VOLUME)

        self.choice = "white_choice"
        self.level_number = 0
        self.sound_eff = True
        self.main_menu()

    def main_menu(self):
        clock = pygame.time.Clock()
        background = pygame.transform.scale(pygame.image.load("data/b.png"), (1920 * self.x, 1080 * self.y))
        background = pygame.transform.scale(background, (self.width, self.height))

        button_play = Button(829, 294, 263.15, 132.38, "data/button_play.png", sound="music/button_click.mp3")
        button_settings = Button(711, 403.56, 498.03, 112.367, "data/button_settings.png",
                                 sound="music/button_click.mp3")
        button_customization = Button(711, 498.81, 498.03, 112.367, "data/button_customization.png",
                                      sound="music/button_click.mp3")
        button_credits = Button(711, 599.18, 498.03, 112.367, "data/button_credits.png", sound="music/button_click.mp3")
        button_exit = Button(897.52, 693.41, 237.789, 120.539, "data/button_exit.png", sound="music/button_click.mp3")
        button_ds = Button(785, 703.63, 115.833, 98.321, "data/button_ds.png", sound="music/button_click.mp3")

        fps = 50
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT and event.button == button_exit:
                    running = False

                if event.type == pygame.USEREVENT and event.button == button_ds:
                    webbrowser.open_new("https://discord.com/")

                if event.type == pygame.USEREVENT and event.button == button_credits:
                    self.credits()

                if event.type == pygame.USEREVENT and event.button == button_settings:
                    self.setting()

                if event.type == pygame.USEREVENT and event.button == button_customization:
                    self.customization()

                if event.type == pygame.USEREVENT and event.button == button_play:
                    self.play()

                for button in [button_play, button_settings, button_customization, button_credits, button_exit,
                               button_ds]:
                    button.event(event)

            for button in [button_play, button_settings, button_customization, button_credits, button_exit, button_ds]:
                button.homing(pygame.mouse.get_pos())
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()
        sys.exit()

    def setting(self):
        global VOLUME
        global SOUND_EFFECT

        clock = pygame.time.Clock()
        background = pygame.image.load("data/background_settings.png")
        background = pygame.transform.scale(background, (1920, 1080))

        sound_on = Button(1096, 490, 100, 100, "data/eff_on.png", sound="music/button_click.mp3")
        sound_off = Button(1096, 490, 100, 100, "data/eff_off.png", sound="music/button_click.mp3")
        volume_zero = Button(744, 374, 106.663, 85.306, "data/value_zero.png", sound="music/button_click.mp3")
        volume_max = Button(906.68, 374, 106.663, 85.306, "data/value_plus.png", sound="music/button_click.mp3")
        volume_min = Button(1069.37, 374, 106.663, 85.306, "data/value_min.png", sound="music/button_click.mp3")
        button_exit = Button(829, 722, 262, 133, "data/button_exit1.png", sound="music/button_click.mp3")

        if SOUND_EFFECT:
            sound = sound_on
        else:
            sound = sound_off

        fps = 50
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT and event.button == button_exit:
                    self.main_menu()

                elif event.type == pygame.USEREVENT and event.button == volume_zero:
                    VOLUME = 0
                    pygame.mixer.music.set_volume(VOLUME)


                elif event.type == pygame.USEREVENT and event.button == volume_max:
                    if VOLUME < 1:
                        VOLUME += 0.2
                        pygame.mixer.music.set_volume(VOLUME)


                elif event.type == pygame.USEREVENT and event.button == volume_min:
                    if VOLUME >= 0.2:
                        VOLUME -= 0.2
                        pygame.mixer.music.set_volume(VOLUME)

                elif event.type == pygame.USEREVENT and event.button == sound:
                    if SOUND_EFFECT:
                        SOUND_EFFECT = False
                    else:
                        SOUND_EFFECT = True
                    self.setting()

                for button in [volume_max, volume_min, volume_zero, button_exit, sound]:
                    button.event(event)

            for button in [volume_max, volume_min, volume_zero, button_exit, sound]:
                button.homing(pygame.mouse.get_pos())
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()

    def play(self):
        clock = pygame.time.Clock()
        background = pygame.image.load("data/b.png")
        background = pygame.transform.scale(background, (self.width, self.height))

        # оформленидля level
        level_1 = Button(713, 438, 494.02, 296.41, "data/level1.png", sound="music/button_click.mp3")
        level_2 = Button(713, 438, 494.02, 296.41, "data/level_2.png", sound="music/button_click.mp3")
        level_3 = Button(713, 438, 494.02, 296.41, "data/level_3.png", sound="music/button_click.mp3")
        level_4 = Button(713, 438, 494.02, 296.41, "data/level_4.png", sound="music/button_click.mp3")

        arrow_right = Button(1197, 536, 100, 100, "data/arrows_right.png", sound="music/button_click.mp3")
        arrow_left = Button(623, 536, 100, 100, "data/arrows_left.png", sound="music/button_click.mp3")
        button_exit = Button(698, 290, 262, 133, "data/exit_level.png", sound="music/button_click.mp3")
        button_play = Button(980, 290, 262, 133, "data/play_level.png", sound="music/button_click.mp3")

        group = [level_1, level_2, level_3, level_4]

        level = group[self.level_number]

        fps = 50
        running = True
        while running:
            self.screen.fill((224, 255, 244, 1))
            self.screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT and event.button == button_exit:
                    self.main_menu()

                if event.type == pygame.USEREVENT and event.button == arrow_right:
                    if self.level_number == 3:
                        self.level_number = 0
                    else:
                        self.level_number += 1
                    self.play()

                if event.type == pygame.USEREVENT and event.button == arrow_left:
                    if self.level_number == 0:
                        self.level_number = 3
                    else:
                        self.level_number -= 1
                    self.play()

                if event.type == pygame.USEREVENT and event.button == button_play:
                    # здесь передаётся цвет, громкость, номер уровня, есть эффекты или нет
                    Play(self.choice, self.level_number + 1, self.sound_eff)

                for button in [level, arrow_left, arrow_right, button_play, button_exit]:
                    button.event(event)

            for button in [level, arrow_left, arrow_right, button_play, button_exit]:
                button.homing(pygame.mouse.get_pos())
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()

    def credits(self):
        clock = pygame.time.Clock()
        background = pygame.image.load("data/bfckground_credits.png")
        background = pygame.transform.scale(background, (self.width, self.height))

        fps = 50
        running = True
        while running:
            self.screen.fill((224, 255, 244, 1))
            self.screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()

            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()

    def customization(self):
        clock = pygame.time.Clock()
        background = pygame.image.load("data/b.png")
        background = pygame.transform.scale(background, (self.width, self.height))

        white_choice = ["white_choice", True]
        red_choice = ["red_choice", False]
        blue_choice = ["blue_choice", False]
        orange_choice = ["orange_choice", False]
        green_choice = ["green_choice", False]
        group = [white_choice, red_choice, blue_choice, orange_choice, green_choice]

        # сдесь нажатия проверяются и меняется картинка
        for i in group:
            if self.choice == str(i[0]):
                i[1] = True
            elif self.choice not in i:
                i[1] = False

        if white_choice[1]:
            white = Button(684, 315, 176.75, 176.75, "data/custom_used_white.png", sound="music/button_click.mp3")
        elif not white_choice[1]:
            white = Button(684, 315, 176.75, 176.75, "data/white_select.png", sound="music/button_click.mp3")

        if red_choice[1]:
            red = Button(871.63, 315, 176.75, 176.75, "data/red_used.png", sound="music/button_click.mp3")
        elif not red_choice[1]:
            red = Button(871.63, 315, 176.75, 176.75, "data/red_select.png", sound="music/button_click.mp3")

        if orange_choice[1]:
            orange = Button(1059.25, 315, 176.75, 176.75, "data/orange_used.png", sound="music/button_click.mp3")
        elif not orange_choice[1]:
            orange = Button(1059.25, 315, 176.75, 176.75, "data/orange_select.png", sound="music/button_click.mp3")

        if green_choice[1]:
            green = Button(684, 537.7, 176.75, 176.75, "data/green_used.png", sound="music/button_click.mp3")
        elif not green_choice[1]:
            green = Button(684, 537.7, 176.75, 176.75, "data/green_select.png", sound="music/button_click.mp3")

        button_exit = Button(829, 722, 262, 133, "data/button_exit1.png", sound="music/button_click.mp3")

        fps = 50
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT and event.button == button_exit:
                    self.main_menu()

                if event.type == pygame.USEREVENT and event.button == white:
                    self.choice = "white_choice"
                    self.customization()

                if event.type == pygame.USEREVENT and event.button == red:
                    self.choice = "red_choice"
                    self.customization()

                if event.type == pygame.USEREVENT and event.button == orange:
                    self.choice = "orange_choice"
                    self.customization()

                if event.type == pygame.USEREVENT and event.button == green:
                    self.choice = "green_choice"
                    self.customization()

                for button in [white, red, orange, green, button_exit]:
                    button.event(event)

            for button in [white, red, orange, green, button_exit]:
                button.homing(pygame.mouse.get_pos())
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()


# класс с игрой
class Play:
    def __init__(self, color, level, sound_eff):
        global START_TIME
        global VOLUME

        self.music_fon = ["music/fon1.mp3", "music/fon4.mp3", "music/fon5.mp3", "music/fon6.mp3"]
        self.color = color
        self.level = level
        self.sound_eff = sound_eff

        size = self.width, self.height = 1920, 1080
        pygame.display.set_caption("GOLF")
        self.window = False
        if self.window:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)
        pygame.mixer.music.load(random.choice(self.music_fon))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(VOLUME)
        self.game()

    def game(self):

        run()

        clock = pygame.time.Clock()
        fps = 50
        running = True
        while running:
            self.screen.fill((224, 255, 244, 1))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()
        sys.exit()


# класс окончания игры
class Finish:
    def __init__(self, time, color, level, sound_eff):
        global VOLUME
        global START_TIME

        self.t = time

        self.color = color
        self.level = level
        self.sound_eff = sound_eff

        size = self.width, self.height = 1920, 1080
        pygame.display.set_caption("GOLF")
        self.window = False
        if self.window:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)

        pygame.mixer.music.load("music/level_complete.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(VOLUME)
        self.fin()

    def fin(self):
        global VOLUME
        global SOUND_EFFECT
        global START_TIME

        # здесь тект текущее время, лучшее время и количество ударров
        font = pygame.font.Font("fonts/JejuHallasan-Regular.ttf", 64, )
        text_1 = font.render(self.t, True, (255, 221, 119, 1))

        font1 = pygame.font.Font("fonts/JejuHallasan-Regular.ttf", 48)
        text_2 = font1.render("    --", True, (255, 221, 119, 1))
        text_3 = font1.render("   --", True, (255, 221, 119, 1))

        background = pygame.image.load("data/background_finish.png")
        background = pygame.transform.scale(background, (1920, 1080))

        replicate = Button(762, 755, 206, 105, "data/button_again.png", sound="music/button_click.mp3")
        menu = Button(952, 755, 206, 105, "data/button_menu.png", sound="music/button_click.mp3")

        clock = pygame.time.Clock()
        fps = 50
        running = True
        while running:
            self.screen.fill((224, 255, 244, 1))
            self.screen.blit(background, (0, 0))
            self.screen.blit(text_1, (880, 429))
            self.screen.blit(text_2, (896, 579))
            self.screen.blit(text_3, (919, 707))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT and event.button == replicate:
                    START_TIME = 0
                    Play(self.color, self.level, self.sound_eff)

                if event.type == pygame.USEREVENT and event.button == menu:
                    START_TIME = 0
                    Menu()

                for button in [replicate, menu]:
                    button.event(event)

            for button in [replicate, menu]:
                button.homing(pygame.mouse.get_pos())
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()
        sys.exit()


# класс паузы


if __name__ == "__main__":
    Menu()
