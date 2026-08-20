\# Synthetic Manuscript Generator



\## Overview



Synthetic Manuscript Generator is an automated Python pipeline for generating realistic synthetic Indic manuscript folios with synchronized ground-truth annotations.



The pipeline supports:



\- Devanagari

\- Modi

\- Sharada



Each generated manuscript image is paired with a Markdown annotation file containing the script, image dimensions, seed, text, and line-level bounding-box annotations.



\## Features



\- Synthetic aged manuscript backgrounds

\- Text rendering for Indic scripts

\- Automatic text wrapping and layout

\- Line-level bounding-box annotations

\- Ink effects and manuscript imperfections

\- Reproducible generation using random seeds

\- Train/validation/test dataset generation

\- Modular Python architecture



\## Dataset



The generated dataset contains:



| Script | Train | Validation | Test | Total |

|---|---:|---:|---:|---:|

| Devanagari | 85 | 10 | 5 | 100 |

| Modi | 85 | 10 | 5 | 100 |

| Sharada | 85 | 10 | 5 | 100 |

| \*\*Total\*\* | \*\*255\*\* | \*\*30\*\* | \*\*15\*\* | \*\*300\*\* |



Each image has a corresponding `.md` annotation file.



\## Project Structure



```text

synthetic-manuscript-generator/

│

├── assets/

│   └── reference/

│

├── config/

│   └── config.py

│

├── src/

│   ├── background.py

│   ├── effects.py

│   ├── generator.py

│   ├── layout.py

│   ├── annotations.py

│   └── tect\_renderer.py

│

├── output/

│   ├── devanagari/

│   │   ├── train/

│   │   ├── validation/

│   │   └── test/

│   │

│   ├── modi/

│   │   ├── train/

│   │   ├── validation/

│   │   └── test/

│   │

│   └── sharada/

│       ├── train/

│       ├── validation/

│       └── test/

│

├── generate.py

├── README.md

└── requirements.txt

