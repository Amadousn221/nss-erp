# NSS ERP — LOT 1A Docker Preparation

**Référence :** NSS_ERP_04
**Date :** 24 septembre 2026
**Auteur :** Claude Code (préparation technique)
**Statut :** préparation locale versionnée — **rien n'a été déployé sur le VPS**
**Prérequis :** NSS_ERP_02 (architecture), NSS_ERP_03 (audit VPS + architecture d'isolation Docker validée PO)

---

## 1. Objectif

Préparer et versionner, sans toucher au VPS, l'architecture Docker Compose
du pilote NSS ERP TEST : Odoo 18 Community + PostgreSQL 16, isolés
strictement de l'Odoo 19 existant, de ses bases clientes, de PostgreSQL
système et des conteneurs n8n déjà présents sur le VPS.

Ce lot (1A) ne fait que créer des fichiers dans ce dépôt Git. Aucune
connexion SSH n'a été effectuée, aucun conteneur n'a été démarré, aucune
installation n'a eu lieu.

---

## 2. Architecture

Deux conteneurs, un réseau Docker dédié, deux volumes nommés dédiés,
aucune ressource partagée avec l'existant :

```
nss_test_net (réseau Docker dédié)
├── nss-db    (postgres:16)   — volume nss_pg_data, aucun port publié
└── nss-odoo  (odoo:18.0)     — volume nss_odoo_data
                                 + bind mounts : config/odoo.conf (ro),
                                   addons/ (ro)
                               — publié sur 127.0.0.1:8070 uniquement
```

Cette architecture reprend et opérationnalise la section « Architecture
d'isolation validée pour LOT 1 » de `NSS_ERP_03_AUDIT_VPS_HOSTINGER.md`.

---

## 3. Services

| Service | Image | Rôle |
|---|---|---|
| `nss-db` | `postgres:16` | PostgreSQL dédié à NSS TEST |
| `nss-odoo` | `odoo:18.0` | Odoo 18 Community, dépend de `nss-db` |

Détail complet (variables, healthcheck implicite via `depends_on`,
commande de démarrage) dans `deploy/nss-test/compose.yaml`.

---

## 4. Réseau

Réseau Docker dédié `nss_test_net` (driver `bridge`), déclaré dans
`compose.yaml`. Seuls `nss-odoo` et `nss-db` y sont rattachés.
`nss-odoo` s'adresse à `nss-db` uniquement par son nom de service
interne (`nss-db:5432`). Aucune connexion vers les réseaux Docker
utilisés par n8n, ni vers l'interface réseau native de PostgreSQL
système (`127.0.0.1:5432` sur l'hôte).

---

## 5. Volumes

| Volume | Type | Contenu | Partagé avec l'existant ? |
|---|---|---|---|
| `nss_pg_data` | volume Docker nommé | Données PostgreSQL NSS | Non |
| `nss_odoo_data` | volume Docker nommé | `data_dir` Odoo (filestore, sessions) | Non |
| `deploy/nss-test/config/odoo.conf` | bind mount (ro) | Config Odoo NSS | Non |
| `addons/` | bind mount (ro) | Modules NSS spécifiques | Non |

Noms explicitement préfixés `nss_` pour exclure tout conflit avec un
volume existant (n8n, Odoo 19).

---

## 6. Secrets

Aucun secret réel n'est présent dans ce dépôt. Stratégie retenue :

| Secret | Où il est défini | Où il est injecté |
|---|---|---|
| `POSTGRES_PASSWORD` | `.env` (non versionné, local au VPS) | Variables d'environnement des deux conteneurs (`nss-db` via `POSTGRES_PASSWORD`, `nss-odoo` via `PASSWORD`) |
| `ODOO_ADMIN_PASSWD` | `.env` (non versionné) | Argument de démarrage du conteneur `nss-odoo` (`--admin_passwd=${ODOO_ADMIN_PASSWD}`), interpolé par Docker Compose depuis `.env` au moment de la résolution de `compose.yaml` |

`deploy/nss-test/.env.example` ne contient que des placeholders
(`CHANGE_ME`). Le vrai fichier `.env` est ignoré par `.gitignore`
(`.env`, `.env.*`, `**/.env`).

**Limite documentée de la méthode `admin_passwd` :** l'image officielle
Odoo n'expose pas de variable d'environnement dédiée pour `admin_passwd`
(contrairement à la connexion PostgreSQL). La valeur passe donc par un
argument de la commande du conteneur, interpolé côté hôte par Docker
Compose. Elle n'apparaît jamais dans un fichier versionné (`odoo.conf`
en est dépourvu), mais reste visible via `docker inspect` / `docker
compose config` sur le VPS lui-même. Ce compromis est jugé acceptable
pour un pilote TEST à données fictives ; il devra être revu avant une
éventuelle PROD (ex. Docker secrets, ou génération de `odoo.conf` à la
volée depuis un gestionnaire de secrets).

---

## 7. Ports

| Port hôte | Port conteneur | Service | Exposition |
|---|---|---|---|
| `127.0.0.1:8070` | `8069` | `nss-odoo` | localhost du VPS uniquement |
| *(aucun)* | `5432` | `nss-db` | interne au réseau Docker uniquement |

Port `8070` confirmé libre lors de l'audit LOT 0 (`NSS_ERP_03` section
9). Aucun conflit avec les ports déjà utilisés sur le VPS (22, 80, 443,
5432 natif, 5678/5679 n8n, 8069 Odoo 19).

---

## 8. Isolation avec Odoo 19

- Aucune image, aucun volume, aucune variable d'environnement de
  `compose.yaml` ne référence `/etc/odoo/`, `/var/lib/odoo`,
  `/usr/lib/python3/dist-packages/odoo` (chemins natifs de l'Odoo 19
  existant identifiés en LOT 0), ni le service `odoo.service`.
- `nss-odoo` utilise une image Docker officielle (`odoo:18.0`),
  totalement indépendante du paquet système `apt odoo` (19.0) déjà
  installé sur l'hôte.
- Le port `8070` (NSS) est distinct du port `8069` (Odoo 19 existant) ;
  aucun risque de collision.
- Aucune commande de ce lot n'a touché `odoo.service`, sa configuration,
  ni ses logs.

---

## 9. Isolation avec n8n

- `nss_test_net` est un réseau Docker **distinct** des réseaux utilisés
  par les conteneurs `n8n` et `n8n-connect` (identifiés en LOT 0,
  exposés uniquement sur `127.0.0.1:5678`/`5679`).
- Aucun volume, port ou variable d'environnement partagé avec n8n.
- `docker compose down` sur le projet `nss-test` n'a aucun effet sur les
  conteneurs n8n existants (projets Compose distincts).

---

## 10. PostgreSQL NSS

- Conteneur dédié `nss-db` (image `postgres:16`), **distinct** du
  cluster PostgreSQL natif `16-main` identifié en LOT 0.
- Base unique `nss_test`, utilisateur dédié `nss_odoo` (nom réel défini
  via `.env`, `POSTGRES_USER`).
- Aucun port publié sur l'hôte : accès uniquement depuis `nss-odoo` via
  le réseau Docker interne.
- Aucune requête, connexion ou configuration de ce lot ne touche au
  cluster PostgreSQL natif ni aux 3 bases clientes existantes.

---

## 11. Odoo 18 NSS

- Image officielle `odoo:18.0` (Community).
- Configuration dédiée (`deploy/nss-test/config/odoo.conf`), montée en
  lecture seule, sans secret.
- `list_db = False` et `dbfilter = ^nss_test$` : une seule base
  accessible, pas de sélecteur de base exposé.
- `without_demo = all` : pas de données de démonstration Odoo — seules
  des données fictives NSS définies par l'équipe projet seront chargées,
  dans un lot ultérieur.
- `workers = 0` : mode mono-processus, adapté à un pilote à faible
  charge (cf. estimation de ressources `NSS_ERP_03`).
- `addons_path` combine les addons natifs de l'image et
  `/mnt/extra-addons` (répertoire `addons/` du dépôt, actuellement vide
  — voir `addons/README.md`).

---

## 12. Validation locale

Docker n'est **pas installé** sur le poste de travail local utilisé pour
ce lot (`docker`, `docker compose` : commande introuvable). Conformément
à la consigne (« si Docker n'est pas installé localement : ne l'installe
pas »), aucune installation n'a été tentée.

Validation effectuée à la place :

- **Relecture manuelle** de `compose.yaml` (indentation YAML,
  cohérence des noms de services/volumes/réseaux, absence de tabulations,
  correspondance entre les chemins montés et l'arborescence réelle du
  dépôt).
- **Vérification des chemins relatifs** : `./config/odoo.conf` et
  `../../addons` résolus depuis `deploy/nss-test/` pointent bien vers
  `deploy/nss-test/config/odoo.conf` et `addons/` à la racine du dépôt.
- **Recherche de secrets** : aucun mot de passe, token ou clé dans
  `compose.yaml`, `odoo.conf`, ou tout fichier versionné de ce lot
  (recherche manuelle + relecture ligne par ligne).
- **Recherche de références à l'existant** : aucune occurrence de
  `odoo.service`, `/etc/odoo`, `16-main`, `5432` (hôte), `5678`, `5679`,
  ou des noms de bases clientes identifiés en LOT 0, dans les fichiers
  créés.
- **Vérification des ports** : `8070` (NSS) ne recoupe aucun port déjà
  utilisé sur le VPS d'après l'audit LOT 0 (22, 80, 443, 5432, 5678,
  5679, 8069).

**Aucune commande Docker n'a été exécutée** (ni `docker compose config`,
ni `up`, ni `pull`), faute d'environnement Docker disponible localement,
conformément à la consigne de ne pas installer Docker pour ce lot. La
validation `docker compose config` reste à faire en LOT 1B, sur le VPS
ou un poste disposant de Docker, avant tout `docker compose up`.

---

## 13. Risques

| # | Risque | Impact | Mitigation |
|---|---|---|---|
| R1 | `docker compose config` non exécuté (Docker indisponible localement) | Une erreur de syntaxe YAML pourrait ne pas être détectée avant LOT 1B | Exécuter `docker compose config` en tout premier lieu en LOT 1B, avant tout `up` |
| R2 | Tags d'image flottants (`odoo:18.0`, `postgres:16`) | Une mise à jour amont de l'image pourrait changer le comportement entre deux déploiements | Documenté en section 9 du README ; figer une version précise avant PROD |
| R3 | Secret `admin_passwd` visible via `docker inspect`/`compose config` sur le VPS | Exposition limitée au VPS lui-même (pas dans Git) | Acceptable pour un pilote TEST à données fictives ; à revoir avant PROD (section 6) |
| R4 | Absence de `docker compose config` validé signifie que des erreurs de référence (nom de service, variable manquante) ne sont pas garanties absentes | Échec au démarrage en LOT 1B | Premier test en LOT 1B sur environnement isolé, avant toute donnée réelle |

---

## 14. Prérequis LOT 1B

1. Valider `docker compose config` (syntaxe + interpolation des
   variables) — nécessite un environnement avec Docker (VPS ou poste
   avec Docker installé).
2. Créer le fichier `.env` réel (non versionné) à partir de
   `.env.example`, avec de vrais mots de passe forts, différents de
   toute valeur utilisée ailleurs sur le VPS.
3. Décision PO sur le sous-domaine NSS TEST (ARCH-06, déjà ouvert dans
   `NSS_ERP_02` et rappelé dans `NSS_ERP_03`) — nécessaire avant la
   configuration Nginx (hors LOT 1B).
4. Confirmation PO explicite avant tout `docker compose up` sur le VPS.
5. Mise en place du script de sauvegarde dédié NSS (voir ci-dessous),
   à préparer en parallèle du LOT 1B, avant toute donnée même fictive
   durable.

### Stratégie de sauvegarde future (documentée, non implémentée)

Comme relevé en LOT 0 (`NSS_ERP_03` section 10), aucune sauvegarde
n'existe sur le VPS pour quelque base que ce soit. Pour NSS TEST, la
stratégie future (à mettre en œuvre en LOT 1B ou juste après) sera :

- `docker compose exec nss-db pg_dump -U <user> nss_test` → dump
  compressé, en cron dédié NSS.
- Sauvegarde du volume `nss_odoo_data` (filestore) via `docker run
  --rm -v nss_odoo_data:/data ... tar czf ...`.
- Versionnement de `deploy/nss-test/` (config, compose, addons) déjà
  assuré par ce dépôt Git — pas d'action supplémentaire nécessaire pour
  cette partie.
- Copie chiffrée vers un stockage externe au VPS avant toute donnée
  réelle ou tout passage en PROD (conforme à `NSS_ERP_02` section 19).
- Cette sauvegarde NSS reste **indépendante** de toute sauvegarde de
  l'Odoo 19 existant (qui n'en a pas non plus).

---

## 15. Fichiers qui seront créés sur le VPS

Aucun fichier n'a été créé sur le VPS dans ce lot. En LOT 1B, le
déploiement créera (sur le VPS uniquement, après copie du contenu de
`deploy/nss-test/` et `addons/`) :

- des conteneurs Docker `nss_test_db` et `nss_test_odoo` ;
- un réseau Docker `nss_test_net` ;
- des volumes Docker `nss_pg_data` et `nss_odoo_data` (gérés par Docker,
  physiquement sous `/var/lib/docker/volumes/` par défaut) ;
- un fichier `.env` réel (non versionné), local au répertoire de
  déploiement choisi sur le VPS (ex. `/opt/nss-test/.env` ou équivalent
  — chemin exact à confirmer en LOT 1B).

Aucun de ces éléments n'existe à ce jour.

---

## 16. Commandes prévues pour LOT 1B

**Documentées ici pour préparation — non exécutées dans ce lot.**

```bash
# Sur le VPS, après copie du contenu de deploy/nss-test/ et addons/ :
cd /opt/nss-test   # chemin exact à confirmer en LOT 1B
cp .env.example .env
# éditer .env avec de vrais mots de passe forts

docker compose config          # validation syntaxe + interpolation
docker compose up -d           # démarrage (uniquement après validation PO)
docker compose ps
docker compose logs -f nss-odoo
```

Arrêt (également LOT 1B, documenté seulement) :

```bash
docker compose down            # conserve les volumes
# docker compose down -v       # supprime aussi les volumes — jamais sans confirmation PO explicite
```

---

*Fin du document NSS_ERP_04_LOT1_DOCKER_PREPARATION.md*
