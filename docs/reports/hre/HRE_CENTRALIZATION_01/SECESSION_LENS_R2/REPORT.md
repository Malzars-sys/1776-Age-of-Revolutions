# SERG — une seule entrée de départ dans la lentille diplomatique

## Installé

Pour un pays reconnu comme membre impérial ET actuellement dans le bloc portant l’identité impériale, « Quitter le bloc de nations » est masqué dans les exigences diplomatiques. « Sécession impériale » reste l’entrée spécialisée, sous ses conditions préexistantes. Le dirigeant du bloc ne reçoit pas un droit de sécession : l’exclusion existante de l’empereur est conservée.

Le contrôle porte sur `selectable_in_lens`, pas seulement sur le texte ou le nombre affiché. La même garde dans `possible` empêche le lancement de la sortie générique par un autre point d’entrée scripté. Cela ne remplace pas tous les boutons natifs de l’interface du bloc ; l’identité impériale interdit déjà la sortie volontaire ordinaire.

Les autres blocs gardent la sortie native. Un TAG historiquement impérial appartenant à un bloc étranger n’est pas bloqué sur la seule foi de son TAG. Les pays hors de l’Empire ne voient pas apparaître la sécession impériale du fait de ce correctif.

## Préservé

Aucune fusion de mécanismes de paix, aucun renommage global des textes vanilla. Objectif de guerre, coût en manœuvres, infamie et effets de victoire de la sécession inchangés. Les conditions de sujétion, de cible impériale et de relations restent celles du coup existant. Aucun assouplissement pour les nouveaux sujets centralisés n’est introduit par cette correction d’affichage.

Taux15 %/10 %, chaîne d’autonomie, descriptions communes, mécanismes d’élection et prototype isolé inchangés. Aucun historique, territoire, habitant, bâtiment, unité ou registre modifié. Aucun commit, push, changement de branche ou d’index. L’installation du jeu reste en lecture seule.

## Technique et vérifications

Cinq fichiers fonctionnels : `common/diplomatic_plays/00_diplomatic_plays.txt` (override local du fichier installé, tous les autres coups conservés à l’identique), `common/diplomatic_plays/1776_imperial_plays.txt` (deux gardes supplémentaires seulement), `common/scripted_triggers/1776_imperial_secession_lens.txt` et deux ajouts de messages de validation FR/EN dans les localisations constitutionnelles. Le compilateur impérial applique cette couche en dernier pour préserver le correctif lors d’une régénération.

30/30 contrôles statiques et 42 tests réussis. Les tests comparent les arbres des autres coups natifs et la sécession existante après retrait des seules gardes déclarées. Les scénarios logiques ne sont pas des tests moteur.

**STATIC_PASS_RUNTIME_PENDING.** Après redémarrage : ouvrir les exigences diplomatiques avec un membre non empereur du SERG, constater l’absence de « Quitter le bloc de nations » et la présence de « Sécession impériale ». Les causes normales d’indisponibilité restent applicables. Contrôler ensuite un membre d’un autre bloc : sa sortie native doit rester disponible selon les règles habituelles. Aucun résultat en jeu n’est présumé acquis.
