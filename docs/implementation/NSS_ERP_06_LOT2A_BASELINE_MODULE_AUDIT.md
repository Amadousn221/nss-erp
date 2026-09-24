# NSS ERP — LOT 2A Baseline & Module Audit

**Référence :** NSS_ERP_06
**Date :** 24 septembre 2026
**Statut :** audit documentaire + sauvegarde baseline — **aucune installation fonctionnelle réalisée**
**Prérequis :** LOT 1B clôturé et fusionné dans `main` (`NSS_ERP_05_LOT1B_DEPLOIEMENT_TEST.md`)

---

## 1. État avant intervention

Avant toute action de ce lot, l'environnement NSS ERP TEST était stable et conforme à l'état laissé par le LOT 1B :

| Élément | État constaté |
|---|---|
| `nss_test_odoo` | RUNNING |
| `nss_test_db` | HEALTHY |
| `https://erp-test.wasafrica.org/web/login` | HTTP 200 |
| Odoo 19 (existant) | actif, inchangé |
| n8n / n8n-connect | actifs, inchangés |
| PostgreSQL système | actif, inchangé |
| Nginx | actif, inchangé |

Aucune anomalie détectée avant démarrage de la sauvegarde baseline.

---

## 2. Backup baseline

Dossier créé sur le VPS : `/var/backups/nss-erp/baseline-20260924-1855/` (permissions `700`, `root:root`).

Pour garantir une baseline cohérente, **seul `nss_test_odoo` a été arrêté temporairement** (`docker compose stop nss-odoo`). `nss_test_db`, Odoo 19, n8n, PostgreSQL système et Nginx sont restés actifs sans interruption.

| Fichier | Contenu | Taille | Permissions |
|---|---|---|---|
| `nss_test_baseline.dump` | `pg_dump -Fc` de la base `nss_test`, exécuté depuis le conteneur `nss-db` | 1 428 783 octets | `600` |
| `nss_test_filestore.tar.gz` | Filestore Odoo (`filestore/` uniquement, `sessions/` exclu) depuis le volume `nss_odoo_data` | 1 711 644 octets | `600` |
| `BASELINE_MANIFEST.txt` | Métadonnées de la baseline (sans secret) | 1 972 octets | `600` |

Aucun `POSTGRES_PASSWORD` n'a été affiché à aucun moment (le dump est exécuté à l'intérieur du conteneur, via le socket local, sans authentification par mot de passe explicite).

`nss_test_odoo` a été relancé immédiatement après la sauvegarde (`docker compose start nss-odoo`).

---

## 3. Vérification intégrité backup

- **Dump PostgreSQL :** validé avec `pg_restore --list` (mode liste uniquement, aucune restauration effectuée). Résultat : archive `CUSTOM` lisible, **2312 entrées TOC**, dump PostgreSQL 16.15 cohérent avec la version du conteneur `nss-db`.
- **Filestore :** validé avec `tar -tzf`. Résultat : archive lisible, **61 entrées**, contenu conforme (`filestore/nss_test/...`), aucune entrée `sessions/`.
- **Aucune restauration n'a été effectuée**, conformément à la consigne.

Après la sauvegarde, l'environnement a été revérifié sain :

| Vérification | Résultat |
|---|---|
| `https://erp-test.wasafrica.org/web/login` | HTTP 200 |
| Port `8070` | `127.0.0.1:8070` uniquement |
| Odoo 19 | actif, inchangé |
| n8n / n8n-connect | actifs, inchangés |
| PostgreSQL système | actif, inchangé |
| Nginx | actif, inchangé |

---

## 4. Copie locale hors Git

Le répertoire `local-backups/` a été créé à la racine du dépôt et ajouté à `.gitignore` (`/local-backups/`). Les trois fichiers de la baseline ont été copiés via `scp` depuis le VPS vers `local-backups/baseline-20260924-1855/`.

**Comparaison SHA256 (VPS vs local) :**

| Fichier | SHA256 | Identique |
|---|---|---|
| `nss_test_baseline.dump` | `d487935c2852dc80513133e330175f6628606c8167d9b7bfe8a5ad39f4e61c1c` | ✅ OUI |
| `nss_test_filestore.tar.gz` | `6ae02dceab64e2c39c82ff96d6229ccc4839b74ed87739deea638501369b8118` | ✅ OUI |

`local-backups/` n'est ni commité ni poussé sur GitHub (vérifié via `git status` avant commit — voir section 16).

---

## 5. Modules Odoo natifs (Community 18.0)

Établi à partir de `NSS_ERP_01` (§26 MVP) et `NSS_ERP_02` (§5 mapping, §21), et vérifié directement dans le dépôt officiel `odoo/odoo` (branche `18.0`) le 24 septembre 2026.

| Module technique | Fonction | Dépendances (manifest) | Natif Community 18 | Nécessité MVP | Ordre futur d'installation |
|---|---|---|---|---|---|
| `base` | Utilisateurs, groupes, record rules (`ir.rule`), pays (`res.country`), socle technique | — (module racine) | OUI | OUI | 1 — toujours présent (socle) |
| `contacts` | Annuaire organisations et personnes (`res.partner`) | `base`, `mail` | OUI (confirmé présent dans `addons/`) | OUI | 2 |
| `mail` | Chatter, pièces jointes, notifications, log des modifications | `base` | OUI (confirmé présent dans `addons/`) | OUI | 2 (avec `contacts`) |
| `project` | Projets (`project.project`) et tâches/activités (`project.task`) | `mail`, `portal`, `web` | OUI (confirmé présent dans `addons/`) | OUI | 3 |
| `account` | Comptabilité transactionnelle : plan comptable, journaux, écritures, factures, paiements, multi-devise | `base`, `mail`, `analytic` (entre autres) | OUI (confirmé présent dans `addons/`) | OUI (décision PO ERP-Q24) | 4 |
| `analytic` | Comptabilité analytique multi-dimensions (plans et comptes analytiques : Pays, Projet, Bailleur) | `base` | OUI (confirmé présent dans `addons/`) | OUI | 4 (avec `account`) |

**Constat :** les 6 modules figurent bien dans `odoo/odoo` branche `18.0` à la date de l'audit — aucun écart avec ce que prévoit `NSS_ERP_02`. Aucun de ces modules n'a été installé sur `nss_test` dans ce lot.

---

## 6. Modules OCA

Audité exclusivement par lecture des dépôts officiels OCA via l'API GitHub en lecture seule (branches, manifests, activité). **Aucun clone, aucun montage d'addon, aucune exécution de code tiers sur le VPS.**

| Module OCA | Dépôt | Branche 18.0 | Nom technique | Licence | Dépendances (manifest) | Activité récente | Maturité TEST | Recommandation |
|---|---|---|---|---|---|---|---|---|
| Budgets | `OCA/account-budgeting` | ✅ OUI | `account_budget_oca` (v18.0.1.2.0) | LGPL-3 | `account` | Dernier commit 18.0 : 26 juillet 2026 ; dépôt actif (32 issues ouvertes, 44 ★) | Bonne — dépendance unique (`account`), pas de chaîne complexe | **INSTALLER PLUS TARD** (Lot 2B/2C, après socle `account`) |
| Rapports financiers | `OCA/account-financial-reporting` | ✅ OUI | `account_financial_report` (v18.0.1.4.26) | **AGPL-3** (⚠️ à noter, différent de LGPL) | `account`, `date_range` (OCA `server-ux`), `report_xlsx` (OCA `reporting-engine`) | Dernier commit 18.0 : 23 septembre 2026 (veille de l'audit) ; dépôt très actif (47 issues, 313 ★) | Bonne — module mature (v1.4.x), mais 2 dépendances OCA supplémentaires à installer | **INSTALLER PLUS TARD** — nécessite d'abord de valider `date_range` et `report_xlsx` (branches 18.0 confirmées disponibles) |
| Rapprochement bancaire | `OCA/account-reconcile` | ✅ OUI | `account_reconcile_oca` (v18.0.1.1.14) | **AGPL-3** | `account_statement_base`, `account_reconcile_model_oca` (même dépôt), `base_sparse_field` (natif Odoo, confirmé présent) | Dernier commit 18.0 : 8 septembre 2026 ; dépôt actif (54 issues, 198 ★) | Moyenne — chaîne de 3 dépendances internes au dépôt, module récent en réécriture (post_init_hook, JS widgets) | **À TESTER** avant toute décision — ne pas installer avant validation en TEST isolé |
| Rapprochement (modèles) | `OCA/account-reconcile` | ✅ OUI | `account_reconcile_model_oca` (v18.0.1.1.3) | LGPL-3 | `account` (`excludes: account_accountant`) | Idem ci-dessus | Bonne — dépendance unique, `excludes` bien défini contre le module Enterprise | **À TESTER** avec `account_reconcile_oca` (dépendance directe) |

**Correction par rapport à `NSS_ERP_02` §20 :** les noms de modules `account_reconcile_oca` et `account_reconcile_model_oca` cités dans l'architecture sont confirmés **exacts** (aucune correction de nom nécessaire) — mais leur maturité doit être testée avant tout usage, et non simplement « à tester » comme mentionné : ils dépendent l'un de l'autre et d'un troisième module du même dépôt (`account_statement_base`).

**Point d'attention nouveau (non documenté dans `NSS_ERP_02`) :** `account_financial_report` et `account_reconcile_oca`/`account_reconcile_model_oca` sont sous licence **AGPL-3**, plus contraignante que la LGPL-3 utilisée par `account_budget_oca` et `account_reconcile_model_oca`. Cela n'empêche pas leur usage pour un ERP interne non redistribué, mais doit être noté pour toute décision de distribution future de modules NSS qui en dépendraient. `[À VALIDER PO — non bloquant]`.

Aucun de ces modules n'a été cloné, monté ou installé sur le VPS.

---

## 7. Dépendances

**Dépendances critiques identifiées pour la suite du projet :**

1. `account_financial_report` (OCA) nécessite **deux modules OCA supplémentaires** non mentionnés explicitement comme prérequis dans `NSS_ERP_02` §20 : `date_range` (`OCA/server-ux`, branche 18.0 confirmée disponible) et `report_xlsx` (`OCA/reporting-engine`, branche 18.0 confirmée disponible).
2. `account_reconcile_oca` dépend de deux autres modules du même dépôt (`account_statement_base`, `account_reconcile_model_oca`) et d'un module technique natif (`base_sparse_field`, confirmé présent nativement).
3. `account_budget_oca` a une dépendance unique et directe (`account`) — le module le moins risqué des quatre.
4. Aucune dépendance Python externe (hors stack Odoo standard) n'a été identifiée dans les manifests consultés.

---

## 8. Localisation comptable

**Ce qui est déjà décidé (`NSS_ERP_01` ERP-Q24, `NSS_ERP_02` §10/§16) :**
- Comptabilité complète/officielle requise (pas seulement suivi recettes/dépenses) — **VALIDÉ PO**.
- Architecture mono-société centralisée pour le pilote (Option A) — **recommandée**, hypothèse SYSCOHADA à confirmer.
- Siège NSS au Sénégal → hypothèse `l10n_sn` / SYSCOHADA.

**Vérification technique effectuée dans ce lot (nouveau) :**

Le module natif `l10n_syscohada` (« OHADA - Accounting », licence LGPL-3, dépendance : `account`) a été inspecté directement dans `odoo/odoo` branche `18.0`. Sa description couvre nommément les pays OHADA suivants : Bénin, Burkina Faso, Cameroun, RCA, Comores, Congo, **Côte d'Ivoire**, Gabon, **Guinée**, **Guinée-Bissau**, Guinée équatoriale, **Mali**, Niger, RDC, **Sénégal**, Tchad, **Togo**.

Sur les **10 pays NSS**, **8 sont couverts par le référentiel SYSCOHADA/OHADA** : Bénin, Burkina Faso, Côte d'Ivoire, Guinée, Guinée-Bissau, Mali, Sénégal, Togo. **2 pays ne sont pas couverts** : **Ghana** et **Gambie** (référentiels anglophones non-OHADA), ce qui confirme exactement le constat déjà fait dans `NSS_ERP_02` §16 (« Ghana et Gambie, référentiels anglophones non-OHADA »).

Le module `l10n_sn` (« Sénégal - Accounting ») dépend de `l10n_syscohada` + `account`, est natif Community 18.0, licence LGPL-3, et ajoute uniquement les taxes spécifiques au Sénégal par-dessus le plan OHADA commun.

**Décidé (technique) :** le socle SYSCOHADA existe nativement en Odoo 18 Community et couvre 8/10 pays NSS sans développement spécifique.

**Reste `[POINT_A_VALIDER_PO]` :**
- Société pilote / entité comptable exacte à créer dans Odoo (nom, adresse, régime).
- Devise de base (hypothèse XOF — `NSS_ERP_02` ARCH-09, non confirmée).
- Exercice fiscal (hypothèse année civile — ARCH-04, non confirmée).
- Validation par la fonction comptable NSS que `l10n_syscohada`/`l10n_sn` couvrent réellement les obligations NSS (au-delà de la simple présence technique du module).
- Traitement Ghana/Gambie : aucune localisation Odoo native identifiée dans ce lot pour ces deux pays — à traiter en analytique uniquement pour le pilote (pas de développement spécifique envisagé au MVP), sauf nouvelle décision PO.

---

## 9. Module spécifique `nss_network`

**`[CONFLIT DE SOURCES]`** entre deux documents :

- `NSS_ERP_02` §1 (Executive Summary) mentionne **un module NSS unique : `nss_network`**.
- `NSS_ERP_02` §21 (« Développements NSS minimums », section corrigée lors du contrôle technique ChatGPT) recommande au contraire **trois modules séparés** : `nss_core` (obligatoire), `nss_project` (extension), `nss_account` (si nécessaire) — et déconseille explicitement un module unique combinant `contacts` + `project` + `account`.

L'instruction explicite et datée du Product Owner pour ce LOT 2A (24 septembre 2026) tranche ce conflit pour la suite immédiate du projet : **le module spécifique retenu est `nss_network`**, et aucun autre module (`nss_core`, `nss_project`, etc.) ne doit être créé sans nouvelle décision PO. Conformément à la hiérarchie des sources de vérité (`CLAUDE.md` §3), cette décision explicite et récente du PO prévaut sur la recommandation documentaire antérieure. Ce conflit doit rester visible et n'est pas résolu silencieusement.

**Aucun code n'a été écrit pour `nss_network` dans ce lot** — audit de périmètre uniquement, à partir de `NSS_ERP_02` §6/§7/§8 :

| Domaine prévu | Modèle Odoo envisagé | Dépendances envisagées |
|---|---|---|
| Pays NSS (statut, dates, coordination) | `nss.country.membership` | `res.country` (lien, pas d'extension directe) |
| Coordination nationale | Champs sur `nss.country.membership` (coordinatrice, org. point focal) | `res.partner` |
| Organisations membres | Extensions sur `res.partner` (`nss_country_id`, `nss_org_type`, `nss_founding_member`) | `contacts` |
| Adhésions | `nss.membership` | `res.partner` |
| Statistiques membres déclarées | Champs sur `nss.membership` (source unique, pas de duplication) | — |
| Historique de responsabilités | `nss.responsibility.history` | `res.partner`, `nss.country.membership` |
| Extensions Contacts | Champs additionnels sur `res.partner` | `contacts` |
| Extensions Project | Champs sur `project.project` (pays, bailleur) et `project.task` (type activité, lieu) | `project` |

**Compatibilité Odoo 18 après déploiement réel :** la version effectivement installée sur `nss_test` (**Odoo 18.0.1.3**, vérifiée aux Checkpoints 3–4 du LOT 1B) correspond à la version cible de `NSS_ERP_02`. Les modèles natifs utilisés comme base (`res.partner`, `res.country`, `project.project`, `project.task`) sont bien présents dans cette version (section 5 ci-dessus). Aucune incompatibilité identifiée à ce stade — **sous réserve d'une revue de code réelle au moment du développement**, non effectuée dans ce lot.

Aucune décision métier n'a été changée dans cette section.

---

## 10. Réseau des 10 pays

Confirmé à partir de `NSS_ERP_00` (§3) et `NSS_ERP_01` (§5.1), tous deux marqués **[VALIDÉ PO — décision du 23 septembre 2026]** :

1. Bénin (BJ)
2. Burkina Faso (BF)
3. Côte d'Ivoire (CI)
4. Gambie (GM)
5. Ghana (GH)
6. Guinée (GN)
7. Guinée-Bissau (GW)
8. Mali (ML)
9. Sénégal (SN)
10. Togo (TG)

**Statut : CONFIRMÉE** — la liste nominative des 10 pays elle-même est une donnée validée PO et n'est pas un point ouvert. Restent en revanche `[À VALIDER PO]`, individuellement, pour chaque pays : la coordinatrice/représentante actuelle, l'organisation point focal, et la date d'entrée exacte pour les pays « extension » (Côte d'Ivoire, Gambie, Guinée-Bissau) — voir `NSS_ERP_01` §9 et §30 (ERP-Q10, ERP-Q11). Ces éléments sont des données de migration, pas des bloqueurs d'architecture.

**Aucun pays n'a été créé dans Odoo** dans ce lot.

---

## 11. Ordre d'installation futur

Sur la base des dépendances vérifiées (sections 5 à 8), ordre recommandé pour un futur lot d'installation (non exécuté ici) :

1. `base`, `contacts`, `mail` (socle + annuaire)
2. `project` (projets/activités)
3. Développement `nss_network` (dépend de `contacts`, `project` — et potentiellement `account` selon le périmètre final retenu)
4. `account`, `analytic` (comptabilité + analytique)
5. `l10n_syscohada` puis `l10n_sn` (localisation comptable, société pilote Sénégal)
6. `account_budget_oca` (dépendance simple, budgets)
7. `date_range` + `report_xlsx` (OCA, prérequis techniques) puis `account_financial_report`
8. `account_statement_base` + `account_reconcile_model_oca` + `account_reconcile_oca` (à tester en dernier, chaîne de dépendances la plus longue)

Cet ordre est une proposition documentaire ; aucune installation n'a eu lieu.

---

## 12. Risques

| # | Risque | Impact | Mitigation proposée |
|---|---|---|---|
| R1 | Conflit non résolu entre `nss_network` (module unique) et la recommandation `nss_core`/`nss_project`/`nss_account` de `NSS_ERP_02` §21 | Confusion à l'implémentation | Décision PO du 24/09/2026 fait foi (`nss_network`) ; mettre à jour `NSS_ERP_02` §21 lors d'une prochaine révision si le PO confirme définitivement |
| R2 | `account_financial_report` et `account_reconcile_oca`/`account_reconcile_model_oca` sous licence AGPL-3 | Contrainte de distribution si ces modules sont un jour redistribués hors usage interne | Non bloquant pour un usage interne NSS ; à documenter si distribution future |
| R3 | `account_reconcile_oca` a une chaîne de 3 dépendances internes au même dépôt, module relativement jeune (réécriture récente avec `post_init_hook`) | Risque d'instabilité à l'installation | Tester isolément sur `nss_test` avant toute décision d'installation définitive (déjà la règle posée par `NSS_ERP_02` §20) |
| R4 | Ghana et Gambie non couverts par SYSCOHADA | Écritures analytiques possibles mais pas de plan comptable localisé natif pour ces 2 pays | Traiter en analytique uniquement au MVP (mono-société) ; réévaluer en Phase 2 si besoin confirmé (cf. `NSS_ERP_02` §16 trajectoire progressive) |
| R5 | Baseline VPS et copie locale contiennent des données de test Odoo réelles (structure, pas de données métier NSS) | Faible — aucune donnée réelle NSS, mais dump contient la structure complète de la base pilote | Dump et archive restent en local (`700`/`600`) et hors Git (`.gitignore`) ; à ne jamais committer |

---

## 13. Points à valider PO

```
POINTS_A_VALIDER_PO — LOT 2A

1. Conflit de source : confirmer définitivement que "nss_network" (module unique)
   remplace la recommandation nss_core/nss_project/nss_account de NSS_ERP_02 §21,
   pour mise à jour formelle de NSS_ERP_02 lors d'une prochaine révision.

2. Société pilote Odoo : nom exact, adresse, régime comptable à créer pour le TEST.

3. Devise de base (hypothèse XOF, ARCH-09 NSS_ERP_02 — non confirmée).

4. Exercice fiscal (hypothèse année civile, ARCH-04 NSS_ERP_02 — non confirmée).

5. Validation par la fonction comptable NSS que l10n_syscohada / l10n_sn couvrent
   réellement les obligations NSS (présence technique du module confirmée dans ce
   lot, mais pas sa suffisance fonctionnelle).

6. Traitement comptable de Ghana et Gambie (non couverts par SYSCOHADA) : rester en
   analytique seul au MVP, ou besoin d'une localisation dédiée en Phase 2 ?

7. Coordinatrices/représentantes actuelles et organisations point focal pour les
   10 pays (ERP-Q10/ERP-Q11 de NSS_ERP_01 — non bloquant pour l'architecture, mais
   nécessaire avant tout import de données réelles).

8. Licence AGPL-3 de account_financial_report et account_reconcile_oca /
   account_reconcile_model_oca : à noter, non bloquant pour un usage interne.
```

---

## 14. Préparation LOT 2B

Non exécuté dans ce lot. Sur la base des constats ci-dessus, un futur LOT 2B pourrait couvrir, **après nouvelle validation PO explicite** :

- Développement du module `nss_network` (périmètre défini section 9), avec données de démonstration 100 % fictives.
- Installation des modules natifs `contacts`, `mail`, `project` sur `nss_test`.
- Chargement des 10 pays (noms réels, car publics) avec coordinations et organisations **fictives**, conformément à `NSS_ERP_02` §23.

Ces actions ne sont ni planifiées ni engagées par ce document — elles nécessitent une nouvelle instruction PO explicite (LOT 2B), conformément à la consigne « NE COMMENCE PAS LOT 2B ».

---

*Fin du document NSS_ERP_06_LOT2A_BASELINE_MODULE_AUDIT.md*
