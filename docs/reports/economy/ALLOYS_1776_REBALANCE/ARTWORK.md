# Quincaillerie — provenance de l'icône transparente

Mode : service intégré `image_gen`, édition `background-extraction`, option `transparent_background=true`. Aucun service ou modèle CLI supplémentaire.

Image cible : pièce jointe du joueur `codex-clipboard-3b705f6e-5f1e-43c4-8318-c56c88afea77.png`, inspectée avant édition. Le fond et le cadre sont retirés ; les objets centraux sont conservés.

Livrables du dépôt :

- `workshop_assets/source/aor1776_hardware_transparent.png` : maître PNG RGBA 1254 × 1254.
- `gfx/interface/icons/goods_icons/aor1776_hardware.dds` : texture de jeu BGRA8 256 × 256, neuf mipmaps.
- `docs/reports/economy/ALLOYS_1776_REBALANCE/HARDWARE_ICON.png` : aperçu transparent 256 × 256.

Le script `tools/build_hardware_icon.py` effectue seulement l'export de format et la réduction avec filtrage de l'alpha prémultiplié. Il ne détoure ni ne repeint l'image. Les tests contrôlent les coins transparents, l'anse ouverte, l'alpha de 0 à 255 et l'identité des pixels du premier niveau DDS avec l'aperçu attendu. L'aperçu a été inspecté visuellement. L'affichage réel dans Victoria 3 reste à valider.

## Prompt appliqué

Edit target: the supplied historical household hardware game icon. Remove ALL dark teal/black background, floor/table surface, the entire thin gold border/frame and all four frame corner ornaments. Keep exactly the original central household objects together: copper kettle with dark handle, pewter tankard, gold brass candlestick and plate, silver fork and spoon, knife with wood handle, brass hinge and doorknob, screwdriver, nails. Preserve their painted realistic Victoria 3 period game-icon style, composition, rich metallic material colours and highlights, and all silhouettes. No added objects, no text. Truly transparent alpha background behind and BETWEEN objects and inside the open handle; clean anti-aliased cutout edges; retain opaque metal highlights and wooden handles. No checkerboard painted into image, no solid backdrop, no floor, no border or cast shadow on an external surface. Entire group fully visible with a small transparent margin on every side, square output. Save edited transparent PNG for game asset integration.
