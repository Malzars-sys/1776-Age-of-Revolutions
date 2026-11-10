# Complément borné : quatre fournisseurs manquants et leur événement de conclusion

9 novembre 2026. Stratégie écrite avant installation de ce complément.

Les messages conservés et l'inventaire courant confirment quatre absences liées : `ai_strategy_confrontation_agenda`, `ai_strategy_consolidation_agenda`, `law_revolutionary_guard` et `je_social_revolution`. Les deux stratégies sont cachées par l'ancien fichier politique du mod, la loi par son ancien modèle d'armée et le journal par l'ancien contenu communiste. Leurs blocs natifs actuels et leurs dépendances ont été consultés. Le prérequis technologique `enlistment_offices`, les lois `law_council_republic` / `law_factory_councils`, les idéologies, helpers, modificateurs et valeurs nécessaires ont des fournisseurs actuels.

Le complément prépare quatre nouveaux fichiers, sans modifier ces anciens masques : deux stratégies politiques, une loi, un journal et un événement. Les deux stratégies et la loi reprennent exactement les champs natifs 1.15. Le journal conserve les conditions, deux conclusions, effets, compteurs et nettoyages natifs ; seul l'identifiant de son événement de réussite est adapté.

## Pourquoi un événement distinct

Le `communism.6` existant du mod donne `institutions_of_socialism_modifier` pendant `long_modifier_time`. Il sert au journal communiste conservé par la mission 39. Le `communism.6` natif actuel donne `modifier_social_revolution` pendant `very_long_modifier_time`, puis exécute `je_social_revolution_cleanup`.

Réutiliser l'ancien événement pour le journal restauré créerait une réussite dont la récompense ne correspond pas à l'aperçu natif et laisserait son compteur sans nettoyage. Remplacer l'ancien événement changerait le contenu du mod déjà migré. Le complément copie donc l'événement natif sous `aor1776_v115_ai_progression.1` et ne change que la référence de conclusion du nouveau journal. Les clés de texte, image, option et effets sont ceux du natif ; les localisations existantes FR/EN doivent être vérifiées avant installation. L'ancien `communism.6` et les fichiers de 39 restent identiques.

## Limites d'activation et protections

Aucun historique national, effet initial, loi active, technologie accordée, journal existant ou profil de départ n'est écrit. La loi restaurée conserve ses conditions natives, notamment la technologie d'enrôlement et les lois politiques requises. Aucun raccord automatique de la vieille chaîne communiste vers la nouvelle n'est ajouté. Ce complément résout des dépendances de scripts et rend les définitions disponibles ; il ne certifie pas le portage complet de toutes les chaînes révolutionnaires du DLC.

Les autres identifiants de familles déjà laissés pour revue dans 39 ne sont pas restaurés par association arbitraire. Tous les blocs existants, reçus et états de validation sont conservés. Les nouvelles preuves appartiennent à 25 et ne remplacent pas celles de 39. Les contrôles statiques et le test moteur restent distincts.

## Complément après le premier contrôle du candidat

Le premier contrôle a identifié une dépendance supplémentaire réelle des deux stratégies : `movement_anti_communist`, masqué lui aussi par l'ancien fichier du mod. Le candidat R2 ajoute sa définition native dans un cinquième fichier neuf. Son déclencheur natif exige une loi de république des conseils ; ses treize références d'idéologies ont déjà des fournisseurs effectifs. Aucun mouvement existant n'est modifié. Le complément compte donc **six objets dans cinq fichiers neufs**, en plus des deux valeurs déjà corrigées dans la stratégie par défaut.

Les deux autres catégories d'échec du premier contrôleur étaient des erreurs de modèle de vérification : `very_long_modifier_time` est une valeur de script scalaire (7 300 jours), et `approaching_bureaucracy_shortage` un déclencheur moteur documenté par sa localisation native, pas une définition de déclencheur scripté à restaurer. Le contrôleur est corrigé pour leurs catégories réelles ; aucun objet factice ni alias n'est créé pour ces noms. Le premier résultat et le premier candidat restent conservés dans `dependencies/` ; le candidat complet est dans `dependencies_R2/`.
