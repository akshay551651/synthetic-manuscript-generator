from pathlib import Path
from generate import generate_page

OUTPUT_DIR = "output/dataset"

SCRIPTS = [
    "devanagari",
    "modi",
    "sharada"
]

PAGES_PER_SCRIPT = 10


def main():

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    for script in SCRIPTS:

        print()
        print("=" * 60)
        print(f"Generating {script} pages...")
        print("=" * 60)

        for page_number in range(1, PAGES_PER_SCRIPT + 1):

            generate_page(
                script,
                OUTPUT_DIR,
                seed=page_number,
                page_number=page_number
            )

    print()
    print("=" * 60)
    print("DATASET GENERATION COMPLETE")
    print("=" * 60)
    print(f"Output folder: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()