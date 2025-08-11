# SCV–Organelle Contact Analysis

This repository contains a Python script to quantify membrane contact sites between **Salmonella-containing vacuoles (SCVs)** and organelles from binary mask images.

The script:
1. Reads SCV and organelle mask `.tif` files.
2. Expands each SCV mask by a fixed nanometer distance set to 45 nm.
3. Calculates the contact area between the dilated SCV mask and each organelle mask.
4. Outputs a **contact mask** image for visualization and a `.csv` file with contact statistics.

---

## Requirements

- Python 3.x
- [NumPy](https://numpy.org/)
- [scikit-image](https://scikit-image.org/)

Install dependencies with:
```bash
pip install numpy scikit-image
```
