# NSS ERP — LOT 2B Checkpoint 3 : installation contrôlée de `nss_network` sur NSS TEST

**Référence :** NSS_ERP_09
**Date :** 25 septembre 2026
**Statut :** `nss_network` installé sur `nss_test`, tests unitaires exécutés (15/15), aucune donnée réelle
**Prérequis :** `NSS_ERP_08` (code développé, non installé) ; validation PO explicite donnée le 25 septembre 2026 pour engager ce Checkpoint 3 (conformément à `NSS_ERP_08` §15)

---

## 1. Objectif

Installer réellement l'addon `nss_network` (commit de référence `3003ebe`, branche `main`) sur l'environnement `nss_test`, exécuter ses tests unitaires dans un vrai conteneur Odoo 18 + PostgreSQL 16, et vérifier l'absence de régression sur les autres services du VPS (Odoo 19 `mpsenegal.com`, `n8n`, `n8n-connect`, PostgreSQL système, Nginx/HTTPS).

Aucune donnée réelle NSS n'est créée. Aucun des 10 pays NSS n'est chargé (reporté à un checkpoint dédié).

---

## 2. Anomalies détectées et traitées avant toute écriture

Deux anomalies ont été identifiées lors du contrôle en lecture seule (checkpoint 2) et résolues avec validation explicite du Product Owner avant de poursuivre :

1. **`.git\config` local corrompu** (poste Windows) : fichier de 901 octets entièrement composé d'octets nuls, empêchant toute commande git locale. Reconstruit à partir du remote identifié dans `.git/FETCH_HEAD` (`https://github.com/Amadousn221/nss-erp`), avec accord PO. `git status`/`git log` de nouveau fonctionnels après reconstruction ; aucun historique perdu (`.git/objects`, `refs`, `packed-refs` intacts).
2. **Prérequis documentaire manquant** : `NSS_ERP_08` §15 réservait explicitement l'installation (ce Checkpoint 3) à une nouvelle validation PO explicite, non tracée au moment de la reprise. Validation donnée explicitement par le PO le 25 septembre 2026 avant toute écriture sur le VPS.

Après résolution, l'état local a été vérifié conforme à la référence annoncée : branche `main`, commit `3003ebe` (après `git fetch` + fast-forward — le dépôt local était simplement en retard d'un commit, aucun conflit réel), working tree propre.

---

## 3. Contrôle VPS avant action (lecture seule)

- Connexion SSH `root@195.35.2.137` (`srv1367494`) via `~/.ssh/claude_nss_local` : OK.
- État Docker conforme à `NSS_ERP_05`/`NSS_ERP_08` : `nss_test_odoo` (`127.0.0.1:8070->8069` uniquement), `nss_test_db` (aucun port publié, healthy), réseau `nss_test_net` isolé, volumes `nss_odoo_data`/`nss_pg_data`.
- `n8n` et `n8n-connect` actifs (`127.0.0.1:5678`/`5679`), aucun lien avec `nss_test_net`.
- `/opt/nss-erp/addons` (hôte) → `/mnt/extra-addons` (conteneur, lecture seule) : ne contenait que `README.md` avant ce checkpoint — confirmation que `nss_network` n'était pas encore déployé.
- `/opt/nss-erp` n'est pas un dépôt git sur le VPS (déploiement par copie de fichiers, pas par `git pull` côté serveur).
- Nginx (`sites-enabled` intact, 4 sites), `certbot.timer` actif, PostgreSQL système actif, HTTPS `erp-test.wasafrica.org` → 200.

Aucune anomalie côté VPS. Environnement conforme au plan de déploiement.

---

## 4. Sauvegarde pré-déploiement

Créée avant toute écriture, sous `/var/backups/nss-erp/pre-checkpoint3-20260925-0700/` (permissions restreintes, `700`/`600`, non versionné) :

- **Dump PostgreSQL pré-déploiement : réalisé.** `nss_test_db.sql` : dump complet de la base `nss_test` (`pg_dump`, format SQL texte, 64 362 lignes, ~8,9 Mo), exécuté via les identifiants déjà injectés dans l'environnement du conteneur `nss_test_db` (jamais lus ni affichés par Claude Code — voir `NSS_ERP_05` §7 sur la non-exposition des secrets).
- **Snapshot addons pré-déploiement : réalisé.** `addons-before.tar.gz` : snapshot de `/opt/nss-erp/addons` avant écriture (contenait uniquement `README.md`).
- **Filestore pré-déploiement dédié : NON réalisé.** Ce backup ne contient aucune archive du répertoire `filestore/nss_test`. Il ne faut pas comprendre le dump PostgreSQL comme couvrant le filestore : ce sont deux composants distincts sur Odoo (base de données vs pièces jointes/documents stockés sur disque).

**Écart factuel documenté :** le backup pré-déploiement réel du 25 septembre 2026 ne comprend donc que le dump PostgreSQL et le snapshot du dossier `addons/`, sans backup filestore dédié ni manifest SHA256 formalisé à ce moment-là. Ceci est corrigé a posteriori par le backup post-déploiement complémentaire (section 4 bis) et ne doit pas être présenté comme ayant été fait initialement.

Ce point a une portée limitée en pratique : aucune donnée métier NSS n'existait dans `nss_test` avant l'installation (le module `nss_network` lui-même n'était pas encore installé, donc ses modèles — et tout filestore associé — n'existaient pas), et le filestore Odoo pré-existant (natif, hors NSS) était déjà couvert par le baseline `baseline-20260924-1855` (LOT 2A, 24 septembre 2026, dump + filestore + manifest SHA256 validés — voir `NSS_ERP_06`). Ce baseline antérieur reste distinct et ne remplace pas un backup pré-déploiement daté du 25 septembre : il documente l'état du 24 septembre, pas celui immédiatement avant ce Checkpoint 3.

Le backup `baseline-20260924-1855` était déjà présent et n'a pas été modifié.

---

## 4 bis. Sauvegarde post-déploiement complémentaire

Pour combler l'écart ci-dessus, une sauvegarde complémentaire a été créée après l'installation et les tests, **sans aucune écriture de donnée métier**, sous `/var/backups/nss-erp/post-checkpoint3-20260925-1110/` (permissions restreintes, `700`/`600`, non versionné). Présentée explicitement comme **POST-déploiement** — elle ne se substitue pas rétroactivement à un backup pré-déploiement.

| Fichier | Contenu | Validation |
|---|---|---|
| `nss_test_post_checkpoint3.dump` | Dump PostgreSQL complet de `nss_test`, format `pg_dump -Fc` (custom) | `pg_restore --list` : **5037 entrées TOC**, exit code 0 |
| `nss_test_filestore.tar.gz` | Archive de `filestore/nss_test/` (répertoire complet) | `tar -tzf` : **76 entrées**, lecture sans erreur |
| `MANIFEST.txt` | Métadonnées : date, type = POST-CHECKPOINT3, SHA256 des deux fichiers, état `nss_network` = `installed`, 0/0/0 lignes dans les 3 tables NSS | Aucun secret — vérifié manuellement avant écriture |

Empreintes SHA256 (également dans `MANIFEST.txt`) :

```
8298d147dda4fb0700ff06a4d351617541208e4620ef1ec893f27f535a0d96e0  nss_test_post_checkpoint3.dump
26a16667703dca339c323ae71c6df26f260d078f27ac250a35ab67048bcd6dc4  nss_test_filestore.tar.gz
```

Recontrôle en lecture seule effectué immédiatement après cette sauvegarde : `nss_network` = `installed`, 0/0/0 ligne dans les tables NSS, `nss_test_odoo`/`nss_test_db` actifs sans interruption, HTTPS 200, Odoo 19/`n8n`/`n8n-connect`/PostgreSQL système/Nginx tous intacts (détail identique à la section 11).

---

## 5. Déploiement du commit validé

- Module `nss_network` empaqueté localement depuis `addons/nss_network/` (commit `3003ebe`), transféré par `scp` vers `/tmp/nss_network.tar.gz` sur le VPS.
- Intégrité vérifiée par `sha256sum` avant/après transfert (empreintes identiques).
- Extrait dans `/opt/nss-erp/addons/nss_network/` (18 fichiers, conformes à la liste documentée dans `NSS_ERP_08` §2), permissions `755`/`644`, propriétaire `root:root`.
- Confirmé visible en lecture seule à l'intérieur du conteneur (`/mnt/extra-addons/nss_network`).
- Compilation Python réelle (`py_compile`) exécutée à l'intérieur du conteneur Odoo 18 : **11/11 fichiers `.py` compilés sans erreur** — limite documentée dans `NSS_ERP_08` §13 (absence de Python local) désormais levée pour cette vérification.

---

## 6. Installation du module

Commande exécutée via l'entrypoint natif de l'image Odoo (nécessaire pour l'injection correcte des identifiants PostgreSQL depuis les variables d'environnement du conteneur) :

```
docker exec nss_test_odoo /entrypoint.sh odoo -d nss_test -i nss_network --stop-after-init
```

Résultat : **succès**, aucune erreur, aucune trace d'exception. `Module nss_network loaded in 0.57s, 391 queries`. 39 modules chargés au total (38 dépendances natives + `nss_network`).

---

## 7. Tests unitaires

Exécution réelle (non simulée) des tests, avec port HTTP alternatif (`--http-port=8090`) pour éviter le conflit avec l'instance `nss-odoo` permanente déjà active sur le port interne 8069 :

```
docker exec nss_test_odoo /entrypoint.sh odoo -d nss_test -u nss_network \
  --test-enable --test-tags /nss_network --http-port=8090 --stop-after-init
```

**Résultat : 15 tests exécutés, 15 réussis, 0 échec, 0 erreur** (`odoo.tests.result: 0 failed, 0 error(s) of 15 tests when loading database 'nss_test'`), cohérent avec `NSS_ERP_08` §12 (15 méthodes de test documentées) et avec le message du commit `3003ebe` (« 15/15 tests », validés au préalable par CI GitHub Actions).

Vérification post-tests : `nss_country_membership`, `nss_membership`, `nss_responsibility_history` contiennent **0 ligne** après exécution — les `TransactionCase` ont bien annulé toutes leurs écritures, aucune donnée de test résiduelle.

---

## 8. Contrôles de non-régression

| Élément | Avant | Après | Résultat |
|---|---|---|---|
| `nss_test_odoo` | Up 11h | Up 11h (jamais redémarré) | Conforme |
| Port 8070 | `127.0.0.1:8070->8069` | `127.0.0.1:8070->8069` | Inchangé |
| `nss_network` (`ir_module_module.state`) | absent | `installed` | Conforme |
| HTTPS `erp-test.wasafrica.org/web/login` | 200 | 200 | Conforme |
| Odoo 19 `mpsenegal.com` | actif | HTTP 303 (réponse serveur normale) | Actif, aucune régression détectée |
| `n8n` / `n8n-connect` | 200 / 200 | 200 / 200 | Conformes |
| PostgreSQL système | actif | actif | Conforme |
| Nginx | actif, config valide | actif, config valide (`nginx -t` OK) | Conforme |
| UFW | 8070/8090 absents | 8070/8090 absents | Conforme (aucun port interne exposé) |

Aucune régression détectée sur les services existants (Odoo 19, n8n, n8n-connect, PostgreSQL système, Nginx/HTTPS).

---

## 9. Sécurité et données

- Aucune donnée réelle NSS créée (0 ligne dans les 3 tables NSS après tests).
- Aucun secret (mot de passe PostgreSQL, mot de passe maître Odoo, clé SSH) lu, affiché ou consigné dans ce document ou dans les sorties de commande capturées.
- Sauvegarde pré-déploiement stockée avec permissions restreintes (`700`/`600`), non versionnée.

---

## 10. Points à valider PO

Aucun point bloquant restant pour ce checkpoint.

Rappels pour la suite (hors périmètre de ce document, cf. `NSS_ERP_08` §15) :
- conception des record rules par pays (affectation utilisateur ↔ pays) ;
- chargement des 10 pays NSS (données publiques, coordinations fictives), dans un checkpoint distinct dédié aux données, nécessitant une nouvelle validation PO explicite avant toute écriture de données.

---

## 11. Contrôle final avant clôture (lecture seule, 25 septembre 2026)

Recontrôle effectué avant clôture du checkpoint, en lecture seule uniquement — aucune écriture supplémentaire sur le VPS :

| Élément | Résultat |
|---|---|
| `nss_network` (`ir_module_module.state`) | `installed` |
| `nss_country_membership` / `nss_membership` / `nss_responsibility_history` | 0 / 0 / 0 ligne |
| `nss_test_odoo` | Up 12h, `127.0.0.1:8070->8069` uniquement |
| `nss_test_db` | Up 19h (healthy) |
| HTTPS `erp-test.wasafrica.org/web/login` | HTTP 200 |
| Odoo 19 `mpsenegal.com` | HTTP 303 (réponse serveur normale, actif) |
| `n8n` / `n8n-connect` | HTTP 200 / 200 |
| PostgreSQL système | actif |
| Nginx | actif |

Aucune anomalie résiduelle constatée. Aucune donnée métier créée à cette étape.

---

*Fin du document NSS_ERP_09_LOT2B_CHECKPOINT3_INSTALLATION.md*
