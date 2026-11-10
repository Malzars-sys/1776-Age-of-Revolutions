# Mission 25 — test groupé du lot IA

État actuel : installation locale vérifiée statiquement, aucun nouveau test moteur. Utiliser une nouvelle partie **1776**, le mod local courant et les fichiers des deux reçus d'installation. Une vieille sauvegarde ne valide pas les affectations initiales réparées par 24.

## Test courant

1. **Chargement.** Lancer avec la configuration DLC habituelle. Conserver les nouveaux logs avec leur date de lancement ; ne pas réutiliser les anciennes captures du 8 novembre pour conclure sur le correctif. Vérifier l'absence de nouvelle erreur de chargement liée aux cinq fichiers `zz_1776_v115_*` de ce lot.
2. **Simulation IA.** Jouer ou observer au moins un mois avec Russie, Grande-Bretagne et pays asiatiques présents, puis sauvegarder et recharger. Cette simulation exerce des évaluations de stratégies et de régions ; elle ne garantit pas que chaque objectif secret ait été recalculé ou sélectionné. Si les erreurs `Event target link 'region' returned an invalid object` reviennent, garder leur chaîne d'appel complète et la sauvegarde. Les 4 127 anciens messages ne sont pas un résultat après correction.
3. **Références.** Dans les logs frais, rechercher les erreurs d'identifiant pour `building_naval_base`, `ai_strategy_confrontation_agenda`, `ai_strategy_consolidation_agenda`, `law_revolutionary_guard`, `je_social_revolution` et `movement_anti_communist`. Une simple occurrence d'un nom dans un message normal n'est pas une erreur. La règle navale corrigée exige l'administration navale au niveau 3 dans l'État russe pertinent, ou conserve son autre branche de port au niveau 5.
4. **Départ préservé.** Vérifier que les lois initiales et les journaux déjà présents restent ceux du scénario. La garde révolutionnaire ne doit pas être accordée par ce lot au lancement ; ses conditions natives incluent la technologie `enlistment_offices` et les lois politiques requises. Les données de population et frontières ne sont pas modifiées.
5. **DLC désactivé, si disponible.** Refaire chargement, quelques jours et rechargement sans State and Revolution. Enregistrer une étape indisponible comme non testée, sans inventer de résultat.

## Cas révolutionnaire avancé, à noter séparément

Ces cas nécessitent une situation éligible ou un scénario de test dédié. Ne pas les déclarer passés à partir du seul lancement 1776 et ne pas modifier la partie principale pour les préparer.

- Vérifier que les deux stratégies politiques peuvent être évaluées dans un gouvernement radical de gauche, avec leurs conditions natives. Leur existence dans la base de données ne prouve pas leur sélection par l'IA.
- Vérifier la garde révolutionnaire dans un pays satisfaisant ses prérequis : disponibilité, activation et comportement des commandants doivent être évalués en jeu. Aucun test de cet effet n'a été effectué par l'agent.
- Dans le nouveau journal de révolution sociale, contrôler le compteur et les deux conclusions. La réussite exige les lois sociales et les quatre institutions au niveau 5 définies dans le natif, ainsi que l'absence de pénurie bureaucratique imminente. L'échec couvre notamment la perte de la république des conseils et les conditions de consolidation. Une activation forcée contourne les conditions de raccordement et ne valide pas leur progression normale.
- La réussite doit appeler `aor1776_v115_ai_progression.1`, accorder `modifier_social_revolution` pendant la durée native de 7 300 jours et nettoyer le compteur. L'ancien `communism.6` doit conserver sa récompense antérieure pour l'ancien journal. Comparer l'aperçu et l'effet, puis sauvegarder/recharger.
- Le mouvement blanc restauré suit son déclencheur natif de république des conseils ; vérifier sa création/dissolution seulement dans un pays éligible.

Pour le retour, préciser quels cas ont réellement été exercés, la configuration DLC, la sauvegarde et les éventuelles erreurs nouvelles. Le test simple de démarrage et les cas avancés gardent des statuts séparés. La clôture globale de 25 exige aussi les autres conditions de sortie déjà suivies ; ce protocole n'accorde aucune nouvelle acceptation aux missions voisines.
