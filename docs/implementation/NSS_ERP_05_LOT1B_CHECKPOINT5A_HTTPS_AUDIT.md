# NSS ERP — LOT 1B Checkpoint 5A : audit Nginx/Certbot et préparation HTTPS

**Référence :** NSS_ERP_05
**Date :** 24 septembre 2026
**Statut :** audit lecture seule — aucune modification Nginx/DNS/SSL effectuée
**Prérequis :** Checkpoint 4 validé (nss_test_odoo RUNNING, nss_test_db HEALTHY, `/web/login` = 200)

---

## 1. Objectif

Documenter l'état actuel de Nginx et Certbot sur le VPS, préparer un
exemple de configuration Nginx pour NSS TEST, et lister la procédure du
Checkpoint 5B — **sans exécuter aucune de ces étapes**.

---

## 2. Constat Nginx

- Version : `nginx/1.24.0 (Ubuntu)`.
- `sites-available` : `default`, `mpsenegal.com`, `n8n.atta-africa.com`,
  `n8n.connect-web.tech`.
- `sites-enabled` : `mpsenegal.com`, `n8n.atta-africa.com`,
  `n8n.connect-web.tech` (tous des symlinks valides).
- `conf.d/` : vide.
- Aucun site NSS TEST n'existe. Aucun site n'a été créé ou modifié par
  ce checkpoint.

### Reverse proxy Odoo existant (`mpsenegal.com` → Odoo 19, port 8069)

- `proxy_pass http://127.0.0.1:8069` pour `/` et `location ~* /web/static/`
  (avec cache 90 min sur le static).
- Timeouts `proxy_read/connect/send_timeout 720s`.
- Headers standards (`Host`, `X-Real-IP`, `X-Forwarded-For`,
  `X-Forwarded-Proto`, `X-Forwarded-Host`).
- Pas de bloc `/websocket` ou `/longpolling` dédié (Odoo 19 sans
  websocket configuré côté proxy, ou traitée en interne).
- Logs dédiés : `/var/log/nginx/odoo-access.log` / `odoo-error.log`.
- HTTPS géré par Certbot (`listen 443 ssl`, certificat ECDSA
  `mpsenegal.com` + `www.mpsenegal.com`), redirection 301 HTTP→HTTPS.

### Reverse proxy n8n existant (`n8n.atta-africa.com` → port 5678)

- `proxy_pass http://127.0.0.1:5678` avec gestion websocket explicite :
  `map $http_upgrade $connection_upgrade { default upgrade; "" close; }`
  + `proxy_http_version 1.1` + `proxy_set_header Upgrade/Connection`.
- `proxy_read_timeout 86400s` (session websocket longue durée).
- HTTPS Certbot, même pattern que ci-dessus.

Ces deux configurations servent de référence directe pour l'exemple
NSS TEST (section 4).

---

## 3. Constat Certbot / SSL

- Certbot `2.9.0` installé.
- 3 certificats gérés actuellement : `mpsenegal.com` (expire 2026-11-10),
  `n8n.atta-africa.com` (expire 2026-10-28), `n8n.connect-web.tech`
  (expire 2026-12-03).
- Renouvellement automatique **actif** : `certbot.timer` (systemd) +
  `/etc/cron.d/certbot` présents.
- HTTPS déjà utilisé sur ce VPS pour tous les sites existants.
- **Aucun certificat demandé pour NSS TEST** — non fait, conformément à
  la consigne.

---

## 4. Ports / firewall

| Port | État observé |
|---|---|
| 80 | Nginx (`0.0.0.0:80`) |
| 443 | Nginx (`0.0.0.0:443`) |
| 8070 | `127.0.0.1:8070` uniquement (docker-proxy) — **pas exposé publiquement** |

UFW actif ; règles autorisées : `22`, `80`, `443`, `5678`, `8080`
(existant, non modifié par ce checkpoint). **8070 n'est pas et ne doit
pas être ajouté** au firewall — l'accès prévu passe uniquement par
Nginx en local (`proxy_pass` vers `127.0.0.1:8070`), jamais directement
depuis Internet.

Aucune règle firewall modifiée.

---

## 5. Vérification Odoo NSS

`proxy_mode = True` confirmé dans
`/opt/nss-erp/deploy/nss-test/config/odoo.local.conf` (ligne vérifiée
par grep ciblé, sans afficher le reste du fichier ni `admin_passwd`).

Architecture cible (non modifiée à ce stade) :

```
Internet → HTTPS 443 → Nginx → 127.0.0.1:8070 → nss_test_odoo
```

---

## 6. Exemple de configuration Nginx préparé (non déployé)

Fichier créé dans ce dépôt (jamais copié sur le VPS) :
`deploy/nss-test/nginx/nss-test.conf.example`.

Points clés repris des configurations existantes (`mpsenegal.com` pour
les timeouts/cache static, `n8n.atta-africa.com` pour le pattern
websocket) :

- `server_name ERP_TEST_DOMAIN` — placeholder, **à remplacer par le PO** ;
- `proxy_pass http://127.0.0.1:8070` ;
- headers `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`,
  `X-Forwarded-Host` ;
- bloc `/websocket` avec `Upgrade`/`Connection` (Odoo 18 — endpoint
  websocket, pertinent même en mode `workers=0` du pilote actuel) ;
- `proxy_read/connect/send_timeout 720s` (aligné sur Odoo 19) ;
- `client_max_body_size 100m` (pièces jointes / imports) ;
- logs dédiés : `/var/log/nginx/nss-test-access.log` et
  `nss-test-error.log` (distincts d'Odoo 19 et n8n) ;
- section HTTPS laissée à Certbot (ajoutée automatiquement au
  Checkpoint 5B via `certbot --nginx`, comme pour les 3 sites existants).

**Recommandation d'emplacement futur (Checkpoint 5B uniquement) :**
`/etc/nginx/sites-available/<ERP_TEST_DOMAIN>`, activé par symlink dans
`sites-enabled/`, suivant exactement le pattern des 3 sites déjà en
place.

---

## 7. Plan DNS (documentation uniquement — aucun enregistrement créé)

```
Type    : A
Nom     : <ERP_TEST_DOMAIN> — [À FOURNIR PO]
Valeur  : 195.35.2.137 (IP publique du VPS, vérifiée en lecture seule)
TTL     : valeur par défaut du registrar (ex. 3600s) — raisonnable, non prescriptive
```

Aucun enregistrement DNS n'a été créé ou modifié.

---

## 8. Procédure future — Checkpoint 5B (documentée, non exécutée)

1. Le PO fournit le sous-domaine (`ERP_TEST_DOMAIN`).
2. Créer le record DNS A correspondant.
3. Attendre la résolution DNS.
4. Créer le server block Nginx NSS à partir de
   `deploy/nss-test/nginx/nss-test.conf.example`.
5. `nginx -t`.
6. `systemctl reload nginx` — uniquement après validation du test.
7. Vérifier HTTP (`curl` sur le domaine, port 80).
8. Demander un certificat Let's Encrypt (`certbot --nginx -d ERP_TEST_DOMAIN`).
9. Vérifier HTTPS.
10. Vérifier l'intégration au renouvellement automatique (`certbot.timer`).
11. Vérifier Odoo NSS dans un navigateur.
12. Revalider Odoo 19 et n8n (non-régression).

Aucune de ces étapes n'a été réalisée dans ce checkpoint.

---

## 9. Points à valider PO

```
POINTS_A_VALIDER_PO
- ERP_TEST_DOMAIN : sous-domaine NSS TEST à fournir par le PO (ARCH-06,
  déjà ouvert dans NSS_ERP_02/NSS_ERP_03/NSS_ERP_04).
```

---

## 10. Anomalies détectées

Aucune.

---

*Fin du document NSS_ERP_05_LOT1B_CHECKPOINT5A_HTTPS_AUDIT.md*
