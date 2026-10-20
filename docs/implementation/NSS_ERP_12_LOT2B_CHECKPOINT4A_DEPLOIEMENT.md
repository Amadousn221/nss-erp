# NSS ERP — LOT 2B Checkpoint 4A : déploiement sur NSS TEST et clôture

**Référence :** NSS_ERP_12
**Date :** 20 octobre 2026
**Statut :** Checkpoint 4A **terminé et validé** (techniquement et fonctionnellement par le Product Owner, 20 octobre 2026) : déployé sur NSS ERP TEST (base `nss_test`), vérifié techniquement (lecture seule) et validé visuellement (11 validations, §7) ; deux anomalies non bloquantes documentées (§8). Le Checkpoint 5 (pays NSS) reste **en préparation** (`NSS_ERP_13`) : rien n'est chargé
**Prérequis :** `NSS_ERP_10` (code 4A, commit `12b5bda`, CI 24/24), `NSS_ERP_11` (Checkpoint 4B-B, société/langue/fuseau configurés)

---

## 1. Objectif

Déployer sur NSS ERP TEST (et sur lui seul) les corrections UX et filtres métier de `nss_network` fusionnées dans GitHub (`NSS_ERP_10`), avec sauvegarde complète, procédure de retour arrière vérifiable et contrôle de non-régression des services hébergés sur le même VPS (Odoo 19 / MPSénégal, n8n, n8n-connect, Nginx, PostgreSQL système).

Aucun des 10 pays NSS n'a été chargé, aucune donnée métier n'a été créée.

---

## 2. Changements fonctionnels déployés

Détail dans `NSS_ERP_10`. Résumé de ce qui est désormais actif sur `nss_test` :

| Domaine | Changement |
|---|---|
| Contacts | `nss_org_type` et `nss_founding_member` visibles uniquement pour une Société (`invisible="not is_company"`) ; `nss_country_id` reste disponible pour Particulier et Société |
| Coordinatrice (`coordinator_id`) | domaine : personnes physiques déjà rattachées à un pays NSS ; création rapide désactivée |
| Organisation point focal (`focal_org_id`) | domaine : sociétés avec un type d'organisation NSS ; création rapide désactivée |
| Adhésions (`organization_id`) | même domaine ; création rapide désactivée |
| Responsabilités (`partner_id`, `organization_id`) | domaines personne / organisation ; création rapide désactivée |
| Projet (`nss_funder_id`) | domaine : sociétés (le bailleur peut être extérieur au réseau NSS) |
| Adhésion, section Cotisation | `currency_id` visible pour tout utilisateur métier (défaut XOF inchangé) |
| Liste Pays NSS | colonnes visibles par défaut : Pays, Statut NSS, Coordinatrice ; colonnes optionnelles masquées : Date d'entrée, Organisation point focal, Nombre d'organisations |

Aucun changement de schéma PostgreSQL, de droits d'accès (`ir.model.access.csv`), de fichier de données ni de dépendance (`__manifest__.py` inchangé).

---

## 3. Commits de référence

| Élément | Référence |
|---|---|
| Code 4A (PR #12) | `12b5bda` — « fix(nss_network): filtres métier et UX Checkpoint 4A (LOT 2B) » |
| Dernier commit de `main` au déploiement | `8446ad9` (PR #13, Checkpoint 4B-B). `git diff 12b5bda 8446ad9 -- addons` est vide : le code déployé est celui de `12b5bda` |
| CI de référence | GitHub Actions run `36137353815` : Odoo 18 + PostgreSQL 16, 24 tests, 24 réussis, 0 échec (`NSS_ERP_10` §12) |

---

## 4. Procédure réellement exécutée (20 octobre 2026)

Tout a été exécuté en phases séparées, chacune soumise à validation du Product Owner. Aucune autorisation SSH root permanente n'a été accordée.

| Phase | Action | Résultat |
|---|---|---|
| 0 | Relevé de référence en lecture seule (dépôt, Compose, conteneurs, disque, volumes, services externes, certificats, état de la base) | PASS |
| 1 | `git archive` de `addons/nss_network` depuis `HEAD` (18 fichiers), SHA-256, contrôle d'intégrité et de contenu | PASS |
| 2A | Transfert SCP de l'archive dans `/tmp/nss_4a.tar.gz`, SHA-256 local = distant | PASS |
| 2B | Sauvegarde cohérente (arrêt de `nss_test_odoo` seul, ~2 s), vérifications d'intégrité, test de restauration indépendant | PASS |
| 3 (préparation) | Extraction dans un répertoire isolé, vérification des 18 fichiers contre le commit | PASS après correction (§4.1) |
| 3 (exécution) | Remplacement de l'addon, `-u nss_network` sur `nss_test`, redémarrage de `nss_test_odoo`, vérifications | **PASS** |

**Exécution de la phase 3 :** début 11:26:04 UTC, fin 11:26:21 UTC. `nss_test_odoo` arrêté à 11:26:07, redémarré à 11:26:18. **Indisponibilité réelle de NSS TEST : 14 secondes** (de `docker stop` à un `/web/health` à 200), contre 2 à 3 minutes estimées. Le script a tourné détaché de la session SSH (`setsid nohup`), avec alerte à 10 min et arrêt contrôlé (avec retour arrière) seulement à 30 min.

**Enchaînement du déploiement :**
1. pré-contrôles (sauvegarde 6/6, répertoire préparé = commit, addon actif = pré-4A, conteneurs éphémères absents, santé, Compose valide, image identique) ;
2. arrêt de `nss_test_odoo` uniquement ;
3. point de retour immédiat : dump `-Fc` de `nss_test`, comptages, configuration et empreinte d'état PostgreSQL ;
4. remplacement de l'addon par deux `mv` sur le même système de fichiers (l'ancien est conservé hors de `addons/`) ;
5. `docker compose run --rm --no-deps -T nss-odoo odoo -d nss_test -u nss_network --stop-after-init --no-http --max-cron-threads=0` dans un conteneur éphémère, pendant que `nss_test_odoo` est arrêté (aucun second processus Odoo sur la base) ;
6. vérifications **avant** redémarrage : vues en base, empreinte d'état différente de l'état initial, comptages et configuration inchangés, registre Odoo chargé avec le nouveau code (6 domaines métier attendus) ;
7. redémarrage de `nss_test_odoo` ;
8. vérifications fonctionnelles et HTTPS ; 9. non-régression des services externes.

### 4.1 Incidents et corrections en cours de route

| Constat | Traitement |
|---|---|
| **Fins de ligne :** `core.autocrlf=true` sur le poste Windows ; `git archive` a produit des fichiers CRLF (empreintes différentes de celles des blobs du commit). L'addon déployé en septembre était lui aussi en CRLF (18/18). Pas d'effet fonctionnel pour Python/XML. | Normalisation CRLF → LF **dans le répertoire isolé uniquement** ; les 18 fichiers correspondent alors exactement aux empreintes du commit `8446ad9`. L'ancien addon a été conservé octet pour octet. |
| Les domaines de champ ne sont pas stockés par Odoo en base (0 domaine non vide dans `ir_model_fields` sur toute la base) : impossible de les vérifier par SQL | Vérification par chargement du registre dans un conteneur éphémère avant redémarrage (sonde `PROBE dom_*`) |
| Défaut dans mon pré-contrôle du script (comparaison du mauvais répertoire) détecté par le contrôle préalable | Corrigé avant lancement ; pré-contrôles testés réellement sur le VPS avant l'exécution |
| Restauration de l'ancien code ≠ restauration des anciennes vues enregistrées en base | Retour arrière réécrit : code **et** base vérifiés identiques à l'état initial (empreinte d'état PostgreSQL, comptages, configuration, registre chargé avec l'ancien code) avant tout redémarrage ; restauration de la base depuis le dump si nécessaire, via une base temporaire ; incident CRITIQUE déclaré sans masquage en cas d'échec |

**Limite :** le retour arrière complet (restauration de la base) n'a pas été exercé en réel, le déploiement ayant réussi. Seul le chemin « aucune modification effectuée » a été exercé (test des pré-contrôles).

**Empreintes :** archive `nss_4a.tar.gz` : `264492c7103aa0bf296a9d4baf53daa3bc72857b2e20150960a586bb6720d44a` ; script de sauvegarde 2B : `8fd62b282b25577e220d798cad5d134e6de8eb9f7982a31a2c496b4147dc1c5a` ; script de déploiement exécuté : `6278533a7ccda95132421f8c9d5071b2546ce5172724c53f029e42737e004afc`.

---

## 5. Sauvegardes et éléments de retour arrière conservés (rien supprimé)

Tous sur le VPS, droits restreints (`700` / `600`), **non versionnés**, contenant des secrets (configuration) ou des données : ne jamais les copier hors du serveur.

| Élément | Emplacement | Contenu |
|---|---|---|
| Sauvegarde pré-4A (11:05) | `/var/backups/nss-erp/pre-checkpoint4a-20261020-1105/` | `nss_test.dump`, `filestore_nss_test.tar.gz` (`filestore/nss_test`), `addon_nss_network_pre4a.tar.gz`, `nss_conf_secret.tar.gz`, `SHA256SUMS.txt` (6/6 OK au 20/10 à 12:22) |
| Point de retour du déploiement (11:26) | `/var/backups/nss-erp/deploy-4a-20261020_1126/` | `nss_test_preupdate.dump`, comptages, configuration et empreinte d'état avant mise à jour, journal `update.log`, sonde du registre, relevés des services externes avant/après |
| Ancien addon (pré-4A, CRLF d'origine) | `/opt/nss-erp/.pre4a_nss_network` | 18 fichiers, conformes à l'état pré-4A (18/18) |
| Répertoire d'extraction | `/opt/nss-erp/.stage_4a_20261020-1111/` | manifestes (`MANIFEST_8446ad9.sha256`, etc.) ; l'addon qu'il contenait est maintenant l'addon actif |
| Archive transférée | `/tmp/nss_4a.tar.gz` | à supprimer sur ordre du PO |
| Script et journal d'exécution | `/var/backups/nss-erp/phase3-run-20261020_112604.{sh,log}` | trace complète du déploiement |
| Sauvegardes antérieures | `baseline-20260924-1855`, `pre-checkpoint3-20260925-0700`, `post-checkpoint3-20260925-1110`, `pre-checkpoint4b-config-20260926-1042` | inchangées |

Espace disque : 85 Go libres sur 96 Go ; l'ensemble des sauvegardes NSS occupe environ 29 Mo.

---

## 6. Résultats des contrôles techniques

Contrôles exécutés par Claude Code, en lecture seule, le 20 octobre 2026 à 12:22 UTC (environ 55 minutes après le déploiement).

| Contrôle | Résultat |
|---|---|
| Module `nss_network` | `installed`, `18.0.1.0.0`, mis à jour le 20/10/2026 11:26:13 |
| Addon actif | 18/18 fichiers = commit `8446ad9` |
| `-u nss_network` | `Module nss_network loaded in 0.89s, 339 queries` ; « Modules loaded » ; 0 `ERROR`, 0 `CRITICAL`, 0 `Traceback`, 0 avertissement |
| Vues après mise à jour | 3 colonnes `optional="hide"` ; champs organisation conditionnés par `is_company` ; devise sans `group_no_one` |
| Domaines (registre chargé avant redémarrage) | `coordinator_id`, `focal_org_id`, `organization_id` (adhésion), `partner_id` et `organization_id` (responsabilité), `nss_funder_id` : 6/6 conformes |
| Configuration conservée | société `NSS ERP TEST`, pays `SN`, devise `XOF`, admin `fr_FR` / `Africa/Dakar` |
| Données | comptages inchangés : société 1, partenaires 6, utilisateurs 5, vues 681, modules 707 ; 0 ligne dans les 3 tables NSS ; 0 record rule NSS |
| Conteneurs NSS | `nss_test_odoo` Up (démarré 11:26:18, 0 redémarrage), `nss_test_db` Up et healthy ; seul `127.0.0.1:8070` publié |
| HTTPS | `/web/login` et `/web/health` : 200 |
| Journaux Odoo NSS depuis le redémarrage | 0 `ERROR` / `CRITICAL` / `Traceback` |
| Odoo 19 / MPSénégal | `odoo.service` active (démarrage inchangé du 16/10) ; `mpsenegal.com` 303, `www` 301 ; 4 bases clientes inchangées |
| n8n / n8n-connect | 200 / 200, mêmes dates de démarrage |
| Nginx, PostgreSQL système | actifs, mêmes dates de démarrage ; certificats inchangés |

Les relevés avant et après déploiement ne diffèrent que par la date de démarrage de `nss_test_odoo` et les nouveaux dossiers de sauvegarde.

---

## 7. Vérifications visuelles du Product Owner

Les **11 validations visuelles** ci-dessous ont été **communiquées par le Product Owner** (validation manuelle dans l'interface) ; elles ne sont pas des tests automatisés exécutés par Claude Code.

| Fonctionnalité | Résultat |
|---|---|
| Contact Particulier : champs organisationnels masqués | PASS |
| Contact Société : champs organisationnels visibles | PASS |
| Type d'organisation NSS : options accessibles | PASS |
| Pays NSS : trois colonnes affichées initialement | PASS |
| Colonnes supplémentaires activables (Date d'entrée, Organisation point focal, Nombre d'organisations) | PASS |
| Adhésions : devise XOF visible | PASS |
| Organisation : création directe désactivée | PASS |
| Coordinatrice : création directe désactivée | PASS |
| Organisation point focal : création directe désactivée | PASS |
| Interface Odoo en français | PASS |
| Fuseau horaire Afrique/Dakar | PASS |

Conséquence : le fuseau `Africa/Dakar`, resté « à confirmer visuellement » depuis `NSS_ERP_11`, est confirmé.

---

## 8. Anomalies non bloquantes

### A. Le partenaire de la société `NSS ERP TEST` apparaît comme « Particulier »

**Constat (base, lecture seule) :** `res_partner` id 1, lié à la société 1 : `is_company = false`, `type = contact`, actif, sans parent.

**Chronologie établie à partir des sauvegardes successives :**

| Sauvegarde | Nom | `is_company` | Dernière écriture |
|---|---|---|---|
| baseline 24/09 | My Company | **vrai** | 24/09 13:20 (uid 1) |
| pre-checkpoint3 25/09 | My Company | vrai | 24/09 19:50 (uid 1) |
| post-checkpoint3 25/09 11:10 | My Company | vrai | 24/09 19:50 (uid 1) |
| pre-checkpoint4b 26/09 10:42 | My Company | **faux** | **25/09 12:31:40, uid 2 (administrateur)** |
| pre-4A 20/10 | NSS ERP TEST | faux | 26/09 12:23 (uid 1, renommage 4B-B) |

**Analyse :**
- Ce n'est **pas** la configuration initiale : à l'installation, le partenaire de la société était une Société.
- Ce n'est **pas** le Checkpoint 4B-B : l'écriture de 4B-B (26/09) n'a modifié que le nom, et le basculement est antérieur.
- La modification a été faite le **25/09/2026 à 12:31 UTC par l'utilisateur administrateur** (uid 2), c'est-à-dire par une action dans l'interface, entre le contrôle post-Checkpoint 3 (11:10) et la sauvegarde pré-4B. L'action exacte n'est pas tracée (`is_company` n'est pas suivi par le chatter). `[HYPOTHÈSE]` : manipulation lors de l'audit visuel des champs conditionnels du Checkpoint 3, à confirmer par le Product Owner.
- **Conséquences sur NSS Network :** aucune actuellement. Ce partenaire n'a ni `nss_country_id` ni `nss_org_type` ; il n'apparaît donc ni dans les sélecteurs de coordinatrice (personne rattachée à un pays NSS) ni d'organisation (société avec type NSS). Hors NSS Network, un « Particulier » comme identité de société peut gêner l'affichage ou les futurs documents officiels.
- **Correction recommandée (non appliquée) :** rebasculer ce contact en **Société** depuis Contacts, par l'interface. **Priorité : basse**, à traiter avant tout document officiel ou avant l'import des organisations. Ne pas utiliser ce partenaire comme organisation NSS.

### B. Adresse de l'administrateur : `admin@example.com`

**Constat :** utilisateur `admin` (id 2, seul utilisateur interne actif), partenaire `Administrator`, courriel `admin@example.com` (valeur d'origine d'Odoo). Aucun serveur de courriel sortant n'est configuré (`ir_mail_server` : 0). `web.base.url` vaut `http://erp-test.wasafrica.org` (http et non https).

**Usage réel / effets observés :** 6 courriels sont en état `exception` (« 111 Connection refused »), tous adressés à cette adresse : 2 résumés périodiques (24 et 25/09, `Digest Emails` est désormais inactif) et 4 notifications « Security Update: Password Changed » (20/10 de 10:17 à 10:31, correspondant aux réinitialisations de mot de passe de l'administrateur). **Aucun courriel n'a quitté le serveur** : rien n'a été livré à `example.com`.

**Conséquences possibles :**
- aucune notification Odoo (chatter, activités, alertes de sécurité) n'atteint un humain ;
- la réinitialisation de mot de passe par courriel est impossible (le mot de passe d'`admin` ne peut être récupéré que via le serveur) ;
- chaque notification supplémentaire (suivis, tracking de `nss_network`) ajoute un courriel en `exception` ;
- les liens générés dans de futurs courriels seraient en `http`.

**Remplacement ultérieur (non appliqué) :** décider d'abord d'une boîte NSS dédiée, puis modifier le courriel de l'utilisateur dans Odoo (Réglages → Utilisateurs, ou Préférences) et, séparément, configurer le courrier sortant. Ne pas configurer de serveur de messagerie avant décision du PO. **Priorité : moyenne** (haute dès qu'un second utilisateur ou un usage réel démarre). Corriger aussi `web.base.url` en `https://erp-test.wasafrica.org` à ce moment-là.

---

## 9. Constats complémentaires

| Constat | Priorité | Action proposée |
|---|---|---|
| Absence de `.gitattributes` avec `core.autocrlf=true` sur le poste Windows : les archives `git archive` sortent en CRLF | Moyenne | Ajouter `* text=auto eol=lf` (et fichiers texte Odoo) dans un commit dédié, sur décision PO |
| `README.md` (« phase de recherche… aucune installation ») et `CLAUDE.md` §2 (« interdiction actuelle ») décrivent un état antérieur | Moyenne | `README.md` et `addons/README.md` actualisés par ce document ; `CLAUDE.md` non modifié (règles de fonctionnement), à actualiser sur décision PO |
| Doc `NSS_ERP_01` : « 14 organisations » (ERP-Q03, ERP-Q11) et « 13 organisations » (§10, conclusion) | Basse | Harmoniser à 13 (13 organisations identifiables dans la brochure 2019) |

---

## 10. Décisions de validation

| Décision | Statut |
|---|---|
| Déploiement du Checkpoint 4A sur NSS TEST, interruption temporaire acceptée | Validé par le PO |
| Checkpoint 4A, après examen du rapport final du 20/10/2026 | **Validé techniquement et fonctionnellement par le PO** ; clôture documentaire dans GitHub autorisée |
| Vérifications visuelles 4A (§7) | Validées par le PO |
| Anomalies A et B : non bloquantes, à traiter ultérieurement, sans modification maintenant | Décision du PO |
| Chargement des 10 pays NSS | **Non engagé** ; préparé dans `NSS_ERP_13`, en attente de validation PO |

---

## 11. Limites et actions restantes

- Le retour arrière complet n'a pas été exercé en réel (§4.1).
- Les tests automatisés `nss_network` n'ont **pas** été relancés sur `nss_test` (volontairement, pour ne pas écrire dans la base). La validation automatisée reste celle de la CI (24/24, run `36137353815`).
- Aucun test de charge ni test multi-utilisateurs (un seul utilisateur interne).
- Nettoyage à faire **sur ordre du PO** : `/tmp/nss_4a.tar.gz`, `/opt/nss-erp/.stage_4a_20261020-1111`, `/var/backups/nss-erp/phase3-run-*` ; conserver `.pre4a_nss_network` et les sauvegardes tant que le 4A n'est pas figé.
- Record rules par pays : toujours non conçues (`NSS_ERP_08` §10).
- Anomalies A et B (§8) et constats §9.

---

## 12. Verdict

**Checkpoint 4A : TERMINÉ (validé par le PO le 20 octobre 2026).** Les preuves disponibles (contrôles en lecture seule du 20/10/2026, journaux du déploiement, comparaison avant/après des services externes, vérifications visuelles du PO) confirment le déploiement et la non-régression. Réserves : retour arrière complet non exercé en réel, tests automatisés non rejoués sur `nss_test`.

---

*Fin du document NSS_ERP_12_LOT2B_CHECKPOINT4A_DEPLOIEMENT.md*
