# #39 — Reprise après migration locale

**État courant du 9 novembre 2026 :** `MIGRATION_R4` est installé et prêt pour une revue moteur. Les 400 contrats legacy ont été migrés ; le catalogue final compte 493 identifiants et aucun ancien champ direct. Lire `MIGRATION_R4/REPORT.md`, `INSTALLATION.json`, les validations et `RUNTIME_PROTOCOL.md` avant toute autre passe.

Prochaine action : revue des limites DLC avec #24 et essais moteur groupés de cette version locale. Préserver le candidat d'intégration figé sous #25 ; ne pas confondre les deux versions et ne pas faire de Git write sans autorisation. Les fichiers témoins #27 restent inchangés. Ne pas réactiver automatiquement les cinq familles natives masquées ni inventer de conclusions aux trois entrées conservées sans outcome.

La suite ci-dessous est l'ancienne prochaine action de l'inventaire, conservée comme historique et remplacée par l'état ci-dessus.

## Historique de l'inventaire initial

Statut réel : In progress, inventaire structurel terminé ; aucune migration installée. Ne pas annoncer In review ou Done sur cette seule base.

1. Relire la fiche #39 et l'état courant de la préparation #25. Préserver leurs changements et l'ordre de travail documenté.
2. Relancer l'inventaire si les empreintes de ses fournisseurs ont changé. Consulter les 490 lignes de `CATALOGUE.csv` et les consommateurs réels avant de préparer des modifications.
3. Traiter les anciens journaux communistes et le consommateur natif de `je_five_year_plan` comme un lot cohérent. Le contrat natif 1.15 contient de nouvelles chaînes ; préserver les choix propres au mod et documenter les dépendances vers #24.
4. Mapper explicitement en-têtes personnalisés, descriptions d'effets/événements, handlers orphelins, délais, all-involved et ordre des conclusions. Aucune conversion regex globale.
5. Préserver en témoins les lots #27 déjà acceptés. Tester les lots sur une version identifiée avant toute demande d'acceptation moteur ; les branches non rencontrées restent non testées.

La migration des 400 contrats anciens et la revue complète des autres entrées restent ouvertes. Les huit identifiants natifs absents et les trois entrées sans outcome ne doivent pas être restaurés ou complétés automatiquement.
