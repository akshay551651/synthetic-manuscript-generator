from pathlib import Path
from PIL import ImageDraw

from src.background import generate_background
from src.layout import create_layout
from src.effects import apply_ink_effects
from src.tect_renderer import get_font, load_text


def generate_page(script, output_dir, seed=1, page_number=1):

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
    for item in positions:

        x, y, line, bbox = item

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

    # Output paths with page numbering
    image_path = output_dir / f"{script}_{page_number:03d}.png"
    annotation_path = output_dir / f"{script}_{page_number:03d}.md"

    # Save image
    image.save(
        image_path,
        format="PNG"
    )

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
        "| Line | Text | X1 | Y1 | X2 | Y2 |",
        "|---:|---|---:|---:|---:|---:|",
    ]

    # Add bounding-box annotations
    for index, item in enumerate(positions, start=1):

        x, y, line, bbox = item

        x1, y1, x2, y2 = bbox

        annotation_lines.append(
            f"| {index} | {line} | "
            f"{x1} | {y1} | {x2} | {y2} |"
        )

    # Save annotation as UTF-8
    annotation_path.write_text(
        "\n".join(annotation_lines),
        encoding="utf-8"
    )

    print(f"Generated: {image_path}")
    print(f"Annotation: {annotation_path}")


if __name__ == "__main__":

    scripts = [
        "devanagari",
        "modi",
        "sharada"
    ]

    for script in scripts:

        generate_page(
            script,
            "output/test",
            seed=1,
            page_number=1
        )