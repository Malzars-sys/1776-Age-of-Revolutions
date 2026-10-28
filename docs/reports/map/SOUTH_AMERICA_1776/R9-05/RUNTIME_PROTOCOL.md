# R9-05 — Contrôles joueur différés

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Version : `CURRENT_RUNTIME_MANIFEST.json`. Le joueur a annoncé qu'il effectuerait les contrôles plus tard ; ce report ne constitue pas une validation de R9-04 ou de R9-05.

1. Commencer une **nouvelle partie au 1er janvier 1776**. Ne pas utiliser une sauvegarde antérieure pour certifier la nouvelle histoire territoriale.
2. Comparer la carte avec `R9_05_AVANT_APRES.png` : postes portugais sur l'Amazone/Solimões, Negro et Branco ; Vila Bela–Cuiabá–Goiás ; Tabatinga portugais ; Maynas partagé entre portions SC2 et autonomes ; secteur du Tapajós autonome. Vérifier l'absence de trous ou de frontières sans propriétaire.
3. Vérifier les noms « Peuples amazoniens » / « Amazonian peoples », sans clé brute. Le TAG AP7 reste un agrégat technique : la localisation n'atteste pas un gouvernement autochtone unique.
4. Inspecter les portions de Pastaza : SC2 a initialement 14 669 habitants dans les données, AP7 50 450 et BRZ **74** ; aucune portion SC3 résiduelle. Relever les dates de lecture, car les effectifs peuvent changer après démarrage. Vérifier culture, religion et statut des cohortes déplacées ; aucun nouveau stock mondial n'est prévu.
5. Côté Portugal/BRZ, vérifier l'accès réel au marché et le ravitaillement de Barcelos, São Gabriel, Tabatinga et Vila Bela/Cuiabá. Les portions sont incorporées et physiquement raccordées ; cela ne certifie pas le calcul du marché par le moteur. Aucun port fluvial ou bâtiment nouveau n'a été inventé. Tester aussi le déplacement militaire, en distinguant topologie et droits d'accès.
6. Côté SC2, vérifier l'accès des missions de Maynas via les territoires espagnols voisins conservés et le maintien de Moyobamba/Cajamarca sous SC3. Vérifier les éventuels besoins d'infrastructure ou restrictions d'accès entre sujets de l'Espagne.
7. Laisser tourner quelques mois en notant les dates réellement simulées : alimentation, prix, emploi, famine, changements de population et comportements coloniaux. Une anomalie économique n'est pas automatiquement une perte de POPs dans les fichiers initiaux ; conserver captures et données de marché pour diagnostic.
8. Contrôler les témoins des passes précédentes : Huilliches/Mapuche R9-04, Chiloé et son port ; Sacramento dans l'Uruguay partagé ; noyaux CENTRAL. Sauvegarder/recharger et vérifier propriétaires, noms, populations et absence de crash.

Conserver les logs datés. Séparer dette préexistante et régression nouvelle. Le reçu humain doit indiquer version, date, durée effectivement jouée et observations ; aucun PASS_RUNTIME_USER_VALIDATED n'est prérempli.
