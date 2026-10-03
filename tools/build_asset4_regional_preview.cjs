#!/usr/bin/env node
// Format-only preview staging and QA. No game textures or definitions are edited.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const sharp = require(require.resolve("sharp", {
  paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")]
}));
const root = path.resolve(__dirname, "..");
const pack = path.join(root, "docs/reports/assets/asset4_import_2026-10-01");
const plan = JSON.parse(fs.readFileSync(path.join(pack, "regional_generation_plan.json"), "utf8"));
const results = JSON.parse(fs.readFileSync(path.join(pack, "regional_generation_results.json"), "utf8"));
const original = JSON.parse(fs.readFileSync(path.join(pack, "preview_manifest.json"), "utf8"));
const revisionFile = ["bombard_perspective_v3.json", "bombard_perspective_v2.json"]
  .map(name => path.join(pack, name)).find(file => fs.existsSync(file));
const revision = revisionFile ? JSON.parse(fs.readFileSync(revisionFile, "utf8")) : { entries: [] };
const approvalFile = path.join(pack, "unit_art_approval.json");
const approvedUnits = fs.existsSync(approvalFile)
  ? JSON.parse(fs.readFileSync(approvalFile, "utf8")).approved_units : [];
const labels = ["Europe / repli", "Asie orientale", "Asie du Sud", "Afrique", "Monde arabe"];
const types = [
  { key: "musket_infantry", label: "Infanterie à mousquet", unit: "combat_unit_type_musket_infantry", dds: "1776_infantry_musket" },
  { key: "bombard", label: "Bombarde", unit: "combat_unit_type_cannon_artillery", dds: "1776_artillery_bombard" },
  { key: "field_cannon", label: "Canon de campagne", unit: "combat_unit_type_improved_cannon_artillery", dds: "1776_artillery_field_cannon" }
];
const allUnitsApproved = types.every(type => approvedUnits.includes(type.unit));
const xml = text => text.replaceAll("&", "&amp;").replaceAll("<", "&lt;");

(async () => {
  if (plan.entries.length !== 12 || results.length !== 12 || new Set(results.map(x => x.key)).size !== 12)
    throw new Error("Expected twelve distinct generated regional assets");
  if (revisionFile && (revision.entries.length !== 5 || new Set(revision.entries.map(x => x.key)).size !== 5))
    throw new Error("A bombard revision must include the fallback and all four regional variants");
  const entries = [];
  for (const initialTask of plan.entries) {
    const replacement = revision.entries.find(x => x.key === initialTask.key);
    const task = { ...initialTask, ...replacement };
    const result = replacement || results.find(x => x.key === task.key);
    if (!result) throw new Error("No generation result for " + task.key);
    const destination = path.join(root, task.preview);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    if (fs.existsSync(destination) && !fs.readFileSync(destination).equals(fs.readFileSync(result.generatedFile)))
      throw new Error("Would overwrite a different preview: " + destination);
    fs.copyFileSync(result.generatedFile, destination);
    entries.push({ ...task, generatedFile: result.generatedFile, alpha: "OPAQUE",
      status: approvedUnits.includes(task.unit) ? "APPROVED_INTEGRATED" : "PREVIEW_AWAITING_APPROVAL" });
  }
  const cellW = 320, cellH = 372, margin = 170, top = 52;
  const layers = [], checks = [];
  const sheetTitle = allUnitsApproved ? "1776 — Trois unités et leurs variantes régionales intégrées" :
    approvedUnits.length ? "1776 — Mousquetiers et canons validés ; bombarde à valider" : "1776 — Variantes régionales : aperçus avant intégration";
  layers.push({ input: Buffer.from(`<svg width="1770" height="52"><text x="16" y="33" fill="#f3eadb" font-family="Segoe UI" font-size="22">${sheetTitle}</text></svg>`), left: 0, top: 0 });
  for (const [row, type] of types.entries()) {
    const initialFallback = original.entries.find(x => x.key === type.key);
    const fallbackRevision = revision.entries.find(x => x.key === type.key);
    const fallback = initialFallback ? { ...initialFallback, ...fallbackRevision } : null;
    if (!fallback) throw new Error("Missing European fallback: " + type.key);
    if (fallbackRevision) {
      const destination = path.join(root, fallback.preview);
      if (fs.existsSync(destination) && !fs.readFileSync(destination).equals(fs.readFileSync(fallback.generatedFile)))
        throw new Error("Would overwrite a different fallback revision: " + destination);
      fs.copyFileSync(fallback.generatedFile, destination);
    }
    const group = [
      { ...fallback, unit: type.unit, region: "FALLBACK", trigger: "FALLBACK", target_dds: `gfx/unit_illustrations/${type.dds}.dds` },
      ...plan.native_branch_order.filter(x => x !== "FALLBACK").map(region => entries.find(x => x.unit === type.unit && x.region === region))
    ];
    if (group.some(x => !x)) throw new Error("Missing cultural branch: " + type.key);
    const rowTitle = `<svg width="170" height="100"><text x="12" y="25" fill="#f3eadb" font-family="Segoe UI" font-size="16">${xml(type.label.replace("Infanterie à mousquet", "Mousquetiers"))}</text></svg>`;
    layers.push({ input: Buffer.from(rowTitle), left: 0, top: top + row * cellH + 144 });
    for (const [column, entry] of group.entries()) {
      const source = path.join(root, entry.preview), bytes = fs.readFileSync(source);
      const meta = await sharp(bytes).metadata();
      if (meta.width !== meta.height || meta.width < 512) throw new Error("Unexpected dimensions: " + entry.key);
      const { data, info } = await sharp(bytes).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
      let alphaMin = 255;
      for (let i = 3; i < data.length; i += info.channels) alphaMin = Math.min(alphaMin, data[i]);
      if (alphaMin !== 255) throw new Error("Non-opaque unit image: " + entry.key);
      const hash = crypto.createHash("sha256").update(bytes).digest("hex").toUpperCase();
      checks.push({ key: entry.key, unit: type.unit, region: entry.region, preview: entry.preview,
        target_dds: entry.target_dds, width: meta.width, height: meta.height, alphaMin, sha256: hash });
      const x = margin + column * cellW, y = top + row * cellH;
      const text = Buffer.from(`<svg width="320" height="40"><text x="9" y="27" fill="#f3eadb" font-family="Segoe UI" font-size="17">${labels[column]}</text></svg>`);
      layers.push({ input: text, left: x, top: y });
      const thumb = await sharp(bytes).resize(304, 304).png().toBuffer();
      layers.push({ input: thumb, left: x + 8, top: y + 42 });
      const tiny = await sharp(bytes).resize(64, 64).png().toBuffer();
      layers.push({ input: tiny, left: x + 240, top: y + 282 });
    }
  }
  if (new Set(checks.map(x => x.target_dds)).size !== 15) throw new Error("Texture name collision");
  const configFile = path.join(root, "common/combat_unit_types/00_land_combat_unit_types.txt");
  const definitions = fs.readFileSync(configFile, "utf8");
  for (const check of checks) {
    const integrated = definitions.includes(check.target_dds);
    if (integrated !== approvedUnits.includes(check.unit))
      throw new Error("Unit approval/integration mismatch: " + check.target_dds);
  }
  const snapshot = crypto.createHash("sha256").update(fs.readFileSync(configFile)).digest("hex");
  await sharp({ create: { width: margin + 5 * cellW, height: top + 3 * cellH, channels: 3, background: "#22282e" } })
    .composite(layers).png().toFile(path.join(pack, "REGIONAL_UNITS_PREVIEW.png"));
  for (const [row, type] of types.entries()) {
    const rowLayers = layers.filter(x => x.top >= top + row * cellH && x.top < top + (row + 1) * cellH)
      .map(x => ({ ...x, top: x.top - top - row * cellH }));
    await sharp({ create: { width: margin + 5 * cellW, height: cellH, channels: 3, background: "#22282e" } })
      .composite(rowLayers).png().toFile(path.join(pack, `REGIONAL_${type.key.toUpperCase()}_PREVIEW.png`));
  }
  fs.writeFileSync(path.join(pack, "regional_preview_manifest.json"), JSON.stringify({
    mode: "built-in image_gen", status: allUnitsApproved ? "ALL_UNIT_FAMILIES_APPROVED_INTEGRATED" :
      approvedUnits.length ? "PARTIAL_INTEGRATION_BOMBARD_PENDING" : "PREVIEW_ONLY_AWAITING_USER_APPROVAL",
    approved_units: approvedUnits, bombard_revision: revisionFile ? path.basename(revisionFile) : null,
    native_branch_order: plan.native_branch_order, definitions_sha256: snapshot,
    notes: ["European fallback previews are retained, including musket V2.",
      "Americas/Polynesia branches exist only on vanilla irregular infantry, not on line infantry/cannon artillery.",
      "Regional illustrations are broad visual evocations, not named historical regiment reconstructions."],
    entries
  }, null, 2) + "\n");
  fs.writeFileSync(path.join(pack, "regional_preview_validation.json"), JSON.stringify({
    status: approvedUnits.length ? "PASS_DIMENSIONS_OPAQUE_UNIQUE_APPROVAL_MATCH" : "PASS_DIMENSIONS_OPAQUE_UNIQUE_PREVIEW_ONLY", illustrations: checks.length, checks
  }, null, 2) + "\n");
  console.log(JSON.stringify({ status: "PASS", newVariants: entries.length, totalIllustrations: checks.length,
    contactSheet: path.join(pack, "REGIONAL_UNITS_PREVIEW.png") }, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
