#!/usr/bin/env node
// Format-only export from preserved sources or approved transparent cutouts.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const sharp = require(require.resolve("sharp", {
  paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")]
}));
const root = path.resolve(__dirname, "..");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "docs/reports/assets/tech8c_laboratory_pm_icons.json"), "utf8"));

(async () => {
  const results = [];
  for (const entry of manifest.entries) {
    const source = path.join(root, entry.source);
    const output = path.join(root, entry.output);
    const sourceBytes = fs.readFileSync(source);
    if (crypto.createHash("sha256").update(sourceBytes).digest("hex") !== entry.sourceSha256)
      throw new Error("Source image changed: " + entry.name);
    let exportBytes = sourceBytes;
    if (entry.cutout) {
      exportBytes = fs.readFileSync(path.join(root, entry.cutout));
      if (crypto.createHash("sha256").update(exportBytes).digest("hex") !== entry.cutoutSha256)
        throw new Error("Transparent cutout changed: " + entry.name);
    }
    if (manifest.transparentBackground && !entry.cutout)
      throw new Error("Missing approved transparent cutout: " + entry.name);
    const metadata = await sharp(exportBytes).metadata();
    const size = manifest.size;
    const base = await sharp(exportBytes).resize(size, size, {
      fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 }, kernel: "lanczos3"
    }).ensureAlpha().raw().toBuffer();
    if (manifest.transparentBackground) {
      let transparent = 0, opaque = 0;
      for (let i = 3; i < base.length; i += 4) {
        if (base[i] === 0) transparent++;
        // Generated cutouts can have an interior alpha of 250-254 instead of 255.
        if (base[i] >= 250) opaque++;
      }
      if (!metadata.hasAlpha || transparent < size * size * 0.2 || opaque < size * size * 0.05)
        throw new Error("Cutout must contain real background transparency and solid icon pixels: " + entry.name);
    }
    const levels = [];
    for (let levelSize = size; levelSize >= 1; levelSize >>= 1) {
      levels.push(await sharp(base, { raw: { width: size, height: size, channels: 4 } })
        .resize(levelSize, levelSize, { kernel: "lanczos3" }).raw().toBuffer());
    }
    // Legacy DDS RGBA8; complete mip chain matching native 208px PM icons.
    const header = Buffer.alloc(128);
    header.write("DDS ", 0, "ascii");
    for (const [offset, value] of [
      [4, 124], [8, 0x2100f], [12, size], [16, size], [20, size * 4], [28, levels.length],
      [76, 32], [80, 0x41], [88, 32], [92, 0xff], [96, 0xff00],
      [100, 0xff0000], [104, 0xff000000], [108, 0x401008]
    ]) header.writeUInt32LE(value, offset);
    const dds = Buffer.concat([header, ...levels]);
    if (size !== 208 || dds.length !== 230828 || levels.length !== manifest.mipLevels)
      throw new Error("Invalid DDS mip payload: " + entry.name);
    fs.mkdirSync(path.dirname(output), { recursive: true });
    fs.writeFileSync(output, dds);
    results.push({ pm: entry.pm, sourceSize: [metadata.width, metadata.height],
      output: entry.output, size: [size, size], mipLevels: levels.length, bytes: dds.length,
      sha256: crypto.createHash("sha256").update(dds).digest("hex") });
  }
  console.log(JSON.stringify(results, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
