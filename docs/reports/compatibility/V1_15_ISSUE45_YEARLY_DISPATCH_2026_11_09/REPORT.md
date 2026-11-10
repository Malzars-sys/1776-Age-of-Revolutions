# Mission 45 — Effets annuels et déclaration additive

9 novembre 2026. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Installation canonique consultée : Victoria 3 **1.15.0**. Aucun résultat moteur ni acceptation humaine nouvelle.

## Problème et correction

Le même hook `on_yearly_pulse` déclarait deux blocs `effect` : la branche de Manille dans `common/on_actions/00_code_on_actions.txt` et le parcours japonais dans `common/on_actions/phase1_japan_tenpo_on_actions.txt`. Le contrat natif `_on_actions.md`, capturé ici, autorise plusieurs fragments pour un on_action mais interdit plusieurs blocs d'effet ou de déclencheur sur ce même nom. Il recommande de chaîner une sous-action pour ajouter un effet.

Le lot ne modifie que le fichier japonais :

```text
on_yearly_pulse = {
    on_actions = { aor1776_phase1_japan_yearly_pulse }
}
aor1776_phase1_japan_yearly_pulse = {
    effect = { ...bloc japonais d'origine intégral... }
}
```

Ce schéma illustre le raccord ; le fichier installé contient le véritable bloc complet. Le hook conserve son unique effet principal et appelle la sous-action japonaise, qui possède son propre effet unique. Le fichier principal et la branche de Manille sont byte-identiques. Le bloc d'effet japonais est conservé textuellement, y compris pays, fenêtres de dates, variables, lois, garde DLC et six appels d'événement.

Il s'agit d'une incompatibilité de déclaration confirmée par le contrat, et non d'une panne moteur reproduite : aucune priorité effective de chargement ou exécution « dernier bloc gagnant » n'est prétendue observée. Les effets distincts ne dépendent pas d'un ordre d'exécution nouvellement imposé.

## Vérifications effectives

- Avant : **321 on_actions effectifs**, **1 132 références de listes/fallback**, six cibles manquantes et un conflit de blocs d'effet.
- Contrôle natif séparé : **287 on_actions**, **1 095 références**, aucune cible manquante ou collision dans ce modèle.
- Candidat et installation réelle : **15/15 contrôles**. **Quatre témoins négatifs** détectent le retour au double effet, une liaison enfant cassée, une date japonaise altérée et une modification du fichier principal. **Un témoin positif** confirme que deux fragments additifs valides ne sont pas traités comme une collision.
- Après : **322 on_actions**, **1 133 références** ; la seule liaison supplémentaire pointe vers le nouvel enfant présent. Zéro conflit de blocs `effect`/`trigger` et zéro erreur de parsing dans le périmètre inventorié.
- Les six événements japonais, les deux lois et le journal Tenpō nommés par ce bloc possèdent leurs fournisseurs existants ; leurs fichiers ne sont pas réécrits.
- Conservation : sur **2 968 fichiers de fonctionnement préexistants**, seul le fichier japonais autorisé diffère, exactement selon le candidat. Aucun fichier de fonctionnement ajouté ; entrées des audits, contrat natif, index et HEAD préservés. Aucun Git write, changement du vanilla ou publication.

Les poids aléatoires, chances, délais et entrées `0` sans événement sont traités comme métadonnées du format, pas comme des identifiants manquants. Le modèle rassemble les fragments d'on_action, conformément au contrat ; il ne simule ni tirage, ni conditions, ni expansions dynamiques, ni cycles d'appel ou exécution des effets. Les appels `trigger_event` directs relèvent du contrôle distinct 44.

## Dette conservée hors du correctif

Les six références suivantes existaient avant et restent explicitement visibles après ; elles ne sont pas effacées pour obtenir un résultat global vert :

| Appelant | Cible absente | Source effective |
| --- | --- | --- |
| `on_yearly_events` | `marx_events.3` | vanilla `common/on_actions/00_on_actions_yearly.txt:246` |
| `japan_yearly_events` | `japan_events.32` | même fichier, ligne 607 |
| `japan_yearly_events` | `japan_events.33` | même fichier, ligne 608 |
| `japan_yearly_events` | `japan_events.34` | même fichier, ligne 609 |
| `japan_yearly_events` | `japan_events.35` | même fichier, ligne 610 |
| `on_yearly_pulse_country` | `on_memento_mori` | mod `common/on_actions/00_code_on_actions.txt:1718` |

Leur qualification exige un lot séparé. En particulier, ne pas ressusciter un ancien handler de mortalité sans comparaison avec le fonctionnement 1.15, ni réactiver automatiquement des événements historiques. Le résultat est donc **PASS_SCOPED_STATIC_ONLY**, tandis que l'inventaire global conserve des constats.

## Preuves et reproduction

Lire `CHANGES.patch`, `NATIVE_ON_ACTIONS_CONTRACT.md`, les versions avant/candidat, `INVENTORY_BEFORE.json`, `NATIVE_CONTROL.json`, `CANDIDATE_VALIDATION.json`, `LIVE_VALIDATION.json`, les dépendances, le reçu d'installation et `SOURCE_PROTECTION.json`.

```text
python -B tools/compatibility/issue45_yearly_dispatch_audit.py --controls --output docs/reports/compatibility/V1_15_ISSUE45_YEARLY_DISPATCH_2026_11_09/RECHECK_NEW.json
```

Choisir un nom neuf ; le validateur n'installe aucun fichier et conserve ses témoins en mémoire. Une invocation préparatoire PowerShell a échoué sur une parenthèse avant toute action ; aucun résultat ni changement n'en a été déduit.

Le tableau a été réconcilié : les missions 42/43/44 sont réellement en **In review** ; la mission 45 a été réservée **In progress**. Les reçus de statut et captures ultérieurs attestent son passage en revue sans clôture ou validation moteur. Les anciennes observations de session déconnectée sont conservées comme historique.
