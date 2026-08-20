from PIL import Image, ImageDraw, ImageFilter
import random


def generate_background(
    width=1600,
    height=2200,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    image = Image.new(
        "RGB",
        (width, height),
        (220, 200, 160)
    )

    pixels = image.load()

    # Natural paper/palm-leaf colour variation
    for y in range(height):
        for x in range(width):

            variation = random.randint(-12, 12)

            r = max(0, min(255, 220 + variation))
            g = max(0, min(255, 200 + variation))
            b = max(0, min(255, 160 + variation))

            pixels[x, y] = (r, g, b)

    draw = ImageDraw.Draw(image)

    # Small natural surface marks
    for _ in range(1200):

        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        radius = random.randint(1, 4)

        shade = random.randint(120, 190)

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=(shade, shade - 10, shade - 30)
        )

    # Slight blur to make the texture natural
    image = image.filter(
        ImageFilter.GaussianBlur(radius=0.6)
    )

    return image