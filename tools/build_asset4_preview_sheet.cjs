#!/usr/bin/env node
// Preview-only contact sheet and alpha QA. Does not touch any game asset or definition.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const sharp = require(require.resolve("sharp", {
  paths: [__dirname, path.resolve(path.dirname(process.execPath), "..")]
}));
const root = path.resolve(__dirname, "..");
const reportDir = path.join(root, "docs/reports/assets/asset4_import_2026-10-01");
const manifest = JSON.parse(fs.readFileSync(path.join(reportDir, "preview_manifest.json"), "utf8"));
const escape = text => text.replaceAll("&", "&amp;").replaceAll("<", "&lt;");

(async () => {
  const layers = [], results = [];
  const cellW = 330, cellH = 398;
  for (const [i, entry] of manifest.entries.entries()) {
    const bytes = fs.readFileSync(path.join(root, entry.preview));
    const metadata = await sharp(bytes).metadata();
    const { data } = await sharp(bytes).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    let alphaZero = 0, alphaMax = 0, minAlpha = 255;
    for (let n = 3; n < data.length; n += 4) {
      if (data[n] === 0) alphaZero++;
      alphaMax = Math.max(alphaMax, data[n]);
      minAlpha = Math.min(minAlpha, data[n]);
    }
    if (entry.alpha === "TRANSPARENT" && (!metadata.hasAlpha || !alphaZero || alphaMax < 240))
      throw new Error("Preview lacks real transparency: " + entry.key);
    if (entry.alpha === "OPAQUE" && minAlpha !== 255)
      throw new Error("Unit illustration not opaque: " + entry.key);
    results.push({ key: entry.key, dimensions: [metadata.width, metadata.height], alpha: entry.alpha, alphaZero, minAlpha, alphaMax });
    const x = (i % 4) * cellW, y = Math.floor(i / 4) * cellH;
    const title = Buffer.from('<svg width="330" height="46"><text x="12" y="30" fill="#f4eee1" font-family="Segoe UI" font-size="15">' + escape(entry.label) + '</text></svg>');
    layers.push({ input: title, left: x, top: y });
    const thumb = await sharp(bytes).resize(304, 304, { fit: "contain", background: "#00000000" })
      .flatten({ background: "#363b42" }).png().toBuffer();
    layers.push({ input: thumb, left: x + 13, top: y + 48 });
    const small = await sharp(bytes).resize(32, 32, { fit: "contain", background: "#00000000" })
      .flatten({ background: "#363b42" }).png().toBuffer();
    layers.push({ input: small, left: x + 13, top: y + 359 });
  }
  await sharp({ create: { width: cellW * 4, height: cellH * 2, channels: 3, background: "#22282e" } })
    .composite(layers).png().toFile(path.join(reportDir, "REMAINING_ASSETS_PREVIEW.png"));
  fs.writeFileSync(path.join(reportDir, "preview_validation.json"), JSON.stringify({ status: "PASS_ALPHA_AND_PREVIEW", results }, null, 2) + "\n");
  console.log(JSON.stringify(results, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
