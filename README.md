
---

# HIVE: Hyperbolic Interactive Visualization Explorer

<p align="center">
  <a href="https://openreview.net/pdf?id=D9LlujFg7d" target="_blank"><img src="https://img.shields.io/badge/View%20Paper-OpenReview-blue" alt="View Paper"></a>
  <a href="./HIVE_demo.mp4"><img src="https://img.shields.io/badge/Demo-Video-green" alt="Demo"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License"></a>
  <a href="https://github.com/thijmennijdam/HIVE/issues"><img src="https://img.shields.io/badge/Issues-Report%20Issue-red" alt="Issues"></a>
</p>

## Overview

**HIVE** is an interactive dashboard for visualizing and exploring hierarchical and hyperbolic data representations. The dashboard is the core contribution of this repo. We include the HyCoCLIP model plus GRIT and ImageNet subsets as example use cases.

🎬 **Demo:** [MP4 video](https://raw.githubusercontent.com/thijmennijdam/HIVE/main/HIVE_demo.mp4)

---

## Quick Start

### 0. Install `uv` (if you don’t already have it)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. Run the dashboard

```bash
# Create a virtual environment
uv venv

# Activate it
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

# Install dependencies
uv sync

# Launch
uv run src/main.py
```

---

## Using Your Own Datasets

We expect datasets to be preprocessed into the following layout:

```
dataset_name/
    trees/
        tree1/
            parent_images/
            parent_texts/
            child_images/
            child_texts/
        ...
    embeddings.pkl
    meta_data_trees.json
```

Once your data matches this structure, run:

```
projections_methods/create_projections.py
```

This script will generate:

```
cosine_embeddings.pkl
horopca_embeddings.pkl
```

You can now load your dataset and projections in the dashboard. Forking and adapting the code for custom data types is straightforward (and coding agents can help automate this).

---

## Features

* Interactive visualization of hierarchical & hyperbolic embeddings
* Built-in support for GRIT and ImageNet
* Compare projection methods (HoroPCA, CO-SNE)
* Dual-view and single-view modes
* Tree, neighbor, and interpolation exploration modes
* Modular codebase for plugging in new models/datasets

---

## Contributing

Pull requests and issues are welcome, whether for bug fixes, new features, or additional dataset/model integrations.

---

## Citation

If you use HIVE or its visualizations, please cite:

```
@inproceedings{nijdamhive,
  title={HIVE: A Hyperbolic Interactive Visualization Explorer for Representation Learning},
  author={Nijdam, Thijmen and Prinzhorn, Derck W. E. and de Heus, Jurgen and Brouwer, Thomas},
  booktitle={2nd Beyond Euclidean Workshop: Hyperbolic and Hyperspherical Learning for Computer Vision}
}
```

---

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
