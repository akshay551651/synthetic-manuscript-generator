from pathlib import Path
import random

from src.generator import generate_page


SCRIPTS = [
    "devanagari",
    "modi",
    "sharada",
]

SPLITS = {
    "train": 85,
    "validation": 10,
    "test": 5,
}


def generate_dataset():
    random.seed(42)

    for script in SCRIPTS:

        image_number = 1

        for split, count in SPLITS.items():

            output_dir = Path("output") / script / split
            output_dir.mkdir(parents=True, exist_ok=True)

            print(
                f"\nGenerating {script} - {split}: {count} images"
            )

            for _ in range(count):

                seed = random.randint(1, 1_000_000)

                generate_page(
                    script,
                    output_dir,
                    seed=seed
                )

                # Rename generated files with sequential numbering
                old_image = output_dir / f"{script}_001.png"
                old_md = output_dir / f"{script}_001.md"

                new_image = (
                    output_dir /
                    f"{script}_{image_number:03d}.png"
                )

                new_md = (
                    output_dir /
                    f"{script}_{image_number:03d}.md"
                )

                old_image.rename(new_image)
                old_md.rename(new_md)

                image_number += 1

    print("\n===================================")
    print("Dataset generation completed!")
    print("300 images generated.")
    print("===================================")


if __name__ == "__main__":
    generate_dataset()