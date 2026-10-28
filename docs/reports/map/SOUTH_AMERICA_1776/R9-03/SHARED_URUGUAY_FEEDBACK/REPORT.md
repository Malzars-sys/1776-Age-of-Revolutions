# R9-03 — Sacramento dans l'Uruguay partagé

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, 28 octobre 2026. Cet amendement remplace la région d'État distincte créée lors de l'installation initiale. Il répond aux deux retours du joueur : noms répétés et appartenance géographique à l'Uruguay.

## Correction installée

`x4E1443` appartient désormais à `STATE_URUGUAY` (ID 370). La portion espagnole SC4 et la portion brésilienne BRZ sont deux États propriétaires au sein d'une même région d'État, selon le mécanisme natif des États partagés. La région distincte `STATE_COLONIA_DO_SACRAMENTO` et ses cinq locators ID 3161 sont retirés. Aucune autre région ou position de hub n'est modifiée.

Le bitmap et les 51 pixels agrandis de l'enclave ne changent pas. Le propriétaire reste BRZ, colonie du Portugal. Les 3 317 habitants, leurs cohortes et leurs statuts restent identiques ; seuls leurs scopes géographiques rejoignent l'Uruguay. Le port commercial de niveau 1 conserve PM et réserves dans la portion BRZ de l'Uruguay. Les potentiels agricoles et de pêche sont réunis à nouveau, sans création de capacité supplémentaire.

L'État garde le nom natif d'**Uruguay** : aucun `set_state_name` ne le rebaptise en Sacramento. Des noms de hubs propres à la portion portugaise distinguent la ville, le port et les environs ; le port est nommé **Port de Sacramento** / **Port of Sacramento**. Les autres propriétaires gardent leurs noms natifs, notamment Montevideo et Punta del Este. Les scripts reprennent `set_hub_name` en scope State du vanilla et les hooks additifs déjà employés dans le mod.

Le moteur doit désormais placer les bâtiments de la portion BRZ dans ses propres provinces, selon son traitement des États partagés. Les hubs généraux d'Uruguay et sa sortie navale 3065 sont conservés. Le placement et le ravitaillement de cette configuration doivent être vérifiés en jeu ; la vérification visuelle de la version distincte antérieure ne les homologue pas.

## Preuves et contrôles

**20/20 contrôles statiques passent** : syntaxe et empreintes, région unique, coexistence SC4/BRZ, conservation des commandes de propriétaires et de toutes les autres attributions, cohortes par propriétaire, effectif de 3 317, port identique, potentiels conservés, autres régions et hubs inchangés, retrait des seuls locators obsolètes, bitmap/terrains inchangés, profils/pactes/armées préservés, noms limités à la portion portugaise, localisation FR/EN, absence de référence runtime à la région supprimée et absence d'écriture runtime non listée depuis la nouvelle baseline.

La baseline est capturée sur le workspace courant. Les travaux Congo présents dans les fichiers partagés sont conservés. Un lancement du vérificateur initial lors du retour sur les noms avait échoué sur des empreintes et scopes anciens, notamment à cause de ces travaux postérieurs. Ce résultat est archivé dans `LABEL_FEEDBACK_01/INHERITED_SNAPSHOT_CHECK.json` ; il n'a pas servi à restaurer les fichiers initiaux. Le reçu original à 26 contrôles est conservé dans `LABEL_FEEDBACK_01/VALIDATION_BEFORE.json`. Le contrat initial reste exécutable séparément avec `tools/r903.py --verify-initial` ; le contrat courant est `tools/r903_shared_uruguay.py --verify`, également appelé par `tools/r903.py --verify`.

Le manifeste courant combine les fichiers de la livraison précédente et cet amendement, avec leurs empreintes réellement installées. Ces empreintes identifient l'état courant des fichiers partagés, sans attribuer aux auteurs de R9 les changements concurrents qu'ils contiennent.

## Validation en jeu encore nécessaire

**Démarrer une nouvelle partie**, car la région d'État initiale a été supprimée du scénario. Une sauvegarde construite avec cette ancienne région ne constitue pas un test du nouveau découpage.

1. Sélectionner l'enclave : titre Uruguay, propriétaire Brésil, région partagée avec la portion espagnole ; aucun État régional indépendant Sacramento.
2. Vérifier les noms de la ville et du port, ainsi que le maintien des noms des localités espagnoles.
3. Vérifier port construit sur les terres BRZ, desserte maritime, accès réel au marché, emplois et nourriture après simulation.
4. Vérifier 3 317 habitants BRZ, cohortes inchangées, puis sauvegarder/recharger.

La capture précédente montre un accès affiché de 100 % au marché portugais, mais aussi une population affamée et un PIB initial nul. Ce sont des observations ponctuelles de l'ancienne configuration : aucune durée de simulation ni résolution de ces indicateurs n'est déduite de cette image. Ils restent à contrôler après la correction ; aucune refonte économique n'est incluse implicitement.

Les sources et le proxy démographique de 1760 restent ceux du dossier R9-03, sans nouvelle prétention de recensement pour 1776. Aucune modification vanilla, aucun commit ou push.
