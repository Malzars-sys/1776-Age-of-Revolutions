# HOTFIX-5C2E4C1A - Copie jetable Sepoy

## 1. Resume

Une copie jetable du fork a ete creee exclusivement a partir des 943 fichiers
retournes par `git ls-files`. Elle possede un nom, un chemin et un descripteur
launcher distincts. Aucun harnais, event, decision ou fichier de localisation
de test n'a ete ajoute.

La comparaison exhaustive donne 942 fichiers suivis identiques et une seule
difference attendue : le nom du `descriptor.mod` interne. Aucun fichier ne
manque et aucune difference inattendue n'a ete detectee.

**Verdict : `READY_FOR_HARNESS`.**

## 2. Etat Git initial

- Racine :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `bda2fd3856f6a643bd511683694d471662e270f9`.
- Commit C0 present : `bda2fd3 Prepare Sepoy functional test scenarios`.
- Aucun fichier suivi modifie.
- Seule exception non suivie : `docs/research/technology/`.
- Stash MARATH present et non applique.

## 3. Exception docs/research/technology

Les sept fichiers non suivis de `docs/research/technology/` n'ont pas ete
copies. Leurs sommes SHA-256 ont ete relevees avant et apres l'operation afin
de verifier leur integrite.

## 4. Chemins resolus

| Role | Chemin absolu |
|---|---|
| Fork source | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` |
| Dossier jetable | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test` |
| Descripteur launcher jetable | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test.mod` |
| Descripteur launcher source | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_age_of_revolutions_fork.mod` |

## 5. Absence de destination prealable

Avant toute creation :

- dossier jetable : `False` ;
- descripteur launcher jetable : `False`.

Aucun fichier preexistant n'a ete supprime, remplace ou deplace.

## 6. Inventaire des descripteurs source

Le `descriptor.mod` interne existe dans le fork. Quatre fichiers `.mod` sont
presents dans le dossier parent, mais un seul pointe exactement vers le fork :
`1776_age_of_revolutions_fork.mod`. Les trois autres pointent vers
`Basileia_Romaion_1736`, `Community_Mod_Framework` et `3472248460` ; ils ne sont
donc pas des modeles ambigus pour cette copie.

| Fichier | Champ | Valeur source | Action dans la copie |
|---|---|---|---|
| Interne | `name` | `1776 - Age of Revolutions Fork` | Remplace par le nom Disposable |
| Interne | `supported_version` | `1.*` | Conserve |
| Interne | `tags` | `Total Conversion` | Conserve |
| Interne | `version` | Absent | Laisse absent |
| Interne | `dependencies` | Absent | Laisse absent |
| Interne | `replace_path` | Absent | Laisse absent |
| Interne | `remote_file_id` | Absent | Confirme absent |
| Interne | `picture` | Absent | Laisse absent |
| Launcher | `name` | `1776 - Age of Revolutions Fork` | Remplace par le nom Disposable |
| Launcher | `path` | Chemin absolu du fork | Remplace par le chemin jetable |
| Launcher | `supported_version` | `1.*` | Conserve |
| Launcher | `tags` | `Total Conversion` | Conserve |
| Launcher | `remote_file_id` | Absent | Confirme absent |

## 7. Methode de copie

1. Resolution des chemins absolus et nouveau controle d'absence.
2. Lecture de la liste `git ls-files` depuis le fork.
3. Creation du dossier jetable.
4. Creation, pour chaque chemin relatif suivi, du dossier parent necessaire.
5. Copie du fichier suivi avec `Copy-Item`.
6. Creation du marqueur de securite dans la copie.
7. Transformation limitee des deux descripteurs jetables.
8. Comparaison SHA-256 de chaque fichier suivi source/destination.

Aucun `git clone`, worktree, robocopy, miroir ou copie recursive non filtree
n'a ete utilise.

## 8. Nombre et taille des fichiers copies

- Fichiers suivis copies : **943**.
- Taille source cumulee : **17 324 764 octets**.
- Taille destination des fichiers suivis : **17 324 770 octets**.
- Ecart : **6 octets**, entierement explique par le nom plus long dans le
  `descriptor.mod` jetable.
- Fichiers dans la copie : **944**, soit les 943 fichiers suivis et le marqueur.
- Descripteur launcher externe : un fichier supplementaire hors de la copie.

## 9. Modification du descriptor.mod jetable

Une seule valeur fonctionnelle a change :

```txt
name="1776 Sepoy Functional Test (Disposable)"
```

`supported_version="1.*"` et le tag `Total Conversion` sont conserves. Aucun
champ de dependance, replace path, version ou picture n'existait dans la
source. Aucun `remote_file_id` ou champ `archive` n'est present dans la copie.

## 10. Descripteur launcher jetable

Sa structure est derivee du seul descripteur launcher qui reference exactement
le fork :

```txt
name="1776 Sepoy Functional Test (Disposable)"
path="C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_sepoy_test"
supported_version="1.*"
tags={
    "Total Conversion"
}
```

Le chemin actif ne contient pas `1776_Age_of_Revolutions_fork`.

## 11. Associations Workshop

- `remote_file_id` dans le descripteur interne jetable : 0 occurrence.
- `remote_file_id` dans le descripteur launcher jetable : 0 occurrence.
- Champ `archive` : absent.
- Aucun identifiant Workshop source n'a ete copie ou ajoute.
- Le marqueur contient explicitement `DO NOT PUBLISH`.

## 12. Resultat des hashes

Empreinte agregee initiale des 943 fichiers suivis, construite a partir de
`relative_path|size|sha256` trie par chemin :

`8CCEA5DAEC9F2C94020E6159FBE5D88696DB3097B3DB13F68B255C188E99FD7C`

| Fichier | SHA-256 source | SHA-256 destination | Statut |
|---|---|---|---|
| `common/journal_entries/04_sepoy_mutiny.txt` | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` | Identique | `IDENTICAL` |
| `events/india_events/sepoy_mutiny_events.txt` | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` | Identique | `IDENTICAL` |
| `descriptor.mod` | `93C2AD4C459B1E897A37AA6964EEEFB1C7522D5175F12B43B0BB35020BA82021` | `1921791546626A938E18EEADC765538120325AFA87E0EA309C2C3C6502175B40` | `EXPECTED_DESCRIPTOR_DIFFERENCE` |

Le descripteur launcher source a pour SHA-256
`CD09A66CA07C4DE859341C8B22547B69FD3653E184CF15EAF58AB569223AC60B` ;
le descripteur jetable a pour SHA-256
`FBFDFB891E3E355C05ED996B4A6866475E259081E8196187A2424C9DECCC3733`.

## 13. Resume du manifest

Le manifest contient **945 lignes de donnees** :

- 942 `IDENTICAL` ;
- 1 `EXPECTED_DESCRIPTOR_DIFFERENCE` pour le descripteur interne ;
- 1 creation attendue pour le marqueur jetable ;
- 1 creation attendue pour le descripteur launcher externe ;
- 0 `MISSING` ;
- 0 `UNEXPECTED_DIFFERENCE`.

Les deux creations jetables emploient le statut
`EXPECTED_DESCRIPTOR_DIFFERENCE` et sont distinguees par la note
`DISPOSABLE_CREATION`.

## 14. Absence de .git

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test\.git`
n'existe pas. La copie ne contient ni historique Git, ni refs, ni stash.

## 15. Absence du dossier de recherche

La copie contient zero fichier sous `docs/research/technology/`. Les sept
fichiers non suivis n'ont pas ete inclus par `git ls-files`.

## 16. Absence de harnais

- Fichier `zz_sepoy_functional_test*` : 0.
- Decision de test ajoutee : 0.
- Event de test ajoute : 0.
- Localisation de test ajoutee : 0.
- Victoria 3 et le launcher n'ont pas ete lances.

## 17. Fork inchange

La copie a ete effectuee en lecture seule vis-a-vis des fichiers suivis source.
Les seules creations autorisees dans le fork sont ce rapport et son manifest.
Aucun fichier `common/`, `events/`, `localization/` ou `map_data/` du fork n'a
ete modifie.

Apres copie, le fork compte toujours 943 fichiers suivis pour 17 324 764
octets. Son empreinte agregee recalculee est toujours
`8CCEA5DAEC9F2C94020E6159FBE5D88696DB3097B3DB13F68B255C188E99FD7C`.
Le `descriptor.mod` source conserve aussi son hash initial
`93C2AD4C459B1E897A37AA6964EEEFB1C7522D5175F12B43B0BB35020BA82021`.

## 18. Verification des deux fichiers Sepoy source

| Fichier | Taille avant/apres | SHA-256 avant/apres |
|---|---:|---|
| `common/journal_entries/04_sepoy_mutiny.txt` | 16 040 | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` |
| `events/india_events/sepoy_mutiny_events.txt` | 63 210 | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` |

Les copies destination possedent exactement les memes tailles et hashes.

## 19. Stash MARATH

Le stash suivant reste present, intact et non applique :

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`

Aucun `git stash pop` n'a ete execute.

## 20. Activation future dans un playset separe

Cette procedure n'a pas ete executee dans C1A :

1. ouvrir le launcher lors d'une phase ulterieure ;
2. verifier le nom `1776 Sepoy Functional Test (Disposable)` ;
3. creer un playset exclusivement reserve aux tests Sepoy ;
4. activer la copie jetable dans ce playset ;
5. verifier que le fork principal y est desactive ;
6. ne jamais publier ni televerser cette entree.

## 21. Suppression future

Cette procedure n'a pas ete executee :

1. fermer Victoria 3 et le launcher ;
2. desactiver puis retirer l'entree du playset de test ;
3. verifier textuellement les deux chemins jetables ;
4. supprimer uniquement le dossier
   `1776_Age_of_Revolutions_sepoy_test` ;
5. supprimer uniquement
   `1776_Age_of_Revolutions_sepoy_test.mod` ;
6. verifier que le dossier du fork existe toujours et reste intact.

## 22. Risques restants

- Activer le fork et la copie ensemble produirait des definitions dupliquees.
- Le launcher peut conserver une entree en cache apres suppression ; une
  actualisation manuelle peut etre necessaire.
- La future phase de harnais devra continuer a modifier uniquement la copie.
- Le marqueur cite le chemin source a des fins d'audit ; ce n'est pas un chemin
  launcher actif.

## 23. Verdict

**`READY_FOR_HARNESS`**

La copie est complete, isolee et verifiee. Elle est prete a recevoir un harnais
de test dans une phase ulterieure, sans lancement du jeu pendant C1A.

## 24. Fichiers crees dans le fork

- `docs/reports/hotfix/HOTFIX_5C2E4C1A_SEPOY_DISPOSABLE_COPY_SETUP.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1A_DISPOSABLE_COPY_MANIFEST.csv`

## 25. Chemins crees hors du fork

- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test\`
- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test\DISPOSABLE_SEPOY_TEST_COPY.txt`
- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test.mod`

Les sous-dossiers de la copie sont uniquement ceux necessaires aux 943 chemins
suivis du fork.
