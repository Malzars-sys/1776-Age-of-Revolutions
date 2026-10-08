"""Inspect alpha values only; never retouch, mask or recolor an image."""
import json
from collections import Counter
from PIL import Image
from asset4_style_reference_audit import ROOT
PACK = ROOT / "docs/reports/assets/asset19_preview_2026-10-05"
plan = json.loads((PACK / "generation_plan.json").read_text(encoding="utf-8"))
results = []
for entry in plan["entries"]:
    image = Image.open(PACK / entry["preview"]).convert("RGBA")
    alpha = image.getchannel("A")
    histogram = Counter(alpha.get_flattened_data())
    visible = sum(count for value, count in histogram.items() if value >= 16)
    nearly_opaque = sum(count for value, count in histogram.items() if value >= 250)
    results.append({
        "key": entry["key"],
        "most_common_alpha_values": histogram.most_common(8),
        "alpha_at_least_250_fraction_of_visible": round(nearly_opaque / visible, 6),
        "image_modified": False
    })
report = {"mode": "READ_ONLY_ALPHA_INSPECTION", "entries": results}
(PACK / "alpha_inspection.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps(report, indent=2))

