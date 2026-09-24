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
  renseignées, imposée à la fois par une contrainte Python (`ValidationError`
  explicite) et par une contrainte SQL `CHECK` de sécurité en base.

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

`nss.country.membership`, `nss.membership` héritent de `mail.thread` +
`mail.activity.mixin` ; `nss.responsibility.history` hérite de
`mail.thread`. Les trois vues formulaire correspondantes intègrent le
widget `<chatter/>` natif Odoo 18. `tracking=True` est posé uniquement sur
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

**Ces tests n'ont pas été exécutés dans une instance Odoo** (aucun serveur
Odoo local ni connexion au VPS, conformément à la consigne). Ils sont
prêts à être exécutés lors d'une installation contrôlée future.

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

**Limite documentée persistante :** aucun chargement effectif du module
par un serveur Odoo n'a été effectué, faute d'instance Odoo locale et
conformément à la consigne de ne pas déployer sur le VPS ni installer le
module. `py_compile` garantit l'absence d'erreur de syntaxe Python mais ne
vérifie ni le chargement ORM (modèles, vues, dépendances croisées) ni
l'exécution effective des tests unitaires. La vérification complète
(absence d'erreur de chargement, exécution réelle des 15 tests) ne pourra
être confirmée qu'au moment d'une installation contrôlée future sur un
environnement isolé (cf. section 15).

---

## 14. Limites

- Pas de record rules par pays (reporté, cf. section 10).
- Pas d'exécution réelle des tests dans une instance Odoo (cf. section
  12/13) ; validation Python statique désormais réelle (`py_compile`).
- Le choix de licence `LGPL-3` est documenté mais n'a pas fait l'objet
  d'une revue juridique formelle — cohérent avec les pratiques Odoo
  Community/OCA déjà en usage dans le projet.
- Les vues n'ont pas été testées visuellement (aucune instance Odoo
  chargée) ; leur syntaxe a été vérifiée par comparaison directe avec les
  vues natives Odoo 18 (balise `<list>`, structure `<notebook>`/`<page>`).
- Synchronisation `status = "archive"` ↔ `active = False` volontairement
  absente (cf. section 4) — `[À VALIDER PO]`.

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

*Fin du document NSS_ERP_08_LOT2B_NSS_NETWORK_CORE.md*
