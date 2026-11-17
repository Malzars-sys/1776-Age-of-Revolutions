# Mission 39 — essais groupés et déclenchement direct

Livraison locale du 11 novembre 2026, `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.
Les commandes ci-dessous sont relues contre les scripts actuels, pas exécutées
dans le moteur par l'agent. Le reçu `FINAL_VALIDATION.json` identifie les données
à tester. Les anciennes acceptations restent acquises dans leur périmètre.

## Exécuter un bloc sans attendre l'événement

Lancer une nouvelle partie en 1776 avec le mod de travail et le mode debug.
Faire une sauvegarde de test avant les manipulations. Dans la console, ouvrir
`explorer`, sélectionner **Countries**, le pays indiqué, puis **Script Runner >
Effect**. Coller le bloc seul, sans ajouter `effect = { ... }`. Ouvrir le journal
pendant la pause, puis avancer d'un jour lorsque l'essai demande une évaluation.

`add_journal_entry` contourne les conditions normales d'activation et exécute
les effets immédiats. Il vérifie l'affichage et prépare l'essai ; il ne prouve
pas le déclenchement naturel. Ne pas ajouter toutes les entrées à un même pays.
Les entrées à cible ou à scopes enregistrés doivent garder leur préparation
spécifique. Le catalogue complet et les consommateurs sources sont joints.

## 1. France : fiche active puis échec

Dans **France**, si l'entrée n'est pas déjà présente :

```text
if = {
    limit = { NOT = { has_journal_entry = je_fr_rev_summon_estates } }
    add_journal_entry = { type = je_fr_rev_summon_estates }
}
```

Ouvrir les États généraux : critères, effets et échéance de réussite/échec
doivent être lisibles. Sur une copie distincte, provoquer l'échec :

```text
je:je_fr_rev_summon_estates = {
    set_bar_progress = { name = je_estates_reform_bar value = 0 }
}
```

Après évaluation, l'événement `french_revolution_mod_events.14` doit suivre.
Sauvegarder/recharger : pas de deuxième conclusion ni de nouvel effet répété.

## 2. Réussite simple et continuation

Dans une autre copie avec **France**, activer les Corn Laws, puis les conclure :

```text
if = {
    limit = { NOT = { has_journal_entry = je_corn_laws } }
    add_journal_entry = { type = je_corn_laws }
}
```

Ouvrir d'abord la fiche, puis exécuter séparément :

```text
activate_law = { law = law_type:law_free_trade }
```

Après évaluation, l'événement `corn_laws.1` et la variable `corn_laws_abolished`
sont attendus. Recharger après conclusion ne doit pas doubler les effets.
Cette loi est modifiée uniquement dans la copie de test.

## 3. Été rouge : ancien aperçu rétabli en FR et EN

Dans une copie avec **France** :

```text
if = {
    limit = { NOT = { has_journal_entry = je_red_summer } }
    add_journal_entry = { type = je_red_summer }
}
```

Ouvrir l'issue de réussite : les voies libérale et radicale doivent être
présentées avec leurs événements et effets, sans `red_summer_on_complete_tt`
brut. Refaire l'affichage en anglais. Ce test n'atteste pas la réussite des
deux voies : leurs prédicats et événements demeurent ceux du mod.

## 4. Commune : barre et boutons raccordés

Sur une **copie distincte**, dans France, ce montage sert uniquement au mouvement
de la barre ; il ne crée pas une Commune historiquement préparée :

```text
set_global_variable = { name = paris_commune_progress_var value = 50 }
set_variable = paris_commune_fra_perspective
if = {
    limit = { NOT = { has_journal_entry = je_the_paris_commune_france } }
    add_journal_entry = { type = je_the_paris_commune_france }
}
```

Le bouton de répression doit enlever 10 points. Pour voir l'autre bouton dans
cette copie :

```text
remove_variable = paris_commune_fra_perspective
set_variable = paris_commune_prc_perspective
```

Le bouton de concessions doit ajouter 10 points. Recharger : compteur conservé.
Ne pas ajouter `je_paris_commune`, absent volontairement. Pour les conclusions
à 0/100 et leurs événements, utiliser une Commune réellement préparée avec la
France et les Communards ; le montage de barre ne certifie pas ces événements.

## 5. Familles avancées et exceptions

- **Plan quinquennal natif**, dans une copie d'un pays jouable :
  `add_journal_entry = { type = je_five_year_plan }`. L'initialisation du plan
  doit fournir les objectifs et les boutons ; ne pas confondre avec
  `je_5_year_plan`. Tester la continuation et le rechargement dans une situation
  ayant les conditions politiques requises, pas en déduire une activation
  naturelle de la seule commande.
- **Maroc**, si l'entrée n'est pas active :
  `add_journal_entry = { type = je_lands_of_anarchy }`. Vérifier les trois
  barres et critères ; préserver l'acceptation précédente des modificateurs.
- **Expiration**, **invalidation**, **issues concurrentes**, **effets pour tous
  les pays impliqués**, **mariage Meiji** et **DLC activé/désactivé** : conserver
  le protocole R4 et le protocole de la revue précédente, cités dans le rapport.
  Aucun faux effet de console pour raccourcir les délais n'est proposé.
  Un saut de date seul ou l'appel direct de l'événement final ne valide pas
  l'expiration réelle d'un journal. Les cas non essayés restent non testés.
- Administration coloniale, Nouvel impérialisme et dummy espagnol n'ont pas
  d'issue générale authored : leur absence est normale, pas une migration omise.

## Retour groupé

Indiquer les essais passés et les éventuels noms/critères manquants. L'agent
n'a acquis aucune nouvelle validation moteur pendant cette passe. Une clé
brute, une conclusion répétée ou un bouton sans effet demande la capture et le
nom du journal. Les détails de sauvegarde et de date restent facultatifs.

Pour les nouveaux logs, distinguer le démarrage et les actions de test.
Les anciens logs capturés dans `logs_before/` n'identifient pas cette livraison
du mod ; ils ne servent pas de référence moteur réussie ou de mesure avant/après.
