# Révolution américaine R6 — ouverture française et liste des lois

18 octobre 2026. **384 vérifications statiques réussies ; essai moteur R6 non effectué.**
Résultat : [VALIDATION.json](VALIDATION.json). Outil courant :
`tools/validate_american_revolution_r6.py`, qui réutilise les contrôles financiers
et militaires R5 et remplace explicitement trois attentes de démarrage devenues
obsolètes. Les contrôles structurels et les projections de choix ne sont pas
une exécution du moteur.

## La France prend l’initiative

1. Après trois jours écoulés depuis le lancement, **la France** reçoit
   « Atteindre Londres par-delà l’océan ». Elle peut autoriser les contacts
   avec les insurgés pour affaiblir son rival, ou refuser cette entreprise.
   Les deux options existent pour le joueur et pour l’IA française.
2. **Si elle accepte**, le lendemain, un joueur américain reçoit
   « Une aide venue d’outre-Atlantique ». Son option ouvre le journal du secours.
   Le Congrès peut alors demander l’aide et choisir ses engagements financiers.
3. Si les Américains sont contrôlés par l’IA, leur réaction cachée ouvre le
   journal et envoie la demande. Un joueur français reçoit donc ensuite la
   demande du Congrès, puis décide des conditions financières.
4. **Si la France refuse**, aucun événement américain n’est envoyé et la
   demande d’aide reste fermée. Les anciens boutons, décisions de récupération
   et événements déjà programmés exigent aussi cette autorisation française.

L’initiative et la réponse américaines sont chacune protégées contre les
doublons. Un chargement conserve une décision française déjà prise et ne
reprogramme pas le premier événement. Pour une sauvegarde antérieure à R6,
un ancien projet non signé est nettoyé avant la nouvelle ouverture ; les prêts
déjà signés et leurs paiements sont conservés.

Cette première décision porte sur l’ouverture des **négociations de secours**.
Les conditions du prêt restent soumises aux choix ultérieurs, et l’entrée
militaire conserve son calendrier distinct. Les montants, les taux 0/5 %,
les cinq articles, la dette à dix ans et les corrections de ratification R5
sont inchangés. La France ne déclare pas la guerre en choisissant cette option.

## Les Minutemen remplacent la milice dans la liste américaine

La loi mère « Milice nationale » est masquée uniquement pour les États-Unis,
comme le vanilla masque les levées paysannes au profit de leur variante
japonaise. La visibilité propre des Compagnies de minutemen reste américaine.

La définition de la variante a été déplacée de
`common/laws/1776_usa_minutemen.txt` vers `common/laws/00_army_model.txt`,
immédiatement après sa loi mère et avant la conscription de masse. L’ancien
fichier est retiré afin de conserver **une seule définition**. L’ordre déclaré
de la liste américaine devient : levées paysannes, armée professionnelle,
Compagnies de minutemen, conscription de masse. Le panneau natif filtre les
lignes avec `Law.IsVisible` et ignore les lignes invisibles.

L’identifiant `law_aor1776_minutemen`, son parent, son activation dès le premier
jour, ses conditions et ses effets sont conservés. Tous les autres pays gardent
la Milice nationale habituelle. Aucune modification globale de l’interface
n’est nécessaire ; le rendu de la liste reste à confirmer dans le jeu.

## Conservation et essai

Les contrôles comparent les effets financiers, la variante déplacée et les
autres lois avec les sources précédentes. Les 56 fichiers protégés, comprenant
la carte, les États, les populations, les formations et les corrections R5
hors périmètre, sont inchangés. HEAD et l’index Git sont conservés ; aucune
sauvegarde ni installation vanilla n’a été modifiée.

Les localisations nouvelles existent en français et en anglais, et les huit
événements visibles conservent l’illustration native déjà choisie. Les journaux
restent au statut technique à valider selon le guide du dépôt.

**Redémarrer complètement le jeu.** Sur une nouvelle partie française, vérifier
le premier événement, puis essayer séparément l’accord et le refus. Sur une
partie américaine, vérifier que l’invitation dépend de l’accord français et
que le journal ouvre ensuite la négociation habituelle. Contrôler enfin les
quatre lignes américaines du type d’armée, puis la Milice nationale dans un
autre pays, sans changement des effets de loi.
