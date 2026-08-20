from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


DEVANAGARI_FONT = r"C:\Windows\Fonts\ARIALUNI.ttf"
MODI_FONT = r"assets\reference\NotoSansModi-Regular.ttf"
SHARADA_FONT = r"assets\reference\NotoSansSharada-Regular.ttf"


def get_font(script, size):
    if script == "devanagari":
        path = DEVANAGARI_FONT
    elif script == "modi":
        path = MODI_FONT
    elif script == "sharada":
        path = SHARADA_FONT
    else:
        raise ValueError(f"Unsupported script: {script}")

    return ImageFont.truetype(path, size)


def load_text(script):
    path = Path(f"assets/reference/{script}.txt")

    if not path.exists():
        raise FileNotFoundError(f"Reference file not found: {path}")

    return path.read_text(encoding="utf-8").strip()


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test_line = word if not current else current + " " + word

        bbox = draw.textbbox(
            (0, 0),
            test_line,
            font=font
        )

        if bbox[2] - bbox[0] <= max_width:
            current = test_line
        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


def render_text_page(
    script,
    output_path,
    width=1600,
    height=2200
):
    text = load_text(script)

    image = Image.new(
        "RGB",
        (width, height),
        (220, 200, 160)
    )

    draw = ImageDraw.Draw(image)

    font = get_font(script, 48)

    margin_x = 150
    margin_y = 180

    max_width = width - (2 * margin_x)

    lines = wrap_text(
        text,
        font,
        max_width,
        draw
    )

    y = margin_y

    line_spacing = 25

    for line in lines:

        bbox = draw.textbbox(
            (margin_x, y),
            line,
            font=font
        )

        line_height = bbox[3] - bbox[1]

        if y + line_height > height - margin_y:
            break

        draw.text(
            (margin_x, y),
            line,
            font=font,
            fill=(55, 40, 25)
        )

        y += line_height + line_spacing

    image.save(output_path)

    print(f"Rendered {script}: {output_path}")


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