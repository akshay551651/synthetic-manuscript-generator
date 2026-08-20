from PIL import Image, ImageEnhance, ImageFilter
import random


def apply_ink_effects(image, seed=None):
    if seed is not None:
        random.seed(seed)

    # Slightly soften the rendered ink
    image = image.filter(
        ImageFilter.GaussianBlur(radius=0.25)
    )

    # Slight contrast variation
    contrast = random.uniform(0.95, 1.08)

    image = ImageEnhance.Contrast(image).enhance(
        contrast
    )

    # Slight brightness variation
    brightness = random.uniform(0.96, 1.04)

    image = ImageEnhance.Brightness(image).enhance(
        brightness
    )

    return image