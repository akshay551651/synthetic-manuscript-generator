from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


# --------------------------------------------------
# PROJECT BASE DIRECTORY
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# FONT PATHS
# --------------------------------------------------

DEVANAGARI_FONT = BASE_DIR / "fonts" / "ARIALUNI.ttf"

MODI_FONT = (
    BASE_DIR
    / "assets"
    / "reference"
    / "NotoSansModi-Regular.ttf"
)

SHARADA_FONT = (
    BASE_DIR
    / "assets"
    / "reference"
    / "NotoSansSharada-Regular.ttf"
)


# --------------------------------------------------
# GET FONT
# --------------------------------------------------

def get_font(script, size):

    if script == "devanagari":
        path = DEVANAGARI_FONT

    elif script == "modi":
        path = MODI_FONT

    elif script == "sharada":
        path = SHARADA_FONT

    else:
        raise ValueError(
            f"Unsupported script: {script}"
        )

    if not path.exists():
        raise FileNotFoundError(
            f"Font not found: {path}"
        )

    return ImageFont.truetype(
        str(path),
        size
    )


# --------------------------------------------------
# LOAD REFERENCE TEXT
# --------------------------------------------------

def load_text(script):

    path = (
        BASE_DIR
        / "assets"
        / "reference"
        / f"{script}.txt"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Reference file not found: {path}"
        )

    # UTF-8 with optional BOM support
    text = path.read_text(
        encoding="utf-8-sig"
    )

    return text.strip()


# --------------------------------------------------
# WRAP TEXT
# --------------------------------------------------

def wrap_text(
    text,
    font,
    max_width,
    draw
):

    words = text.split()

    lines = []

    current = ""

    for word in words:

        test_line = (
            word
            if not current
            else current + " " + word
        )

        bbox = draw.textbbox(
            (0, 0),
            test_line,
            font=font
        )

        text_width = (
            bbox[2] - bbox[0]
        )

        if text_width <= max_width:

            current = test_line

        else:

            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


# --------------------------------------------------
# RENDER TEXT PAGE
# --------------------------------------------------

def render_text_page(
    script,
    output_path,
    width=1600,
    height=2200
):

    text = load_text(script)

    # Manuscript-like base background
    image = Image.new(
        "RGB",
        (width, height),
        (220, 200, 160)
    )

    draw = ImageDraw.Draw(image)

    # Font
    font = get_font(
        script,
        48
    )

    # Margins
    margin_x = 150
    margin_y = 180

    max_width = (
        width - (2 * margin_x)
    )

    # Wrap text
    lines = wrap_text(
        text,
        font,
        max_width,
        draw
    )

    # Starting Y position
    y = margin_y

    # Space between lines
    line_spacing = 25

    # Draw lines
    for line in lines:

        bbox = draw.textbbox(
            (margin_x, y),
            line,
            font=font
        )

        line_height = (
            bbox[3] - bbox[1]
        )

        # Stop if page is full
        if (
            y + line_height
            > height - margin_y
        ):
            break

        draw.text(
            (margin_x, y),
            line,
            font=font,
            fill=(55, 40, 25)
        )

        y += (
            line_height
            + line_spacing
        )

    # Save image
    image.save(
        output_path
    )

    print(
        f"Rendered {script}: {output_path}"
    )


# --------------------------------------------------
# TEST ALL THREE SCRIPTS
# --------------------------------------------------

if __name__ == "__main__":

    for script in [
        "devanagari",
        "modi",
        "sharada"
    ]:

        render_text_page(
            script,
            f"{script}_text_test.png"
        )