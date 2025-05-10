import pygame

pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

def play_sound(sound_path):
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(-1)

def stop_sound():
    pygame.mixer.music.stop()