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
| `./config/odoo.local.conf` | bind mount (lecture seule) | Configuration Odoo NSS **réelle**, non versionnée (créée en LOT 1B à partir de `config/odoo.conf.example`) |
| `../../addons` | bind mount (lecture seule) | Modules NSS spécifiques (voir `addons/README.md`) |

Aucun volume générique : tous les noms sont préfixés `nss_` pour éviter
tout conflit avec d'autres projets (n8n, Odoo 19).

## 6. Réseau

Réseau Docker dédié `nss_test_net` (driver `bridge`), déclaré dans
`compose.yaml`. Seuls `nss-odoo` et `nss-db` communiquent entre eux, via
le nom de service interne (`nss-db:5432`) — jamais via le port PostgreSQL
de l'hôte.

`nss-db` déclare un `healthcheck` basé sur `pg_isready` ; `nss-odoo` a une
dépendance `condition: service_healthy` sur `nss-db`, en complément du
mécanisme `wait-for-psql` déjà présent dans l'entrypoint de l'image
officielle Odoo. `nss-odoo` ne démarre donc pas tant que PostgreSQL NSS
n'est pas prêt à accepter des connexions.

## 7. Variables nécessaires (`.env` et `odoo.local.conf`)

Deux fichiers non versionnés à créer avant tout démarrage, à partir des
templates fournis :

**a) `.env`** (copié depuis `.env.example`) — identifiants PostgreSQL
uniquement :

```
POSTGRES_DB=nss_test
POSTGRES_USER=nss_odoo
POSTGRES_PASSWORD=<mot de passe fort>
```

**b) `config/odoo.local.conf`** (copié depuis `config/odoo.conf.example`)
— configuration Odoo complète, avec en plus une ligne `admin_passwd` :

```
[options]
... (contenu identique à odoo.conf.example)
admin_passwd = <mot de passe fort, différent de POSTGRES_PASSWORD>
```

**Ni `.env` ni `config/odoo.local.conf` ne doivent jamais être commités.**
Ils sont ignorés par `.gitignore` :
- `.env`, `.env.*`, `**/.env` (avec exception explicite `!**/.env.example`)
- `**/odoo.local.conf`

Voir aussi section 6 (Secrets) de `NSS_ERP_04_LOT1_DOCKER_PREPARATION.md`
pour la justification de ce choix (pourquoi `admin_passwd` n'est plus
géré via `.env`/variable d'environnement, mais directement dans le
fichier de configuration Odoo).

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

## 9. Procédure future de démarrage (LOT 1B UNIQUEMENT — NON EXÉCUTÉ)

**Important :** une base PostgreSQL vide n'est pas une base Odoo
initialisée. Le premier démarrage doit suivre une séquence contrôlée
d'initialisation, pas un simple `docker compose up -d` global.

```bash
cd deploy/nss-test

# 0. Préparer les fichiers non versionnés
cp .env.example .env                              # éditer avec de vraies valeurs
cp config/odoo.conf.example config/odoo.local.conf # éditer : ajouter admin_passwd = <secret>

# 1. Valider la configuration Compose (syntaxe + interpolation)
docker compose config

# A. Démarrer UNIQUEMENT PostgreSQL NSS
docker compose up -d nss-db

# B. Attendre que PostgreSQL soit prêt (le healthcheck pg_isready du
#    service nss-db le garantit ; vérification manuelle possible) :
docker compose ps nss-db
# STATUS doit afficher "healthy" avant de continuer

# C. Initialisation Odoo contrôlée de la base nss_test : module `base`
#    uniquement, sans données de démonstration, arrêt automatique après
#    initialisation (ne démarre pas le serveur web) :
docker compose run --rm nss-odoo \
  odoo --config /etc/odoo/odoo.conf \
       -d nss_test -i base --without-demo=all --stop-after-init

# D. Seulement après succès de l'étape C, démarrer nss-odoo normalement :
docker compose up -d nss-odoo
docker compose ps
docker compose logs -f nss-odoo
```

Cette séquence (A → B → C → D) est documentée ici pour préparation du
LOT 1B ; **aucune de ces commandes n'a été exécutée dans ce lot**.

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
- Aucun secret réel dans le dépôt Git : `config/odoo.conf.example` (versionné)
  ne contient ni mot de passe PostgreSQL ni `admin_passwd`. Le mot de passe
  PostgreSQL est fourni via `.env` (non versionné) ; `admin_passwd` est
  défini directement dans `config/odoo.local.conf` (non versionné, créé en
  LOT 1B à partir du template).
- `list_db = False` et `dbfilter` restreignent Odoo à la seule base
  `nss_test` : pas de sélecteur de base exposé publiquement.
- Aucune image, configuration ou volume ne référence l'Odoo 19 existant,
  ses bases, PostgreSQL système, ou les conteneurs n8n.
- Avant tout passage en production, revoir le tag d'image (`odoo:18.0`
  et `postgres:16` sont des tags flottants) : figer une version précise
  testée, conformément à `NSS_ERP_02` (règle de sélection des versions).
