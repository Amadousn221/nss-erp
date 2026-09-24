# NSS ERP — nss_network Core

**Référence :** NSS_ERP_08
**Date :** 24 septembre 2026 (mise à jour : revue corrective PR #10)
**Statut :** code développé en local, **non installé sur le VPS**, aucune donnée réelle
**Prérequis :** LOT 2B Checkpoint 1 clôturé et fusionné dans `main` (`NSS_ERP_07_LOT2B_NATIVE_FOUNDATION.md`)

---

## 0. Revue corrective (PR #10, non fusionnée)

Corrections apportées à la suite d'une revue de la PR #10, sur la même
branche `claude/nss-erp-lot2b-nss-network-core`, sans installation ni
fusion :

1. `is_current` (`nss.responsibility.history`) n'est plus stocké
   (`store=True` retiré) : champ calculé dynamique, avec une méthode de
   recherche dédiée (`_search_is_current`) supportant les opérateurs `=`
   et `!=`. Un booléen dépendant de la date du jour ne doit jamais être
   stocké, sous peine de devenir obsolète sans écriture explicite sur
   l'enregistrement.
2. `_compute_display_name` (`nss.country.membership`) déclare désormais
   `@api.depends("country_id")`, pour une invalidation de cache correcte
   en mémoire lors d'un changement de pays.
3. `security/ir.model.access.csv` : `perm_unlink` passé à `0` pour
   `base.group_user` sur les trois modèles NSS (`nss.country.membership`,
   `nss.membership`, `nss.responsibility.history`) — lecture, écriture et
   création restent ouvertes, la suppression est réservée à un niveau
   d'accès supérieur (aucun nouveau groupe créé à ce stade).
4. `nss.responsibility.history` hérite désormais aussi de
   `mail.activity.mixin` (en plus de `mail.thread`), pour bénéficier des
   activités planifiées en plus du chatter, des pièces jointes et de
   l'historique déjà couverts par la vue `<chatter/>` existante.
5. `nss.membership` : `tracking=True` ajouté sur `application_date`,
   `admission_date`, `last_renewal_date`, `fee_due`, `fee_paid`,
   `member_count_declared`, `member_count_date` (`status` et
   `organization_id` étaient déjà tracés).
6. Tests complétés (voir section 12) et validation statique rejouée (voir
   section 13).

---

## 1. Objectif

Développer le premier socle technique de l'addon spécifique unique
`nss_network` (décision PO définitive, `NSS_ERP_02` section 21), sans
l'installer sur `nss_test` ni sur aucun environnement. Aucune connexion
SSH n'a été nécessaire ni effectuée pour ce checkpoint.

---

## 2. Architecture du module

```
addons/nss_network/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── nss_country_membership.py
│   ├── nss_membership.py
│   ├── nss_responsibility_history.py
│   ├── project_project.py
│   ├── project_task.py
│   └── res_partner.py
├── security/
│   └── ir.model.access.csv
├── views/
│   ├── nss_country_membership_views.xml
│   ├── nss_membership_views.xml
│   ├── nss_network_menus.xml
│   ├── nss_responsibility_history_views.xml
│   ├── project_views.xml
│   └── res_partner_views.xml
└── tests/
    ├── __init__.py
    └── test_nss_network.py
```

Un addon unique, conforme à la décision PO : plusieurs modèles Python, vues
et règles de sécurité, mais un seul module Odoo (`application: True`,
`installable: True`).

**Licence :** `LGPL-3`, documentée dans `__manifest__.py`. Choix cohérent
avec la licence des modules natifs Odoo Community et compatible avec les
modules OCA du projet (LGPL-3/AGPL-3, voir `NSS_ERP_06` section 6), sans
imposer de contrainte de copyleft plus stricte que nécessaire pour un usage
interne NSS.

---

## 3. Dépendances

Déclarées dans `__manifest__.py` :

```python
"depends": ["base", "contacts", "mail", "project"],
```

**Aucune dépendance** vers `account`, `analytic` (explicite), un module OCA
ou une localisation comptable. Le module `analytic` reste présent
uniquement comme dépendance transitive native de `project` (déjà
documentée dans `NSS_ERP_07`), sans être déclaré par `nss_network`.

---

## 4. Modèle pays NSS

`nss.country.membership` (`models/nss_country_membership.py`), hérite de
`mail.thread` + `mail.activity.mixin`.

Champs : `country_id` (requis), `status` (fondateur/extension/observation/
archive), `join_date`, `exit_date`, `coordinator_id`, `focal_org_id`,
`active`, `notes`, `organization_ids` (one2many via `res.partner.nss_country_id`),
`organization_count` (calculé).

**Contraintes :**
- unicité d'une fiche **active** par `res.country` (`@api.constrains`
  Python, vérifie l'absence d'un autre enregistrement actif pour le même
  pays) ;
- cohérence des dates : `exit_date >= join_date` lorsque les deux sont
  renseignées, imposée par une contrainte Python (`ValidationError`
  explicite).

**Correction Checkpoint 2.5B (anomalie réelle détectée en CI) :** ce champ
était initialement doublement contraint — par le `@api.constrains` Python
ci-dessus **et** par une contrainte SQL `CHECK` (`join_before_exit_check`)
présentée comme une « sécurité en base » redondante. L'exécution réelle
des tests dans GitHub Actions a révélé que ce n'était pas de la défense en
profondeur : le flush ORM (nécessaire pour obtenir l'identifiant de
l'enregistrement) exécute l'INSERT SQL **avant** l'appel des méthodes
`@api.constrains`, donc la contrainte `CHECK` interceptait systématiquement
la violation en premier, remontant une erreur PostgreSQL brute
(`psycopg2.errors.CheckViolation`) au lieu du `ValidationError` explicite
attendu — rendant la vérification Python inatteignable en pratique via
`create()`/`write()`. La contrainte SQL `CHECK` a donc été supprimée ;
seule la contrainte Python subsiste, comme c'est déjà le cas pour les
contraintes de dates de `nss.membership` et `nss.responsibility.history`
(aucune contrainte SQL dupliquée sur ces modèles). La règle métier
(cohérence des dates d'entrée/sortie) reste strictement identique, avec un
seul point d'application au lieu de deux qui se faisaient concurrence.

Aucun des 10 pays NSS n'est créé par ce module.

**Distinction statut métier / archivage technique :** `status = "archive"`
est une valeur métier NSS (le pays est considéré comme sorti du réseau du
point de vue fonctionnel), tandis que `active = False` est le mécanisme
technique natif d'archivage Odoo (masque l'enregistrement des vues et
recherches par défaut). Ces deux notions sont **volontairement non
synchronisées automatiquement** dans ce checkpoint : passer `status` à
`archive` n'entraîne pas `active = False`, et inversement. La conception
d'une éventuelle synchronisation (et son sens métier exact) est
`[À VALIDER PO]` et reportée à un checkpoint ultérieur.

---

## 5. Organisations

Extension de `res.partner` (`models/res_partner.py`) : `nss_country_id`
(many2one vers `nss.country.membership`), `nss_org_type` (afr/federation/
ong/coordination/point_focal/autre), `nss_founding_member` (booléen).

Aucun nouveau modèle ni menu n'est créé pour les organisations : le module
réutilise entièrement `res.partner`/Contacts, conformément à la consigne.
Le fonctionnement natif de Contacts n'est pas modifié, seuls des champs et
un onglet supplémentaires sont ajoutés (voir section 11).

---

## 6. Adhésions

`nss.membership` (`models/nss_membership.py`), hérite de `mail.thread` +
`mail.activity.mixin`.

Champs : `organization_id` (requis), `status` (en_cours/active/expiree/
suspendue/archivee), `application_date`, `admission_date`,
`last_renewal_date`, `currency_id` (requis, défaut `XOF` via
`self.env.ref("base.XOF")`, sans dépendance vers `account`), `fee_due`,
`fee_paid` (Monetary), `member_count_declared`, `member_count_date`,
`notes`.

**Traçabilité renforcée (revue corrective) :** en plus de `status` et
`organization_id` déjà tracés, `tracking=True` est désormais posé sur
`application_date`, `admission_date`, `last_renewal_date`, `fee_due`,
`fee_paid`, `member_count_declared` et `member_count_date` : toute
modification de ces champs métier sensibles (dates d'adhésion, montants
de cotisation, effectifs déclarés) apparaît dans le chatter.

**Contraintes :** cohérence des dates (demande ≤ adhésion ≤ renouvellement)
et nombre de membres déclaré non négatif. Aucune cotisation réelle, aucune
facturation automatique — la comptabilité reste hors périmètre de ce
checkpoint.

---

## 7. Responsabilités

`nss.responsibility.history` (`models/nss_responsibility_history.py`),
hérite de `mail.thread` **et `mail.activity.mixin`** (ajout revue
corrective) : chatter, activités planifiées, pièces jointes et historique
des messages, sans système documentaire parallèle — la vue formulaire
utilise le widget natif `<chatter/>` existant.

Champs : `partner_id` (requis), `organization_id`, `country_membership_id`,
`role` (requis), `date_start` (requis), `date_end`, `is_current` (calculé,
**non stocké**), `notes`.

`is_current` est calculé (`@api.depends("date_start", "date_end")`) à
partir de la date du jour : vrai si `date_start` est passée ou égale à
aujourd'hui et (`date_end` absente ou non encore atteinte). Contrainte :
`date_end >= date_start` lorsque `date_end` est renseignée.

**Correction revue corrective — champ non stocké :** `is_current` dépend
de la date du jour, une valeur qui évolue sans qu'aucune écriture ne soit
faite sur l'enregistrement ; le stocker (`store=True`) l'aurait rendu
obsolète tant qu'aucune recomputation n'est déclenchée. Le champ est donc
recalculé à chaque lecture. Une méthode `_search_is_current(self,
operator, value)` est fournie pour permettre le filtrage/recherche
(`is_current = True`, `is_current = False`, `is_current != True`, etc.),
avec prise en charge explicite des opérateurs `=` et `!=` (toute autre
tentative lève une `UserError`).

---

## 8. Extensions Project

`project.project` (`models/project_project.py`) : `nss_country_membership_ids`
(many2many vers `nss.country.membership`), `nss_program_tag` (champ texte
simple, conforme au MVP de `NSS_ERP_02` section 9), `nss_funder_id`
(many2one vers `res.partner`).

`project.task` (`models/project_task.py`) : `nss_activity_type`
(formation/iec/camp/atelier/plaidoyer/rencontre/autre), `nss_location`
(texte).

Aucun projet ou activité réel ou fictif n'est créé par ce module.

---

## 9. Traçabilité

`nss.country.membership`, `nss.membership` et `nss.responsibility.history`
héritent tous les trois de `mail.thread` + `mail.activity.mixin` (ajout de
`mail.activity.mixin` sur `nss.responsibility.history` lors de la revue
corrective de la PR #10, cf. section 0/7). Les trois vues formulaire
correspondantes intègrent le widget `<chatter/>` natif Odoo 18, qui
affiche désormais aussi les activités planifiées pour les trois modèles.
`tracking=True` est posé uniquement sur
les champs métier significatifs (statut, dates clés, coordinatrice,
organisation point focal, rôle, montants de cotisation, etc.), pas sur les
champs techniques (`notes`, `active`). Aucun système documentaire
parallèle n'est développé : le chatter Odoo reste l'unique mécanisme de
traçabilité.

---

## 10. Sécurité

`security/ir.model.access.csv` : pour `base.group_user` (tous les
utilisateurs internes), accès lecture/écriture/création sur les trois
modèles NSS principaux, **suppression (`unlink`) refusée** (`perm_unlink
= 0`, correction revue corrective) — un utilisateur standard ne peut donc
plus supprimer une fiche pays, une adhésion ou un historique de
responsabilité, seulement la consulter, la créer et la modifier (y compris
l'archiver via `status`/`active`). Aucun accès portail, aucun accès
public, aucun nouveau groupe NSS créé à ce stade — conformément à la
consigne de rester minimal. Les record rules par pays sont explicitement
reportées à un checkpoint ultérieur, l'affectation utilisateur ↔ pays
n'étant pas encore conçue.

---

## 11. Vues et menus

| Vue | Modèle | Type |
|---|---|---|
| `view_nss_country_membership_list/form/search` | `nss.country.membership` | liste, formulaire, recherche |
| `view_nss_membership_list/form/search` | `nss.membership` | liste, formulaire, recherche |
| `view_nss_responsibility_history_list/form/search` | `nss.responsibility.history` | liste, formulaire, recherche |
| `view_partner_form_nss_network` | `res.partner` (héritée) | onglet « NSS Network » ajouté au formulaire Contacts existant |
| `edit_project_form_nss_network` | `project.project` (héritée) | onglet « NSS Network » ajouté après l'onglet « Settings » |
| `view_task_form2_nss_network` | `project.task` (héritée) | champs ajoutés après `tag_ids` |

Toutes les vues liste utilisent la balise `<list>` (syntaxe Odoo 18 —
vérifiée directement sur les vues natives `project.task` du dépôt officiel
`odoo/odoo` branche `18.0`, qui utilisent déjà `<list>` et non `<tree>`).

Menu racine créé : **NSS Network**, avec 3 sous-menus : **Pays NSS**,
**Adhésions**, **Responsabilités**. Aucun menu ni modèle redondant n'est
créé pour les organisations (réutilisation intégrale de Contacts).

---

## 12. Tests

`tests/test_nss_network.py`, 15 méthodes de test (`TransactionCase`,
`@tagged("post_install", "-at_install")`) — 12 méthodes initiales + 3
ajoutées lors de la revue corrective (points 10 à 12 ci-dessous) :

1. création d'un `nss.country.membership` ;
2. unicité d'une fiche active par pays (`ValidationError` attendue) ;
3. une fiche archivée n'empêche pas la création d'une nouvelle fiche active ;
4. cohérence des dates pays (`exit_date < join_date` → erreur) ;
5. création d'une organisation rattachée à un pays NSS ;
6. création d'une adhésion (`nss.membership`), devise par défaut ;
7. cohérence des dates d'adhésion (`admission_date < application_date` → erreur) ;
8. nombre de membres déclaré négatif refusé ;
9. calcul de `is_current` (passé/présent/futur) ;
10. cohérence des dates de responsabilité (`date_end < date_start` → erreur) ;
11. extension `project.project` (pays, programme, bailleur) ;
12. extension `project.task` (type d'activité, lieu) ;
13. **(revue corrective)** recherche `is_current` (`=` True/False et `!=`
    True), sur un jeu de fiches passée/actuelle/future ;
14. **(revue corrective)** `display_name` de `nss.country.membership` mis
    à jour dynamiquement lors d'un changement de `country_id` ;
15. **(revue corrective)** suppression (`unlink`) d'une fiche
    `nss.country.membership` refusée (`AccessError`) pour un utilisateur
    créé avec uniquement le groupe `base.group_user`.

Toutes les données sont fictives (« Association Test Fictive »,
« Coordinatrice Test », etc.). Les pays réutilisés comme fixtures
techniques (France, Belgique, natifs `res.country`) ne représentent pas le
périmètre géographique réel de NSS — les 10 pays seront chargés dans un
checkpoint séparé.

**Ces 15 tests ont été réellement exécutés** dans une instance Odoo 18
chargée (GitHub Actions, Checkpoint 2.5B, cf. section « Validation réelle
Odoo 18 ») : **0 échec, 0 erreur** sur le second run (après correction de
2 anomalies réelles détectées sur le premier run). Exit code Odoo : `0`.

---

## 13. Validation statique

Validation initiale (checkpoint 2) effectuée sans installer aucun outil
supplémentaire (Python n'était pas disponible sur le poste de travail
local à l'époque) :

| Vérification | Méthode | Résultat |
|---|---|---|
| XML bien formé | `[xml]` PowerShell (`System.Xml`, natif Windows) sur les 6 fichiers XML | **PASS** — 6/6 OK |
| CSV | `Import-Csv` PowerShell sur `ir.model.access.csv` | **PASS** — 3 lignes, colonnes cohérentes |
| Manifest | Relecture manuelle : `depends` limité à `base`/`contacts`/`mail`/`project`, `license` renseignée | **PASS** |
| Imports Python | Vérification manuelle des `__init__.py` (module ↔ fichiers présents) | **PASS** |
| Équilibrage syntaxique Python | Script Node.js (comptage parenthèses/crochets/accolades + détection de tabulations) sur les 11 fichiers `.py` | **PASS** — 11/11 équilibrés, aucune tabulation |
| Recherche de secrets | `grep` récursif (password/passwd/PRIVATE KEY/secret/api_key/token) | **PASS** — aucune occurrence |

**Revalidation (revue corrective, environnement disposant de Python 3) :**

| Vérification | Méthode | Résultat |
|---|---|---|
| Compilation Python réelle | `py_compile` sur les 11 fichiers `.py` du module | **PASS** — 11/11 compilent sans erreur de syntaxe |
| XML bien formé | `xml.dom.minidom` sur les 6 fichiers XML | **PASS** — 6/6 OK |
| CSV | `csv.DictReader` sur `ir.model.access.csv` | **PASS** — 3 lignes, `perm_unlink=0` confirmé sur les 3 modèles NSS |
| Recherche de secrets | `grep` récursif (password/passwd/private key/secret/api_key/token) | **PASS** — aucune occurrence |
| Recherche de données réelles | `grep` récursif sur les noms des 10 pays NSS validés (Bénin, Burkina Faso, Côte d'Ivoire, Gambie, Ghana, Guinée, Guinée-Bissau, Mali, Sénégal, Togo) | **PASS** — aucune occurrence dans l'addon |

**Complément — validation réelle (Checkpoint 2.5B) :** les vérifications
statiques ci-dessus (`py_compile`, XML, CSV, secrets, données réelles) ont
depuis été complétées par une validation réelle de `nss_network` dans une
instance Odoo 18 effectivement chargée, avec PostgreSQL 16, exécutée dans
GitHub Actions sur une base CI éphémère (aucune installation sur le VPS,
aucune donnée réelle NSS) : modèles ORM chargés, vues XML chargées, ACL
chargées et vérifiées activement, et **15 tests sur 15 réussis** (exit
code Odoo `0`). Le détail complet (environnement, anomalies détectées et
corrigées, résultat) est documenté dans la section « Validation réelle
Odoo 18 » ci-dessous ; cette limite (absence de chargement effectif par un
serveur Odoo) est donc désormais levée.

---

## 14. Limites

- Pas de record rules par pays (reporté, cf. section 10).
- Le choix de licence `LGPL-3` est documenté mais n'a pas fait l'objet
  d'une revue juridique formelle — cohérent avec les pratiques Odoo
  Community/OCA déjà en usage dans le projet.
- Les vues ont été chargées avec succès par Odoo 18 en CI (aucune
  `ParseError`) mais n'ont pas été inspectées visuellement dans un
  navigateur (pas d'accès UI depuis GitHub Actions, aucun port publié
  conformément à la consigne).
- Synchronisation `status = "archive"` ↔ `active = False` volontairement
  absente (cf. section 4) — `[À VALIDER PO]`.
- Validation réalisée sur une base CI éphémère à vide (`--without-demo`,
  aucune donnée réelle) ; le comportement avec les données réelles NSS
  (10 pays, organisations) reste à valider lors d'un checkpoint dédié à
  l'import de données, après validation PO explicite.

---

## 15. Préparation Checkpoint 3

Non engagé par ce document. Un futur Checkpoint 3 pourrait, **après
nouvelle validation PO explicite**, couvrir :

- l'installation contrôlée de `nss_network` sur `nss_test` (copie dans
  `addons/`, déjà monté en lecture seule dans `nss-odoo`, puis
  `-i nss_network --stop-after-init`) ;
- l'exécution réelle des tests unitaires (`--test-enable`) ;
- la vérification de non-régression complète (identique aux checkpoints
  précédents) ;
- la conception des record rules par pays (affectation utilisateur ↔ pays) ;
- le chargement des 10 pays NSS (données publiques, coordinations
  fictives), dans un checkpoint distinct dédié aux données.

---

## Validation réelle Odoo 18

### Checkpoint 2.5 (environnement cloud Claude) : `CLOUD_DOCKER_UNAVAILABLE`

Tentative d'exécution réelle de `nss_network` dans un environnement Docker
Odoo 18 / PostgreSQL 16 temporaire, directement dans l'environnement cloud
Claude. `docker --version` répondait mais `docker info` échouait (`failed
to connect to the docker API at unix:///var/run/docker.sock`) : aucun
démon Docker accessible. Conformément à la consigne, aucun contournement
n'a été tenté et le VPS NSS n'a pas été utilisé comme solution de
remplacement. Seules deux corrections mineures préalables ont été
appliquées à ce stade : section 9 (Traçabilité) corrigée pour refléter que
`nss.responsibility.history` hérite bien de `mail.thread` **et**
`mail.activity.mixin`, et remplacement de `datetime.date.today()` par
`fields.Date.context_today(...)` dans les tests `is_current` (voir
correction ci-dessous : cette première tentative de correction contenait
elle-même une erreur, détectée uniquement grâce à l'exécution réelle en
CI).

### Checkpoint 2.5B (GitHub Actions) : environnement Docker CI isolé

Décision : utiliser GitHub Actions (runner Ubuntu hébergé, démon Docker
natif) comme environnement CI Docker isolé, sans toucher au VPS NSS.

Workflow créé : `.github/workflows/nss-network-ci.yml`, déclenché sur
`pull_request` (`addons/nss_network/**`) et manuellement
(`workflow_dispatch`). Il crée un réseau Docker éphémère
`nss-network-ci-net`, démarre un conteneur PostgreSQL 16
`nss-network-ci-db` (base `nss_network_ci`, utilisateur `odoo`, mot de
passe généré aléatoirement par run via `openssl rand`, masqué dans les
logs, jamais committé), attend sa disponibilité via `pg_isready`, puis
lance un conteneur Odoo 18 éphémère (`--rm`, `addons/` monté en lecture
seule sur `/mnt/extra-addons`, aucun port publié, réseau CI uniquement)
avec `-i nss_network --without-demo=all --test-enable --test-tags
/nss_network --stop-after-init`. Le code de sortie Odoo est capturé et
propage l'échec du workflow (`set -Eeuo pipefail`). Nettoyage
(conteneurs + réseau) exécuté systématiquement via `if: always()`.

**Premier run (commit `248a173`) : ÉCHEC réel, anomalies confirmées.**
L'installation elle-même a pleinement réussi (manifest, 39 modules dont
`nss_network`, modèles ORM, vues XML, ACL, héritages `res.partner` /
`project.project` / `project.task` tous chargés sans erreur). Sur les 15
tests nss_network exécutés : 12 réussis, **3 erreurs réelles** :

1. `test_country_membership_date_constraint` : `psycopg2.errors.
   CheckViolation` brut au lieu du `ValidationError` attendu. Cause
   réelle : `nss.country.membership` portait à la fois un `@api.constrains`
   Python et une contrainte SQL `CHECK` (`join_before_exit_check`) sur la
   même règle (cohérence `join_date`/`exit_date`). Le flush ORM (INSERT
   SQL, nécessaire pour obtenir l'identifiant du nouvel enregistrement)
   s'exécute avant l'appel des méthodes `@api.constrains` : la contrainte
   SQL interceptait donc systématiquement la violation en premier,
   rendant la vérification Python inatteignable via `create()`/`write()`
   — ce n'était pas de la défense en profondeur, mais du code mort.
   **Correction :** suppression de la contrainte SQL `CHECK` redondante
   dans `models/nss_country_membership.py` ; seule la contrainte Python
   subsiste désormais (cf. section 4), cohérent avec le traitement déjà
   appliqué aux contraintes de dates de `nss.membership` et
   `nss.responsibility.history` (qui n'ont jamais eu de doublon SQL). Règle
   métier strictement inchangée.
2. et 3. `test_responsibility_history_is_current` et
   `test_responsibility_history_is_current_search` : `AttributeError:
   'TestNssNetwork' object has no attribute '_context'`. Cause réelle :
   la correction du Checkpoint 2.5 avait remplacé `date.today()` par
   `fields.Date.context_today(self)`, mais dans ces méthodes de test
   `self` désigne l'instance `TestCase`, pas un recordset Odoo — ce n'est
   qu'à l'exécution réelle que l'erreur est apparue, aucune exécution
   locale n'ayant été possible avant ce checkpoint. **Correction :**
   `fields.Date.context_today(self.env.user)` dans les deux tests (un
   recordset valide disposant bien d'un `_context`). Aucun changement de
   logique métier ni de test.

Aucun test n'a été désactivé ni affaibli pour obtenir ces corrections ; les
deux anomalies étaient réelles et ont été corrigées à la racine.

**Second run (commit `6d75314`, après corrections) : SUCCÈS réel.**
Installation `nss_network` réussie (39 modules chargés, dont
`nss_network` en position 37/39, manifest/dépendances/ORM/vues
XML/héritages `res.partner`/`project.project`/`project.task` tous
conformes), ACL chargées et vérifiées activement par
`test_country_membership_unlink_forbidden_for_standard_user` (« Access
Denied by ACLs for operation: unlink »). Résultat Odoo :
**« 0 failed, 0 error(s) of 15 tests when loading database
'nss_network_ci' »**. **Exit code Odoo : `0`.** Run :
<https://github.com/Amadousn221/nss-erp/actions/runs/36067699565>.

Nettoyage : effectué automatiquement à chaque run (les deux) par l'étape
dédiée (`if: always()`), aucune base ni conteneur CI persistant, aucune
donnée réelle NSS, aucun accès au VPS `nss_test`.

---

*Fin du document NSS_ERP_08_LOT2B_NSS_NETWORK_CORE.md*
