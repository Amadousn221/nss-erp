# NSS ERP — Audit VPS Hostinger

**Référence :** NSS_ERP_03
**Version :** 1.0
**Date :** 23 septembre 2026
**Auteur :** Claude Code — développeur / intégrateur technique
**Statut :** audit non réalisable en l'état — accès technique indisponible dans cette session
**Prérequis :** NSS_ERP_00, NSS_ERP_01, NSS_ERP_02 (lus et respectés)
**Périmètre :** lecture seule. Aucune installation, aucune modification, aucune commande à effet de bord n'a été exécutée.

---

## 1. Résumé exécutif

Cet audit devait mesurer l'état réel du VPS Hostinger (OS, CPU, RAM, disque, services, instances Odoo existantes, PostgreSQL, Nginx, réseau, sauvegardes, sécurité) afin de répondre à la question posée par `NSS_ERP_02` (sections 17 et 25, points ARCH-05 et ARCH-07) : le VPS peut-il accueillir une instance NSS ERP TEST sans mettre en danger les instances existantes ?

**Constat central : l'audit n'a pas pu être réalisé, faute d'accès technique au VPS dans cette session.**

- Le serveur MCP Hostinger apparaît comme connecté dans la session, mais tout appel effectué (y compris des appels de lecture simple comme la liste des abonnements ou le catalogue) retourne une erreur d'authentification (HTTP 401). Le connecteur n'est donc pas réellement authentifié pour ce compte.
- Les seuls outils Hostinger exposés à cette session concernant les VPS sont des outils **d'action** (activer/désactiver un pare-feu, créer une règle de pare-feu, attacher une clé publique, créer un snapshot, créer un enregistrement PTR, déployer un projet Docker Compose, créer un script post-installation). **Aucun outil de lecture** (liste des VPS, détails d'une instance, métriques CPU/RAM/disque, exécution de commande diagnostique) n'est disponible via ce serveur MCP, même une fois l'authentification résolue.
- Aucun accès SSH n'est configuré dans cet environnement (pas d'identifiants, pas de clé, pas d'hôte connu). Conformément aux règles du LOT 0, **aucun mot de passe n'a été demandé dans le chat** et aucune tentative d'exploration de secrets/identifiants n'a été effectuée.

**Conséquence directe :** toutes les sections « mesures réelles » de ce rapport (3 à 12) sont documentées comme **non disponibles**, avec les commandes en lecture seule qui *auraient dû* être exécutées si l'accès avait été disponible (pour permettre une exécution manuelle par le PO ou lors d'une prochaine session correctement connectée).

Ce document ne doit pas être interprété comme un audit favorable ou défavorable du VPS : c'est un **rapport de blocage d'accès**, accompagné d'une proposition d'architecture cible (section 14) qui reste valable une fois les mesures obtenues.

---

## 2. Méthode et périmètre

### 2.1 Ce qui a été fait

1. Synchronisation de la branche `main` du dépôt `Amadousn221/nss-erp`.
2. Création de la branche `claude/nss-erp-vps-audit` (alignée sur `main`, commit `dea24b6`).
3. Lecture de `CLAUDE.md`, `docs/NSS_ERP_00_RECHERCHE_PAYS_2026.md`, `docs/NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md`, `docs/NSS_ERP_02_ARCHITECTURE_ODOO.md`.
4. Recherche exhaustive des outils Hostinger disponibles via MCP dans cette session (recherche par mots-clés : VPS, virtual machine, metrics, list, get, execute, SSH).
5. Test d'appels Hostinger strictement en lecture (`billing_getSubscriptionListV1`, `billing_getCatalogItemListV1`) pour vérifier l'état de connexion — les deux ont échoué avec une erreur 401.
6. Vérification qu'aucun accès SSH n'est pré-configuré dans l'environnement (sans tenter de lire ou d'extraire des identifiants).

### 2.2 Ce qui n'a PAS été fait (conformément aux interdictions du LOT 0)

- Aucune commande d'installation, de mise à jour système, de modification de service, de base de données, de réseau, de pare-feu ou de cron.
- Aucune demande de mot de passe dans le chat.
- Aucune tentative de contournement de l'échec d'authentification MCP (pas de nouvelle tentative de connexion, pas de manipulation d'identifiants).
- Aucun secret, token ou donnée sensible n'a été consulté, ni recopié dans ce dépôt.

### 2.3 Limite méthodologique à retenir

Les sections 3 à 12 ci-dessous suivent la structure demandée, mais **ne contiennent aucune mesure réelle**. Chaque section indique :
- le statut `[NON DISPONIBLE — ACCÈS REQUIS]` ;
- les commandes en lecture seule qui permettraient d'obtenir l'information une fois l'accès rétabli (MCP authentifié ou accès SSH en lecture autorisé).

---

## 3. Caractéristiques du VPS

`[NON DISPONIBLE — ACCÈS REQUIS]`

Aucune information sur le système d'exploitation, la version Ubuntu ou l'architecture CPU n'a pu être obtenue.

Commandes de lecture à exécuter lors d'un prochain audit (aucun effet de bord) :

```bash
hostnamectl
lsb_release -a
uname -m
```

---

## 4. CPU / RAM / disque

`[NON DISPONIBLE — ACCÈS REQUIS]`

Aucune mesure de vCPU, RAM totale/utilisée/disponible, swap, disque total/utilisé/disponible, filesystem, uptime ou load average n'a pu être collectée.

Commandes de lecture à exécuter lors d'un prochain audit :

```bash
nproc
free -h
swapon --show
df -hT
uptime
cat /proc/loadavg
```

---

## 5. Services actifs

`[NON DISPONIBLE — ACCÈS REQUIS]`

Impossible de confirmer la présence, le statut ou la consommation de : Odoo, PostgreSQL, Nginx, Apache, Docker, Redis, Certbot ou tout autre service.

Commandes de lecture à exécuter (aucune modification, uniquement des commandes `status`) :

```bash
systemctl list-units --type=service --state=running
systemctl status postgresql --no-pager
systemctl status nginx --no-pager
systemctl status docker --no-pager
systemctl status redis --no-pager
systemctl list-timers --all
```

---

## 6. Instances Odoo existantes

`[NON DISPONIBLE — ACCÈS REQUIS]`

`NSS_ERP_02` (section 17) part de l'hypothèse qu'une instance Odoo existe déjà sur ce VPS. Cette hypothèse **n'a pas pu être vérifiée**. Aucune information sur la version, l'édition (Community/Enterprise), le service systemd, le port, l'utilisateur système, les chemins d'installation/addons, le fichier de configuration ou le nombre de workers n'a été collectée.

Commandes de lecture à exécuter (jamais de commande `admin_passwd`, mot de passe ou secret) :

```bash
systemctl list-units --type=service | grep -i odoo
ps aux | grep -i odoo
ss -tlnp | grep -i python
find / -maxdepth 4 -iname "*odoo*.conf" 2>/dev/null
```

**Rappel impératif pour la suite :** ne jamais afficher `admin_passwd`, mot de passe PostgreSQL, token ou secret. Si une commande en révèle un par accident, il doit être remplacé par `[MASQUÉ]` avant toute écriture dans ce dépôt.

---

## 7. PostgreSQL

`[NON DISPONIBLE — ACCÈS REQUIS]`

Version, état du service, port, nombre approximatif de bases, bases associées à Odoo, rôles PostgreSQL et espace disque utilisé : aucune donnée disponible.

Commandes de lecture à exécuter (connexion en lecture seule, sans jamais afficher les mots de passe de rôle) :

```bash
psql --version
systemctl status postgresql --no-pager
ss -tlnp | grep 5432
sudo -u postgres psql -c "\l"
sudo -u postgres psql -c "\du"
du -sh /var/lib/postgresql/*
```

---

## 8. Nginx / HTTPS

`[NON DISPONIBLE — ACCÈS REQUIS]`

Version Nginx, server blocks existants, domaines/sous-domaines liés à Odoo, ports proxyfiés, présence HTTPS, certificats : aucune donnée disponible.

Commandes de lecture à exécuter (ne jamais afficher les clés privées SSL) :

```bash
nginx -v
ls -la /etc/nginx/sites-enabled/
grep -R "server_name" /etc/nginx/sites-enabled/
certbot certificates
```

---

## 9. Ports et réseau

`[NON DISPONIBLE — ACCÈS REQUIS]`

Impossible d'établir la liste des ports en écoute (22, 80, 443, 5432, ports Odoo existants, autres) ni de proposer un port réellement libre pour NSS TEST tant que cette liste n'est pas obtenue.

Commande de lecture à exécuter :

```bash
ss -tlnp
```

**Conséquence sur la section 14 :** le port 8070 proposé pour NSS TEST est repris de l'exemple donné dans les instructions du LOT 0 et de `NSS_ERP_02`. Il reste **à confirmer** comme réellement libre une fois `ss -tlnp` exécuté.

---

## 10. Sauvegardes

`[NON DISPONIBLE — ACCÈS REQUIS]`

Aucune information sur les sauvegardes Hostinger, snapshots, scripts de backup présents, fréquence, emplacement ou existence d'une sauvegarde externe.

Vérifications à effectuer lors d'un prochain audit (sans ouvrir le contenu des sauvegardes) :

```bash
crontab -l
ls -la /etc/cron.d/
ls -la /backup 2>/dev/null
```

Côté panel Hostinger : vérifier la présence de snapshots VPS actifs via hPanel (lecture seule), sans en créer de nouveau — la création d'un snapshot écraserait un snapshot existant, ce qui est une action interdite dans ce LOT 0.

---

## 11. Sécurité observée

`[NON DISPONIBLE — ACCÈS REQUIS]`

Aucune vérification possible de : configuration SSH, authentification par clé, accès root direct, pare-feu Hostinger, UFW, fail2ban, HTTPS, ports publiquement exposés, permissions générales.

Commandes de lecture à exécuter :

```bash
grep -E "^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)" /etc/ssh/sshd_config
ufw status verbose
systemctl status fail2ban --no-pager
```

---

## 12. Risques de coexistence

Sans mesures réelles (CPU/RAM/disque disponibles, nombre d'instances Odoo déjà actives, consommation actuelle), **aucun risque de coexistence ne peut être évalué de façon fiable.**

Risques génériques déjà identifiés par `NSS_ERP_02` (section 24, risque T02 et T07) et qui restent pertinents tant que l'audit réel n'est pas fait :

| Risque | Statut |
|---|---|
| VPS Hostinger insuffisant en RAM/CPU pour une deuxième instance Odoo | `[À VALIDER PO]` — dépend des mesures réelles |
| Instance Odoo existante impactée par l'installation NSS | `[À VALIDER PO]` — dépend de l'isolation réellement en place |
| Absence de sauvegarde externe déjà en place | `[À VALIDER PO]` |
| Accès root/SSH mal sécurisé | `[À VALIDER PO]` |

---

## 13. Capacité NSS TEST

**Réponse à la question « Peut-on installer NSS ERP TEST sur ce VPS sans mettre en danger les instances Odoo existantes ? » :**

## NON — EN L'ÉTAT, LA QUESTION NE PEUT PAS ÊTRE TRANCHÉE

Justification : aucune mesure réelle du VPS (CPU, RAM, disque, services actifs, instances Odoo existantes) n'a pu être obtenue dans cette session. `NSS_ERP_02` (section 17) est explicite : *« Ne pas retenir l'estimation "512 Mo / 1 worker" comme dimensionnement de référence. […] Avant installation NSS, relever obligatoirement : vCPU ; RAM totale / RAM réellement libre ; swap ; espace disque libre ; version Ubuntu ; version PostgreSQL ; nombre d'instances/services Odoo déjà actifs ; consommation mémoire/CPU actuelle ; stratégie de sauvegarde existante. »* Aucun de ces éléments n'a pu être relevé.

Décider **OUI** ou **OUI SOUS CONDITIONS** sans ces mesures reviendrait à formuler une hypothèse dangereuse sur un VPS de production hébergeant potentiellement une instance Odoo déjà active — ce qui est explicitement interdit par `CLAUDE.md` (section 12, exception pour les actions destructives/irréversibles/de production) et par les interdictions absolues du LOT 0.

Ce **NON** est un constat de blocage d'accès, pas une évaluation négative de la capacité réelle du VPS.

---

## 14. Architecture proposée NSS TEST

Cette section reste **une proposition non engageante**, reprise et affinée de `NSS_ERP_02` (section 17), à confirmer une fois les mesures réelles disponibles. Rien n'a été créé sur le VPS.

| Élément | Proposition | Statut |
|---|---|---|
| Utilisateur système NSS | `odoo-nss` | `[HYPOTHÈSE]` — à adapter si un nom est déjà utilisé sur le VPS |
| Chemin Odoo NSS | `/opt/odoo-nss/` | `[HYPOTHÈSE]` |
| Service systemd | `odoo-nss-test.service` | `[HYPOTHÈSE]` |
| Port | `8070` | `[À CONFIRMER]` — dépend du résultat de `ss -tlnp` (section 9) |
| Rôle PostgreSQL | `odoo_nss` (accès limité à ses propres bases) | `[HYPOTHÈSE]` |
| Nom DB TEST | `nss_test` | `[HYPOTHÈSE]` |
| Fichier de configuration | `/etc/odoo/odoo-nss-test.conf` | `[HYPOTHÈSE]` |
| Filestore | `/opt/odoo-nss/filestore/` | `[HYPOTHÈSE]` |
| Addons NSS | `/opt/odoo-nss/addons-nss/` (modules `nss_core`, `nss_project`, `nss_account` — cf. `NSS_ERP_02` section 21) | `[HYPOTHÈSE]` |
| Sous-domaine | `nss-test.<domaine à définir>` | `[À VALIDER PO]` — ARCH-06 dans `NSS_ERP_02`, toujours ouvert |
| Reverse proxy | Nouveau server block Nginx dédié, sans toucher aux server blocks existants | `[HYPOTHÈSE]` |
| HTTPS | Certificat Let's Encrypt via certbot, obtenu pour le nouveau sous-domaine uniquement | `[HYPOTHÈSE]` |
| Stratégie de sauvegarde | `pg_dump` quotidien de `nss_test` + `tar` du filestore, rétention 30 jours, copie externe chiffrée avant toute mise en PROD (cf. `NSS_ERP_02` section 19) | `[HYPOTHÈSE]` |

Principe d'isolation à respecter strictement lors du LOT 1 (rappelé de `NSS_ERP_02` section 17) : utilisateur système dédié, base de données séparée, rôle PostgreSQL dédié à accès restreint, filestore séparé, fichier de configuration séparé, service systemd séparé — **aucun élément partagé avec une instance Odoo existante.**

---

## 15. Pré-requis avant installation

Avant tout LOT 1 (installation), les éléments suivants doivent être obtenus :

1. **Accès technique fonctionnel**, au choix du PO :
   - reconnecter/ré-autoriser le connecteur MCP Hostinger pour ce compte (l'appel `billing_getSubscriptionListV1` doit répondre 200, pas 401) — sans que cela ne garantisse à lui seul un outil de lecture VPS ; **ou**
   - fournir un accès SSH en lecture (utilisateur, hôte, clé) déposé dans les paramètres sécurisés de l'environnement (jamais collé dans le chat), avec des droits suffisants pour exécuter les commandes de diagnostic listées aux sections 3 à 11.
2. Exécution effective des commandes de lecture listées aux sections 3 à 11 et mise à jour de ce rapport avec les résultats réels.
3. Confirmation explicite du PO sur : sous-domaine NSS TEST (ARCH-06), référentiel comptable (ARCH-03), exercice fiscal (ARCH-04), devise principale (ARCH-09) — ces points restaient déjà ouverts dans `NSS_ERP_02` et ne sont pas résolus par cet audit.

---

## 16. Points bloquants

`POINTS_A_VALIDER_PO` — regroupement des blocages, conformément à la règle anti allers-retours de `CLAUDE.md` (section 12) :

| ID | Blocage | Type | Action nécessaire |
|---|---|---|---|
| VPS-01 | Connecteur MCP Hostinger non authentifié (401) pour ce compte dans cette session | Technique | Reconnecter le connecteur Hostinger pour le compte concerné, puis relancer une session |
| VPS-02 | Aucun outil de lecture VPS (liste, détails, métriques, exécution diagnostique) n'est exposé par le serveur MCP Hostinger disponible dans cette session, même une fois authentifié — seuls des outils de configuration (pare-feu, clés, snapshot, PTR, Docker Compose) sont exposés | Technique | Vérifier si un outil de lecture VPS existe côté Hostinger et doit être activé séparément, ou prévoir un accès SSH en complément |
| VPS-03 | Aucun accès SSH configuré dans l'environnement de session | Technique | Le PO fournit un accès SSH en lecture via les paramètres sécurisés de l'environnement (jamais dans le chat) |
| VPS-04 | Sous-domaine NSS TEST non défini (ARCH-06, déjà ouvert dans `NSS_ERP_02`) | Fonctionnel | Décision PO |
| VPS-05 | Existence et état réels d'une instance Odoo déjà active sur le VPS non confirmés | Technique | Dépend de VPS-01/02/03 |

Aucun de ces points n'est destructif, irréversible ou financier : conformément à la section 12 de `CLAUDE.md`, le travail possible sans ces informations (ce rapport, la structure d'architecture proposée) a été mené à son terme malgré les blocages.

---

## 17. Recommandation LOT 1

**Ne pas démarrer le LOT 1.**

Le LOT 1 (« Socle et réseau NSS ») dépend du LOT 0 (« Infrastructure »), qui exige lui-même un audit réel des ressources VPS (`NSS_ERP_02`, section 22). Cet audit n'a pas pu être réalisé faute d'accès. Démarrer une installation sur la seule base d'hypothèses irait à l'encontre des interdictions absolues de ce LOT 0 et du principe de prudence de `CLAUDE.md`.

**Prochaine étape recommandée :** résoudre les points VPS-01 à VPS-03 (section 16), puis relancer un audit LOT 0 identique à celui-ci pour obtenir les mesures réelles avant toute décision GO/NO-GO.

---

## Conclusion

**STOP — VPS À ADAPTER**

*(Précision : ce STOP porte sur l'accès technique à auditer le VPS, non sur une mesure défavorable de sa capacité. Aucune conclusion sur la capacité réelle du VPS ne peut être formulée tant que les sections 3 à 12 n'ont pas été complétées avec des données réelles.)*

---

*Fin du document NSS_ERP_03_AUDIT_VPS_HOSTINGER.md*
