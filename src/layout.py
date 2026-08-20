from PIL import ImageDraw


def create_layout(image, text, font):
    """
    Create text positions and bounding boxes.

    Returns:
        [
            (x, y, line, bbox),
            ...
        ]
    """

    draw = ImageDraw.Draw(image)

    width, height = image.size

    margin_x = 150
    margin_y = 180

    max_width = width - (2 * margin_x)

    # Split text into words
    words = text.split()

    lines = []
    current_line = ""

    # Build lines according to available width
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

        text_width = bbox[2] - bbox[0]

        if text_width <= max_width:
            current_line = test_line

        else:

            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    positions = []

    y = margin_y

    line_spacing = 25

    for line in lines:

        bbox = draw.textbbox(
            (margin_x, y),
            line,
            font=font
        )

        x1, y1, x2, y2 = bbox

        line_height = y2 - y1

        # Stop if text reaches bottom of page
        if y + line_height > height - margin_y:
            break

        positions.append(
            (
                margin_x,
                y,
                line,
                (
                    x1,
                    y1,
                    x2,
                    y2
                )
            )
        )

        y += line_height + line_spacing

    return positions