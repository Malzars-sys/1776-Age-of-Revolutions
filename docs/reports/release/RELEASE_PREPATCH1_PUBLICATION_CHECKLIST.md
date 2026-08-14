# RELEASE-PREPATCH-1 — Checklist de publication

Baseline auditée : `538648fd0eb23ca7b14325e108ff682dea6f8fce`.

Version confirmée : `2.3.0`.

Tag confirmé : `workshop-release-2.3.0-20260814`.

RELEASE-PREPATCH-2 finalise les fichiers de release et les références Git. La publication GitHub/Workshop reste une opération séparée et n'est pas exécutée ici.

- [x] confirmer version
- [x] confirmer changelog
- [x] éventuellement mettre à jour version/descriptor
- [ ] test runtime final uniquement si réellement requis — `NOT_REQUIRED — no gameplay delta since validated runtime baseline`
- [ ] stage exact des fichiers release
- [ ] commit release
- [ ] vérifier worktree clean
- [ ] créer tag
- [ ] push branche
- [ ] push tag
- [ ] publication GitHub/Workshop si applicable
- [ ] contrôle post-publication

## Contrôles avant autorisation de publication

- Recalculer l'empreinte gameplay et exiger 877 fichiers avec le hash `7319D86F6EB2AAB9181BD32A95D8D498FAFE1BDAEF57127EB83FF3E864C0A80F` tant qu'aucune phase gameplay séparée n'a été autorisée.
- Confirmer que les trois fichiers technologiques `PRELIMINARY / UNVERIFIED` restent présentés comme recherche non autoritative.
- Relire les neuf dettes `DEFERRED_POST_RELEASE` du rapport principal ; leur existence n'autorise aucune correction opportuniste pendant le commit de release.
- Si la version publique `2.3.0` est confirmée, mettre à jour uniquement les métadonnées explicitement autorisées dans la phase de publication suivante.
- Arrêter la publication si un nouveau chemin gameplay, une erreur de diff, un tag inattendu ou un changement non expliqué apparaît.

## État de RELEASE-PREPATCH-1

```text
STAGE_PERFORMED = NO
COMMIT_CREATED = NO
TAG_CREATED = NO
PUSH_PERFORMED = NO
PUBLICATION_PERFORMED = NO
VICTORIA_3_LAUNCHED = NO
```
