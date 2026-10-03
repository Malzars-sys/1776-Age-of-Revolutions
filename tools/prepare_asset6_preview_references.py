"""Prepare petroleum artwork references and immutable gameplay snapshot; no integration."""
import hashlib
import json

from asset4_style_reference_audit import GAME, ROOT, catalog, decode, field

PACK = ROOT / "docs/reports/assets/asset6_preview_2026-10-02"
SUBJECTS = {
    "GOOD": ("common/goods", ["oil", "engines", "steel"]),
    "BUILDING": ("common/buildings", ["building_chemical_plant", "building_steel_mill"]),
    "PM": ("common/production_methods", ["pm_patent_stills", "pm_open_hearth_process"]),
}
ENTRIES = [
    ("refined_fuels", "GOOD", "refined_fuels", "Carburants raffinés", "Bidon métallique ancien à bec court et bouteille de distillat jaune pâle. Silhouette compacte, sans jerrican moderne ni flamme décorative."),
    ("lubricants", "GOOD", "lubricants", "Lubrifiants", "Burette industrielle à long bec, huile ambrée et petit engrenage. Forme différente des carburants, ni tonneau ni bouteille de boisson."),
    ("heavy_petroleum_products", "GOOD", "heavy_petroleum_products", "Produits pétroliers lourds", "Petit tonneau ouvert rempli de résidu noir visqueux et masse compacte de bitume à son pied. Ni charbon granuleux ni pétrole clair."),
    ("oil_refinery", "BUILDING", "building_oil_refinery", "Raffinerie de pétrole", "Petit site industriel maçonné en trois quarts : cornues/réservoirs rivetés et appareils de distillation, conduites sobres. Produit carburant au premier plan. Cadre patiné arrondi, intérieur opaque, coins extérieurs transparents."),
    ("fractional_distillation_refinery", "PM", "pm_fractional_distillation_refinery", "Distillation fractionnée", "Glyphe de colonne de distillation à trois sorties en étages et petite goutte. Bas-relief ocre mat, deux symboles maximum."),
    ("thermal_catalytic_cracking_refinery", "PM", "pm_thermal_catalytic_cracking_refinery", "Craquage thermique et catalytique", "Glyphe de réacteur industriel court sur foyer et goutte scindée. Bas-relief ocre mat, forme différente de la colonne de distillation."),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if PACK.exists():
        raise FileExistsError("Preview batch already exists; do not overwrite: " + str(PACK))
    refs = PACK / "references"
    refs.mkdir(parents=True)
    (PACK / "previews").mkdir()
    native_refs = []
    for family, (folder, keys) in SUBJECTS.items():
        native = catalog(folder, native_only=True)
        for key in keys:
            tokens, _ = native[key]
            relative = field(tokens, "icon" if family == "BUILDING" else "texture")
            source = GAME / relative
            target = refs / f"vanilla_{key}.png"
            rgba = decode(source)
            rgba.save(target)
            native_refs.append({"family": family, "id": key, "native_texture": relative,
                                "native_sha256": digest(source), "preview": str(target.relative_to(PACK)).replace("\\", "/"),
                                "role": "STYLE_ONLY_NOT_AN_ORIGINAL_ASSET", "size": list(rgba.size)})
    definitions = {family: catalog(folder) for family, (folder, _) in SUBJECTS.items()}
    technologies = catalog("common/technology/technologies")
    entries = []
    for key, family, ident, label, brief in ENTRIES:
        tokens, definition = definitions[family][ident]
        techs = field(tokens, "unlocking_technologies", [])
        size = 208 if family == "PM" else 256
        folder = {"GOOD": "goods_icons", "BUILDING": "building_icons", "PM": "production_method_icons"}[family]
        target_dds = f"gfx/interface/icons/{folder}/1776_{key}.dds"
        assert not (ROOT / target_dds).exists(), target_dds
        entries.append({"key": key, "id": ident, "family": family, "label_fr": label,
                        "definition": str(definition.relative_to(ROOT)).replace("\\", "/"),
                        "current_texture": field(tokens, "icon" if family == "BUILDING" else "texture"),
                        "unlocking_technologies": techs,
                        "eras": {t: field(technologies[t][0], "era") for t in techs},
                        "visual_brief": brief, "preview": f"previews/{key}.png", "target_dds": target_dds,
                        "target_size": size, "mips": 8 if family == "PM" else 9,
                        "status": "PREPARED_NOT_GENERATED"})
    manifest = {"date": "2026-10-02", "mode": "BUILTIN_IMAGE_GEN", "status": "PREPARATION_ONLY",
                "approval_required_before_integration": True, "entries": entries,
                "preserved_native_technology": "fractional_distillation",
                "excluded": ["copper chain", "laboratory/data assets", "gameplay balance"]}
    (PACK / "preview_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PACK / "native_references.json").write_text(json.dumps(native_refs, indent=2) + "\n", encoding="utf-8")
    baseline = {str(p.relative_to(ROOT)).replace("\\", "/"): digest(p)
                for folder in ("common", "gfx") for p in (ROOT / folder).rglob("*") if p.is_file()}
    (PACK / "gameplay_and_gfx_baseline.json").write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_refs": len(native_refs), "previews": len(entries), "protected_files": len(baseline), "pack": str(PACK)}))


if __name__ == "__main__":
    main()
