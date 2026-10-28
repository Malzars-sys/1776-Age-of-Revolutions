# ColGrep — mesure de cette passe

Un appel local à `C:/Users/simeo/.cargo/bin/colgrep.exe --agent`, dépôt `.` :

> Read-only localization: find existing research and current implementation for the northern New Spain frontier (California missions, Tubac, Santa Fe, Texas presidios) and Russian America in January 1776. Locate relevant country histories, state owners and naming definitions for Russian-American Company. Return at most eight file paths with useful line ranges. No edits or apply scripts.

L'accès au verrou de l'index local a été autorisé pour cette exécution. **Retour terminé, code 0, 272,6506085 secondes** mesurées autour de la commande complète. Mode agent local configuré par les instructions installées pour ColGrep-Agent-2B ; aucun modèle, paramètre d'intégration ou index intégral remplacé. Le temps GPU/inférence et les tokens propres au modèle ne sont pas isolés par cette mesure.

Pistes obtenues et vérifiées :

- `common/history/countries/rus - russia.txt:1–80` : fichier et bloc de création de compagnie vérifiés, utiles mais déjà trouvés par identifiant exact.
- `events/alaska_events.txt:1–310` : fichier réel, contenu de vente ultérieure ; ne résout pas la localisation de 1776 et n'est pas modifié.
- `docs/reports/map/NORTH_AMERICA_1776/COLONIES-01/FRONTIER/patch/common/country_definitions/00_countries.txt:1476–1886` : archive réelle, passage indien Bundelkhand/Gwalior, **faux positif pour la mission**, écarté.

Les dossiers R8 et les RGB ont exigé recherche ciblée, lecture et validation propres à Codex. Les appels `rg` n'ont pas été instrumentés individuellement ; pas de total exact reconstitué artificiellement. Pas de compteur de tokens Codex par mission accessible ici, et pas de comparaison témoin fiable. **Aucune économie exacte de quota ni gain de temps démontrés pour cet appel** ; sa pertinence est partielle et son coût temporel élevé. Aucun appel redondant n'a été ajouté pour fabriquer une comparaison.
