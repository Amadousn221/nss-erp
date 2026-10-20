# NSS ERP — LOT 2B Checkpoint 5 (proposé) : préparation de l'intégration des 10 pays NSS

**Référence :** NSS_ERP_13
**Date :** 20 octobre 2026
**Statut :** **préparation uniquement** — aucune donnée créée, aucun code modifié, aucun déploiement ; en attente des décisions du Product Owner (§8)
**Prérequis :** `NSS_ERP_12` (Checkpoint 4A déployé et clôturable), `NSS_ERP_00` (recherche pays), `NSS_ERP_01` §5, §9, §10, §24, §30

---

## 1. Objectif et périmètre

Préparer le chargement des **10 pays NSS** dans `nss_test` (liste officielle validée par le Product Owner le 23 septembre 2026, dynamique, jamais codée en dur). La liste « Pays NSS » est aujourd'hui vide : `nss_country_membership` = 0 ligne, ainsi que `nss_membership` et `nss_responsibility_history`.

Ce document établit : le modèle réel, l'état des sources par pays, la stratégie d'intégration, le périmètre proposé du prochain checkpoint et les décisions à prendre. **Il ne charge rien.**

Légende : **[CERTAIN]** = validé par le PO ou observé directement dans le code ou la base ; **[À VÉRIFIER]** = source récente non validée ; **[INDISPONIBLE]** = aucune source dans le projet.

---

## 2. Modèle de données (noms vérifiés dans le code et dans la base)

### 2.1 `nss.country.membership` (table `nss_country_membership`)

| Champ | Type | Contrainte / remarque |
|---|---|---|
| `country_id` | Many2one `res.country` | **requis**, indexé, suivi (tracking) |
| `status` | Sélection : `fondateur`, `extension`, `observation`, `archive` | **requis**, défaut `extension` |
| `join_date` | Date | libre ; doit être ≤ `exit_date` si les deux sont renseignées |
| `exit_date` | Date | idem |
| `coordinator_id` | Many2one `res.partner` | domaine (interface) : personne physique (`is_company = False`) avec `nss_country_id` renseigné |
| `focal_org_id` | Many2one `res.partner` | domaine (interface) : société (`is_company = True`) avec `nss_org_type` renseigné |
| `active` | Booléen | défaut vrai |
| `notes` | Texte | **seul champ de provenance existant** |
| `organization_ids` | One2many `res.partner` (inverse de `nss_country_id`) | calculé, non stocké |
| `organization_count` | Entier calculé | non stocké |

Colonnes PostgreSQL réelles : `id, country_id, coordinator_id, focal_org_id, status, join_date, exit_date, notes, active` (+ colonnes techniques). Hérite de `mail.thread` et `mail.activity.mixin`.

**Contraintes :**
- **Unicité d'une fiche active par pays** : contrainte **Python** (`@api.constrains`) uniquement. Il n'existe **aucune contrainte SQL d'unicité** (seulement la clé primaire, les clés étrangères et un index sur `country_id`) : l'idempotence d'un import doit donc être assurée par l'import lui-même.
- Cohérence des dates (Python).
- `status = archive` et `active = False` ne sont pas synchronisés (`NSS_ERP_08` §4, `[À VALIDER PO]`).
- **Les domaines des Many2one ne sont appliqués que dans l'interface** : l'ORM n'empêche pas d'écrire un `coordinator_id` hors domaine. Un import doit donc vérifier lui-même ces règles.

### 2.2 Liens avec Contacts, adhésions, responsabilités

| Modèle | Champs NSS | Lien |
|---|---|---|
| `res.partner` (extension) | `nss_country_id` (→ `nss.country.membership`), `nss_org_type` (`afr`, `federation`, `ong`, `coordination`, `point_focal`, `autre`), `nss_founding_member` | une personne **ou** une organisation se rattache à un pays NSS |
| `nss.membership` | `organization_id`, `status` (`en_cours`, `active`, `expiree`, `suspendue`, `archivee`), `application_date`, `admission_date`, `last_renewal_date`, `currency_id` (défaut XOF), `fee_due`, `fee_paid`, `member_count_declared`, `member_count_date` | adhésion d'une organisation (aucun lien direct vers le pays : le pays se déduit de `organization_id.nss_country_id`) |
| `nss.responsibility.history` | `partner_id` (requis), `organization_id`, `country_membership_id`, `role` (requis), `date_start` (**requis**), `date_end`, `is_current` (calculé) | historique des fonctions, y compris coordination nationale |
| `project.project` | `nss_country_membership_ids` (Many2many), `nss_funder_id`, `nss_program_tag` | hors périmètre de ce checkpoint |

**Dépendance circulaire à respecter pour l'ordre de création :** pour qu'une personne soit proposée comme coordinatrice, elle doit déjà avoir un `nss_country_id`, donc la fiche pays doit exister avant la personne, et la coordinatrice n'est renseignée sur la fiche pays qu'ensuite. De même pour l'organisation point focal.

### 2.3 Sécurité

`ir.model.access.csv` : `base.group_user` en lecture/écriture/création, **pas de suppression** (`perm_unlink = 0`), sur les trois modèles NSS. **Aucune record rule** (0 en base), aucun groupe NSS. Un seul utilisateur interne actif existe (`admin`). Conséquence : tout utilisateur interne pourrait modifier n'importe quelle fiche pays ; acceptable tant qu'il n'y a qu'un administrateur, à traiter avant l'ouverture à d'autres utilisateurs.

### 2.4 `res.country`

[CERTAIN] Les 10 pays existent dans `res.country` (250 pays en base), avec leurs identifiants externes standard et leurs noms français (langue `fr_FR` active) :

| ISO | Identifiant externe | Nom EN | Nom FR |
|---|---|---|---|
| BJ | `base.bj` | Benin | Bénin |
| BF | `base.bf` | Burkina Faso | Burkina Faso |
| CI | `base.ci` | Côte d'Ivoire | Côte d'Ivoire |
| GM | `base.gm` | Gambia | Gambie |
| GH | `base.gh` | Ghana | Ghana |
| GN | `base.gn` | Guinea | Guinée |
| GW | `base.gw` | Guinea-Bissau | Guinée-Bissau |
| ML | `base.ml` | Mali | Mali |
| SN | `base.sn` | Senegal | Sénégal |
| TG | `base.tg` | Togo | Togo |

---

## 3. Les 10 pays : sources et niveau de validation

Sources du projet : `NSS_ERP_00` (§3, §6), `NSS_ERP_01` (§5.1, §9, §10), `CLAUDE.md` (§4, §5), et, **à titre de recoupement uniquement**, les données éditoriales du site NSS (sauvegarde Sanity de staging du 04/10/2026 et `lib/network/countries.ts`), qui **ne sont pas validées pour l'ERP**.

### 3.1 Liste, statut, date d'entrée

| # | Pays | ISO | Statut NSS | Date d'entrée | Source | Validation |
|---|---|---|---|---|---|---|
| 1 | Bénin | BJ | `extension` | 13 juin 2026 (implantation officielle) | `NSS_ERP_00` §2, §6 ; `NSS_ERP_01` §5.1 (« Juin 2026 ») | pays et statut **[CERTAIN]** (table validée PO) ; date exacte **[À VÉRIFIER]** |
| 2 | Burkina Faso | BF | `fondateur` | 2011 (année seule) | `NSS_ERP_00` §2 ; `NSS_ERP_01` §5.1 | pays/statut **[CERTAIN]** ; jour/mois **[INDISPONIBLE]** |
| 3 | Côte d'Ivoire | CI | `extension` | non établie ; présence documentée en 2023 | `NSS_ERP_00` §2 ; `NSS_ERP_01` §5.1 | pays/statut **[CERTAIN]** ; date **[INDISPONIBLE]** |
| 4 | Gambie | GM | `extension` | non établie ; présence documentée en 2019 | idem | pays/statut **[CERTAIN]** ; date **[INDISPONIBLE]** |
| 5 | Ghana | GH | `fondateur` | 2011 (année seule) | idem | pays/statut **[CERTAIN]** ; jour/mois **[INDISPONIBLE]** |
| 6 | Guinée | GN | `fondateur` | 2011 (année seule) | idem | idem |
| 7 | Guinée-Bissau | GW | `extension` | non établie ; présence documentée en 2019 | idem | pays/statut **[CERTAIN]** ; date **[INDISPONIBLE]** |
| 8 | Mali | ML | `fondateur` | 2011 (année seule) | idem | pays/statut **[CERTAIN]** ; jour/mois **[INDISPONIBLE]** |
| 9 | Sénégal | SN | `fondateur` | 2011 (année seule) | idem | idem |
| 10 | Togo | TG | `extension` | 18 juillet 2026 (lancement officiel, Kpalimé) | `NSS_ERP_00` §2, §6 ; `NSS_ERP_01` §5.1 (« Juillet 2026 ») | pays/statut **[CERTAIN]** ; date exacte **[À VÉRIFIER]** |

Le site NSS (code et staging Sanity) retient les mêmes 10 codes ISO, tous « actifs » avec la portée `NSS10` : cohérent, mais ce n'est pas une validation pour l'ERP.

`join_date` est un champ **Date** : une année seule (« 2011 ») ne peut pas y être saisie sans inventer un jour et un mois (§8, décision D2). Aucune date de sortie n'est documentée : `exit_date` reste vide partout.

### 3.2 Coordinatrice / représentante et organisation point focal

Toutes ces informations sont des **sources récentes non validées** (`[SOURCE RÉCENTE — À VALIDER PO]`, `NSS_ERP_01` §9, §10). Le modèle validé (ERP-Q02) sépare la personne coordinatrice et l'organisation point focal éventuelle.

| Pays | Coordinatrice / représentante citée | Organisation point focal citée | Source | Validation |
|---|---|---|---|---|
| BJ | Clarisse ADONSI (représentante nationale) | FAEB — Fédération Agroécologique du Bénin (« appui cité ») | `NSS_ERP_00` §2, §6 | **[À VÉRIFIER]** |
| BF | — | — | — | **[INDISPONIBLE]** |
| CI | Monique Konan (coordinatrice, citée en 2026) | — | `NSS_ERP_00` §2, §6 | **[À VÉRIFIER]** ; point focal **[INDISPONIBLE]** |
| GM | — | — | — | **[INDISPONIBLE]** |
| GH | — | — | — | **[INDISPONIBLE]** |
| GN | — | — | — | **[INDISPONIBLE]** |
| GW | — | — | — | **[INDISPONIBLE]** |
| ML | — | — | — | **[INDISPONIBLE]** |
| SN | Mariama Sonko est citée comme **présidente panafricaine**, et non comme coordinatrice nationale du Sénégal | — | `NSS_ERP_00` §6 ; `NSS_ERP_01` §9 | **[CONFLIT DE RÔLE — À VALIDER PO]** : ne pas la saisir comme coordinatrice sans décision |
| TG | Aku Afefa Agbeka-Adiku (coordinatrice nationale) | Eco-Impact (point focal cité) ; responsable cité : Jean-Charles Sossou | `NSS_ERP_00` §2, §6 | **[À VÉRIFIER]** |

Écart noté : pour FAEB, le site NSS indique le rôle « partner » (et non « member ») alors que `NSS_ERP_01` §10 la décrit comme organisation point focal. Pour Eco-Impact, le site indique « member / currentMember ». Aucun type `nss_org_type` n'est documenté pour ces deux organisations.

### 3.3 Organisations associées documentées (brochure 2019, 13 organisations)

Source : `NSS_ERP_01` §10 `[HISTORIQUE]` — **« ne pas importer automatiquement »** ; statut actuel à vérifier. La colonne « Site NSS » est l'état éditorial du staging du 03/10/2026 (non validé pour l'ERP).

| Pays | Organisation (sigle) | Site NSS (03/10/2026) |
|---|---|---|
| BF | Fédération Nationale des Organisations Paysannes (FENOP) | membre actuel |
| BF | Réseau d'Appui à la Citoyenneté des Femmes Rurales Ouest-Africaines et du Tchad (RESACIFROAT) | membre historique |
| GM | Catalunya Gambia Foundation (CGF) | membre historique |
| GH | Rural Women Farmers Association of Ghana (RUWFAG) | membre historique |
| GH | « Assono Organic Farming Project (ABOFAB) » dans `NSS_ERP_01` ; « Abrono Organic Farming Project (ABOFAP) » sur le site | membre actuel — **[CONFLIT DE SOURCES]** sur le nom et le sigle |
| GN | Association Guinéenne pour l'Allègement des Charges Féminines (AGACFEM) | membre historique |
| GN | Association Guinéenne pour la Sécurité et la Souveraineté Alimentaires (AGUISSA) | membre actuel |
| GW | Fédération Paysanne de KAFO / « Fédération paysanne KAFO » (KAFO) | membre historique |
| ML | Association Malienne pour la Sécurité et la Souveraineté Alimentaire (AMASSA) | membre historique |
| ML | Association des Organisations Professionnelles Paysannes (AOPP) | membre historique |
| ML | Coordination des associations et ONG féminines du Mali (CAFO) | membre historique |
| SN | Association des Jeunes Agriculteurs de Casamance (AJAC) | membre actuel |
| SN | Union des Groupements Paysans de Mékhé (UGPM) | membre actuel |

Aucune organisation n'est documentée pour le Bénin, la Côte d'Ivoire et le Togo en dehors des points focaux cités au §3.2. Les 800+ associations du réseau ne sont pas listées dans les sources.

### 3.4 Écarts documentaires à conserver (non bloquants)

« Bénin 12e pays » et « 14 pays » (AFSA) : **ne modifient pas la liste de 10** (`NSS_ERP_00` §4). Incohérence interne mineure : `NSS_ERP_01` parle de 14 organisations (ERP-Q03, ERP-Q11) et de 13 (§10, conclusion) ; 13 sont identifiables.

---

## 4. Constats techniques qui conditionnent l'import

1. **Provenance :** `CLAUDE.md` §14 demande `source`, `source_date`, `verification_status`, `verified_at`, `verified_by`, `notes`. Le modèle ne porte que `notes`. Pour les pays, des mentions structurées dans `notes` suffisent ; pour les personnes et organisations, il faudra décider d'ajouter des champs (développement dans un checkpoint dédié).
2. **Courriel :** aucun serveur sortant n'est configuré et l'administrateur est `admin@example.com` (`NSS_ERP_12` §8.B). Toute création suivie par le chatter peut générer des courriels en échec. L'import doit désactiver le suivi/les notifications (`tracking_disable`, `mail_notrack`, `mail_create_nosubscribe`) — la traçabilité vient alors du journal d'import et de la sauvegarde.
3. **Contacts existants :** 6 partenaires (société, OdooBot, Administrator, utilisateurs techniques). Aucun ne doit être modifié ; l'import des pays seuls **ne crée ni ne modifie aucun contact**.
4. **Domaines non appliqués par l'ORM** et **unicité par pays uniquement en Python** (§2.1) : contrôles à porter par l'import.
5. **Historique de coordination :** `date_start` est obligatoire dans `nss.responsibility.history` ; aucune date de nomination n'est connue. Ne créer aucune ligne d'historique tant que ces dates ne sont pas fournies (`coordinator_id` porte la valeur courante).
6. **Fins de ligne :** corriger la gestion CRLF/LF avant tout nouveau déploiement de code (`NSS_ERP_12` §9).

---

## 5. Stratégie d'intégration proposée

### 5.1 Découpage en trois lots, du plus sûr au plus sensible

| Lot | Contenu | Données personnelles | Code à modifier |
|---|---|---|---|
| **5a** | 10 fiches pays : `country_id`, `status`, `active`, `join_date` (seulement si connue), `notes` (provenance) | aucune | non |
| **5b** | Coordinatrices et points focaux validés : création des personnes/organisations (nom, `nss_country_id`, `nss_org_type`) puis renseignement de `coordinator_id` / `focal_org_id` | noms de personnes (aucun téléphone ni courriel) | selon décision D6 (champs de provenance) |
| **5c** | Organisations historiques (13) avec statut « à vérifier » | noms d'organisations | selon D6 |

Recommandation : **ne livrer que 5a** dans le prochain checkpoint ; 5b et 5c ensuite, après validation par pays par le PO (`NSS_ERP_01` §24).

### 5.2 Ordre de création (lot 5a, puis 5b)

1. Sauvegarde (dump `nss_test` + comptages), relevé des services externes.
2. Lot 5a : créer les 10 fiches pays, sans coordinatrice ni point focal.
3. Contrôles : 10 fiches, un pays actif chacune, comptages des contacts inchangés (6).
4. Lot 5b (plus tard) : créer chaque personne/organisation **avec** `nss_country_id` → puis renseigner `coordinator_id` / `focal_org_id`.

### 5.3 Méthode (Odoo 18)

**Recommandation : un fichier de données versionné + un script d'import idempotent**, exécuté dans un conteneur éphémère `odoo shell` (même mécanisme que la mise à jour du 4A), avec :
- **clé naturelle** `res.country` (par code ISO) **et** identifiant externe `nss_network.country_<iso>` (module `ir.model.data`) pour retrouver les fiches ;
- mode **simulation (dry-run) par défaut** : rapport des créations/différences, aucune écriture ; l'écriture exige un indicateur explicite ;
- relance sans effet (second passage = 0 création, 0 modification) ; par défaut une relance **ne réécrit jamais** un champ modifié ensuite par un utilisateur, la mise à jour étant un mode explicite ;
- **une seule transaction** : en cas d'erreur, rien n'est validé ;
- journal détaillé sans donnée sensible.

Alternative : import CSV natif Odoo (colonnes `id`, `country_id/id` = `base.sn`…, `status`, `join_date`, `notes`) : idempotent via les identifiants externes, sans code, mais sans dry-run, sans contrôles métier ni rapport. Acceptable pour 5a seul si le PO préfère la simplicité.

Le fichier de données ne contient que des informations publiques validées ; il est versionné dans le dépôt (chemin à décider), jamais de secret, téléphone ou courriel.

### 5.4 Contrôles anti-doublons et de cohérence

- un seul enregistrement actif par pays (déjà imposé en Python) ; refus si une fiche existe sans identifiant externe (réconciliation manuelle) ;
- pays inexistant dans `res.country` → arrêt ;
- `status` ∈ valeurs du modèle ; `exit_date` ≥ `join_date` ;
- avant 5b : une coordinatrice est une personne (`is_company = False`) rattachée au bon pays ; un point focal est une société avec `nss_org_type` ; recherche de doublons par nom normalisé avant création de tout contact ; aucun contact existant modifié ;
- le partenaire de la société `NSS ERP TEST` n'est jamais utilisé comme organisation NSS (`NSS_ERP_12` §8.A).

### 5.5 Sauvegarde et retour arrière

Sauvegarde cohérente avant écriture (dump `nss_test`, comptages, empreinte), comme pour le 4A. Le lot 5a ne fait que des créations : retour arrière par suppression des enregistrements portant les identifiants externes `nss_network.country_*` (droits administrateur, transaction contrôlée), vérifié par comptage ; en dernier recours, restauration du dump dans une base temporaire puis bascule par renommage.

---

## 6. Prochain checkpoint proposé : « Checkpoint 5 — Pays NSS (lot 5a) »

**Périmètre :** créer les 10 fiches pays de NSS ERP TEST (lot 5a), rien d'autre.

**Livrables :** fichier de données (10 lignes, sources notées) ; script d'import idempotent avec dry-run ; document `NSS_ERP_14` (exécution et résultats) ; sauvegardes ; rapport de vérification.

**Dépendances :** décisions PO D1 à D4 (§8) ; sauvegarde fraîche ; aucune modification de l'addon.

**Risques :** date inventée (si D2 n'est pas tranchée) ; courriels en échec générés par le suivi (traité par la désactivation du suivi) ; import de personnes ou d'organisations non validées (exclus du lot 5a) ; fiche créée avec un mauvais statut.

**Critères d'acceptation :** 10 fiches actives, une par pays ; statuts conformes à la table validée ; aucune fiche en double ; `nss_country_membership` = 10 lignes, `nss_membership` et `nss_responsibility_history` = 0 ; 6 contacts inchangés ; seconde exécution du script sans aucun changement ; services externes inchangés ; vérification visuelle du PO.

**Plan de tests :**
- *Techniques :* dry-run (aucune écriture), exécution réelle, relance idempotente, tentative de doublon refusée, pays inconnu refusé, rollback transactionnel simulé, comptages avant/après, journaux Odoo sans erreur, absence de nouveaux courriels en `exception`.
- *Fonctionnels (PO) :* liste « Pays NSS » (10 lignes, 3 colonnes par défaut, colonnes optionnelles), fiche de chaque pays, filtres Actifs / Fondateur / Extension, regroupement par statut, noms français des pays.

---

## 7. Ordre d'exécution recommandé

1. Décisions PO (§8) ; 2. correction `.gitattributes` si validée (empêche le CRLF dans les archives) ; 3. préparation du fichier de données et du script (checkpoint sans déploiement) ; 4. exécution du lot 5a sur NSS TEST (sauvegarde, dry-run, exécution, vérifications) ; 5. vérification visuelle du PO ; 6. clôture ; 7. seulement ensuite, collecte des informations manquantes et lots 5b / 5c.

---

## 8. Décisions et informations demandées au Product Owner

| ID | Décision / information | Bloque |
|---|---|---|
| D1 | Confirmer que le tableau §3.1 (pays, statut `fondateur` / `extension`) est la baseline de chargement | lot 5a |
| D2 | **Dates d'entrée :** pour les 5 pays fondateurs (« 2011 ») et CI / GM / GW (dates inconnues), laisser `join_date` vide avec l'année en note (recommandé), ou fournir les dates exactes, ou accepter une convention approximative explicitement marquée | lot 5a |
| D3 | Confirmer 13 juin 2026 (Bénin) et 18 juillet 2026 (Togo) comme dates d'entrée dans NSS | lot 5a |
| D4 | Convention de provenance dans `notes` pour le lot 5a (source, date de la source, statut `[À VALIDER PO]` / `po_confirmed`) | lot 5a |
| D5 | Coordinatrices : confirmer, pays par pays, la personne en poste ; trancher le cas du Sénégal (Mariama Sonko = présidente panafricaine, pas nécessairement coordinatrice nationale) | lot 5b |
| D6 | Provenance structurée : ajouter des champs (`source`, `source_date`, `verification_status`, `verified_at`, `verified_by`) dans un développement dédié, ou continuer avec `notes` | lots 5b, 5c |
| D7 | Points focaux : FAEB (Bénin) et Eco-Impact (Togo) sont-ils les points focaux ? Quel `nss_org_type` pour chacun ? Point focal de la Côte d'Ivoire ? | lot 5b |
| D8 | Historique de coordination : fournir les dates de début de fonction avant toute ligne dans `nss.responsibility.history` | lot 5b |
| D9 | Périmètre de migration des 13 organisations de 2019 (ERP-Q18) et résolution du conflit ABOFAB / ABOFAP | lot 5c |
| D10 | Rôle des utilisateurs et droits par pays avant d'ouvrir NSS TEST à d'autres utilisateurs (record rules non conçues) | hors 5a |

**Informations manquantes (par ordre de criticité) :** coordinatrice actuelle des pays BF, GM, GH, GN, GW, ML ; point focal de BF, CI, GM, GH, GN, GW, ML, SN ; dates d'entrée exactes ; organisations actives par pays et leurs responsables actuels (ERP-Q10, ERP-Q11).

---

*Fin du document NSS_ERP_13_LOT2B_CHECKPOINT5_PAYS_NSS_PREPARATION.md*
