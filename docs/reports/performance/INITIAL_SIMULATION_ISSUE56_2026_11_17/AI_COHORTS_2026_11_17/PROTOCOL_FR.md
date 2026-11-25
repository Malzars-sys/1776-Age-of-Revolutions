# Issue #56 — contrôleurs IA, protocole de la passe du 17 novembre 2026

Laboratoire externe : `C:/Users/simeo/AppData/Local/Temp/aor56_ai_20261117`.
Réutilisation du runtime figé, de la sauvegarde S0, des réglages, caches préparés, sonde DAY, échantillonneur CPU/RAM et échantillonneur de threads de la passe précédente. Steam 1.15.1 sans DLC de gameplay, jamais l’installation locale 1.15.0 avec DLC. Même interface de laboratoire, fermée pendant les fenêtres ; Legacy ScriptProfiling désactivé dans les comparaisons de débit.

Ordre prévu : **AI_OFF3 → AI_ON3**, puis **AI_DEC1 → AI_OTHER1 → AI_ON4**, et une répétition IA OFF si possible. Les noms représentent des essais à exécuter, pas des résultats déjà obtenus. Si la capture bloque avant simulation, conserver la tentative et la distinguer d’une mesure.

Inventaire structurel complet de S0 : 646 contrôleurs, 244 pays décentralisés peuplés, deux décentralisés sans population enregistrée (S72/country856/controller402 et S74/country858/controller554), 400 autres pays peuplés (123 recognized, 258 unrecognized, 19 colonial). Aucun pays absent de la classification, aucune suppression de contenu. La cohorte DEC comprend **246**, le complément OTHER **400**.

ALL OFF est appliqué par la même commande native `disable_ai all` que précédemment ; ON garde l’IA normale. Les variantes DEC/OTHER changent exclusivement les champs `AI.enabled` des contrôleurs concernés dans une copie de S0. Elles conservent tous les autres octets hors ces remplacements, notamment l’ensemble des données historiques et économiques. Les empreintes et identités ciblées sont archivées. La classification de départ fixe la cohorte ; un changement de type ultérieur ne redéfinit pas celle-ci silencieusement.

Chaque passage doit obtenir une sauvegarde native initiale en pause et une sauvegarde après les mesures, puis vérifier les flags réellement sérialisés, les contrôleurs absents/créés et l’IA hors cible. Une copie d’entrée du nouveau profil peut être renommée REFERENCE_S0.v3 pour laisser le nom natif de sauvegarde initiale libre ; le fichier source préexistant reste intact et la copie de référence garde ses octets.

Vitesse 5 observée. Fenêtres DAY S+1 puis 14/28/56 jours complets, timestamps natifs HH:mm:ss, calendrier moteur365 jours. Aucun chargement, temps de menu ou pause inclus. Préparation et vérification de fichiers lourds hors des fenêtres de simulation. Comparaisons contemporaines ; les anciennes durées 93/122/149 s ne servent pas de témoins actuels.

Après les comparaisons : analyser les objectifs/stratégies, investissements, critères impossibles et évolution économique dans la cohorte impliquée. Employer les méthodes de profilage supportées sans contourner la restriction Windows sur les piles CPU. Toute référence vanilla doit rester sur le même exécutable Steam et expliciter 1836, pays/population/monde/DLC différents ; elle n’est pas un contrôle équivalent de 1776.

Préservation avant : empreintes des 2996 fichiers runtime normaux,80 fichiers du profil normal,Git/exécutable/diplomatie,468 rapports antérieurs,28 outils ; copie stable de la base ACTUELLE du lanceur. Aucune restauration historique, aucun réglage de sécurité changé, aucune opération Git d’écriture, aucune correction expérimentale intégrée.
