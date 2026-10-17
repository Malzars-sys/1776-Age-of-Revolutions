# Protections déclarées et contrôles

1. Les deux nouveaux types et le Lien impérial ont `annex_on_country_formation=no`.
2. Les trois listes d’alternatives d’autonomie sont vides : aucune sortie vers une Terre de la Couronne ou un fantoche annexable par cette chaîne.
3. L’interaction native de baisse d’autonomie refuse ces types dans potential et possible.
4. Le but `annex_country` refuse une cible relevant de ces types dans valid. Le coup vanilla d’annexion ne connaît de toute façon pas nos nouveaux pactes.
5. Le but d’unification refuse, dans possible et valid, les États de ces sujets.
6. La prise d’État par le suzerain utilise une liste native qui exclut nos types. Les interactions entre pays indépendants ne sont pas globalement interdites.
7. L’ancienne réforme impériale3 n’a plus d’effet `annex`, ni de conversion préalable. Ses boutons et effets sont verrouillés, sans exception pour les électeurs.

Un test compare les AST des trois remplacements partagés avec le vanilla après retrait de nos seules gardes : aucune autre règle native n’est changée.

**Démonstration : statique uniquement.** Il faut encore tester les interactions réellement affichées, les buts automatiques et une unification en nouvelle partie. Aucune immunité contre un autre mod, un effet console `annex`, toutes les guerres étrangères ou tout article de traité n’est revendiquée.

Pour rendre plus tard un État impérial ordinaire annexable, une réforme devra explicitement modifier les gardes et le chemin d’annexion, en réexaminant les alternatives et les effets de formation. Aucun déverrouillage actif n’est livré. L’électorat n’a aucune exception d’annexion dans cette mission.
