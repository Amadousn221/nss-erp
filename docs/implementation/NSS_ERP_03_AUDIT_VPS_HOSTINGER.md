# NSS ERP — Audit VPS Hostinger

**Référence :** NSS_ERP_03
**Date :** 24 septembre 2026
**Auteur :** Claude Code (audit technique)
**Statut :** audit en lecture seule — aucune modification apportée au VPS
**Prérequis :** NSS_ERP_02 V1.1 (architecture proposée, non encore installée)

---

## 1. Résumé exécutif

Le VPS Hostinger cible est un serveur Ubuntu 24.04 LTS déjà en production, hébergeant **une instance Odoo 19.0 Community existante** (installée via paquet système `apt`, et non en environnement isolé) qui sert **trois bases de données clients tierces réelles**, ainsi qu'un service **n8n** (automatisation, via Docker) pour d'autres domaines. Ce VPS n'est donc pas un serveur vide : c'est une infrastructure de production partagée avec des tiers, sans lien avec NSS.

Les ressources disponibles (CPU, RAM, disque) sont largement suffisantes pour héberger une instance NSS TEST légère à côté de l'existant. En revanche, plusieurs conditions doivent être respectées avant toute installation :

- l'instance existante tourne en **Odoo 19.0**, pas 18.0 comme prévu dans `NSS_ERP_02` — l'installation d'un Odoo 18.0 séparé devra se faire par une méthode qui n'entre pas en conflit avec le paquet système `odoo` déjà installé (environnement virtuel Python dédié ou conteneur, pas un second paquet `apt`) ;
- **aucune sauvegarde automatisée n'existe actuellement** sur ce VPS pour les bases Odoo/PostgreSQL — NSS devra mettre en place sa propre stratégie de sauvegarde de façon autonome, sans compter sur une infrastructure existante ;
- des lacunes de sécurité préexistantes ont été observées (connexion root SSH autorisée, authentification par mot de passe active, absence de fail2ban, port Odoo exposé directement sur toutes les interfaces) — ces points ne concernent pas NSS à l'origine et ne doivent pas être corrigés dans le cadre de ce projet, mais doivent être connus du PO ;
- par principe de minimisation des données, les noms des bases et domaines appartenant aux tiers hébergés sur ce VPS ne sont pas reproduits nommément dans ce document (ils sont dénombrés uniquement).

**Conclusion : GO LOT 1 SOUS CONDITIONS** (voir section 17).

---

## 2. Méthode

Audit réalisé exclusivement par connexion SSH en lecture seule, avec la clé dédiée `~/.ssh/claude_nss_local`, vers `root@195.35.2.137`.

Aucune commande d'écriture, d'installation, de mise à jour, de redémarrage de service ou de modification de configuration n'a été exécutée. Aucune donnée métier contenue dans les bases PostgreSQL n'a été consultée (seules les métadonnées : liste des bases, tailles, rôles ont été lues). Aucun contenu de clé privée ni de secret (mot de passe, token, `admin_passwd`) n'a été affiché ou copié dans ce rapport.

---

## 3. VPS

| Élément | Valeur |
|---|---|
| Fournisseur | Hostinger |
| IP | 195.35.2.137 |
| Hostname | `srv1367494` |
| OS | Ubuntu 24.04.4 LTS (Noble Numbat) |
| Noyau | Linux 6.8.0-117-generic, x86_64 |
| Uptime | 116 jours (dernier redémarrage : ~fin mai 2026) |

---

## 4. CPU / RAM / disque

| Ressource | Valeur |
|---|---|
| vCPU | 2 (AMD EPYC 9354P, 1 thread/core) |
| RAM totale | 7,8 Gi |
| RAM utilisée | 1,6 Gi |
| RAM disponible (estimée) | 6,2 Gi |
| Swap | 0 (aucun swap configuré) |
| Disque total (`/`) | 96 G (ext4) |
| Disque utilisé | 8,3 G (9 %) |
| Disque disponible | 88 G |
| Partitions | `/` (96G ext4), `/boot` (881M ext4), `/boot/efi` (105M vfat), volumes overlay Docker sur le même disque |
| Load average | 0.15 / 0.03 / 0.01 (quasi inactif) |

**Constat :** marge confortable en CPU, RAM et disque pour une instance TEST légère. L'absence de swap est un facteur de risque en cas de pic mémoire imprévu, à surveiller plutôt qu'à corriger dans l'immédiat.

---

## 5. Services

Services actifs identifiés (`systemctl list-units --state=running`) :

- `docker.service`, `containerd.service`
- `nginx.service`
- `odoo.service`
- `postgresql@16-main.service`
- `ssh.service`
- services système standards (cron, dbus, rsyslog, unattended-upgrades, systemd-*, etc.)

Outils présents : `docker` (29.5.1), `certbot`. Absents : `redis-cli`/`redis-server`, `fail2ban-client`, `apache2`.

**Conteneurs Docker actifs :** 2 conteneurs `n8n` (image `docker.n8n.io/n8nio/n8n`), exposés uniquement sur `127.0.0.1` (ports internes 5678/5679), utilisés pour de l'automatisation — **sans lien avec NSS**.

**Processus consommant le plus de mémoire :** les processus Node.js de n8n (cumul approximatif ~900 Mo de RSS), suivis d'Odoo (~190 Mo) et PostgreSQL (~100 Mo au total). CPU quasi inutilisé au moment de l'audit.

---

## 6. Instances Odoo existantes

**Une seule instance Odoo détectée**, en production :

| Champ | Valeur |
|---|---|
| Version | **Odoo 19.0** (`19.0.20260520`), édition Community (paquet `odoo` installé via `apt`, aucun indice d'Enterprise) |
| Service systemd | `odoo.service` (actif depuis 2 jours au moment de l'audit) |
| Utilisateur système | `odoo` (uid 110, shell `/usr/sbin/nologin`) |
| Port | `8069` (xmlrpc), exposé sur **toutes les interfaces** (`0.0.0.0:8069`), pas seulement en local |
| Chemin d'installation | paquet système global (`/usr/lib/python3/dist-packages/odoo`) |
| Chemin des addons | `/usr/lib/python3/dist-packages/odoo/addons` (chemin natif du paquet, pas de addons custom séparés détectés) |
| Chemin du fichier de config (référence uniquement) | `/etc/odoo/odoo.conf` |
| Workers | non configuré explicitement (absence de la clé `workers` dans la config) → mode mono-processus par défaut |
| Bases servies | 3 bases de production appartenant à des tiers (voir section 7) |
| Consommation | ~190 Mo RAM, CPU négligeable |

**Point d'architecture important :** cette instance est installée comme **paquet système unique** (`dpkg -l | grep odoo` → un seul paquet `odoo` 19.0). Il n'y a pas de mécanisme natif permettant d'installer un second paquet `odoo` de version différente à côté. L'installation d'Odoo 18.0 Community pour NSS devra donc se faire via une méthode indépendante du gestionnaire de paquets système (environnement virtuel Python avec sources Odoo 18 clonées, ou conteneur Docker dédié), sans jamais toucher au paquet `odoo` existant ni à `odoo.service`.

---

## 7. PostgreSQL

| Champ | Valeur |
|---|---|
| Version | PostgreSQL 16 (cluster `16-main`) |
| Statut | actif, en ligne |
| Port | `5432`, bindé uniquement sur `127.0.0.1` / `::1` (pas exposé publiquement) |
| Nombre de bases applicatives | 3 (+ `postgres`, `template0`, `template1` systèmes) |
| Tailles approximatives | ~83 Mo, ~98 Mo, ~91 Mo (bases applicatives) ; ~392 Mo pour le répertoire de données complet |
| Rôles visibles | `postgres` (superuser) et `odoo` (droit `CREATE DB`, propriétaire des 3 bases) |
| Consommation | ~100 Mo RAM au total, CPU négligeable |

Les 3 bases applicatives appartiennent à des tiers sans lien avec NSS ; leurs noms ne sont pas reproduits ici (principe de minimisation). Aucune donnée métier de ces bases n'a été consultée — seule la liste des bases et leur taille (`\l+`) a été lue.

**Point d'architecture :** le rôle `odoo` a le droit `CREATE DB` mais n'est pas superuser. Pour NSS, il faudra soit réutiliser un rôle PostgreSQL dédié `odoo_nss` avec des droits restreints à ses propres bases (`nss_test`), conformément à ce que prévoyait déjà `NSS_ERP_02`, soit créer un rôle spécifique — décision à prendre en LOT 1, pas en LOT 0.

---

## 8. Nginx / HTTPS

| Champ | Valeur |
|---|---|
| Version | nginx/1.24.0 (Ubuntu) |
| Server blocks actifs | 3 (`sites-enabled`) |
| Dont lié à Odoo existant | 1 site (proxy vers `127.0.0.1:8069`) — tiers, hors périmètre NSS |
| Dont lié à n8n | 2 sites (proxy vers `127.0.0.1:5678` et `127.0.0.1:5679`) — tiers, hors périmètre NSS |
| HTTPS | activé sur les 3 sites via **Let's Encrypt / Certbot**, certificats valides (renouvellement automatique `certbot` détecté dans `/etc/cron.d/certbot`) |
| Clés privées TLS | non lues (principe respecté : jamais de lecture des clés privées) |

**Constat :** aucun sous-domaine n'est encore réservé pour NSS. Le choix du sous-domaine reste `[À VALIDER PO]` (déjà identifié comme ARCH-06 dans `NSS_ERP_02`).

---

## 9. Réseau / ports

Ports en écoute observés (`ss -tlnp`) :

| Port | Service | Exposition |
|---|---|---|
| 22 | SSH | toutes interfaces (IPv4 + IPv6) |
| 80 | Nginx (HTTP) | toutes interfaces |
| 443 | Nginx (HTTPS) | toutes interfaces |
| 5432 | PostgreSQL | localhost uniquement |
| 5678, 5679 | n8n (via docker-proxy) | localhost uniquement |
| 8069 | Odoo existant | **toutes interfaces** (exposition directe, pas seulement via Nginx) |
| 53 | systemd-resolved | interne uniquement |

**Règles UFW actives** (pare-feu actif, politique par défaut : deny en entrée) : autorisent `22`, `80`, `443`, `5678`, `8080`. Le port `8080` est autorisé dans UFW mais aucun service ne l'utilise actuellement au moment de l'audit — à clarifier avec le PO/l'administrateur existant si utile, sans agir dessus.

**Port libre proposé pour NSS TEST : `8070`** (non utilisé actuellement, conforme à la proposition initiale de `NSS_ERP_02`).

**Remarque sécurité (constat, pas correction) :** le port 8069 de l'Odoo existant est exposé sur toutes les interfaces réseau, alors que Nginx fait déjà le reverse proxy en HTTPS. Cela signifie qu'Odoo est accessible directement en HTTP non chiffré sur `195.35.2.137:8069`, en plus de l'accès HTTPS via Nginx. Ce point préexiste à NSS et ne doit pas être corrigé dans ce lot ; pour l'installation NSS, il est recommandé de ne PAS reproduire ce schéma (lier l'Odoo NSS uniquement à `127.0.0.1:8070` et ne l'exposer qu'via Nginx).

---

## 10. Sauvegardes

**Aucune sauvegarde applicative (PostgreSQL ou filestore Odoo) n'a été trouvée sur ce VPS.**

Constats :
- `crontab -l` pour root : vide (« no crontab for root »)
- `/etc/cron.d/` : seulement des tâches système standards (certbot, sysstat, e2scrub, docker-builder-prune) — rien lié à des sauvegardes de bases
- `/var/backups/` : ne contient que des sauvegardes système Debian standards (dpkg, apt, alternatives) — 2,7 Mo au total, rien lié à PostgreSQL ou Odoo
- Aucun script ni répertoire de sauvegarde applicative trouvé dans les emplacements usuels

**Conséquence directe pour NSS :** la stratégie de sauvegarde décrite dans `NSS_ERP_02` (section 19 — `pg_dump` quotidien, sauvegarde du filestore, copie externe chiffrée) devra être mise en place **intégralement par NSS**, sans dépendre d'un mécanisme existant sur le VPS. Ce n'est pas un point bloquant, mais un prérequis explicite du LOT 0/1 à ne pas oublier.

---

## 11. Sécurité

Observations (aucune correction appliquée) :

| Point | Constat |
|---|---|
| Connexion root SSH | **autorisée** (`PermitRootLogin yes`, confirmé par `sshd -T`) |
| Authentification par mot de passe | **activée** (`PasswordAuthentication yes` effectif, malgré une directive contradictoire dans un des fichiers `sshd_config.d/`) |
| Authentification par clé | activée également (`PubkeyAuthentication yes`) — la clé NSS dédiée fonctionne |
| UFW (pare-feu) | actif, politique par défaut restrictive, logging activé |
| Fail2ban | **non installé** |
| Utilisateurs systèmes avec shell interactif | `root`, `ubuntu`, `postgres` (+ `sync` technique) |
| Séparation des instances | l'utilisateur `odoo` existant n'a pas de shell (`nologin`) — bonne pratique déjà en place pour l'instance existante |
| Exposition Odoo | port 8069 exposé publiquement en HTTP en plus du HTTPS via Nginx (voir section 9) |

**Ces constats préexistent au projet NSS et ne relèvent pas de son périmètre de correction.** Ils sont documentés pour information du PO. Aucune action corrective n'a été effectuée, conformément à la consigne « ne corrige rien ».

---

## 12. Risques de coexistence

| # | Risque | Impact potentiel | Commentaire |
|---|---|---|---|
| C01 | VPS déjà en **production réelle** pour 3 clients tiers (Odoo) + automatisation n8n pour 2 autres domaines | Élevé si mal isolé | Ce n'est pas un VPS de test vide ; toute erreur de configuration touchant `odoo.service`, `/etc/odoo/`, le cluster PostgreSQL partagé ou Nginx peut impacter des tiers réels |
| C02 | Odoo existant en 19.0 alors que NSS cible 18.0 | Moyen | Nécessite une méthode d'installation non-`apt` pour NSS (venv/source ou conteneur), à documenter en LOT 1 |
| C03 | Un seul cluster PostgreSQL 16 partagé | Moyen | La base `nss_test` devra être créée dans ce même cluster (ou un second cluster dédié à évaluer), avec un rôle applicatif dédié et des droits strictement limités à ses propres bases |
| C04 | Absence de sauvegarde existante | Élevé pour NSS | NSS ne peut compter sur aucun filet de sécurité existant ; sa propre sauvegarde est indispensable dès le LOT 1 |
| C05 | Absence de swap | Faible à moyen | Pic mémoire imprévu (Odoo NSS + Odoo existant + n8n) pourrait déclencher un OOM kill ; à surveiller après installation |
| C06 | Lacunes de sécurité globales du VPS (root SSH, pas de fail2ban) | Hors périmètre NSS mais risque systémique | Impacte indirectement NSS si le VPS est compromis via un autre vecteur (n8n, site tiers) |

---

## 13. Capacité NSS TEST

**Réponse : OUI SOUS CONDITIONS**

Justification à partir des mesures réelles :
- CPU : charge quasi nulle (load average 0.15 sur 2 vCPU) → large marge pour une instance TEST mono-utilisateur légère
- RAM : ~6,2 Gi disponibles sur 7,8 Gi ; l'instance Odoo existante ne consomme que ~190 Mo, une seconde instance légère (mode mono-processus, sans workers, données fictives) devrait rester dans un ordre de grandeur comparable
- Disque : 88 Go disponibles sur 96 Go → largement suffisant pour une base de test + filestore + logs
- Le principal facteur limitant n'est pas la ressource brute mais la **cohabitation avec de la production réelle tierce** et l'**absence de sauvegarde existante**, d'où le « SOUS CONDITIONS »

---

## 14. Architecture NSS TEST proposée

> **Note :** cette proposition initiale (installation via environnement virtuel Python) est **remplacée** par l'architecture Docker Compose décrite dans la section dédiée « Architecture d'isolation validée pour LOT 1 » ci-après, validée par le PO le 24 septembre 2026. Elle est conservée ici à titre de trace de l'analyse initiale.

Sans rien créer, proposition adaptée à l'environnement réellement observé :

| Élément | Proposition |
|---|---|
| Utilisateur système | `nss` (dédié, distinct de `odoo` existant), shell `nologin` |
| Méthode d'installation Odoo 18 | environnement virtuel Python dédié (ex. `/opt/nss/odoo18/venv`) avec sources Odoo 18.0 Community clonées séparément — **pas** via le paquet `apt odoo` déjà utilisé par l'instance 19.0 |
| Chemin d'installation | `/opt/nss/odoo18/` |
| Chemin des addons NSS | `/opt/nss/odoo18/custom-addons/` (modules `nss_core`, `nss_project`, etc. de `NSS_ERP_02`) |
| Port | `8070` (libre, confirmé en section 9) |
| Service systemd | `nss-odoo-test.service` (nom distinct de `odoo.service`) |
| Rôle PostgreSQL | `odoo_nss` (droits limités à ses propres bases, dans le cluster `16-main` existant — ou cluster séparé à évaluer si l'isolation stricte est jugée nécessaire) |
| Base de données | `nss_test` |
| Fichier de config | `/etc/nss/odoo-nss-test.conf` (chemin dédié, distinct de `/etc/odoo/`) |
| Filestore | `/opt/nss/filestore-test/` |
| Logs | `/var/log/nss/odoo-nss-test.log` |
| Reverse proxy | nouveau server block Nginx dédié, distinct des 3 existants |
| Sous-domaine | à définir — `[À VALIDER PO]` (ARCH-06) |
| SSL | certificat Let's Encrypt dédié via Certbot, une fois le sous-domaine choisi |
| Sauvegardes | script `pg_dump` + `tar` du filestore, cron dédié à NSS, copie externe — à mettre en place dès le LOT 1 puisqu'aucune infrastructure de sauvegarde n'existe (section 10) |

Cette proposition respecte le principe d'isolation stricte déjà posé dans `NSS_ERP_02` (section 17), renforcé ici par le fait que l'instance existante sert des clients réels.

---

## Architecture d'isolation validée pour LOT 1

**Statut : [VALIDÉ PO — 24 septembre 2026].** Cette section remplace la proposition de la section 14 (installation via environnement virtuel Python) par une architecture **Docker Compose**, conformément à la décision du PO. Aucun élément décrit ici n'a été installé, lancé ou créé sur le VPS : il s'agit d'une proposition documentée, en attente du LOT 1.

### Pourquoi Docker est retenu

- **Docker est déjà présent et opérationnel** sur ce VPS (version 29.5.1, `docker.service` actif), utilisé en production pour n8n. Retenir Docker pour NSS ne nécessite donc **aucune installation de moteur supplémentaire** — seul un projet `docker-compose` propre à NSS sera ajouté en LOT 1.
- Docker Compose permet une **isolation complète** (processus, réseau, système de fichiers) entre l'Odoo 19 existant et l'Odoo 18 NSS, sans dépendre d'un environnement virtuel Python partagé avec le système hôte.
- Cela évite tout conflit avec le paquet système `odoo` 19.0 déjà installé via `apt` (un seul paquet `odoo` peut exister nativement sur l'hôte ; un conteneur contourne cette limite proprement).
- Le cycle de vie (démarrage, arrêt, mise à jour, suppression) de NSS TEST devient entièrement indépendant de l'instance existante : `docker compose down` sur le projet NSS n'a aucun effet sur `odoo.service`, sur les conteneurs n8n, ni sur PostgreSQL natif.
- La migration future TEST → PROD est facilitée : le même `docker-compose.yml` (avec un fichier `.env` différent) peut être redéployé pour la PROD, conformément à la logique déjà prévue par `NSS_ERP_02` (bases et configuration séparées, pas de duplication brute).

### Architecture des containers

Deux services dans un même projet Compose dédié à NSS :

| Service | Image de base | Rôle |
|---|---|---|
| `nss-odoo` | `odoo:18.0` (image officielle Community) | Application Odoo 18, avec les addons NSS montés en volume |
| `nss-db` | `postgres:16` | Base de données PostgreSQL dédiée à NSS, **totalement séparée** du cluster PostgreSQL natif `16-main` existant |

**Point important :** contrairement à la proposition initiale de la section 14 (réutiliser le cluster PostgreSQL natif avec un rôle dédié), l'architecture Docker isole PostgreSQL dans son propre conteneur. Cela renforce l'isolation demandée par le PO : aucune connexion réseau ni aucun partage de processus entre `nss-db` et le PostgreSQL natif qui sert les 3 bases clientes tierces.

### Volumes

Tous les volumes sont nommés et dédiés au projet NSS (aucun volume partagé avec n8n ou l'Odoo existant) :

| Volume | Contenu | Type |
|---|---|---|
| `nss_pg_data` | Données PostgreSQL de `nss-db` | Volume Docker nommé |
| `nss_odoo_filestore` | Filestore Odoo (pièces jointes, documents) | Volume Docker nommé |
| `./addons` (bind mount) | Modules NSS spécifiques (`nss_core`, `nss_project`…) | Bind mount en lecture, répertoire dédié sur l'hôte (ex. `/opt/nss/addons/`) — permet l'édition/déploiement des modules sans reconstruire l'image |
| `./config` (bind mount) | Fichier `odoo.conf` propre à NSS (sans secret dedans — les secrets passent par `.env`) | Bind mount, répertoire dédié (ex. `/opt/nss/config/`) |

### Réseau

- Un **réseau Docker dédié** (bridge), ex. `nss_network`, créé par le `docker-compose.yml` du projet NSS.
- Seuls les services `nss-odoo` et `nss-db` sont rattachés à ce réseau.
- **Aucune connexion** de ce réseau vers le réseau Docker utilisé par les conteneurs n8n existants (`n8n` et `n8n-connect`), ni vers PostgreSQL natif (`16-main`), ni vers l'Odoo 19 existant.
- `nss-odoo` communique avec `nss-db` uniquement via le nom de service interne au réseau Compose (`nss-db:5432`), jamais via le port 5432 natif de l'hôte.

### Ports

- Le port interne du conteneur `nss-odoo` (8069 à l'intérieur du conteneur) est mappé **uniquement sur `127.0.0.1:8070`** de l'hôte (`127.0.0.1:8070:8069`), jamais sur `0.0.0.0`.
- Ce choix corrige explicitement l'écart observé sur l'instance existante (port 8069 exposé sur toutes les interfaces, section 9) : NSS ne doit pas reproduire cette exposition directe.
- Le port PostgreSQL du conteneur `nss-db` (5432 interne) **n'est pas publié** sur l'hôte du tout — seul `nss-odoo` y accède via le réseau Docker interne.
- Le port `8070` est confirmé libre sur l'hôte (section 9).

### Stratégie de secrets

- Un fichier **`.env` local, non versionné**, à la racine du projet Compose NSS (ex. `/opt/nss/.env`), contenant : mot de passe PostgreSQL du conteneur `nss-db`, `admin_passwd` Odoo, et toute autre variable sensible.
- Le `docker-compose.yml` référence ces valeurs via des variables (`${POSTGRES_PASSWORD}`, etc.), jamais en clair dans le fichier versionné.
- `.env` est déjà couvert par les motifs `.env` / `.env.*` du `.gitignore` du dépôt NSS (section 4/mise en place initiale) — à répliquer dans un `.gitignore` local si le répertoire `/opt/nss/` est lui-même un jour suivi par un outil de version sur le VPS (non prévu actuellement : le déploiement se fait par copie/déploiement, pas par `git clone` direct sur le VPS).
- Aucun secret ne doit apparaître dans le `docker-compose.yml`, dans les logs de conteneur, ni dans ce dépôt Git.

### Stratégie de sauvegarde

Comme relevé en section 10, **aucune sauvegarde n'existe actuellement sur ce VPS** pour quelque base que ce soit. L'architecture Docker ne change pas ce constat mais le rend plus simple à traiter :

- `pg_dump` exécuté via `docker compose exec nss-db pg_dump -U <user> nss_test`, en cron dédié NSS (hors des cron systèmes existants).
- Sauvegarde du volume `nss_odoo_filestore` via `tar` (ou `docker run --rm -v nss_odoo_filestore:/data ... tar czf ...`).
- Copie chiffrée vers un stockage externe au VPS avant tout passage en PROD (conforme à `NSS_ERP_02` section 19).
- Cette sauvegarde est **indépendante** de toute sauvegarde éventuelle de l'Odoo 19 existant (qui n'en a pas non plus) — NSS ne doit pas dépendre d'une infrastructure de sauvegarde tierce inexistante.

### Coexistence avec Odoo 19 et n8n

| Aspect | Odoo 19 existant | n8n (Docker) | NSS TEST (Docker, proposé) |
|---|---|---|---|
| Mécanisme | paquet `apt` natif | conteneurs Docker existants | conteneurs Docker dédiés |
| Réseau Docker | non applicable | réseau(x) propre(s) à n8n | réseau `nss_network` dédié, aucune interconnexion |
| PostgreSQL | cluster natif `16-main` | aucun (n8n n'utilise pas ce PostgreSQL) | conteneur `nss-db` séparé |
| Port exposé host | `0.0.0.0:8069` (existant, non modifié) | `127.0.0.1:5678` / `127.0.0.1:5679` (existant, non modifié) | `127.0.0.1:8070` (nouveau, isolé) |
| Volumes | chemins système (`/var/lib/odoo`, `/var/lib/postgresql/16/main`) | volumes Docker propres à n8n | volumes Docker propres à NSS (`nss_pg_data`, `nss_odoo_filestore`) |
| Interaction prévue avec NSS | **aucune** | **aucune** | — |

Aucune commande, configuration ou volume proposé ici ne touche, ne référence ni ne partage quoi que ce soit avec l'Odoo 19 existant, ses bases, ou les conteneurs n8n.

### Ressources estimées

Sur la base des mesures de l'audit (sections 4 et 5) et de valeurs usuelles pour un conteneur Odoo 18 + PostgreSQL 16 en mode test/pilote (charge faible, données fictives, 10-20 utilisateurs) :

| Composant | RAM estimée | CPU estimé | Disque estimé |
|---|---|---|---|
| Conteneur `nss-odoo` (mono-worker, test) | 250–400 Mo | faible (pics ponctuels) | quelques centaines de Mo (image + code) |
| Conteneur `nss-db` (PostgreSQL 16, base de test) | 100–200 Mo | faible | quelques dizaines de Mo au démarrage, croissance lente avec des données fictives |
| **Total estimé** | **~400–600 Mo** | **négligeable au repos** | **< 1 Go au démarrage** |

Rapporté aux **~6,2 Gi de RAM disponible** et aux **88 Go de disque disponible** mesurés en section 4, cette charge supplémentaire reste très largement absorbable sans risque pour l'Odoo 19 existant ni pour n8n. Un contrôle de charge réel sera fait après déploiement en LOT 1 (pas d'hypothèse figée au-delà de cette estimation).

### Procédure future TEST → PROD

Cohérent avec la stratégie déjà posée dans `NSS_ERP_02` (section 18 — pas de duplication brute d'une base de test vers la production) :

1. **TEST** : déploiement du projet Compose NSS avec données 100 % fictives, port `127.0.0.1:8070`, sans exposition publique tant que le PO n'a pas validé les workflows.
2. **Validation fonctionnelle** : PO valide les lots MVP en environnement TEST (conforme à `NSS_ERP_01`/`NSS_ERP_02`).
3. **Exposition externe contrôlée** : une fois validé, un server block Nginx dédié (existant sur le VPS, non modifié pour l'instant) sera configuré pour faire reverse proxy en HTTPS vers `127.0.0.1:8070`, avec un sous-domaine à définir par le PO (ARCH-06) et un certificat Certbot dédié — **cette étape n'est pas réalisée dans ce lot**.
4. **PROD** : un second projet Compose (`docker-compose.prod.yml` ou fichier `.env` distinct), avec ses propres volumes (`nss_pg_data_prod`, `nss_odoo_filestore_prod`) et son propre port interne (ex. `127.0.0.1:8071`), déployé séparément — jamais en réutilisant les volumes ou la base du projet TEST.
5. **Migration des données réelles** : uniquement après validation des droits d'accès, des sauvegardes, et du processus de migration, conformément à `NSS_ERP_02` section 23.

Cette procédure ne modifie ni Nginx, ni le firewall, ni aucun service existant à ce stade : elle est documentée pour préparer le LOT 1 et les lots suivants, pas pour être exécutée maintenant.

---

## 15. Prérequis avant installation

1. Décision PO sur le sous-domaine NSS TEST (ARCH-06, déjà ouvert dans `NSS_ERP_02`)
2. Validation de la méthode d'installation Odoo 18 (venv/source vs conteneur Docker) — nouveau point né de cet audit
3. Mise en place d'un script de sauvegarde dédié NSS dès le LOT 1 (aucune sauvegarde existante à réutiliser)
4. Confirmation que l'isolation utilisateur/port/config proposée en section 14 convient
5. Décision sur le cluster PostgreSQL : réutiliser `16-main` avec un rôle dédié, ou cluster séparé (question ouverte, à trancher en LOT 1)

---

## 16. Points bloquants

**Aucun point strictement bloquant pour démarrer le LOT 1**, sous réserve des conditions listées en section 15 et 17. Le VPS a la capacité technique nécessaire, et l'instance existante n'a pas besoin d'être modifiée pour que NSS s'installe à côté.

---

## 17. Recommandation LOT 1

**GO LOT 1 SOUS CONDITIONS**

Conditions :
1. Respecter l'isolation stricte proposée en section 14 (utilisateur, chemins, port, service, rôle PostgreSQL, config — tous distincts de l'existant)
2. Installer Odoo 18.0 par une méthode indépendante du paquet système `apt odoo` déjà en place (venv/source ou conteneur)
3. Ne jamais modifier `odoo.service`, `/etc/odoo/odoo.conf`, les bases de données tierces existantes, ni les server blocks Nginx existants
4. Mettre en place la sauvegarde NSS dès le LOT 1 (aucun filet de sécurité existant à réutiliser)
5. Ne pas exposer le port Odoo NSS directement sur internet — passer uniquement par Nginx/HTTPS, contrairement à ce qui est observé pour l'instance existante
6. Obtenir la décision PO sur le sous-domaine avant de configurer Nginx/Certbot pour NSS

---

*Fin du document NSS_ERP_03_AUDIT_VPS_HOSTINGER.md*
