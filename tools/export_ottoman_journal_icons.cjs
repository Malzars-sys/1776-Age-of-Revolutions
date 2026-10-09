#!/usr/bin/env node
"use strict";
// The supplied artwork already has transparent alpha: no generation or removal
// of dark foreground details. Retain PNG masters and only resize/convert here.
const fs = require("node:fs"), path = require("node:path");
const { nativeIconDds } = require("./native_icon_dds.cjs");
const sharp = require(require.resolve("sharp", {
  paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")]
}));
const root = path.resolve(__dirname, "..");
const folder = path.join(root, "gfx/interface/icons/event_icons");
const keys = ["1776_porte_burden", "1776_many_masters"];
const size = 150; // Matches vanilla event_scales.dds used by these entries.

async function exportIcons() {
  for (const key of keys) {
    const source = path.join(folder, key + "_source.png");
    const metadata = await sharp(source).metadata();
    if (!metadata.hasAlpha || metadata.width !== metadata.height) {
      throw Error("Expected square transparent master: " + key);
    }
    const base = await sharp(source).resize(size, size, { kernel: "lanczos3" })
      .ensureAlpha().raw().toBuffer();
    if (base[3] !== 0 || !base.some((v, i) => i % 4 === 3 && v > 240)) {
      throw Error("Missing transparent background or visible foreground: " + key);
    }
    const levels = [];
    for (let side = size; side >= 1; side = Math.floor(side / 2)) {
      levels.push(await sharp(base, { raw: { width: size, height: size, channels: 4 } })
        .resize(side, side, { kernel: "lanczos3" }).raw().toBuffer());
    }
    const header = Buffer.alloc(128);
    header.write("DDS ", 0, "ascii");
    for (const [offset, value] of [
      [4, 124], [8, 0x2100f], [12, size], [16, size], [20, size * 4],
      [28, levels.length], [76, 32], [80, 0x41], [88, 32],
      [92, 0xff], [96, 0xff00], [100, 0xff0000], [104, 0xff000000],
      [108, 0x401008]
    ]) header.writeUInt32LE(value, offset);
    const dds = nativeIconDds(Buffer.concat([header, ...levels]));
    if (dds.length !== 119808) throw Error("Invalid native texture size: " + key);
    fs.writeFileSync(path.join(folder, key + ".dds"), dds);
    console.log(`${key}: ${size}x${size}, ${levels.length} mipmaps, BGRA8, alpha preserved`);
  }
}
exportIcons().catch(error => { console.error(error); process.exitCode = 1; });
