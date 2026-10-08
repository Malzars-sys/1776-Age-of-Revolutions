#!/usr/bin/env node
// Format-only export of explicitly user-approved unit families. No generated edits.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const { nativeIconDds } = require("./native_icon_dds.cjs");
const sharp = require(require.resolve("sharp", {
  paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")]
}));
const root = path.resolve(__dirname, "..");
const pack = path.join(root, "docs/reports/assets/asset4_import_2026-10-01");
const approval = JSON.parse(fs.readFileSync(path.join(pack, "unit_art_approval.json"), "utf8"));
const checks = JSON.parse(fs.readFileSync(path.join(pack, approval.approved_source_checks), "utf8")).checks;
const digest = bytes => crypto.createHash("sha256").update(bytes).digest("hex").toUpperCase();

(async () => {
  const entries = checks.filter(x => approval.approved_units.includes(x.unit));
  const allowedUnits = ["combat_unit_type_musket_infantry", "combat_unit_type_improved_cannon_artillery", "combat_unit_type_cannon_artillery"];
  if (!approval.approved_units.length || new Set(approval.approved_units).size !== approval.approved_units.length ||
      approval.approved_units.some(unit => !allowedUnits.includes(unit)) || entries.length !== 5 * approval.approved_units.length ||
      new Set(entries.map(x => x.target_dds)).size !== entries.length)
    throw new Error("Only complete, distinct, explicitly approved unit families may be exported");
  const regions = ["FALLBACK", "east_asian", "south_asian", "african", "arabic"];
  for (const unit of approval.approved_units) {
    const group = entries.filter(x => x.unit === unit);
    if (group.length !== 5 || regions.some(region => group.filter(x => x.region === region).length !== 1))
      throw new Error("Incomplete cultural family: " + unit);
  }
  if (approval.approved_units.includes("combat_unit_type_cannon_artillery")) {
    const approvedRevision = approval.approved_revisions?.combat_unit_type_cannon_artillery;
    if (approvedRevision?.revision !== 3) throw new Error("Bombard V3 requires explicit revision approval");
    const revision = JSON.parse(fs.readFileSync(path.join(pack, approvedRevision.manifest), "utf8"));
    const pinnedChecks = JSON.parse(fs.readFileSync(path.join(pack, approvedRevision.checks), "utf8")).images;
    const group = entries.filter(x => x.unit === "combat_unit_type_cannon_artillery");
    if (revision.revision !== 3 || revision.entries.length !== 5 || pinnedChecks.length !== 5)
      throw new Error("Invalid approved bombard revision");
    for (const entry of group) {
      const source = revision.entries.find(x => x.key === entry.key);
      const pinned = pinnedChecks.find(x => x.key === entry.key);
      if (!source || source.revision !== 3 || source.preview !== entry.preview || source.target_dds !== entry.target_dds ||
          !pinned || pinned.preview !== entry.preview || pinned.sha256 !== entry.sha256)
        throw new Error("Bombard source is not the approved V3: " + entry.key);
    }
  }
  const results = [];
  for (const entry of entries) {
    const source = fs.readFileSync(path.join(root, entry.preview));
    if (digest(source) !== entry.sha256) throw new Error("Approved preview changed: " + entry.key);
    const size = 512;
    const base = await sharp(source).resize(size, size, { kernel: "lanczos3" }).ensureAlpha().raw().toBuffer();
    for (let i = 3; i < base.length; i += 4) if (base[i] !== 255)
      throw new Error("Military illustration is not opaque: " + entry.key);
    const levels = [];
    for (let n = size; n >= 1; n >>= 1) levels.push(await sharp(base, {
      raw: { width: size, height: size, channels: 4 }
    }).resize(n, n, { kernel: "lanczos3" }).raw().toBuffer());
    const header = Buffer.alloc(128);
    header.write("DDS ", 0, "ascii");
    for (const [offset, value] of [
      [4, 124], [8, 0x2100f], [12, size], [16, size], [20, size * 4], [28, levels.length],
      [76, 32], [80, 0x41], [88, 32], [92, 0xff], [96, 0xff00],
      [100, 0xff0000], [104, 0xff000000], [108, 0x401008]
    ]) header.writeUInt32LE(value, offset);
    const dds = nativeIconDds(Buffer.concat([header, ...levels]));
    if (levels.length !== 10 || dds.length !== 1398228) throw new Error("Invalid DDS payload");
    const destination = path.join(root, entry.target_dds);
    if (fs.existsSync(destination)) {
      if (!fs.readFileSync(destination).equals(dds))
        throw new Error("Refusing to overwrite different art: " + destination);
    } else {
      fs.mkdirSync(path.dirname(destination), { recursive: true });
      fs.writeFileSync(destination, dds);
    }
    results.push({ ...entry, export_size: size, mipLevels: levels.length, bytes: dds.length,
      export_sha256: digest(dds), format: "DDS BGRA8 native asset layout, opaque" });
  }
  fs.writeFileSync(path.join(pack, "approved_unit_export_validation.json"), JSON.stringify({
    status: "PASS_DDS_EXPORT", approval: "unit_art_approval.json", results,
    limitation: "File checks only; not tested in a running game."
  }, null, 2) + "\n");
  console.log(JSON.stringify({ status: "PASS_DDS_EXPORT", exported: results.length, mipLevels: 10 }));
})().catch(error => { console.error(error); process.exitCode = 1; });
