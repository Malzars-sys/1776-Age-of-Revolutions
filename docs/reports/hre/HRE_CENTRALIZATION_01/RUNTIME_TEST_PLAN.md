# Plan de test moteur — aucun résultat prérempli

## Partie normale, mod principal seul

Redémarrer le jeu pour recharger les types, localisations et textures. Nouvelle partie1776. Vérifier la table : un Lien impérial, un État impérial et un Électorat impérial, sans ancienne deuxième Terre de la Couronne impériale. Vérifier les trois titres sans icône, leurs descriptions en français puis anglais, et ouvrir les infobulles des concepts liés.

La bannière aux trois couronnes doit identifier l’électorat ; la grande couronne, l’État impérial. Vérifier les textures sur fond sombre aux tailles de liste et d’infobulle. Aucun pays ne doit commencer avec les deux nouveaux pactes. Contrôler OLD–HLB, bloc, registre, frontières, économies et armées inchangés, puis un mois de simulation.

## Compagnon isolé

Ne pas l’activer sur une sauvegarde à conserver. Copier manuellement le descripteur `docs/prototypes/HRE_CENTRALIZATION_01/HRE_CENTRALIZATION_01_TEST.mod` dans le dossier de mods utilisateur si nécessaire, et placer le compagnon après le mod principal dans un playset de test. Aucune de ces opérations n’a été faite par cette livraison. Activer le mode debug pour la console et lancer une nouvelle partie.

1. Dans la console d’effets, armer explicitement : `effect set_global_variable = aor1776_hre_c01_dev_armed`.
2. Exécuter `effect aor1776_hre_c01_dev_setup = yes`. Vérifier ANH15% et KPF10% sous l’empereur courant, tous deux distincts et non annexés (taux révisés R1). Si un précontrôle refuse, ne pas forcer une conversion générale.
3. Laisser passer au moins un prélèvement hebdomadaire : comparer une seule sortie et une seule entrée du pacte ; pas de deuxième taxe cachée. Relever valeurs réelles et effet de l’emploi/dépenses, sans les confondre avec le taux natif.
4. Tester guerre offensive/défensive de l’empereur, puis empereur simple soutien. Vérifier qui rejoint, sans prétendre que ces cas sont équivalents.
5. Essayer annexion, baisse d’autonomie, prise d’État et unification sur KPF ; vérifier que les actions ne permettent pas de contourner sa protection. Tester une interaction indépendante ordinaire pour vérifier qu’elle n’est pas globalement bloquée.
6. Déclencher l’élection par le système existant après décès et choisir PRU. Pour isoler uniquement le transfert, la console peut appeler `effect c:PRU = { aor1776_hre_install_elected_country = yes }` dans cette partie de test ; ce raccourci ne valide PAS le scrutin lui-même.
7. Vérifier ANH et KPF sous PRU, ancien AUS autonome, gouvernements, populations, bâtiments, armées et territoires conservés. Vérifier OLD–HLB et autres pactes hors sélection. Contrôler absence de cycle, désir de liberté et marchés.
8. Refaire séparément avec KPF, auparavant sujet, comme élu. Le candidat doit devenir indépendant avant le transfert des autres sujets. Vérifier les élections suivantes, pas seulement un appel de transfert.
9. Hors scrutin, dans le test uniquement : donner à ANH `aor1776_hre_constitutional_privilege_change_authorized`, appeler `aor1776_hre_grant_electoral_privilege`, vérifier type et voix ; réautoriser puis appeler revoke pour vérifier le retour sans perte de désir de liberté. Pendant un scrutin, la mutation doit être refusée.
10. Tester un candidat sujet étranger et un cas de création de bloc refusée. Les sujets étrangers ne doivent pas être libérés ; l’échec ne doit pas être masqué par un drapeau de réussite.

Relever erreurs nouvelles dans les journaux. Conclure chaque catégorie séparément : affichage, paiement, diplomatie, guerre, annexion et succession. Un mois de simulation sans crash ne certifie pas toutes les branches. La conversion générale reste une mission distincte.
