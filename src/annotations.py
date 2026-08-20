from pathlib import Path
from PIL import ImageDraw

from src.background import generate_background
from src.layout import create_layout
from src.effects import apply_ink_effects
from src.tect_renderer import get_font, load_text


def generate_page(script, output_dir, seed=1):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate manuscript background
    image = generate_background(seed=seed)

    # Load reference text and font
    text = load_text(script)
    font = get_font(script, 48)

    # Create text layout with bounding boxes
    positions = create_layout(
        image,
        text,
        font
    )

    draw = ImageDraw.Draw(image)

    # Draw each text line
    for x, y, line, bbox in positions:

        draw.text(
            (x, y),
            line,
            font=font,
            fill=(55, 40, 25)
        )

    # Apply manuscript ink effects
    image = apply_ink_effects(
        image,
        seed=seed
    )

    # Output paths
    image_path = output_dir / f"{script}_001.png"
    annotation_path = output_dir / f"{script}_001.md"

    # Save image
    image.save(image_path)

    # Create annotation
    annotation_lines = [
        "# Synthetic Manuscript Annotation",
        "",
        f"- Script: {script}",
        f"- Image: {image_path.name}",
        f"- Width: {image.width}",
        f"- Height: {image.height}",
        f"- Seed: {seed}",
        "",
        "## Text",
        "",
        text,
        "",
        "## Line Annotations",
        "",
    ]

    for index, (x, y, line, bbox) in enumerate(
        positions,
        start=1
    ):

        annotation_lines.append(
            f"{index}. "
            f"Text: `{line}`  "
            f"BoundingBox: `{bbox}`"
        )

    annotation_path.write_text(
        "\n".join(annotation_lines),
        encoding="utf-8"
    )

    print(f"Generated: {image_path}")
    print(f"Annotation: {annotation_path}")


if __name__ == "__main__":

    for script in [
        "devanagari",
        "modi",
        "sharada"
    ]:

        generate_page(
            script,
            "output/test",
            seed=1
        )