# NSS ERP

Projet ERP pour **Nous Sommes la Solution (NSS)**, mouvement panafricain de femmes rurales présent dans 10 pays d'Afrique de l'Ouest.

## État du projet

**Phase de recherche et d'audit fonctionnel.** L'architecture technique (`NSS_ERP_02`) est rédigée mais pas encore validée par le Product Owner : aucune installation, configuration ou développement de l'ERP ne doit démarrer avant cette validation (voir `CLAUDE.md`, section 2).

## Documents

- [`CLAUDE.md`](./CLAUDE.md) — règles de fonctionnement pour Claude Code sur ce projet.
- [`docs/NSS_ERP_00_RECHERCHE_PAYS_2026.md`](./docs/NSS_ERP_00_RECHERCHE_PAYS_2026.md) — recherche sur l'implantation géographique de NSS.
- [`docs/NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md`](./docs/NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md) — audit des processus et besoins métier.
- [`docs/NSS_ERP_02_ARCHITECTURE_ODOO.md`](./docs/NSS_ERP_02_ARCHITECTURE_ODOO.md) — architecture technique Odoo proposée.

## Solution envisagée

Odoo 18 Community, complété par des modules OCA si nécessaire, avec du développement spécifique NSS limité au strict minimum (réseau des pays/organisations, adhésions, historisation des responsabilités).

## Décision de référence

La liste officielle des pays NSS pour l'ERP est fixée à **10 pays** (décision PO du 23 septembre 2026), mais reste une donnée dynamique : le code ne doit jamais coder ce nombre en dur.
