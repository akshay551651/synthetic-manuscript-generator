from PIL import Image, ImageEnhance, ImageFilter
import numpy as np


def apply_ink_effects(image, seed=1):
    """
    Add subtle historical manuscript-style paper and ink effects.
    Keeps text readable while introducing natural variation.
    """

    rng = np.random.default_rng(seed)

    # Convert image to RGB
    image = image.convert("RGB")

    width, height = image.size

    # ---------------------------------------------------------
    # 1. Create subtle paper texture
    # ---------------------------------------------------------

    base = np.full(
        (height, width, 3),
        238,
        dtype=np.float32
    )

    # Low-frequency paper texture
    small_h = max(1, height // 20)
    small_w = max(1, width // 20)

    texture_small = rng.normal(
        loc=0,
        scale=5,
        size=(small_h, small_w)
    ).astype(np.float32)

    texture = Image.fromarray(
        np.clip(
            texture_small + 128,
            0,
            255
        ).astype(np.uint8)
    )

    texture = texture.resize(
        (width, height),
        Image.Resampling.BICUBIC
    )

    texture_array = (
        np.asarray(texture).astype(np.float32) - 128
    )

    for channel in range(3):
        base[:, :, channel] += texture_array

    # ---------------------------------------------------------
    # 2. Add fine paper grain
    # ---------------------------------------------------------

    grain = rng.normal(
        loc=0,
        scale=2.2,
        size=(height, width, 1)
    )

    base += grain

    base = np.clip(
        base,
        0,
        255
    ).astype(np.uint8)

    paper = Image.fromarray(
        base,
        "RGB"
    )

    # ---------------------------------------------------------
    # 3. Blend paper texture with generated manuscript
    # ---------------------------------------------------------

    image = Image.blend(
        paper,
        image,
        0.82
    )

    # ---------------------------------------------------------
    # 4. Slight blur for natural ink edges
    # ---------------------------------------------------------

    image = image.filter(
        ImageFilter.GaussianBlur(
            radius=0.25
        )
    )

    # ---------------------------------------------------------
    # 5. Slight contrast and brightness variation
    # ---------------------------------------------------------

    image = ImageEnhance.Contrast(
        image
    ).enhance(1.04)

    image = ImageEnhance.Brightness(
        image
    ).enhance(0.98)

    # ---------------------------------------------------------
    # 6. Add subtle final noise
    # ---------------------------------------------------------

    arr = np.asarray(
        image
    ).astype(np.int16)

    noise = rng.normal(
        loc=0,
        scale=1.5,
        size=arr.shape
    )

    arr = arr + noise

    arr = np.clip(
        arr,
        0,
        255
    ).astype(np.uint8)

    return Image.fromarray(
        arr,
        "RGB"
    )