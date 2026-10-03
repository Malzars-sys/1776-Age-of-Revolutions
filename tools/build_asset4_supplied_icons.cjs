#!/usr/bin/env node
// Format-only preparation: split supplied sheets and export PNG masters + RGBA8 DDS.
// No recoloring, alpha guessing, background removal, or generated-art integration.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const sharp = require(require.resolve("sharp", {
  paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")]
}));
const root = path.resolve(__dirname, "..");
const reportDir = path.join(root, "docs/reports/assets/asset4_import_2026-10-01");
const manifest = JSON.parse(fs.readFileSync(path.join(reportDir, "manifest.json"), "utf8"));
const digest = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const escape = text => text.replaceAll("&", "&amp;").replaceAll("<", "&lt;");

async function exportDds(master, size, output) {
  const base = await sharp(master).resize(size, size, {
    fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 }, kernel: "lanczos3"
  }).ensureAlpha().raw().toBuffer();
  let transparent = 0, solid = 0;
  for (let i = 3; i < base.length; i += 4) {
    if (base[i] === 0) transparent++;
    if (base[i] >= 240) solid++;
  }
  if (!transparent || solid < size * size * 0.05)
    throw new Error("Missing true alpha or solid subject: " + output);
  const levels = [];
  for (let n = size; n >= 1; n >>= 1) {
    levels.push(await sharp(base, { raw: { width: size, height: size, channels: 4 } })
      .resize(n, n, { kernel: "lanczos3" }).raw().toBuffer());
  }
  const header = Buffer.alloc(128);
  header.write("DDS ", 0, "ascii");
  for (const [offset, value] of [
    [4, 124], [8, 0x2100f], [12, size], [16, size], [20, size * 4], [28, levels.length],
    [76, 32], [80, 0x41], [88, 32], [92, 0xff], [96, 0xff00],
    [100, 0xff0000], [104, 0xff000000], [108, 0x401008]
  ]) header.writeUInt32LE(value, offset);
  const dds = Buffer.concat([header, ...levels]);
  const expectedMips = size === 208 ? 8 : 9;
  const expectedBytes = size === 208 ? 230828 : 349652;
  if (levels.length !== expectedMips || dds.length !== expectedBytes)
    throw new Error("Invalid mip payload: " + output);
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, dds);
  return { dimensions: [size, size], mipLevels: levels.length, bytes: dds.length,
    alphaZeroPixels: transparent, solidPixels: solid, sha256: digest(dds) };
}

(async () => {
  const results = [], tiles = [];
  const cellW = 280, cellH = 294;
  for (const [index, entry] of manifest.entries.entries()) {
    const bytes = fs.readFileSync(path.join(root, entry.source));
    let pipeline = sharp(bytes);
    if (entry.crop) pipeline = pipeline.extract(entry.crop);
    const master = await pipeline.ensureAlpha().png().toBuffer();
    fs.mkdirSync(path.dirname(path.join(root, entry.master)), { recursive: true });
    fs.writeFileSync(path.join(root, entry.master), master);
    const metadata = await sharp(master).metadata();
    results.push({ id: entry.id, output: entry.dds, master: entry.master,
      source: entry.source, sourceSha256: digest(bytes), masterSha256: digest(master),
      sourceDimensions: [metadata.width, metadata.height],
      ...(await exportDds(master, entry.size, path.join(root, entry.dds))) });
    const x = (index % 4) * cellW, y = Math.floor(index / 4) * cellH;
    const title = Buffer.from('<svg width="280" height="38"><text x="12" y="25" fill="#f4eee1" font-family="Segoe UI" font-size="16">' + escape(entry.label) + '</text></svg>');
    tiles.push({ input: title, left: x, top: y });
    for (const [bg, left] of [["#30363c", 8], ["#b6ada0", 144]]) {
      const thumb = await sharp(master).resize(128, 128, { fit: "contain", background: "#00000000" })
        .flatten({ background: bg }).png().toBuffer();
      tiles.push({ input: thumb, left: x + left, top: y + 44 });
      for (const [n, dx] of [[32, 14], [64, 58]]) {
        const mini = await sharp(master).resize(n, n, { fit: "contain", background: "#00000000" })
          .flatten({ background: bg }).png().toBuffer();
        tiles.push({ input: mini, left: x + left + dx, top: y + 195 });
      }
    }
  }
  await sharp({ create: { width: 4 * cellW, height: 2 * cellH, channels: 3, background: "#22282e" } })
    .composite(tiles).png().toFile(path.join(reportDir, "SUPPLIED_ASSETS_QA.png"));
  fs.writeFileSync(path.join(reportDir, "export_validation.json"), JSON.stringify({
    status: "PASS_EXPORT", results,
    limitations: "File-format and visual previews only; game not launched by this exporter."
  }, null, 2) + "\n");
  console.log(JSON.stringify(results, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
