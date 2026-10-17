# Chine — cavalerie de départ uniquement en lanciers

**PASS_STATIC_PENDING_RUNTIME** — nouvelle partie requise, aucun lancement du moteur.

Les **28 bataillons de dragons et 32 bataillons de hussards chinois** deviennent **60 bataillons de lanciers**, conformément à la consigne de ne donner que des lanciers à la Chine. Dix entrées de recrutement sont modifiées, sans changement des effectifs, des États de recrutement, du type de service, des formations, des QG, des noms ou des commandes de sauvegarde de portée. Infanterie, artillerie, flotte et unités étrangères inchangées.

Seul fichier fonctionnel modifié : `common/history/military_formations/06_military_formations_asia.txt`, uniquement dans `c:CHI`. Les définitions globales des unités ne sont pas modifiées. Les lanciers n'ont pas d'entrée de consommation d'armes légères dans leur entretien défini ; cela ne signifie pas que toute autre consommation militaire chinoise a été supprimée.

Aucune technologie accordée. Aucun changement aux manufactures, aux vingt nouveaux niveaux de thé, au système des cantons, aux infrastructures, aux populations ou à la carte. Aucun changement destiné à interdire définitivement les améliorations de cavalerie ultérieures.

Contrôle reproductible : `tools/china_lancers_2026_10_15.py validate` — dix contrôles statiques. Comparaison exacte avec une transformation ne changeant que les dix champs de type d'unité, inventaire effectif de toutes les cavaleries chinoises et empreintes des autres fichiers fonctionnels. HEAD et index Git préservés ; aucun commit ou push.

Référence avant modification et détail des dix entrées : `BASELINE.json`. Résultats : `VALIDATION.json`. À vérifier dans une nouvelle partie : les huit formations terrestres chinoises, leurs 60 bataillons de cavalerie désormais lanciers, les recrutements et leur entretien.
