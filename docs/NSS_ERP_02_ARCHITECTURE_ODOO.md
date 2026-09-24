# NSS ERP — Architecture Odoo

**Référence :** NSS_ERP_02
**Version :** 1.1 — contrôle technique ChatGPT
**Date :** 23 septembre 2026
**Auteur :** Architecte fonctionnel (Claude Opus)
**Statut :** [VALIDÉ PO — 24 septembre 2026]
**Prérequis :** NSS_ERP_01 V1.2 validée

---

## 1. Executive Summary

Ce document traduit l'audit fonctionnel NSS_ERP_01 en architecture technique Odoo Community. Il couvre le mapping des besoins métier vers les modules natifs, OCA et développements spécifiques, le modèle de données, l'infrastructure VPS Hostinger, la stratégie comptable et le plan d'implémentation MVP.

**Choix structurants :**

- **Version Odoo :** 18.0 Community
- **Architecture comptable pilote :** mono-société avec analytique multi-dimensions (Option A)
- **Hébergement :** VPS Hostinger, instance isolée, PostgreSQL dédié
- **Données :** données fictives uniquement pendant le pilote
- **Développement spécifique :** un module NSS unique (`nss_network`) pour le réseau, les adhésions et les coordinations pays — le strict minimum non couvert par Odoo natif

Le MVP est découpé en **5 lots** avec dépendances claires.

---

## 2. Décisions PO intégrées

| Réf. | Décision | Source |
|---|---|---|
| ERP-Q01 | Organisations + statistiques déclaratives de membres ; pas de membres individuels au MVP | VALIDÉ PO |
| ERP-Q02 | Coordinatrice/représentante + organisation point focal éventuelle, indépendantes | VALIDÉ PO |
| ERP-Q05 | Architecture comptable : centralisée (Option A, mono-société) retenue pour le pilote | VALIDÉ PO 24/09/2026 — traité en section 16 |
| ERP-Q15 | 10–20 utilisateurs max pour le pilote | VALIDÉ PO |
| ERP-Q17 | VPS Hostinger avec Odoo Community | VALIDÉ PO |
| ERP-Q24 | Comptabilité complète/officielle (pas seulement recettes/dépenses) | VALIDÉ PO |
| — | Données fictives uniquement pour la première implémentation | VALIDÉ PO |
| — | 10 pays NSS, liste dynamique | VALIDÉ PO |
| — | Addon spécifique unique `nss_network` (remplace `nss_core`/`nss_project`/`nss_account`) | VALIDÉ PO 24/09/2026 — section 21 |
| — | Société pilote « NSS ERP TEST », Sénégal, sans donnée juridique réelle | VALIDÉ PO 24/09/2026 |
| — | Devise pilote XOF ; exercice fiscal civil (01/01–31/12) | VALIDÉ PO 24/09/2026 |
| — | `l10n_syscohada` + `l10n_sn` pour le TEST (validation technique, pas de conformité officielle) | VALIDÉ PO 24/09/2026 |
| — | Ghana/Gambie : dimensions analytiques uniquement au MVP | VALIDÉ PO 24/09/2026 |
| — | Licences OCA AGPL-3 acceptées pour usage interne NSS TEST | VALIDÉ PO 24/09/2026 |

---

## 3. Version Odoo recommandée

### Recommandation corrigée : Odoo 18.0 Community

**Pourquoi 18.0 :**

- Odoo 17 arrive à la fin de sa période de support standard en septembre 2026 : démarrer un nouveau projet dessus créerait une dette de migration immédiate.
- Odoo 18 reste sous support standard jusqu'en septembre 2027.
- L'écosystème OCA 18.0 est aujourd'hui suffisamment mature pour les briques nécessaires au projet NSS, notamment les budgets et les rapports financiers.
- Odoo 19 est plus récent, mais plusieurs briques OCA utiles au projet sont encore en migration ou moins stabilisées. Pour le pilote NSS, la maturité d'Odoo 18 est préférable.

**Important — Community vs Enterprise :**

Odoo Community fournit le socle comptable transactionnel (`account`) : factures, écritures, journaux, paiements, comptes, analytique et données comptables de base.

En revanche, il ne faut PAS considérer que Community fournit à elle seule toute la « comptabilité complète » visible dans Odoo Enterprise. Les rapports financiers avancés et certains outils de rapprochement nécessitent des compléments.

Pour répondre au besoin PO de **comptabilité complète/officielle en restant sur Community**, l'architecture du pilote doit combiner :

- Odoo 18 Community — socle `account`
- OCA `account_financial_report` — rapports financiers Community
- OCA `account_budget_oca` — budgets
- OCA `account_reconcile_oca` / `account_reconcile_model_oca` si le rapprochement natif s'avère insuffisant lors des tests

**Décision d'architecture :** Odoo 18 Community devient la version de référence pour NSS-ERP-02 V1.1.

---

## 4. Architecture générale

```
┌─────────────────────────────────────────────────┐
│                  ODOO 18 COMMUNITY              │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Contacts │  │ Projets  │  │ Comptabilité │  │
│  │res.partner│ │ project  │  │   account    │  │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │
│       │              │               │          │
│  ┌────┴──────────────┴───────────────┴───────┐  │
│  │           MODULE NSS (nss_network)        │  │
│  │  • Pays NSS (nss.country.membership)      │  │
│  │  • Coordination nationale                 │  │
│  │  • Adhésion organisation                  │  │
│  │  • Historique responsabilité              │  │
│  │  • Statistiques membres déclarés          │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────┐  ┌───────────┐  ┌─────────────┐  │
│  │   OCA    │  │   OCA     │  │    OCA      │  │
│  │ Budget   │  │ Analytique│  │ Projets ext │  │
│  └──────────┘  └───────────┘  └─────────────┘  │
└─────────────────────────────────────────────────┘
         │
    ┌────┴────┐
    │ PostgreSQL │
    └────┬────┘
    ┌────┴────┐
    │  Nginx  │ (reverse proxy + HTTPS)
    └────┬────┘
    ┌────┴────┐
    │   VPS   │ Hostinger
    └─────────┘
```

---

## 5. Mapping besoins → Odoo Community / OCA / spécifique

| Besoin fonctionnel | Solution | Module / mécanisme | Détail |
|---|---|---|---|
| **Annuaire organisations** | Odoo natif | `contacts` (`res.partner`) | Partners avec catégories/tags |
| **Annuaire personnes / responsables** | Odoo natif | `contacts` (`res.partner`) | Type = personne, lié à son organisation |
| **Pays NSS (statut, type, date entrée)** | **Spécifique NSS** | `nss.country.membership` | Étend `res.country` sans le modifier |
| **Coordination nationale** | **Spécifique NSS** | Champs sur `nss.country.membership` | Lien vers coordinatrice (res.partner) + org point focal (res.partner) |
| **Adhésion organisation** | **Spécifique NSS** | `nss.membership` | Statut, cotisation, dates, historique |
| **Statistiques membres déclarés** | **Spécifique NSS** | Champ sur `res.partner` (organisation) | Nombre déclaratif, date de déclaration |
| **Historique de responsabilité** | **Spécifique NSS** | `nss.responsibility.history` | Qui, quand, quelle fonction, période |
| **Projets** | Odoo natif | `project` | Projets avec tâches |
| **Activités / tâches** | Odoo natif | `project.task` | Tâches dans un projet, avec tags type |
| **Programmes** | Odoo natif | Tags ou champ parent sur `project.project` | Un programme = tag ou catégorie regroupant des projets |
| **Comptabilité générale transactionnelle** | Odoo natif | `account` | Plan comptable, journaux, écritures, factures, paiements |
| **Factures fournisseurs / dépenses** | Odoo natif | `account` (factures fournisseurs) | Saisie, validation, paiement |
| **Multi-devise** | Odoo natif | `account` | Activation dans paramètres |
| **Comptabilité analytique** | Odoo natif | `account` / analytique Odoo 18 | Dimensions : pays, projet, bailleur |
| **Budgets** | **OCA** | `account_budget_oca` (`OCA/account-budgeting`, 18.0) | Budgets analytiques + comparaison prévu/réalisé |
| **Partenaires / bailleurs** | Odoo natif | `contacts` (`res.partner`) | Tag « Bailleur » + champs |
| **Documents / pièces jointes** | Odoo natif | `mail` (chatter + attachments) | Pièce jointe sur tout enregistrement |
| **Utilisateurs / droits** | Odoo natif | `base` (groupes, règles d'accès) | Groupes + record rules par pays |
| **Reporting opérationnel** | Odoo natif | Vues pivot, graphiques, listes | Projets, contacts, données opérationnelles |
| **États financiers Community** | **OCA** | `account_financial_report` (`OCA/account-financial-reporting`, 18.0) | Rapports financiers à valider en TEST |

---

## 6. Modèle de données Odoo

### 6.1 Modèles natifs utilisés

**`res.partner`** — contact unifié Odoo

Utilisé pour :
- Organisations membres NSS (company = True)
- Personnes / responsables (company = False, parent_id = organisation)
- Bailleurs et partenaires
- Fournisseurs

Distinction par **catégories (tags)** :
- `Organisation NSS`
- `Bailleur`
- `Partenaire technique`
- `Fournisseur`

Champs personnalisés ajoutés par le module NSS :
- `nss_country_id` → lien vers `nss.country.membership`
- `nss_org_type` → sélection (AFR / fédération / ONG / coordination / point focal / autre)
- `nss_founding_member` → booléen

**`res.country`** — pays natif Odoo (non modifié)

Les 10 pays existent déjà dans `res.country`. Le module NSS crée un modèle lié plutôt que d'étendre `res.country` directement, pour éviter les conflits.

**`project.project`** — projet

Champs personnalisés ajoutés :
- `nss_country_membership_ids` → many2many vers `nss.country.membership` (pays NSS concernés)
- `nss_program_tag` → tag ou champ texte pour regroupement par programme
- `nss_funder_id` → many2one vers `res.partner` (bailleur principal)

**`project.task`** — activité / tâche

Champs personnalisés envisagés :
- `nss_activity_type` → sélection (formation / IEC / camp / atelier / plaidoyer / rencontre / autre)
- `nss_location` → char (lieu de l'activité)

**`account.move`** — écriture comptable / facture

Utilisé tel quel. Les dimensions analytiques (pays, projet, bailleur) sont portées par les plans analytiques natifs d'Odoo 17.

### 6.2 Modèles spécifiques NSS

**`nss.country.membership`** — Adhésion pays au mouvement

| Champ | Type | Description |
|---|---|---|
| `country_id` | Many2one → `res.country` | Pays |
| `status` | Selection | fondateur / extension / observation / archivé |
| `join_date` | Date | Date d'entrée dans le mouvement |
| `exit_date` | Date | Date de sortie éventuelle |
| `coordinator_id` | Many2one → `res.partner` | Coordinatrice / représentante nationale |
| `focal_org_id` | Many2one → `res.partner` | Organisation point focal |
| `active` | Boolean | Actif / archivé |
| `notes` | Text | Notes libres |
| `organization_ids` | One2many → `res.partner` | Organisations rattachées (via `nss_country_id`) |

**`nss.membership`** — Adhésion d'une organisation

| Champ | Type | Description |
|---|---|---|
| `organization_id` | Many2one → `res.partner` | Organisation |
| `status` | Selection | en_cours / active / expiree / suspendue / archivee |
| `application_date` | Date | Date de demande |
| `admission_date` | Date | Date d'adhésion effective |
| `last_renewal_date` | Date | Dernier renouvellement |
| `fee_due` | Monetary | Cotisation due |
| `fee_paid` | Monetary | Cotisation payée |
| `member_count_declared` | Integer | Nombre de membres déclaré |
| `member_count_date` | Date | Date de cette déclaration |
| `notes` | Text | |

**`nss.responsibility.history`** — Historique de responsabilité

| Champ | Type | Description |
|---|---|---|
| `partner_id` | Many2one → `res.partner` | Personne |
| `organization_id` | Many2one → `res.partner` | Organisation (ou pays via country membership) |
| `country_membership_id` | Many2one → `nss.country.membership` | Coordination pays (si applicable) |
| `role` | Char | Fonction exercée |
| `date_start` | Date | Début de fonction |
| `date_end` | Date | Fin de fonction |
| `is_current` | Boolean | Calculé : en poste actuellement |

---

## 7. Réseau NSS et coordinations

### Architecture Odoo

Le réseau NSS s'appuie sur :
1. **`res.partner`** pour les organisations et les personnes (modèle natif, pas de duplication)
2. **`nss.country.membership`** pour la couche « pays membre NSS » au-dessus de `res.country`
3. **`nss.responsibility.history`** pour tracer les changements de responsables dans le temps

### Navigation

- Vue liste des pays NSS → `nss.country.membership` tree/form
- Depuis un pays → voir la coordinatrice, l'org point focal, les organisations rattachées
- Depuis une organisation → voir son pays, ses responsables, ses adhésions, ses projets

### Pourquoi ne pas utiliser res.company

`res.company` dans Odoo représente une entité juridique/comptable. Les pays NSS ne sont pas des entités juridiques distinctes (du moins pas dans l'Option A centralisée). Créer un `nss.country.membership` séparé est plus propre et n'interfère pas avec la structure comptable.

---

## 8. Adhésions

### Architecture Odoo

Le module Odoo natif `membership` existe mais est conçu pour des adhésions individuelles (personne → produit d'adhésion). Il ne correspond pas bien au modèle NSS où des organisations adhèrent à un mouvement.

**Recommandation :** ne pas utiliser le module `membership` natif. Créer `nss.membership` dans le module spécifique NSS. C'est plus simple, plus lisible et sans dépendance inutile.

### Workflow d'adhésion [PROPOSITION]

```
Demande → En cours → Active → (Renouvellement → Active / Expirée)
                                    ↓
                              Suspendue → Archivée
```

La validation se fait par changement de statut. Pour le MVP, pas de workflow Odoo formel — un simple changement de champ `status` avec traçabilité dans le chatter suffit.

---

## 9. Projets et activités

### Architecture Odoo

Le module `project` natif couvre :
- Création de projets avec responsable, description, dates
- Tâches (= activités NSS) avec assignation, dates, étapes, tags
- Vues Kanban, liste, calendrier, Gantt (Gantt = Enterprise, mais liste/Kanban suffisent)
- Feuilles de temps (optionnel, probablement hors MVP)

### Mapping

| Concept NSS | Modèle Odoo | Mécanisme |
|---|---|---|
| Programme | Tag sur `project.project` | Un tag « Programme X » regroupe les projets du programme |
| Projet | `project.project` | Un enregistrement par projet |
| Activité | `project.task` | Une tâche par activité, avec type, lieu, dates |
| Pays du projet | Champ personnalisé `nss_country_membership_ids` | Many2many vers les pays membres NSS |
| Bailleur du projet | Champ personnalisé `nss_funder_id` | Many2one vers `res.partner` (tag Bailleur) |

### Alternative pour les programmes (Phase 2)

Si le besoin se confirme, un modèle `nss.program` pourrait regrouper les projets. Pour le MVP, le tag suffit et évite un modèle supplémentaire.

---

## 10. Comptabilité

### Principe corrigé : Community + OCA

Le besoin validé par le PO est une **comptabilité complète/officielle**. Odoo Community seul ne doit pas être présenté comme équivalent à l'application Comptabilité Enterprise.

### Socle Odoo 18 Community

Le module `account` sert de base pour :
- plan de comptes ;
- journaux ;
- écritures comptables ;
- factures clients et fournisseurs ;
- paiements ;
- taxes ;
- multi-devise ;
- comptes analytiques / distributions analytiques ;
- données bancaires et opérations de rapprochement de base.

### Compléments OCA requis ou à tester

| Besoin | Solution retenue |
|---|---|
| Rapports financiers complets Community | OCA `account_financial_report` — repo `OCA/account-financial-reporting`, branche 18.0 |
| Budgets | OCA `account_budget_oca` — repo `OCA/account-budgeting`, branche 18.0 |
| Rapprochement avancé si nécessaire | OCA `account_reconcile_oca` / `account_reconcile_model_oca` — repo `OCA/account-reconcile`, branche 18.0 |
| Immobilisations | À évaluer uniquement si NSS en a besoin ; OCA `account_asset_management` existe en 18.0 |

**Règle :** aucun de ces modules n'est installé en PROD avant validation fonctionnelle en TEST.

### Plan comptable

**[VALIDÉ PO — 24 septembre 2026] Pour le pilote TEST : `l10n_syscohada` + `l10n_sn`.**

Le siège NSS étant au Sénégal, le référentiel retenu pour le pilote est le SYSCOHADA révisé (`l10n_syscohada`) complété par la localisation Sénégal native (`l10n_sn`). Cette décision valide l'**utilisation technique en TEST** uniquement — elle ne constitue **pas** une validation de conformité comptable officielle. Avant PROD, la fonction comptable NSS devra confirmer que cette configuration répond réellement aux obligations comptables de l'organisation.

### Ghana / Gambie [VALIDÉ PO — 24 septembre 2026]

Ghana et Gambie ne sont pas couverts par `l10n_syscohada` (référentiels anglophones non-OHADA). Pour le MVP, ces deux pays restent gérés comme **dimensions opérationnelles/analytiques uniquement** (plan analytique « Pays », voir section 11) — aucune localisation comptable spécifique Ghana/Gambie n'est développée ni installée dans le MVP. Une réévaluation n'aura lieu en Phase 2 que si un besoin est confirmé.

### Configuration pilote

- **Société pilote [VALIDÉ PO — 24 septembre 2026] :** nom « NSS ERP TEST », pays Sénégal. Aucune donnée juridique réelle à ce stade (SIRET, RCCM, capital, etc.) ; les informations officielles seront validées avant PROD.
- **Devise principale [VALIDÉ PO — 24 septembre 2026] : XOF.**
- Multi-devise activé
- Journaux de test : achats, banque, caisse, opérations diverses
- Plans analytiques : Pays (dont Ghana/Gambie en analytique pur), Projet, Bailleur
- Rapports financiers : OCA
- Données comptables : 100 % fictives pendant le pilote
- **Exercice fiscal [VALIDÉ PO — 24 septembre 2026] : année civile, 1er janvier → 31 décembre.**

---

## 11. Comptabilité analytique et budgets

### Comptabilité analytique — Odoo 18

Odoo 18 permet d'utiliser plusieurs plans analytiques et des distributions analytiques. Cela permet d'affecter chaque écriture comptable à plusieurs dimensions simultanément.

**Plans analytiques proposés :**

| Plan | Comptes analytiques | Usage |
|---|---|---|
| **Pays** | BJ, BF, CI, GM, GH, GN, GW, ML, SN, TG | Ventilation géographique |
| **Projet** | Un compte par projet | Suivi budgétaire par projet |
| **Bailleur** | Un compte par bailleur | Reporting bailleur |

Chaque facture fournisseur / écriture peut être ventilée sur ces 3 dimensions simultanément.

Cela permet les reportings :
- Dépenses par pays
- Dépenses par projet
- Dépenses par bailleur
- Croisement pays × projet × bailleur

### Budgets — OCA

**Module : `account_budget_oca`**

- **Repo OCA :** `OCA/account-budgeting` (branche 18.0)
- **Fonction :** permet de définir des lignes budgétaires par compte analytique et par période, puis de comparer budget prévu vs réalisé
- **Dépendances :** `account`
- **Compatibilité 18.0 :** module disponible sur la branche 18.0 ; figer un commit/tag testé avant déploiement
- **Nécessité :** Odoo Community n'a plus de module budget natif depuis v16. Sans ce module OCA, le suivi budgétaire devrait se faire dans un tableur externe.

**Configuration budgets MVP :**

- Budget par projet (= par compte analytique projet)
- Montant prévu par période (trimestre ou année)
- Comparaison automatique avec les écritures réelles sur le même compte analytique

Budget par programme et budget par bailleur : Phase 2, quand les besoins seront affinés.

---

## 12. Partenaires et financements

### Partenaires — Odoo natif

Les bailleurs et partenaires techniques sont des `res.partner` avec le tag `Bailleur` ou `Partenaire technique`.

Champs utiles natifs :
- Nom, adresse, pays, contacts
- Notes internes
- Documents rattachés (chatter)

### Financements / conventions — Phase 2

Pour le MVP, le lien bailleur → projet se fait via le champ `nss_funder_id` sur le projet.

En Phase 2, un modèle `nss.funding` pourrait gérer :
- Convention avec montant, devise, dates, tranches
- Lien vers les projets financés
- Suivi décaissements vs prévisionnel
- Documents rattachés

---

## 13. Documents

### Odoo natif — chatter et pièces jointes

Chaque enregistrement Odoo (contact, projet, facture, etc.) dispose d'un chatter permettant :
- Pièces jointes (PDF, images, documents)
- Notes internes
- Log des modifications
- Suivi des échanges

**Pour le MVP, c'est suffisant.** Pas besoin de GED dédiée.

### Phase 2

Si nécessaire :
- OCA `document` ou `dms` pour une gestion documentaire centralisée avec catégories, tags, recherche
- Alertes d'expiration de conventions

---

## 14. Multi-devise

### Odoo natif

Activation dans Paramètres > Comptabilité > Multi-devise.

**Devises à configurer :**

| Devise | Code | Pays NSS | Remarque |
|---|---|---|---|
| Franc CFA UEMOA | XOF | BJ, BF, CI, ML, SN, TG | Devise principale |
| Franc CFA UEMOA | XOF | GW | Guinée-Bissau (UEMOA) |
| Cedi | GHS | GH | |
| Dalasi | GMD | GM | |
| Franc guinéen | GNF | GN | |
| Euro | EUR | — | Bailleurs européens |
| Dollar US | USD | — | Bailleurs américains |

**Taux de change :** Odoo peut mettre à jour les taux automatiquement via des services en ligne (BCE, etc.). Pour le MVP avec données fictives, des taux manuels suffisent.

**Note :** XOF est arrimé à l'EUR (1 EUR = 655,957 XOF), donc le taux est fixe. GHS, GMD et GNF ont des taux variables.

---

## 15. Droits et sécurité

### Groupes utilisateurs proposés

| Groupe | Accès | Nbr estimé |
|---|---|---|
| `NSS / Admin` | Tout accès, paramétrage, configuration | 1–2 |
| `NSS / Direction` | Lecture/écriture global, validations, comptabilité complète | 2–3 |
| `NSS / Finance` | Comptabilité, budgets, factures, paiements | 1–2 |
| `NSS / Coordination pays` | Organisations, contacts, activités de son pays | 10 (1/pays) |
| `NSS / Consultation` | Lecture seule sur périmètre autorisé | Variable |

### Règles d'accès par pays (record rules)

**Principe :** un utilisateur `Coordination pays` ne voit que les données de son pays.

Implémentation Odoo :
- Chaque utilisateur a un champ `allowed_nss_country_ids` (many2many vers `nss.country.membership`) pour permettre un ou plusieurs pays
- Des **record rules** filtrent :
  - `res.partner` : `nss_country_id = user.nss_country_id`
  - `project.project` : `nss_country_ids contains user.nss_country_id`
  - `nss.membership` : via l'organisation → pays
- Les groupes `Admin`, `Direction`, `Finance` ont accès global (pas de filtre pays)

### Données sensibles

- Les champs téléphone et email sont visibles uniquement par les groupes autorisés (record rules sur `res.partner` + champs `groups` sur les vues)
- Les données comptables sont restreintes aux groupes Finance, Direction, Admin

---

## 16. Comparatif mono-société vs multi-société

### Option A — Mono-société centralisée

**Description :** une seule société Odoo « NSS » basée à Dakar. Tous les pays, projets, dépenses sont gérés dans cette société unique. La ventilation géographique se fait par comptabilité analytique.

| Critère | Évaluation |
|---|---|
| **Simplicité** | Très simple. Un seul plan comptable, un seul exercice, une seule configuration. |
| **Comptabilité** | Plan comptable SYSCOHADA unique. Toutes les écritures sont centrales. |
| **Analytique** | Plan analytique « Pays » pour ventiler les dépenses/recettes par pays. |
| **Droits** | Record rules par pays sur les opérations non comptables. Pour la comptabilité, les record rules sont plus complexes (filtrer les écritures par analytique pays). |
| **Multi-devise** | Natif. Les factures en GHS, GMD, GNF sont converties en XOF. |
| **Reporting** | Simple : rapport analytique par pays/projet/bailleur. |
| **Migration future** | Passage vers multi-société possible mais implique une migration comptable significative. |
| **Limites** | Ne convient pas si un pays doit produire des états financiers locaux indépendants ou respecter un référentiel comptable différent. |
| **Complexité déploiement** | Faible |

### Option B — Multi-société

**Description :** une société « NSS Central » + des sociétés enfants par pays (ou par zone). Chaque société a son propre plan comptable et ses propres exercices.

| Critère | Évaluation |
|---|---|
| **Simplicité** | Complexe. Chaque société = plan comptable, journaux, exercice, configuration séparés. |
| **Comptabilité** | Chaque pays peut avoir son propre référentiel (SYSCOHADA pour UEMOA, IFRS pour Ghana/Gambie…). |
| **Analytique** | Toujours possible en complément. |
| **Droits** | Plus naturel : chaque utilisateur est affecté à sa société. Mais inter-société = complexité. |
| **Multi-devise** | Chaque société a sa devise locale comme devise de base. |
| **Reporting** | Consolidation nécessaire. Odoo Community ne propose PAS de consolidation multi-société native. Il faudrait OCA (`account_consolidation`) ou un développement. |
| **Migration future** | Architecture plus pérenne pour un réseau décentralisé. Mais plus lourde à maintenir. |
| **Limites** | 10 sociétés = 10 configurations comptables à maintenir. Excessif pour 10–20 utilisateurs avec données fictives. |
| **Complexité déploiement** | Élevée |

### Recommandation

**Pilote / MVP → Option A (mono-société) — [VALIDÉ PO 24 septembre 2026]**

Raisons :
1. 10–20 utilisateurs, données fictives → la complexité multi-société n'est pas justifiée
2. NSS est un mouvement, pas un groupe de 10 entreprises indépendantes
3. La comptabilité analytique multi-dimensions d'Odoo 17 couvre le besoin de ventilation par pays
4. L'équipe ERP est réduite ; maintenir 10 plans comptables est irréaliste au démarrage
5. Huit des dix pays NSS sont membres de l'OHADA ; le pilote central au Sénégal peut donc tester une base SYSCOHADA, sous réserve de validation comptable

**Trajectoire progressive :**

1. **MVP** — mono-société, analytique par pays
2. **Phase 2** — évaluer si un ou deux pays ont réellement besoin d'une comptabilité locale séparée (Ghana et Gambie, référentiels anglophones non-OHADA)
3. **Phase 3** — si besoin confirmé, créer des sociétés enfants pour ces pays uniquement, avec une solution de consolidation à évaluer (OCA ou autre) — ne pas présumer sa maturité avant test

Cette trajectoire ne ferme aucune porte : les comptes analytiques « pays » du MVP se transforment naturellement en sociétés séparées si nécessaire, car les données analytiques restent exploitables.

---

## 17. Architecture VPS Hostinger

### Hypothèses

- VPS Hostinger existant (Ubuntu probablement)
- Instance Odoo existante (à ne pas toucher)
- Ressources VPS : [À VALIDER PO — RAM, CPU, disque disponibles]

### Architecture cible

```
VPS Hostinger
├── Instance existante (inchangée)
│   ├── Odoo existant (port XXXX)
│   └── PostgreSQL DB existante
│
├── Instance NSS TEST
│   ├── Odoo 18.0 (port 8070)
│   ├── PostgreSQL DB : nss_test
│   └── Config : /etc/odoo/odoo-nss-test.conf
│
├── Instance NSS PROD (Phase 2)
│   ├── Odoo 18.0 (port 8071)
│   ├── PostgreSQL DB : nss_prod
│   └── Config : /etc/odoo/odoo-nss-prod.conf
│
├── Nginx (reverse proxy)
│   ├── nss-test.domaine.tld → localhost:8070
│   └── nss.domaine.tld → localhost:8071 (quand activé)
│
└── Sauvegardes
    └── Script cron : dump PostgreSQL + filestore
```

### Isolation

- **Utilisateur système dédié :** `odoo-nss` (pas le même que l'instance existante)
- **Base de données séparée :** `nss_test` / `nss_prod` dans le même PostgreSQL, mais rôle PostgreSQL dédié `odoo_nss` avec accès uniquement à ses bases
- **Répertoire filestore séparé :** `/opt/odoo-nss/filestore/`
- **Fichier de configuration séparé :** `/etc/odoo/odoo-nss-test.conf`
- **Service systemd séparé :** `odoo-nss-test.service`

### Prérequis techniques

| Composant | Version recommandée |
|---|---|
| Ubuntu | 22.04 LTS ou 24.04 LTS |
| Python | 3.10+ |
| PostgreSQL | 14+ (probablement déjà installé) |
| Nginx | dernière stable |
| Certificat HTTPS | Let's Encrypt via certbot |
| wkhtmltopdf | 0.12.6.1 (pour les rapports PDF Odoo) |

### Dimensionnement — à auditer avant installation

Ne pas retenir l'estimation « 512 Mo / 1 worker » comme dimensionnement de référence.

Le VPS héberge déjà d'autres services Odoo. Avant installation NSS, relever obligatoirement :
- vCPU ;
- RAM totale / RAM réellement libre ;
- swap ;
- espace disque libre ;
- version Ubuntu ;
- version PostgreSQL ;
- nombre d'instances/services Odoo déjà actifs ;
- consommation mémoire/CPU actuelle ;
- stratégie de sauvegarde existante.

**Pilote :** installer uniquement NSS TEST sur le VPS existant si l'audit confirme une marge suffisante.

**Production :** décider après le pilote si NSS PROD peut partager le VPS ou doit disposer d'un VPS dédié.

---

## 18. Environnements TEST / PROD

### Stratégie

| Environnement | Base de données | Port | Usage | Données |
|---|---|---|---|---|
| TEST | `nss_test` | 8070 | Configuration, développement, validation | Fictives uniquement |
| PROD | `nss_prod` | 8071 | Production réelle (Phase 2+) | Réelles après validation |

### Processus de déploiement

1. Toute modification est d'abord appliquée en TEST
2. Validation fonctionnelle par le PO en TEST
3. Reproduction contrôlée de la configuration en PROD ; ne pas dupliquer automatiquement une base TEST contenant des données fictives
4. Pas de développement directement en PROD

### Cycle MVP

Le MVP entier se déroule en TEST. Le passage en PROD n'intervient qu'après :
- Validation de tous les lots MVP
- Validation des droits d'accès
- Validation des sauvegardes
- Validation du processus de migration des données réelles

---

## 19. Sauvegardes et restauration

### Stratégie de sauvegarde

| Élément | Fréquence | Méthode | Rétention |
|---|---|---|---|
| Base PostgreSQL | Quotidienne | `pg_dump` compressé | 30 jours |
| Filestore | Quotidienne | `rsync` ou `tar` | 30 jours |
| Configuration Odoo | À chaque modification | Copie manuelle ou git | Indéfinie |

### Script de sauvegarde

Un script cron quotidien :
1. `pg_dump -Fc nss_test > /backup/nss_test_YYYYMMDD.dump`
2. `tar czf /backup/nss_filestore_YYYYMMDD.tar.gz /opt/odoo-nss/filestore/`
3. Suppression des sauvegardes > 30 jours
4. Copie externe chiffrée obligatoire avant mise en PROD (stockage objet, autre VPS ou équivalent)

### Restauration

```bash
pg_restore -d nss_test_restore /backup/nss_test_YYYYMMDD.dump
# + restauration du filestore correspondant
```

Test de restauration : obligatoire avant passage en production, puis périodique.

---

## 20. Modules OCA proposés

### MVP — modules à valider en TEST

| Module OCA | Repo | Branche | Fonction | Statut pour NSS |
|---|---|---|---|---|
| `account_budget_oca` | `OCA/account-budgeting` | 18.0 | Budgets analytiques / prévu vs réalisé | **Requis pour le MVP budgets** |
| `account_financial_report` | `OCA/account-financial-reporting` | 18.0 | Rapports financiers pour Community | **Requis pour la comptabilité officielle Community** |
| `account_reconcile_oca` | `OCA/account-reconcile` | 18.0 | Outils de rapprochement Community | À tester |
| `account_reconcile_model_oca` | `OCA/account-reconcile` | 18.0 | Modèles de rapprochement complémentaires | À tester |

### Modules à évaluer plus tard

- `account_asset_management` — si NSS doit gérer des immobilisations.
- DMS / GED avancée — Phase 2.
- Consolidation multi-société — uniquement si l'Option B devient réelle ; vérifier alors la maturité des modules au moment du besoin.

### Règle de sélection

Avant installation :
1. vérifier branche 18.0 et état du module ;
2. figer le commit/tag exact testé ;
3. lire les dépendances et migrations ;
4. tester installation et scénario NSS sur `nss_test` ;
5. documenter la version installée.

Aucun module OCA n'est ajouté « au cas où ».

---

## 21. Développements NSS minimums

### Décision définitive [VALIDÉ PO — 24 septembre 2026] : un addon unique `nss_network`

**Cette section annule et remplace la recommandation précédente (« petits modules séparés » `nss_core`/`nss_project`/`nss_account`), qui contredisait le choix structurant énoncé en section 1.** Le Product Owner tranche formellement en faveur d'un **addon Odoo unique : `nss_network`**.

Dépendances : `base`, `contacts`, `mail`, `project`, `account` (+ modules OCA validés le cas échéant).

Un addon unique ne signifie pas un modèle unique : `nss_network` peut contenir plusieurs modèles Python, vues, règles de sécurité et extensions internes, organisés en sous-répertoires (`models/`, `views/`, `security/`, `data/`) comme n'importe quel module Odoo. Il contient notamment :

- `nss.country.membership`
- `nss.membership`
- `nss.responsibility.history`
- extensions NSS de `res.partner` (organisation, personne)
- coordinatrice / organisation point focal
- statistiques déclaratives de membres
- extensions NSS de `project.project` / `project.task` (pays, bailleur, type/lieu d'activité)
- règles d'accès (record rules) par pays
- menus Réseau NSS
- groupes NSS de base
- données de démonstration fictives

**Règle associée [VALIDÉ PO] :** aucun autre addon spécifique NSS ne doit être créé sans nouvelle validation explicite du PO.

### Source unique pour les statistiques membres

Ne pas dupliquer `member_count` à la fois sur `res.partner` et `nss.membership`.

Pour le MVP, `nss.membership.member_count_declared` + `member_count_date` constituent la source de vérité.

### Hors MVP
- portail public ;
- membres individuels ;
- conventions/financements avancés ;
- consolidation multi-société ;
- automatisations non nécessaires ;
- import de données réelles.

---

## 22. Plan d'implémentation MVP

### Lot 0 — Infrastructure (prérequis)

- Installation Odoo 18 Community sur VPS Hostinger (instance NSS isolée)
- Configuration PostgreSQL, Nginx, HTTPS
- Mise en place des sauvegardes
- Création de la base `nss_test`
- Accès admin initial

**Dépendances :** accès VPS, ressources disponibles

### Lot 1 — Socle et réseau NSS

- Installation modules natifs : `contacts`, `project`
- Développement `nss_core` (modèles, vues, menus, droits)
- Configuration des tags partenaires (Organisation NSS, Bailleur, Partenaire technique)
- Chargement données fictives : 10 pays, 20 organisations fictives, coordinatrices fictives
- Test : navigation réseau, création organisations, historique responsabilité

**Dépendances :** Lot 0

### Lot 2 — Projets et activités

- Configuration module `project`
- Installation/développement léger de `nss_project`
- Configuration des étapes de tâches (tags activité)
- Chargement données fictives : 3 projets, 10 activités
- Test : création projet, ajout activités, lien pays/bailleur

**Dépendances :** Lot 1

### Lot 3 — Comptabilité et analytique

- Installation module `account`
- Configuration plan comptable (SYSCOHADA ou plan simplifié de test)
- Configuration société NSS, devise XOF, multi-devise
- Création des journaux (achats, banque, caisse, divers)
- Configuration des plans analytiques (Pays, Projet, Bailleur)
- Création des comptes analytiques (10 pays fictifs, projets fictifs, bailleurs fictifs)
- Chargement données fictives : factures fournisseurs, paiements
- Test : saisie facture, ventilation analytique, rapports

**Dépendances :** Lot 1 (pour les partenaires fournisseurs)

### Lot 4 — Budgets et reporting

- Installation OCA `account_budget_oca` (18.0, version figée/testée)
- Configuration budgets par projet (comptes analytiques)
- Saisie de budgets fictifs
- Test : comparaison budget vs réalisé
- Installation et validation OCA `account_financial_report` + rapports analytiques
- Vues pivot et graphiques pour le reporting de base

**Dépendances :** Lot 3

### Lot 5 — Droits, sécurité et validation

- Création des groupes utilisateurs NSS
- Configuration des record rules par pays
- Création des utilisateurs de test (1 admin, 2 direction, 1 finance, 3 coordination pays)
- Test : vérification que chaque rôle ne voit que ce qu'il doit voir
- Test de sauvegarde et restauration
- Documentation utilisateur minimale

**Dépendances :** Lots 1–4

### Résumé

| Lot | Contenu | Dépendances |
|---|---|---|
| 0 | Infrastructure | — |
| 1 | Socle + réseau NSS | Lot 0 |
| 2 | Projets / activités | Lot 1 |
| 3 | Comptabilité / analytique | Lot 1 |
| 4 | Budgets / reporting | Lot 3 |
| 5 | Droits / sécurité / validation | Lots 1–4 |

Les lots 2 et 3 peuvent être menés en parallèle après le lot 1.

---

## 23. Stratégie de tests avec données fictives

### Principe

Aucune donnée réelle NSS n'est utilisée pendant le MVP. Toutes les données sont inventées pour :
- Protéger les données personnelles réelles
- Permettre de casser et reconstruire sans risque
- Valider les processus avant de s'engager

### Jeu de données fictives

| Entité | Volume | Exemples |
|---|---|---|
| Pays NSS | 10 | Noms réels de pays (car publics), mais coordinations fictives |
| Organisations | 20 | « Association Test Bénin 1 », « Fédération Fictive Mali » |
| Personnes / contacts | 30 | Noms inventés |
| Projets | 3 | « Projet pilote agroécologie », « Formation semences 2026 » |
| Activités | 10 | « Atelier IEC Dakar », « Camp formation Ouaga » |
| Bailleurs | 3 | « Bailleur Test A », « Fondation Fictive B » |
| Factures fournisseurs | 10 | Montants fictifs en XOF et EUR |
| Budgets | 3 | Budgets par projet fictif |
| Utilisateurs | 7 | Comptes de test par rôle |

### Critères de passage en production

1. Tous les lots MVP sont fonctionnels en TEST
2. Les droits d'accès par pays sont validés
3. Les sauvegardes et restaurations sont testées
4. Le PO a validé les workflows (adhésion, dépense, projet)
5. Un plan de migration des données réelles est défini
6. Les utilisateurs réels sont formés

---

## 24. Risques techniques

| # | Risque | Impact | Probabilité | Mitigation |
|---|---|---|---|---|
| T01 | Incompatibilité/régression d'un module OCA 18.0 | Fonction concernée indisponible | Moyenne | Figer les versions testées et valider sur `nss_test` |
| T02 | VPS Hostinger insuffisant (RAM/CPU) pour 2 instances Odoo | Lenteur, crashs | Moyenne | Auditer les ressources avant installation. Option : VPS dédié NSS si nécessaire |
| T03 | Plan comptable SYSCOHADA pas disponible dans Odoo 17 pour le Sénégal | Configuration manuelle longue | Faible | Le localization package `l10n_sn` existe. Vérifier sa qualité. |
| T04 | Record rules par pays trop restrictives ou mal configurées | Utilisateurs ne voient pas ce qu'il faut, ou voient trop | Haute | Tests exhaustifs en Lot 5 avec des scénarios par rôle |
| T05 | Module `nss_network` mal architecturé | Maintenance difficile, bugs | Moyenne | Code review avant déploiement, tests unitaires |
| T06 | Perte de données (pas de sauvegarde) | Critique | Faible si sauvegardes en place | Sauvegardes quotidiennes, test de restauration |
| T07 | Instance existante impactée par l'installation NSS | Dommage collatéral | Faible si isolation respectée | Isolation stricte (utilisateur, DB, ports, service séparés) |
| T08 | Connectivité limitée pour les coordinatrices pays | Adoption faible | Haute | Interface légère Odoo, pas de fonctionnalité lourde. Évaluer mode offline en Phase 3 |
| T09 | Manque de compétences Odoo pour maintenance | Dépendance externe | Haute | Documenter tout, garder l'architecture simple, former 1–2 personnes |

---

## 25. Points à valider par le PO avant implémentation

| ID | Domaine | Situation actuelle | Décision nécessaire | Impact | Priorité |
|---|---|---|---|---|---|
| ARCH-01 | Version Odoo | **Recommandation corrigée : 18.0 Community** | Confirmer Odoo 18 pour le pilote | Compatibilité OCA / durée de support | CRITIQUE |
| ARCH-02 | Architecture comptable | Option A mono-société pour le pilote | **VALIDÉ PO 24/09/2026 : mono-société « NSS ERP TEST », Sénégal, données fictives** | Toute la configuration comptable | VALIDÉ |
| ARCH-03 | Plan comptable | Hypothèse SYSCOHADA / `l10n_sn` | **VALIDÉ PO 24/09/2026 : `l10n_syscohada` + `l10n_sn` pour le TEST — validation technique uniquement, pas de validation de conformité officielle avant PROD** | Configuration comptable | VALIDÉ (TEST) |
| ARCH-04 | Exercice fiscal | Hypothèse : année civile | **VALIDÉ PO 24/09/2026 : 1er janvier → 31 décembre** | Configuration comptable | VALIDÉ |
| ARCH-05 | Ressources VPS | Inconnues | Fournir : RAM totale, RAM disponible, CPU, disque disponible, OS, version PostgreSQL | Dimensionnement infrastructure | CRITIQUE |
| ARCH-06 | Domaine | Non défini | Quel sous-domaine pour l'ERP NSS ? (ex: nss-test.mondomaine.tld) | Configuration Nginx + HTTPS | HAUTE |
| ARCH-07 | Accès VPS | Non vérifié | Confirmer accès SSH root ou sudo pour l'installation | Déploiement | CRITIQUE |
| ARCH-08 | Instance existante | Le PO a demandé une instance NSS séparée | **Considéré validé : ne pas modifier l'instance existante ; créer NSS à côté après audit ressources** | Isolation | VALIDÉ |
| ARCH-09 | Devise principale | Hypothèse : XOF | **VALIDÉ PO 24/09/2026 : XOF** | Configuration comptable | VALIDÉ |
| ARCH-10 | Langue ERP | Hypothèse : français principal, anglais secondaire | Confirmer | Configuration i18n | MOYENNE |
| ARCH-11 | Catégories de dépenses | Non documenté | Fournir les catégories budgétaires / types de dépenses utilisés par NSS (même approximatifs) pour configurer le plan comptable et les budgets | Comptabilité + budgets | HAUTE |
| ARCH-12 | Workflow dépense | Non documenté | Valider ou ajuster le workflow proposé : saisie → justificatif → validation → paiement | Processus comptable | MOYENNE |
| ARCH-13 | Ghana / Gambie (comptabilité) | Non couverts par SYSCOHADA | **VALIDÉ PO 24/09/2026 : dimensions analytiques uniquement pour le MVP ; réévaluation en Phase 2 si besoin confirmé** | Configuration comptable | VALIDÉ |
| ARCH-14 | Licences OCA (AGPL-3) | `account_financial_report`, `account_reconcile_oca`, `account_reconcile_model_oca` identifiés en AGPL-3/LGPL-3 | **VALIDÉ PO 24/09/2026 : usage accepté pour l'environnement interne NSS TEST ; pas de modification ni redistribution hors projet sans nouvelle revue de licence** | Conformité licences | VALIDÉ |

---

## 26. Contrôle technique ChatGPT — V1.1

Corrections structurantes apportées :

1. **Odoo 17 → Odoo 18 Community** : Odoo 17 arrive en fin de support standard en septembre 2026.
2. **Community ≠ Enterprise complet** : les rapports financiers avancés ne doivent pas être supposés natifs en Community.
3. **Budget OCA corrigé** : `account_budget_oca` appartient à `OCA/account-budgeting`.
4. **Rapports financiers Community** : ajout de `account_financial_report`.
5. **Rapprochement** : ajout d'options OCA à tester.
6. **Modularité NSS** : `nss_core` + `nss_project` + `nss_account` si nécessaire. **[ANNULÉ — VALIDÉ PO 24 septembre 2026, voir section 21] :** le PO tranche pour un addon unique `nss_network`. Cette correction ChatGPT n°6 ne s'applique plus.
7. **Statistiques membres** : une seule source de vérité dans `nss.membership`.
8. **Droits pays** : plusieurs pays autorisés par utilisateur et gestion des partenaires globaux.
9. **VPS** : audit réel obligatoire avant installation ; suppression du dimensionnement trop optimiste.
10. **Sauvegardes** : copie hors VPS obligatoire avant PROD et restauration testée.
11. **TEST/PROD** : pas de duplication brute de la base fictive vers PROD.
12. **SYSCOHADA / Sénégal** : `l10n_sn` doit être testé et validé par la fonction comptable NSS.


---

*Fin du document NSS_ERP_02_ARCHITECTURE_ODOO.md*
