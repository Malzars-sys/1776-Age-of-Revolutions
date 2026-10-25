# Ressources visuelles R4

## Événements

La vidéo native **`ep2_intellectual_writer`**, Great Wave, est référencée dans
les sept événements visibles du fichier `events/1776_american_diplomacy.txt`.
Le fichier existe dans l’installation canonique :

`C:/Games/Victoria 3/game/dlc/dlc018_ep2/gfx/event_pictures/ep2_intellectual_writer.bk2`

Références natives : `events/japan_events/ep2_imperial_events.txt` et
`events/japan_events/ep2_iwakura_events.txt`. La vidéo n’a pas été copiée dans
le mod. Son rendu dans les événements R4 reste à confirmer en jeu.

## Reconnaissance de dette

Source fournie par l’utilisateur :
`C:/Users/simeo/AppData/Local/Temp/codex-clipboard-59074e20-c9a6-46fc-a637-8b334e6b0818.png`.

**Mode : outil intégré `image_gen`, édition avec transparence**, selon la
compétence imagegen. Le traitement demande le retrait du fond blanc et la
conservation de l’illustration. L’export DDS est une conversion de format
avec réduction à 256 × 256 et neuf niveaux de mipmap ; il ne redessine pas
l’illustration. Le maître conserve un canal alpha réel.

Fichiers finaux dans le dépôt :

- [Maître PNG transparent](../../../../workshop_assets/source/aor1776_deferred_debt_transparent.png), 1 254 × 1 254 RGBA.
- [Icône DDS](../../../../gfx/interface/icons/diplomatic_treaties_articles_icons/aor1776_deferred_debt.dds), 256 × 256 BGRA8, neuf mipmaps, 349 652 octets.

Sortie initiale de l’outil :
`C:/Users/simeo/.codex/generated_images/01a149d5-1620-7bf2-bf90-7fa9bf443072/exec-1975650c-db1d-47b8-b54b-e8602897f463.png`.

### Consigne finale exacte

```text
Use case: background-extraction. Asset type: Victoria 3 treaty article icon. Input image 1 is the edit target supplied by the user. Remove only the white surrounding background to actual transparency. Preserve the supplied icon exactly: its parchment IOU, red wax seal with pound symbol, teal curved repayment arrow with gold outline, gold coin stacks, composition, colors, drawing and painterly texture. Do not redesign, change lettering, add objects or a frame, or alter the arrangement. Preserve the natural silhouette and clean soft edge shading. Center the complete unchanged icon within a square transparent canvas with a small safe margin.
```
