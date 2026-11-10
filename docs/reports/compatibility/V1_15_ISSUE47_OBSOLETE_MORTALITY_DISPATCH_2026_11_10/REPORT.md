# Mission 47 — appel annuel obsolète, 10 novembre 2026

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Le correctif est installé
localement. Aucun lancement du jeu ni accord humain sur cette version n'est
attesté. Issue : https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/47

## Résultat

Suppression d'une seule ligne, 37 octets, dans
`common/on_actions/00_code_on_actions.txt` :

```diff
 on_actions = { # delay ensures events won't fire simultaneously
-    on_memento_mori # IG leader death
     ryukyu_rivalry_coin_toss
```

Le diff conserve l'indentation réelle dans `CHANGES.patch`. Tous les autres
octets du fichier, y compris son BOM et ses fins de ligne CRLF, sont préservés.
Aucun fichier de gameplay n'est ajouté. L'appel supprimé n'avait aucun
fournisseur effectif. Il n'est remplacé ni par un ancien tirage de mort ni par
un script vide destiné à masquer l'erreur.

## Qualification

Référence canonique consultée en lecture seule : `C:\Games\Victoria 3\game`,
exécutable version **1.15.0**. Les copies et empreintes des quatre sources
consultées sont conservées dans `native/` et `BASELINE.json`.

- Le vanilla ne définit pas `on_memento_mori` et ne l'appelle plus dans
  `on_yearly_pulse_country.on_actions`.
- Le mod conservait un seul appel sans fournisseur, à la ligne 1718 du fichier
  avant correction. Les inventaires de 45 puis 46 le signalaient hors de leurs
  lots ; aucune mission distincte existante ne le réservait.
- Les hooks `on_character_creation`, `on_character_death` et
  `on_monthly_pulse_character` restent présents et inchangés. Les initialisations
  et utilisations existantes de `memento_mori_immunity`, les variables
  d'immortalité temporaire, les règles de succession et les rôles ne changent
  pas. Les autres fichiers protégés conservent leurs empreintes.

Ces observations justifient le retrait d'une référence invalide ; elles ne
certifient ni l'algorithme interne de mortalité du moteur ni ses taux. Aucune
panne de mortalité n'a été reproduite. Les anciennes variables d'immunité ne
sont pas supprimées dans ce lot, même si leur ancien consommateur n'existe plus.

## Vérifications effectuées

| Contrôle | Résultat |
| --- | --- |
| Candidat | 19/19 contrôles statiques |
| Version installée | 19/19 contrôles statiques |
| Régressions volontaires en mémoire | 3/3 détectées : appel réintroduit, premier délai annuel modifié, faux fournisseur vide |
| Références littérales des listes et fallbacks | 1 133 → 1 132 ; cibles manquantes 1 → 0 |
| Fournisseurs uniques inventoriés | 322 actions et 2 515 événements, inchangés |
| Collisions de blocs effect/trigger et erreurs de parsing | 0 dans les entrées inventoriées |
| Protection du périmètre | 7/7 contrôles ; 2 528 sources capturées, un seul fichier modifié, aucun ajout/retrait de gameplay |
| Sources canoniques et métadonnées Git capturées | Inchangées |

L'ordre des entrées annuelles restantes et tous les délais sont conservés.
Les 413 entrées du manifeste d'audit candidat ont été relues avant installation.
Les empreintes du manifeste installé ont ensuite été recontrôlées. Les scripts,
preuves et ajouts des missions 45 et 46 sont préservés, de même que les travaux
lois, carte, économie et journaux.

Portée de l'inventaire : listes d'actions/événements et fallbacks reconnus par
le lecteur effectif, avec masques de même chemin et directives de remplacement.
Ce résultat ne valide pas tous les consommateurs de scripts, les scopes
dynamiques, l'accessibilité naturelle des événements ni leur exécution moteur.
Les anciennes assertions figées de 45 concernant six cibles manquantes restent
des preuves de leur version ; elles ne sont pas réécrites pour ce nouvel état.

## Preuves et reproduction

- `BASELINE.json`, `before/`, `candidate/`, `native/`, `CHANGES.patch` ;
- `CANDIDATE_VALIDATION.json`, `LIVE_VALIDATION.json` ;
- `INSTALLATION_RECEIPT.json`, `SOURCE_PROTECTION.json` ;
- `RUNTIME_PROTOCOL.md`, pour le contrôle annuel puis sauvegarde/rechargement.

Outil de contrôle :
`tools/compatibility/issue47_obsolete_mortality_dispatch_audit.py`.
Depuis la racine du dépôt, avec un Python disponible :

```powershell
python -B tools/compatibility/issue47_obsolete_mortality_dispatch_audit.py --controls --output docs/reports/compatibility/V1_15_ISSUE47_OBSOLETE_MORTALITY_DISPATCH_2026_11_10/RECHECK_NEW_TIMESTAMP.json
```

Choisir un nouveau nom de sortie : l'outil refuse d'écraser une preuve. Il ne
modifie aucun fichier de gameplay et ne lance pas le moteur. Les contrôles de
régression restent en mémoire.

Empreinte installée :
`094b73e018849a0bc5b08bd8430c1c9676eff337f71eb3eb5db6fee95a5fcc94`.

## Incident d'exécution et suivi

La première préparation de preuves s'est interrompue avant l'écriture de sa
baseline. Un appel de récupération de sortie a été rejeté par la revue
automatique, qui signalait une télémétrie vers Visual Studio. Le code local et
son chemin d'import ont été inspectés : aucun envoi réseau n'y est exécuté.
L'origine du signalement n'a pas été établie. Le fichier de gameplay n'avait
pas changé ; les premières copies et le diff sont conservés. La nouvelle
capture a utilisé un shell sans profil et le chemin explicite du Python local ;
les validations et l'installation ci-dessus ont ensuite terminé normalement.
Aucun envoi externe n'a été autorisé ou ajouté.

L'issue 47 est réservée et son corps est actualisé pour la revue moteur. La
colonne Project n'a pas été modifiée : le connecteur disponible n'expose pas
cette opération et aucun outil de navigateur connecté n'est disponible dans
cette session. La mission reste ouverte ; aucun statut Done n'est revendiqué.
