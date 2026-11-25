# Ablation des callbacks moddés de priorité de construction

Le retrait des blocs `ai_goal` ne désactive pas durablement l'extension des bâtiments. Le test suivant garde donc **tous les contrôleurs et objectifs natifs**, et ne retire que la couche de script moddé de priorité de certains candidats à la construction.

L'inventaire statique du runtime figé identifie 12 blocs `ai_value` contenant des callbacks `aor1776_ai_…`, dans neuf fichiers. Le diagnostic remplace chacun de ces seuls blocs par sa propre constante de base : outils et chemins de fer 2 000 ; alliages 1 600 ; autres cibles 1 000. Les cibles sont les ateliers d'outillage, aciéries, moteurs, charbon, fer, centrales, camps de bûcherons, carrières de calcaire, chemins de fer, cimenteries, raffineries et alliages.

Tous les autres octets de ces fichiers sont conservés. Les autres définitions de bâtiments, PM, budgets, technologies, pays, populations, marchés, fréquences IA et scripts historiques restent identiques. Les contrôleurs mensuels régionaux et du SERG, ainsi que les routines journalières, restent normaux. Les bonus de priorité sont retirés : **les choix de construction peuvent changer**. Ce diagnostic n'est pas une optimisation équivalente à intégrer.

Le pack mince est externe : `building_priority_bases_20261118` dans le laboratoire. Il surcharge neuf fichiers ; il ne contient pas une copie du mod. `SCORE_BASES_SETUP_20261118.json` donne les 12 blocs, les empreintes avant/après et les profils. Le même S0 de 1776, avec la seule vitesse de chargement réglée à 5, est copié dans les quatre profils ; 646 contrôleurs actifs et les 400 objectifs d'extension sont préservés dans la source.

Ordre prévu : **SCORQ1 → ECNQ1 → ECNQ2 → SCORQ2**. Il fournit deux passages par condition dans l'ordre inversé. Seuls les témoins Q contemporains serviront à interpréter les écarts ; ECN1 et les anciens témoins sont des références de contexte.

La méthode de sauvegarde est celle de [PROTOCOL_AUTOSAVE_FR.md](PROTOCOL_AUTOSAVE_FR.md) : mêmes préférences trimestrielles locales dans tous les Q, aucune sauvegarde permise dans les fenêtres des 2 janvier–27 février, source vérifiée et preuve native d'avril. Le jeu continue après les 56 jours pour produire le témoin et vider les journaux. Ce temps supplémentaire n'entre pas dans les durées. Il n'y a pas de PRE native manuelle à confondre avec la preuve de source.

Trois preuves sont requises avant toute conclusion : empreinte intacte de la source ; sauvegarde native POST avec tous les flags attendus et objectifs des contrôleurs communs conservés ; **empreintes de chargement natives** montrant que les neuf fichiers ciblés diffèrent entre diagnostic et témoin, alors que les autres fichiers virtuels restent identiques. Un simple dossier de patch préparé ne remplit pas ce dernier critère.

Les fenêtres 14/28/56 sont cumulées et ne constituent pas trois répétitions indépendantes. Deux processus par condition ne suffisent pas à établir une distribution de bruit précise. De petites différences, ou des différences dépendantes de l'ordre, ne valident pas une optimisation. Un résultat nul sur cette couche n'exclurait ni les autres callbacks, ni les coûts natifs de rentabilité, de construction, d'investissement ou de sélection de PM.

## Reprise du 19 novembre — changement explicite d'affichage

SCORQ1 a terminé ses fenêtres (52/101/174 s) et son POST natif d'avril ; ECNQ1 s'est fermé sans aucun DAY. L'ancien ordre prévu ne constitue donc pas une paire complète. ECNQ2 n'a servi qu'au réglage d'affichage et n'a pas simulé. SCORQ2, SCORQ3 et ECNQ3 sont préparés mais non exécutés à ce stade.

L'utilisateur demande de laisser le grand 4K OLED libre et d'utiliser exclusivement l'écran secondaire plus petit. Le jeu a réellement sélectionné **(1) GAOMON156 PRO**, en fenêtre **1600×900**. L'observation finale mesure 1604×960 pixels avec les bordures, origine de capture −1762/278 ; la fenêtre est entièrement à gauche de l'écran principal. Aucune résolution du bureau Windows n'a été changée. Les essais utilisent leurs propres préférences, pas celles du profil normal.

Une nouvelle série indépendante est préparée : **ECNG1 → SCORG1 → SCORG2 → ECNG2**. Les six préférences, y compris les deux nouvelles références vanilla, portent la même empreinte initiale `cafe60bc5f8da6c03aeeb976ee4c8c6b9cfacaf45e196121ea8c1636a69df47c`. Les seules différences sémantiques ajoutées au réglage Q commun sont la résolution 1600×900 et l'écran 1 explicitement choisi. Les copies de caches sont terminées avant le début de la simulation. La variante de score reste strictement la même ; aucun second système de gameplay n'est modifié.

Les chiffres de SCORQ1 et des anciens témoins restent dans leur session propre et ne doivent pas être agrégés avec cette série. L'exécution et la validation de chaque nouveau passage doivent être constatées dans ses fichiers RESULTS, dans le CSV final et dans les preuves natives de ressources chargées. L'ordre indiqué ici est un protocole, pas une attestation de réalisation.
