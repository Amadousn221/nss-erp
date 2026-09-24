# NSS ERP TEST — Déploiement Docker Compose

**Statut : préparation (LOT 1A) — non déployé.** Ce répertoire contient la
définition de l'environnement Docker Compose pour le pilote NSS ERP TEST.
Aucune commande de ce document n'a été exécutée sur le VPS à ce stade.
Le démarrage effectif relève du LOT 1B, après validation du Product Owner.

## 1. Objectif

Fournir un environnement Odoo 18 Community + PostgreSQL 16 pour le pilote
NSS ERP, **totalement isolé** de l'Odoo 19 existant, de ses 3 bases
clientes, du PostgreSQL système et des conteneurs n8n déjà présents sur
le VPS (voir `docs/implementation/NSS_ERP_03_AUDIT_VPS_HOSTINGER.md`).

Uniquement des données fictives seront utilisées (conformément à
`NSS_ERP_02` §23) — aucune donnée réelle NSS.

## 2. Architecture

```
┌─────────────────────────────────────────────┐
│              VPS Hostinger                   │
│                                               │
│  Existant (non touché)     NSS TEST (nouveau)│
│  ┌──────────────┐          ┌───────────────┐ │
│  │ Odoo 19 (apt)│          │ nss-odoo      │ │
│  │ :8069 (0.0.0.0)         │ (odoo:18.0)   │ │
│  └──────┬───────┘          │ 127.0.0.1:8070│ │
│         │                  └───────┬───────┘ │
│  ┌──────┴───────┐                  │         │
│  │ PostgreSQL 16│          ┌───────┴───────┐ │
│  │ natif (5432) │          │ nss-db        │ │
│  │ 3 bases      │          │ (postgres:16) │ │
│  │ clientes     │          │ pas de port   │ │
│  └──────────────┘          │ publié        │ │
│                             └───────────────┘ │
│  n8n (Docker, réseau propre) — sans lien      │
│                                               │
│  Nginx existant — utilisé plus tard en        │
│  reverse proxy pour NSS (non configuré ici)  │
└─────────────────────────────────────────────┘
```

Réseau Docker dédié `nss_test_net` : seuls `nss-odoo` et `nss-db` y sont
rattachés. Aucune connexion vers les réseaux Docker de n8n, ni vers le
PostgreSQL natif de l'hôte.

## 3. Services

| Service | Image | Rôle |
|---|---|---|
| `nss-db` | `postgres:16` | Base de données PostgreSQL dédiée NSS TEST |
| `nss-odoo` | `odoo:18.0` | Application Odoo 18 Community |

## 4. Ports

| Port hôte | Port conteneur | Service | Exposition |
|---|---|---|---|
| `127.0.0.1:8070` | `8069` | `nss-odoo` | localhost du VPS uniquement |
| *(aucun)* | `5432` | `nss-db` | aucune — accessible uniquement via le réseau Docker interne |

Le port `8070` a été confirmé libre sur le VPS lors de l'audit LOT 0
(`NSS_ERP_03`, section 9).

## 5. Volumes

| Volume | Type | Contenu |
|---|---|---|
| `nss_pg_data` | volume Docker nommé | Données PostgreSQL NSS |
| `nss_odoo_data` | volume Docker nommé | `data_dir` Odoo (filestore, sessions) |
| `./config/odoo.conf` | bind mount (lecture seule) | Configuration Odoo NSS |
| `../../addons` | bind mount (lecture seule) | Modules NSS spécifiques (voir `addons/README.md`) |

Aucun volume générique : tous les noms sont préfixés `nss_` pour éviter
tout conflit avec d'autres projets (n8n, Odoo 19).

## 6. Réseau

Réseau Docker dédié `nss_test_net` (driver `bridge`), déclaré dans
`compose.yaml`. Seuls `nss-odoo` et `nss-db` communiquent entre eux, via
le nom de service interne (`nss-db:5432`) — jamais via le port PostgreSQL
de l'hôte.

## 7. Variables nécessaires (`.env`)

Copier `.env.example` en `.env` (même répertoire) et renseigner de
vraies valeurs avant tout démarrage :

```
POSTGRES_DB=nss_test
POSTGRES_USER=nss_odoo
POSTGRES_PASSWORD=<mot de passe fort>
ODOO_ADMIN_PASSWD=<mot de passe fort>
```

**`.env` ne doit jamais être commité.** Il est ignoré par `.gitignore`
(`.env`, `.env.*`, `**/.env`).

## 8. Comment valider la configuration (sans démarrer)

Depuis ce répertoire (`deploy/nss-test/`), une fois `.env` créé :

```bash
docker compose config
```

Cette commande valide la syntaxe YAML et affiche la configuration
résolue (variables interpolées), **sans démarrer aucun conteneur**.

En LOT 1A, cette validation a été faite par relecture manuelle
(Docker non installé sur le poste local) — voir
`docs/implementation/NSS_ERP_04_LOT1_DOCKER_PREPARATION.md` section 12
pour le détail.

## 9. Procédure future de démarrage (LOT 1B — non exécutée ici)

```bash
cd deploy/nss-test
cp .env.example .env        # puis éditer .env avec de vraies valeurs
docker compose config       # validation
docker compose up -d        # démarrage (LOT 1B uniquement, après validation PO)
docker compose ps
docker compose logs -f nss-odoo
```

## 10. Procédure future d'arrêt (LOT 1B — non exécutée ici)

```bash
cd deploy/nss-test
docker compose down          # arrête et supprime les conteneurs, garde les volumes
# docker compose down -v     # ⚠️ supprime aussi les volumes (données) — ne jamais
                              # utiliser sans confirmation explicite du PO
```

## 11. Sécurité

- PostgreSQL NSS n'est **jamais** exposé sur l'hôte ni sur Internet : accès
  uniquement via le réseau Docker interne depuis `nss-odoo`.
- Odoo NSS est publié uniquement sur `127.0.0.1:8070` : pas d'accès direct
  depuis Internet tant que le reverse proxy Nginx n'est pas configuré
  (lot ultérieur, hors LOT 1A).
- Aucun secret réel dans le dépôt Git : `odoo.conf` ne contient ni mot de
  passe PostgreSQL ni `admin_passwd` ; ceux-ci sont injectés au démarrage
  du conteneur via `.env` (non versionné).
- `list_db = False` et `dbfilter` restreignent Odoo à la seule base
  `nss_test` : pas de sélecteur de base exposé publiquement.
- Aucune image, configuration ou volume ne référence l'Odoo 19 existant,
  ses bases, PostgreSQL système, ou les conteneurs n8n.
- Avant tout passage en production, revoir le tag d'image (`odoo:18.0`
  et `postgres:16` sont des tags flottants) : figer une version précise
  testée, conformément à `NSS_ERP_02` (règle de sélection des versions).
