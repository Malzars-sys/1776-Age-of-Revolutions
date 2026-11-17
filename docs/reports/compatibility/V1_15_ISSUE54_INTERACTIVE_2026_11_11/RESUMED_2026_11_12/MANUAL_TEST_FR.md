# Issue 54 — test de l'arbre restant à réaliser

Le contrôle automatique du jeu est partiel. **Aucune mesure A/B n'est acquise.** Ne pas relancer les anciens benchmarks CPU de démarrage. Les options Steam normales ont été remises à vide.

## Préparer une seule sauvegarde

1. Dans Steam → Victoria 3 → Propriétés → Général, utiliser temporairement ces options pour A1, puis lancer depuis Steam et le lanceur Paradox. Le test précédent a confirmé la prise en compte du dossier isolé par cette route. Ne pas changer de playset normal.

   ```text
   --userdir=C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/runtime_ui_controlled/A1/user_data -debug_mode
   ```

2. Vérifier **1.15.1**, le même ensemble de DLC pour toute la série, et une fenêtre entièrement visible. Choisir une résolution adaptée à l'écran et conserver exactement les mêmes réglages pour les quatre essais. Démarrer la **France au 1er janvier 1776**, rester en pause et enregistrer sous **TECHPERF54**. Les anciennes copies d'autosauvegarde de Russie 1870 ont été écartées et ne doivent pas être utilisées.
3. Dans la console du jeu (touche habituelle de ton clavier), exécuter `3dstats`, puis fermer la console. Vérifier que les compteurs sont réellement affichés. L'avertissement FPS du mode debug constitue aussi une lecture instantanée ; il ne donne pas à lui seul une série de temps de trame.
4. Terminer A1, quitter le jeu, puis copier **le fichier `.v3` effectivement créé** et `pdx_settings.json` d'A1 vers les trois profils isolés. Par exemple dans une fenêtre PowerShell ordinaire, après avoir vérifié le nom exact de la sauvegarde :

   ```powershell
   $tech54 = 'C:\Users\simeo\AppData\Local\Temp\aor1776_techperf54_20261111\runtime_ui_controlled'
   $tech54Save = Join-Path $tech54 'A1\user_data\save games\TECHPERF54.v3'
   if (-not (Test-Path -LiteralPath $tech54Save)) { throw 'Vérifier le nom exact de TECHPERF54 dans le dossier A1.' }
   foreach ($tech54Trial in 'B1','B2','A2') {
       $tech54Target = Join-Path $tech54 "$tech54Trial\user_data\save games\TECHPERF54.v3"
       if (Test-Path -LiteralPath $tech54Target) { throw "Une sauvegarde existe déjà pour $tech54Trial : la conserver." }
       Copy-Item -LiteralPath $tech54Save -Destination $tech54Target
       Copy-Item -LiteralPath (Join-Path $tech54 'A1\user_data\pdx_settings.json') -Destination (Join-Path $tech54 "$tech54Trial\user_data\pdx_settings.json")
   }
   ```

## Gestes à répéter dans A1, B1, B2, A2

Pour les essais suivants, remplacer seulement `A1` par le nom du profil dans les options Steam et charger **TECHPERF54**. Garder le pays, la date, la pause, les réglages, le masque DLC et les vues identiques. Attendre 30 secondes après chargement.

1. Arbre fermé : relever 15 secondes de FPS et CPU sur la carte en pause.
2. Ouvrir l'arbre **Technologie**. Ouvrir une fois Production, Militaire et Société pour les préparer. Pour chaque onglet, relever 15 secondes immobile, puis le même déplacement vers le bas et vers le haut avec le **bouton gauche maintenu**. Garder le zoom fixe : la molette change le zoom.
3. Fermer et rouvrir l'arbre trois fois. Une vidéo du clic et de la première image complète permet de mesurer le délai ; la durée d'un appel d'automatisation ou le CPU ne le remplacent pas.
4. Quitter et passer au profil suivant dans l'ordre **A1–B1–B2–A2**, soit deux essais par version. Consigner aussi tout incident, popup ou changement de premier plan.

## Collecteur CPU déjà prêt

Depuis ta session Windows ordinaire, lancer **une commande à la fois** lorsque l'état correspondant est déjà prêt. Le collecteur attend cinq secondes, puis observe 15 secondes ; revenir au jeu pendant ce délai. Il ne démarre pas le jeu et ne mesure pas son lancement.

```powershell
& "$tech54\Measure_UI_CPU.ps1" -Trial A1 -Phase closed_paused -Category none
& "$tech54\Measure_UI_CPU.ps1" -Trial A1 -Phase tree_stationary -Category production
& "$tech54\Measure_UI_CPU.ps1" -Trial A1 -Phase tree_scroll -Category production
```

Remplacer `production` par `military` et `society`, puis `A1` par `B1`, `B2`, `A2`. Le nom historique `tree_scroll` désigne ici le déplacement par glisser, pas la molette. Le script vérifie le chemin de l'exécutable. S'il ne peut pas lire le processus dans cette session, conserver l'erreur et marquer le CPU non mesuré ; aucune élévation n'est nécessaire au protocole.

Les CSV sont écrits dans `<profil>/measurements`. Noter les FPS visibles, la disponibilité réelle de temps de trame et les délais séparément. Ne pas convertir quelques FPS instantanés en moyenne certifiée ou en centiles de temps de trame. Une prise sans accès effectif à l'arbre est invalide.

À la fin, **remettre les options Steam à vide**. La copie C reste un diagnostic distinct, à tester ensuite avec le même protocole, sans modifier les technologies.
