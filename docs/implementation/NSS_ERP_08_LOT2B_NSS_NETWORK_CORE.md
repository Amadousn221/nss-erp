# NSS ERP — nss_network Core

**Référence :** NSS_ERP_08
**Date :** 24 septembre 2026
**Statut :** code développé en local, **non installé sur le VPS**, aucune donnée réelle
**Prérequis :** LOT 2B Checkpoint 1 clôturé et fusionné dans `main` (`NSS_ERP_07_LOT2B_NATIVE_FOUNDATION.md`)

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

**Contraintes :** cohérence des dates (demande ≤ adhésion ≤ renouvellement)
et nombre de membres déclaré non négatif. Aucune cotisation réelle, aucune
facturation automatique — la comptabilité reste hors périmètre de ce
checkpoint.

---

## 7. Responsabilités

`nss.responsibility.history` (`models/nss_responsibility_history.py`),
hérite de `mail.thread`.

Champs : `partner_id` (requis), `organization_id`, `country_membership_id`,
`role` (requis), `date_start` (requis), `date_end`, `is_current` (calculé,
stocké), `notes`.

`is_current` est calculé (`@api.depends("date_start", "date_end")`) à
partir de la date du jour : vrai si `date_start` est passée ou égale à
aujourd'hui et (`date_end` absente ou non encore atteinte). Contrainte :
`date_end >= date_start` lorsque `date_end` est renseignée.

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

`security/ir.model.access.csv` : accès complet (lecture/écriture/création/
suppression) pour `base.group_user` (tous les utilisateurs internes) sur
les trois modèles NSS principaux. Aucun accès portail, aucun accès public,
aucun groupe NSS spécifique créé à ce stade — conformément à la consigne
de rester minimal. Les record rules par pays sont explicitement reportées
à un checkpoint ultérieur, l'affectation utilisateur ↔ pays n'étant pas
encore conçue.

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

`tests/test_nss_network.py`, 12 méthodes de test (`TransactionCase`,
`@tagged("post_install", "-at_install")`) :

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
12. extension `project.task` (type d'activité, lieu).

Toutes les données sont fictives (« Association Test Fictive »,
« Coordinatrice Test », etc.). Les pays réutilisés comme fixtures
techniques (France, Belgique, natifs `res.country`) ne représentent pas le
périmètre géographique réel de NSS — les 10 pays seront chargés dans un
checkpoint séparé.

**Ces tests n'ont pas été exécutés** dans ce checkpoint (aucune instance
Odoo locale ni connexion au VPS, conformément à la consigne). Ils sont
prêts à être exécutés lors d'une installation contrôlée future.

---

## 13. Validation statique

Effectuée sans installer aucun outil supplémentaire (conformément à la
consigne — Python n'est pas disponible sur le poste de travail local) :

| Vérification | Méthode | Résultat |
|---|---|---|
| XML bien formé | `[xml]` PowerShell (`System.Xml`, natif Windows) sur les 6 fichiers XML | **PASS** — 6/6 OK |
| CSV | `Import-Csv` PowerShell sur `ir.model.access.csv` | **PASS** — 3 lignes, colonnes cohérentes |
| Manifest | Relecture manuelle : `depends` limité à `base`/`contacts`/`mail`/`project`, `license` renseignée | **PASS** |
| Imports Python | Vérification manuelle des `__init__.py` (module ↔ fichiers présents) | **PASS** |
| Équilibrage syntaxique Python | Script Node.js (comptage parenthèses/crochets/accolades + détection de tabulations) sur les 11 fichiers `.py` | **PASS** — 11/11 équilibrés, aucune tabulation |
| Recherche de secrets | `grep` récursif (password/passwd/PRIVATE KEY/secret/api_key/token) | **PASS** — aucune occurrence |

**Limite documentée :** aucune compilation Python réelle (`py_compile`) ni
chargement effectif du module par un serveur Odoo n'a été effectuée, faute
de Python et d'instance Odoo locale — conformément à la consigne de ne pas
installer d'outil supplémentaire. La vérification de la validité complète
du module (absence d'erreur de chargement, exécution effective des tests)
ne pourra être confirmée qu'au moment d'une installation contrôlée future
sur un environnement isolé.

---

## 14. Limites

- Pas de record rules par pays (reporté, cf. section 10).
- Pas d'exécution réelle des tests (cf. section 12/13).
- Le choix de licence `LGPL-3` est documenté mais n'a pas fait l'objet
  d'une revue juridique formelle — cohérent avec les pratiques Odoo
  Community/OCA déjà en usage dans le projet.
- Les vues n'ont pas été testées visuellement (aucune instance Odoo
  chargée) ; leur syntaxe a été vérifiée par comparaison directe avec les
  vues natives Odoo 18 (balise `<list>`, structure `<notebook>`/`<page>`).

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
