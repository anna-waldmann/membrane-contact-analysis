import numpy as np
from skimage.io import imread, imsave
from skimage.morphology import dilation, disk
from pathlib import Path
import csv
import sys

# === SETTINGS ===
pixel_size_nm = 1.089
threshold_nm = 45
threshold_px = int(np.round(threshold_nm / pixel_size_nm))

# === PATHS ===
base_dir_str = sys.argv[1]
base_dir = Path(base_dir_str)
scv_dir = base_dir / "scv_masks"    
org_dir = base_dir / "organelle_masks"
out_dir = base_dir / "output"
out_dir.mkdir(exist_ok=True)

scv_files = list(scv_dir.glob("*.tif"))
org_files = list(org_dir.glob("*.tif"))

results = []

for scv_file in scv_files:
    scv_mask = imread(scv_file) > 0
    scv_name = scv_file.stem

    # Find organelle files with overlapping name parts
    # matches = [f for f in org_files if any(word in f.name for word in scv_name.split())]
    # if not matches:
    #     print(f"No organelle match found for: {scv_name}")
    #     continue
    matches = org_files

    for org_file in matches:
        org_mask = imread(org_file) > 0
        org_name = org_file.stem

        # Dilate SCV mask
        scv_dilated = dilation(scv_mask, disk(threshold_px))
        contact_mask = scv_dilated & org_mask

        scv_area = np.sum(scv_mask) * (pixel_size_nm ** 2)
        contact_area = np.sum(contact_mask) * (pixel_size_nm ** 2)
        percent_contact = (contact_area / scv_area * 100) if scv_area > 0 else 0

        # Save contact mask
        contact_out = out_dir / f"{scv_name}__{org_name}__contact_mask.tif"
        imsave(contact_out, (contact_mask * 255).astype(np.uint8))

        results.append({
            "SCV Mask": scv_name,
            "Organelle Mask": org_name,
            "Contact Detected": "Yes" if contact_area > 0 else "No",
            "SCV Area (nm²)": round(scv_area, 2),
            "Contact Area (nm²)": round(contact_area, 2),
            "Percent Contact (%)": round(percent_contact, 2)
        })

# Save CSV
csv_out = out_dir / "contact_results.csv"
if results:
    with open(csv_out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\n✅ Analysis complete. Results saved to: {csv_out}")
else:
    print("\n⚠️ No valid SCV-organelle pairs processed.")
