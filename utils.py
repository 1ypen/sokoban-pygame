import os
import pygame
from settings import TILE_SIZE


def load_images(path):
    """
    Loads all images in directory. The directory must only contain images.

    Args:
        path: The relative or absolute path to the directory to load images from.

    Returns:
        List of images.
    """
    images = []
    for file_name in os.listdir(path):
        full_image = pygame.image.load(path + os.sep + file_name).convert_alpha()
        image = pygame.transform.scale(full_image, (TILE_SIZE, TILE_SIZE))
        images.append(image)
    return images


