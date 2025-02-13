import pygame
import os
from settings import CARD_SIZE  # Used to scale images

def load_assets():
    """Loads fonts, sounds, images, and background music with error handling."""
    assets = {}

    # 🎨 Load font
    try:
        assets["font"] = pygame.font.Font(None, 72)  # Default large font
    except Exception as e:
        print(f"Error loading font: {e}")
        assets["font"] = pygame.font.SysFont("Arial", 72)

    # 🔊 Load sounds dynamically from the 'sounds/' directory
    assets["sounds"] = {}
    sound_dir = "sounds"

    if os.path.exists(sound_dir):
        for file in os.listdir(sound_dir):
            if file.endswith(".wav") or file.endswith(".mp3"):
                key = file.split(".")[0]  # Extract name without extension
                path = os.path.join(sound_dir, file)
                try:
                    assets["sounds"][key] = pygame.mixer.Sound(path)
                    assets["sounds"][key].set_volume(0.5)  # Set default volume
                except pygame.error as e:
                    print(f"Error loading sound {file}: {e}")
                    assets["sounds"][key] = None
    else:
        print(f"Warning: Sound directory '{sound_dir}' not found!")

    # 🖼️ Load images for cards from the 'images/' directory
    assets["images"] = {}
    image_dir = "images"
    if os.path.exists(image_dir):
        for file in os.listdir(image_dir):
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                try:
                    # Load and scale image to the card size
                    image_surface = pygame.image.load(os.path.join(image_dir, file)).convert_alpha()
                    image_surface = pygame.transform.smoothscale(image_surface, (CARD_SIZE, CARD_SIZE))
                    # File name without extension is used as key (e.g., "apple")
                    key = file.split('.')[0]
                    assets["images"][key] = image_surface
                except Exception as e:
                    print(f"Error loading image {file}: {e}")
    else:
        print("Warning: Images directory 'images' not found!")

    # 🎵 Load background music
    bg_music = os.path.join(sound_dir, "background.mp3")
    if os.path.exists(bg_music):
        try:
            pygame.mixer.music.load(bg_music)
            pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
            pygame.mixer.music.play(-1)  # Loop background music
        except pygame.error as e:
            print(f"Error loading background music: {e}")
    else:
        print(f"Warning: Missing background music {bg_music}")

    return assets
