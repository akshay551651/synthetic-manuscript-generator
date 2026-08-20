from PIL import ImageDraw


def create_layout(
    image,
    text,
    font,
    margin_x=150,
    margin_y=180,
    line_spacing=25,
):
    """
    Calculate text lines and positions so that text
    stays inside manuscript boundaries.
    """

    draw = ImageDraw.Draw(image)

    max_width = image.width - (2 * margin_x)
    max_height = image.height - (2 * margin_y)

    words = text.split()

    lines = []
    current_line = ""

    for word in words:
        test_line = (
            word
            if not current_line
            else current_line + " " + word
        )

        bbox = draw.textbbox(
            (0, 0),
            test_line,
            font=font
        )

        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line

        else:
            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    positions = []

    y = margin_y

    for line in lines:

        bbox = draw.textbbox(
            (margin_x, y),
            line,
            font=font
        )

        line_height = bbox[3] - bbox[1]

        if y + line_height > margin_y + max_height:
            break

        positions.append(
            (margin_x, y, line)
        )

        y += line_height + line_spacing

    return positions