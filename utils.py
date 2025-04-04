# utils.py
import pygame
from pygame import mixer

def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

# Function to draw text on the screen at a specified position
def draw_text(screen, text, pos, size, color):
    # Load the default font with the specified size
    font = pygame.font.Font(None, size)

    # Render the text with the chosen font and color
    rendered_text = font.render(text, True, color)

    # Draw the rendered text at the specified position on the screen
    screen.blit(rendered_text, pos)

def play_sound(sound_file, volume=0.1):
    """Plays a sound file."""
    mixer.init()
    sound = mixer.Sound(sound_file)
    sound.set_volume(volume)  # Volume range: 0.0 (mute) to 1.0 (full)
    sound.play()