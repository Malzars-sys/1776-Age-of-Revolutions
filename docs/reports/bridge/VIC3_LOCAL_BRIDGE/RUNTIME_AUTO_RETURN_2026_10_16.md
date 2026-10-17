# Retour automatique observé : témoin 0 → 1 → 0

Statut limité : **PASS_RUNTIME_PROBE_ABA_OBSERVED**.

Après l'annonce du retour au suivi automatique et les exports du joueur, le
journal contient **11 nouveaux blocs complets valides** depuis le curseur du
forçage, dans la même session. Le dernier complet, à **00:48:35 le 16 octobre**,
indique FRA / STATE_ILE_DE_FRANCE, **0 témoin**, mode **auto**, toujours **17 niveaux
d'infrastructures** et les mêmes PM : routes traditionnelles, sans canaux/rails.
La date en jeu de ce relevé est **3 février 1776**.

La séquence observée est donc : automatique 0, forcé 1, automatique 0. Les niveaux
du bâtiment régional et ses trois PM n'ont pas changé dans ces trois observations.
Cela ne constitue pas une vérification de toutes les données économiques.

**Attention : un bloc plus récent, à 00:48:36, est encore incomplet.** Le lecteur
standard le refuse. L'analyse complémentaire lit explicitement les blocs complets
antérieurs mais nouveaux depuis le curseur ; elle ne les présente pas comme un
état actuel certifié et ne masque pas ce dernier bloc partiel. Le retour automatique
a été effectivement observé ; le tout dernier export n'est pas déclaré complet.

Il n'est pas nécessaire de continuer à cliquer pour prouver ce retour déjà observé.
La latence d'écriture des journaux reste une limite ouverte du pont. Ni les rails
au sol, ni un pilotage entrant du jeu, ni une intégration MCP native dans la
conversation ne sont validés par cette séquence. Aucun mod principal, carte,
PM économique ou fichier de sauvegarde n'est modifié par l'enregistrement du test.
