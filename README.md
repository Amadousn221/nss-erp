# NSS ERP

Projet ERP pour **Nous Sommes la Solution (NSS)**, mouvement panafricain de femmes rurales présent dans 10 pays d'Afrique de l'Ouest.

## État du projet

**Implémentation en cours sur l'environnement de test NSS ERP TEST (LOT 2B), checkpoint par checkpoint, sous validation explicite du Product Owner.** Le module `nss_network` est installé sur `nss_test` (Odoo 18 Community, PostgreSQL 16, Docker, VPS Hostinger) ; le Checkpoint 4A (UX et filtres métier) y est déployé (20 octobre 2026). Aucune donnée métier NSS n'est encore chargée (liste « Pays NSS » vide) ; aucun déploiement de production n'est engagé. Le journal détaillé de chaque checkpoint est dans `docs/implementation/` (dernier : `NSS_ERP_12`, prochain : `NSS_ERP_13`).

## Documents

- [`CLAUDE.md`](./CLAUDE.md) — règles de fonctionnement pour Claude Code sur ce projet.
- [`docs/NSS_ERP_00_RECHERCHE_PAYS_2026.md`](./docs/NSS_ERP_00_RECHERCHE_PAYS_2026.md) — recherche sur l'implantation géographique de NSS.
- [`docs/NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md`](./docs/NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md) — audit des processus et besoins métier.
- [`docs/NSS_ERP_02_ARCHITECTURE_ODOO.md`](./docs/NSS_ERP_02_ARCHITECTURE_ODOO.md) — architecture technique Odoo proposée.
- [`docs/implementation/`](./docs/implementation/) — journal d'implémentation (audit VPS, déploiement NSS TEST, module `nss_network`, checkpoints) : `NSS_ERP_03` à `NSS_ERP_13`.
  - [`NSS_ERP_12`](./docs/implementation/NSS_ERP_12_LOT2B_CHECKPOINT4A_DEPLOIEMENT.md) — Checkpoint 4A : déploiement et clôture.
  - [`NSS_ERP_13`](./docs/implementation/NSS_ERP_13_LOT2B_CHECKPOINT5_PAYS_NSS_PREPARATION.md) — préparation de l'intégration des 10 pays NSS (aucune donnée chargée).

## Solution envisagée

Odoo 18 Community, complété par des modules OCA si nécessaire, avec du développement spécifique NSS limité au strict minimum (réseau des pays/organisations, adhésions, historisation des responsabilités).

## Décision de référence

La liste officielle des pays NSS pour l'ERP est fixée à **10 pays** (décision PO du 23 septembre 2026), mais reste une donnée dynamique : le code ne doit jamais coder ce nombre en dur.
