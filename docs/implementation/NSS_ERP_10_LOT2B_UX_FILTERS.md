# NSS ERP — Checkpoint 4A UX & filtres métier

**Référence :** NSS_ERP_10
**Date :** 25 septembre 2026
**Statut :** code modifié dans `nss_network`, **non installé sur le VPS**, aucune donnée métier NSS créée
**Prérequis :** `NSS_ERP_09` (Checkpoint 3, `nss_network` installé sur `nss_test`, 15/15 tests) ; ce checkpoint travaille uniquement en Git + GitHub Actions, sans toucher au VPS.

---

## 1. Contexte audit visuel

Suite à l'installation réelle de `nss_network` sur `nss_test` (Checkpoint 3), un audit visuel de l'interface a mis en évidence plusieurs points UX et filtres métier à corriger **avant** le chargement des 10 pays NSS :

- des champs organisation (`nss_org_type`, `nss_founding_member`) affichés même sur des contacts de type Individu ;
- des sélecteurs Many2one (coordinatrice, organisation point focal, organisation d'adhésion, responsabilités, bailleur) proposant tous les `res.partner` sans filtre, y compris `Administrator` ou `My Company` ;
- la devise des adhésions non visible pour l'utilisateur métier standard ;
- la liste des pays NSS trop dense sur mobile.

Ce checkpoint corrige ces points, sans francisation du code, sans modification de la société `My Company`, et sans toucher au VPS.

---

## 2. Contacts

Dans la vue formulaire `res.partner` (`views/res_partner_views.xml`, onglet « NSS Network ») :

- `nss_country_id` reste disponible pour **Individual et Company** : une personne comme une organisation peut être rattachée à un pays NSS. Le `help` du champ (`models/res_partner.py`) a été reformulé pour couvrir « ce contact ou cette organisation » (au lieu de ne parler que d'organisation).
- `nss_org_type` et `nss_founding_member` sont désormais regroupés dans un `<group invisible="not is_company">` : ils ne s'affichent que lorsque `is_company = True` (syntaxe Odoo 18, expression Python directe dans l'attribut `invisible`).
- Aucun champ natif Contacts n'a été modifié ou masqué.

---

## 3. Coordinatrices

`nss.country.membership.coordinator_id` (`models/nss_country_membership.py`) porte désormais un domaine métier :

```python
domain="[('is_company', '=', False), ('nss_country_id', '!=', False)]"
```

Seules les personnes physiques déjà rattachées à un pays NSS sont proposées (`Administrator` et les contacts non configurés disparaissent du sélecteur). La création rapide est désactivée dans la vue (`options="{'no_create': True}"`) : un contact doit être créé et configuré dans Contacts avant d'être choisi comme coordinatrice.

---

## 4. Organisations NSS

`nss.country.membership.focal_org_id` porte le domaine :

```python
domain="[('is_company', '=', True), ('nss_org_type', '!=', False)]"
```

Seules les organisations de type Company avec un `nss_org_type` renseigné sont proposées. Création rapide désactivée (`no_create`).

---

## 5. Adhésions

`nss.membership.organization_id` (`models/nss_membership.py`) porte le même type de domaine :

```python
domain="[('is_company', '=', True), ('nss_org_type', '!=', False)]"
```

Création rapide désactivée dans la vue formulaire. Les organisations doivent être préparées dans Contacts avant la création d'une adhésion.

---

## 6. Responsabilités

`nss.responsibility.history` (`models/nss_responsibility_history.py`) :

- `partner_id` : domaine `[('is_company', '=', False), ('nss_country_id', '!=', False)]`.
- `organization_id` : domaine `[('is_company', '=', True), ('nss_org_type', '!=', False)]`.

Création rapide désactivée pour les deux champs dans la vue formulaire. Aucune logique de `is_current`, de dates ou de `tracking` n'a été modifiée.

---

## 7. Project

`project.project.nss_funder_id` (`models/project_project.py`) est volontairement **moins restrictif** : le bailleur peut être extérieur au réseau NSS. Seul `is_company = True` est exigé ; `nss_org_type` n'est pas requis. Aucun autre champ Project n'a été modifié.

---

## 8. Devise

Dans la vue formulaire `nss.membership` (`views/nss_membership_views.xml`), la section « Cotisation » affiche désormais explicitement :

1. `currency_id` (Devise)
2. `fee_due` (Cotisation due)
3. `fee_paid` (Cotisation payée)

`currency_id` n'est plus réservé à `base.group_no_one` : il est visible pour tout utilisateur métier standard. Le défaut applicatif est inchangé (XOF si disponible via `self.env.ref("base.XOF", ...)`, sinon devise société). Aucune logique comptable n'a été modifiée.

---

## 9. Mobile

Dans la vue liste `nss.country.membership` (`views/nss_country_membership_views.xml`) :

- colonnes prioritaires (toujours visibles) : **Pays**, **Statut NSS**, **Coordinatrice / Représentante** ;
- colonnes optionnelles, masquées par défaut (`optional="hide"`) : **Date d'entrée**, **Organisation point focal**, **Nombre d'organisations**.

Aucun champ n'est supprimé : un utilisateur PC peut les réactiver via le menu des colonnes optionnelles de la vue liste Odoo.

---

## 10. Langue / configuration reportée

Conformément à la consigne, aucune traduction artificielle n'a été codée dans `nss_network` (labels natifs Odoo comme New, Project, Company, Clear, noms de pays, etc.). La francisation globale de l'interface reste une configuration Odoo/utilisateur, traitée dans un checkpoint de configuration séparé.

De même, la société `My Company` (nom attendu : « NSS ERP TEST », pays Sénégal, langue utilisateur Français) n'a fait l'objet d'**aucune écriture** dans ce checkpoint. Un audit de configuration TEST devra vérifier ultérieurement `res.company` sur `nss_test` :

- nom de société ;
- pays de la société ;
- langue par défaut des utilisateurs.

`[À VALIDER PO avant configuration]`.

---

## 11. Tests

`tests/test_nss_network.py` conserve ses 15 tests existants (aucun désactivé) et en ajoute 9, portant spécifiquement sur ce checkpoint :

16. domaine de `coordinator_id` (contient `is_company` et `nss_country_id`) ;
17. domaine de `focal_org_id` (contient `is_company` et `nss_org_type`) ;
18. domaine de `nss.membership.organization_id` (contient `is_company` et `nss_org_type`) ;
19. domaines de `nss.responsibility.history.partner_id` et `.organization_id` ;
20. domaine de `project.project.nss_funder_id` (contient `is_company`, ne contient pas `nss_org_type`) ;
21. `nss_country_id` utilisable aussi bien sur un partenaire Individu que Company ;
22. vue `res.partner` : `nss_org_type`/`nss_founding_member` bien conditionnés par `invisible="not is_company"` ;
23. vue `nss.membership` : `currency_id` bien affiché sans restriction `group_no_one` ;
24. vue `nss.country.membership` (liste) : colonnes mobiles optionnelles bien marquées `optional="hide"`.

Toutes les données de test restent fictives. Total : **24 tests**.

---

## 12. GitHub Actions

Le workflow existant `.github/workflows/nss-network-ci.yml` a été réutilisé sans modification (Odoo 18 + PostgreSQL 16, installation réelle de `nss_network`, exécution des tests via `--test-tags /nss_network`), déclenché automatiquement à l'ouverture de la Pull Request #12 de ce checkpoint.

Validation locale préalable, sans Docker (environnement cloud Claude, démon Docker non accessible — `failed to connect to the docker API at unix:///var/run/docker.sock`, identique à la limite déjà documentée dans `NSS_ERP_08`) :

- compilation Python réelle (`py_compile`) sur les 11 fichiers `.py` du module : **PASS** ;
- XML bien formé (`xml.dom.minidom`) sur les 6 fichiers de vues : **PASS** ;
- recherche de secrets (`password`/`passwd`/`private key`/`secret`/`api_key`/`token`) : **PASS**, aucune occurrence ;
- recherche des noms des 10 pays NSS validés dans l'addon : **PASS**, aucune occurrence.

**Résultat réel GitHub Actions (run de référence [`36137353815`](https://github.com/Amadousn221/nss-erp/actions/runs/36137353815), commit `9264e91`) :**

- Odoo 18 : **PASS**
- PostgreSQL 16 : **PASS**
- `nss_network` installé (module réellement chargé) : **PASS**
- 24 tests exécutés
- 24 tests réussis
- 0 échec
- 0 erreur
- exit code Odoo : `0`
- nettoyage Docker (conteneurs + réseau) : **PASS**

---

## 13. Limites

- Docker n'était pas disponible dans l'environnement cloud Claude utilisé pour ce checkpoint (même limite que celle déjà documentée dans `NSS_ERP_08`, §« Validation réelle Odoo 18 », Checkpoint 2.5). La validation réelle a donc été effectuée avec succès dans GitHub Actions (run `36137353815`, cf. section 12) : aucune validation locale Docker n'a été nécessaire.
- La configuration de `res.company` (« My Company ») n'a fait l'objet d'aucune vérification ni écriture réelle dans ce checkpoint : seule la nécessité d'un futur audit est documentée (section 10).
- Les record rules par pays restent hors périmètre (déjà documenté dans `NSS_ERP_08` §10/§14).
- La synchronisation `status = "archive"` ↔ `active = False` reste volontairement absente (`NSS_ERP_08` §4), non traitée par ce checkpoint.

---

## 14. Étape suivante

Après validation PO de ce Checkpoint 4A (fusion de la Pull Request) :

- audit de configuration `res.company` sur `nss_test` (section 10) ;
- conception des record rules par pays ;
- chargement des 10 pays NSS (données publiques, coordinations fictives), dans un checkpoint distinct dédié aux données, nécessitant une nouvelle validation PO explicite avant toute écriture.

**Rappel explicite :**

- aucun des 10 pays NSS n'est chargé par ce checkpoint ;
- aucune donnée métier NSS n'est créée par ce checkpoint ;
- aucun VPS n'a été modifié ni même contacté dans ce checkpoint.

---

*Fin du document NSS_ERP_10_LOT2B_UX_FILTERS.md*
