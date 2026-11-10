# #50 — Test moteur ciblé

Version : fichier de l'Acre identifié par `CONTRACT.json`, statut **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Aucun test moteur n'est encore attesté pour cette modification.

1. Relancer complètement le jeu pour charger le correctif, puis ouvrir une nouvelle partie en 1776 avec le mod et la configuration DLC habituelle.
2. Dans la sélection des pays et les aperçus du journal, passer entre plusieurs pays, notamment un pays sud-américain existant et une grande puissance. Le différend de l'Acre ne doit pas être proposé à un pays étranger à sa condition bolivienne. Aucun pays bolivien ne doit être créé par le correctif.
3. Comparer uniquement les nouvelles lignes du journal d'erreurs après ce lancement avec les six messages conservés dans `OBSERVED_DIAGNOSTICS.json`. Vérifier l'absence des erreurs « Event target link 'c' returned an unset scope » et « Invalid left side during comparison 'c' » pour `02_acre_dispute.txt` dans son bloc d'affichage. Le numéro de ligne peut changer après la correction.
4. Lancer la partie, laisser passer quelques jours, sauvegarder et recharger. Vérifier le fonctionnement habituel des journaux du pays choisi. Les effets et conclusions de l'Acre n'ont pas été modifiés.
5. Si le contenu Colossus of the South peut être désactivé pour un second lancement, vérifier que son entrée reste masquée et que le chargement fonctionne. Ne pas conclure qu'un DLC absent a été testé si cette configuration n'a pas été utilisée.
6. Le cas positif « Bolivie existante, consultée comme pays courant, avec DLC » exige une partie avancée ou une sauvegarde de test adaptée. S'il n'est pas disponible, le marquer non testé ; ne pas ajouter un pays ni modifier le scénario pour obtenir une attestation.

Ce contrôle peut être regroupé avec la prochaine revue moteur. Les autres messages, dont ceux de diplomatie, du Maroc ou des connexions navales, restent des sujets séparés : cette passe ne les annonce pas corrigés. Indiquer simplement les cas réellement vérifiés et tout nouveau message lié au fichier de l'Acre.
