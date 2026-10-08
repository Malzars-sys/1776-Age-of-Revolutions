#!/usr/bin/env node
// Format-only export of the user-supplied illustration. No crop or redesign.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const { nativeBuildingDds } = require("./native_building_dds.cjs");
const sharp = require(require.resolve("sharp", {
  paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")]
}));
const root = path.resolve(__dirname, "..");
const source = path.join(root, "docs/reports/assets/tech8c_research_laboratory_source.png");
const output = path.join(root, "gfx/interface/icons/building_icons/1776_research_laboratory.dds");
const preview = path.join(root, "docs/reports/assets/tech8c_research_laboratory_preview.png");

(async () => {
  const metadata = await sharp(source).metadata();
  const base = await sharp(source).resize(256, 256, {
    fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 }, kernel: "lanczos3"
  }).ensureAlpha().raw().toBuffer();
  const levels = [];
  for (let size = 256; size >= 1; size >>= 1) {
    levels.push(await sharp(base, { raw: { width: 256, height: 256, channels: 4 } })
      .resize(size, size, { kernel: "lanczos3" }).raw().toBuffer());
  }
  // Assemble RGBA, then convert storage to native building BGRA without recoloring.
  const header = Buffer.alloc(128);
  header.write("DDS ", 0, "ascii");
  for (const [offset, value] of [
    [4, 124], [8, 0x2100f], [12, 256], [16, 256], [20, 256 * 4], [28, levels.length],
    [76, 32], [80, 0x41], [88, 32], [92, 0xff], [96, 0xff00],
    [100, 0xff0000], [104, 0xff000000], [108, 0x401008]
  ]) header.writeUInt32LE(value, offset);
  const dds = nativeBuildingDds(Buffer.concat([header, ...levels]));
  if (dds.length !== 349652 || levels.length !== 9) throw new Error("Invalid DDS mip payload");
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, dds);
  await sharp(base, { raw: { width: 256, height: 256, channels: 4 } }).png().toFile(preview);
  console.log(JSON.stringify({
    source, sourceSize: [metadata.width, metadata.height], output, size: [256, 256],
    mipLevels: levels.length, bytes: dds.length, preview,
    sha256: crypto.createHash("sha256").update(dds).digest("hex")
  }, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
