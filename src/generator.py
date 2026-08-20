from pathlib import Path
from PIL import ImageDraw

from src.background import generate_background
from src.layout import create_layout
from src.effects import apply_ink_effects
from src.tect_renderer import get_font, load_text


def generate_page(script, output_dir, seed=1):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image = generate_background(seed=seed)

    text = load_text(script)
    font = get_font(script, 48)

    positions = create_layout(
        image,
        text,
        font
    )

    draw = ImageDraw.Draw(image)

    annotations = []

    for x, y, line in positions:

        bbox = draw.textbbox(
            (x, y),
            line,
            font=font
        )

        x1, y1, x2, y2 = bbox

        draw.text(
            (x, y),
            line,
            font=font,
            fill=(55, 40, 25)
        )

        annotations.append({
            "text": line,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        })

    image = apply_ink_effects(
        image,
        seed=seed
    )

    image_path = output_dir / f"{script}_001.png"
    annotation_path = output_dir / f"{script}_001.md"

    image.save(image_path)

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
        "|---:|---|---:|---:|---:|---:|"
    ]

    for index, item in enumerate(annotations, start=1):

        safe_text = item["text"].replace("|", "\\|")

        annotation_lines.append(
            f"| {index} | {safe_text} | "
            f"{item['x1']} | {item['y1']} | "
            f"{item['x2']} | {item['y2']} |"
        )

    annotation = "\n".join(annotation_lines) + "\n"

    annotation_path.write_text(
        annotation,
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
