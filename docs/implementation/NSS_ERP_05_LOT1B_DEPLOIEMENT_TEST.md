# NSS ERP — LOT 1B : déploiement NSS ERP TEST (Checkpoints 1 à 5B)

**Référence :** NSS_ERP_05
**Date :** 24 septembre 2026
**Statut :** NSS ERP TEST accessible en HTTPS — pilote uniquement, aucune donnée réelle
**Prérequis :** `NSS_ERP_02` validé PO le 24 septembre 2026 ; `NSS_ERP_03` (audit VPS) ; `NSS_ERP_04` (préparation Docker)

---

## 1. Domaine

```
https://erp-test.wasafrica.org
```

DNS : enregistrement A `erp-test.wasafrica.org` → `195.35.2.137`, créé par
le PO, vérifié résolu via résolveur local, `1.1.1.1` et `8.8.8.8` avant
toute action Nginx.

---

## 2. Architecture déployée

```
Internet
  ↓ HTTPS 443
Nginx (existant, 1.24.0)
  ↓ proxy_pass
127.0.0.1:8070  (Odoo NSS — jamais exposé directement)
  ↓
nss_test_odoo (conteneur Docker, odoo:18.0)
  ↓
nss_test_db (conteneur Docker, postgres:16, réseau nss_test_net, aucun port publié)
```

Isolation confirmée à chaque checkpoint : réseau Docker dédié
(`nss_test_net`), volumes dédiés (`nss_pg_data`, `nss_odoo_data`), aucune
ressource partagée avec Odoo 19, PostgreSQL système ou n8n.

---

## 3. Nginx

- Sauvegarde de `/etc/nginx` effectuée avant toute modification :
  `/root/nginx-backup-before-nss-20260924-1424.tar.gz` (sur le VPS,
  non versionné, ne contient pas de secret applicatif NSS).
- Fichier créé : `/etc/nginx/sites-available/erp-test.wasafrica.org`
  (server block HTTP initial, puis complété par Certbot avec la section
  `listen 443 ssl` et la redirection HTTP→HTTPS).
- Activé par symlink dans `/etc/nginx/sites-enabled/` — aucun autre
  symlink existant modifié ou supprimé.
- Logs dédiés : `/var/log/nginx/nss-erp-test-access.log` et
  `nss-erp-test-error.log` (distincts d'Odoo 19 et n8n).
- `nginx -t` validé avant chaque `reload` (jamais de `restart`).
- Exemple de référence utilisé : `deploy/nss-test/nginx/nss-test.conf.example`
  (Checkpoint 5A), adapté avec le domaine réel fourni par le PO.

---

## 4. HTTPS / Certbot

- Certificat Let's Encrypt émis via `certbot --nginx -d erp-test.wasafrica.org --redirect`.
- Expiration : 2026-12-23.
- Intégré au mécanisme de renouvellement automatique existant
  (`certbot.timer`, déjà utilisé pour les 3 autres domaines du VPS).
- Redirection HTTP → HTTPS active et vérifiée (301).
- Certificat vérifié : `CN = erp-test.wasafrica.org`, émis par Let's Encrypt.

**Note :** l'enregistrement Certbot a utilisé l'adresse de contact
`contact@atta-africa.com` (compte NSS ERP) pour les notifications
d'expiration Let's Encrypt — aucune autre donnée transmise à un tiers.

---

## 5. Résultats des checkpoints

| Checkpoint | Contenu | Résultat |
|---|---|---|
| 1 | Copie du dépôt sur le VPS, `.env` et `odoo.local.conf` créés (secrets, non versionnés) | Validé (fait avant ce lot de sessions) |
| 2 | Pull images `postgres:16`/`odoo:18.0`, UID/GID Odoo (100/101), permissions `odoo.local.conf` (root:101, 640), démarrage `nss-db` seul | Validé |
| 3 | Initialisation contrôlée de la base `nss_test` (module `base`, sans démo, `--stop-after-init`) | Validé — Odoo 18.0.1.3, 121 tables |
| 4 | Démarrage permanent `nss-odoo` sur `127.0.0.1:8070` | Validé — `/web/login` = 200 |
| 5A | Audit Nginx/Certbot en lecture seule, préparation exemple de config | Validé — aucune modification serveur |
| 5B | Déploiement Nginx + HTTPS réel sur `erp-test.wasafrica.org` | Validé — HTTPS fonctionnel, isolation confirmée |

---

## 6. Isolation vérifiée après déploiement

- `nss_test_odoo` et `nss_test_db` : uniquement sur le réseau
  `nss_test_net`, aucun lien avec les réseaux n8n.
- Port `8070` : toujours `127.0.0.1:8070` uniquement (jamais
  `0.0.0.0` ni `:::8070`), y compris après activation HTTPS.
- PostgreSQL NSS : aucun port publié sur l'hôte.
- Odoo 19 (`mpsenegal.com`, port 8069), n8n (`n8n.atta-africa.com`,
  `n8n.connect-web.tech`), PostgreSQL système : tous vérifiés actifs et
  fonctionnels après chaque étape, aucune régression détectée.
- Firewall (UFW) inchangé — le port 8070 n'y a jamais été ajouté ;
  l'accès public passe exclusivement par Nginx (80/443).

---

## 7. Secrets — non documentés ici

Conformément à la consigne, ce document ne contient et ne doit jamais
contenir : `admin_passwd`, `POSTGRES_PASSWORD`, ni aucune clé SSH privée.
Ces valeurs restent uniquement dans les fichiers non versionnés du VPS
(`.env`, `config/odoo.local.conf`) et dans `~/.ssh/` en local.

---

## 8. Points à valider PO

Aucun point bloquant restant pour ce lot. Rappel : NSS ERP TEST reste un
pilote — aucune donnée réelle NSS, aucun identifiant `admin/admin`
modifié, aucun module NSS ou OCA installé à ce stade (hors périmètre de
ce checkpoint).

---

*Fin du document NSS_ERP_05_LOT1B_DEPLOIEMENT_TEST.md*
