# Nationalité officielle : accès avant le nationalisme

7 novembre 2026 — `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.

Le joueur demande que cette variante de la sujétion précède le nationalisme. Le prérequis `nationalism` ajouté en R1 est donc retiré, sans lui substituer un autre verrou technologique arbitraire. La définition native de `law_official_nationality` ne possède pas non plus de prérequis technologique.

La nationalité officielle est désormais identique à sa définition vanilla canonique : variante de `law_subjecthood`, visibilité réservée à `RUS`, conditions politiques natives de monarchie, théocratie ou chefferie, effets et opinions héritées préservés. La préférence tsariste ajoutée en R1 reste en place. La loi peut être proposée avant la recherche du nationalisme si les conditions politiques de promulgation sont réunies ; elle n'est pas activée au départ de 1776.

La Troisième section conserve son déblocage par la police civile professionnelle. Bureaucrates militaires, Héritage noble, profils initiaux, colonisation, technologies et autres lois restent inchangés.

Note de lecture de l'arbre actuel : l'État ethnique demande `pan-nationalism` dans `common/laws/00_citizenship.txt`. Ce prérequis n'a pas été modifié. Aucun changement à l'arbre n'est nécessaire pour avancer la variante russe.

## Preuves

- Seul changement chargé par le jeu : suppression du champ `unlocking_technologies = { nationalism }` dans `common/laws/1776_v115_russian_laws.txt`.
- `laws_before.txt` et `CHANGES.patch` conservent la préimage et le changement borné.
- `INSTALLATION.json` porte les empreintes de l'état R2 ; le manifeste R1 est conservé à l'identique.
- Le validateur conserve ses contrôles de restrictions, d'effets, d'initialisation et de non-régression. Il exige maintenant l'absence de verrou technologique pour la nationalité officielle et compare toute sa définition à celle du vanilla.
- Un contrôle négatif supplémentaire réintroduit le verrou de nationalisme en mémoire pour vérifier son rejet. Les anciens contrôles restent présents.
- Résultats de cette révision dans `VALIDATION.json`. Les constats antérieurs du validateur général de technologies ne sont ni effacés ni présentés comme corrigés.
- Résultat obtenu : **PASS_STATIC_ONLY**, neuf contrôles négatifs rejetés, aucun nouveau constat de technologie initiale sur les six pays témoins.
- Concurrence : `common/defines/00_defines.txt`, présent dans la baseline R1, a été supprimé extérieurement entre les deux passes. La première exécution du validateur s'est arrêtée sur ce fichier absent ; le contrôle a été corrigé pour inventorier une suppression comme différence concurrente plutôt que tenter sa lecture. Aucun fichier n'a été restauré, et les contrats des lois restent tous exigés.

Commande : `python -B tools/compatibility/v115_russian_laws_implementation_audit.py --output docs/reports/compatibility/V1_15_RUSSIAN_LAWS_IMPLEMENTATION_2026_11_07/R2/VALIDATION.json`.

Contrôle moteur restant : redémarrer le jeu et vérifier, en Russie sans nationalisme recherché, la présence de la variante, ses conditions politiques et le soutien affiché des forces armées tsaristes. Vérifier qu'elle n'est pas active automatiquement et que les autres pays n'y ont pas accès. Aucun test en jeu ni validation humaine n'est déclaré.
