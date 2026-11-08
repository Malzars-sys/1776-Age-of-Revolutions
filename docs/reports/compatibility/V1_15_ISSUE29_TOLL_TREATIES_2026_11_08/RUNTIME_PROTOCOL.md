# Mission 29 — protocole moteur borné

Statut livré : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Aucune ligne de ce protocole n’atteste qu’un essai a eu lieu.

## Version et contexte à consigner

1. Relancer Victoria 3 **1.15.0** avec le mod local contenant les deux empreintes d’`INSTALLATION.json`, puis commencer une **nouvelle partie en 1776**. Noter build, DLC actifs, playset, date de test et pays contrôlés.
2. Conserver les nouveaux logs séparément de `LOG_BEFORE_EXCERPT.txt` et de la baseline de la mission 20. Ne pas utiliser le log encore ouvert avant rechargement comme preuve après correctif.
3. Choisir un contrôleur de détroit **S** possédant une province de détroit dans sa hiérarchie et le contrôle effectif, puis un pays **T** dont les routes sont mesurées comme dépendantes de S. Le Danemark et la Grande-Bretagne sont des candidats à vérifier, pas un couple déjà certifié dans la sauvegarde testée.
4. Vérifier la technologie `commercial_insurance_markets` chez les participants selon les règles d’accès aux articles. Si les pays choisis ne l’ont pas, utiliser une copie de test isolée et consigner tout déblocage de console ; ne pas modifier leur histoire initiale dans le mod.

## Matrice minimale

| Cas | Observation attendue et preuve à relever |
| --- | --- |
| S possède/contrôle le détroit | Les articles peuvent apparaître lorsque leurs conditions et technologies sont remplies ; absence d’erreur de scope dans `visible`/`possible`. |
| Pays sans province/contrôle | La restriction demeure ; aucun article proposé sur un contrôleur inexistant. |
| T demande une exemption à S | S est la source, T le bénéficiaire ; relever séparément les raisons d’acceptation de S et les autres facteurs diplomatiques. |
| S offre une exemption à T | Même droit dirigé, avec la proposition dans l’autre sens ; vérifier les libellés et le pays exempté. |
| T demande l’absence générale de péages | S demeure le contrôleur concerné ; l’article ne doit pas être interprété comme une simple exemption personnelle. |
| Dépendance inférieure à 5 / au moins 5 | Relever la raison « non-dépendance » ou « dépendance » et son signe. Si l’interface ne permet pas de fixer précisément le seuil, consigner les valeurs réellement disponibles plutôt qu’inventer un cas à 5. |
| T sous libre-échange ou variante | L’IA privilégie l’absence générale de péages lorsque son grief est positif. Observer une proposition effective si possible ; un score statique seul ne prouve pas ce comportement. |
| T sans libre-échange | L’exemption personnelle est l’option privilégiée dans les mêmes conditions. |
| Grief nul / positif | Relever la différence de poids de proposition ; ne pas attribuer tous les changements d’acceptation au seul grief. |

Le natif ne permet à l’IA que de **demander** `no_tolls`. Vérifier une offre manuelle seulement si l’interface l’autorise ; son absence parmi les offres IA n’est pas un défaut de cette livraison.

## Effets et non-régression

1. Ratifier chaque article dans des copies de sauvegarde distinctes ; vérifier le réglage et la facturation réels des péages, leurs bénéficiaires et l’étendue de la suppression générale. Comparer avec l’état avant traité.
2. Simuler au moins une mise à jour pertinente pour les effets observés ; noter la durée réellement simulée. Sauvegarder puis recharger : article, droits et paramètres doivent persister sans double application.
3. Vérifier le retrait ou la rupture sur une copie de test, y compris la variation de relations déjà existante. Confirmer que les règles anti-doublon entre les deux articles restent actives.
4. Comparer les nouveaux logs avec la baseline : plus de lien `strait_trade_importance_by` ni d’erreur de scope/type provenant des six anciennes lignes de visibilité/possibilité. Une absence d’erreurs ne suffit pas à certifier les effets.
5. Les trois objectifs de guerre de la mission 32 sont testés par l’autre agent. Si un essai impose un article par la guerre, noter la version de ses modifications et distinguer les responsabilités ; ne pas modifier ses fichiers pour faire passer ce protocole.

Avant Done : joindre les pays et sauvegardes réellement testés, les captures des raisons d’acceptation et paramètres de détroit, les logs, les branches non exercées et l’acceptation explicite du mainteneur. Aucune durée ni observation ne doit être ajoutée si elle n’a pas été relevée.
