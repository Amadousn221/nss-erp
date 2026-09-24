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
