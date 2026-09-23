# NSS ERP — Audit VPS Hostinger

**Référence :** NSS_ERP_03
**Version :** 1.0
**Date :** 23 septembre 2026
**Auteur :** Claude Code (intégrateur technique)
**Statut :** audit bloqué — accès technique insuffisant (voir section 1)
**Prérequis :** NSS_ERP_02 V1.1 (architecture Odoo)

---

## 1. Résumé exécutif

Cet audit devait déterminer, en lecture seule, si le VPS Hostinger déjà utilisé par le Product Owner peut accueillir une instance NSS ERP TEST (Odoo 18 Community) sans mettre en danger les services existants.

**L'audit n'a pas pu être exécuté techniquement.** Aucune des deux voies d'accès prévues par la mission n'a abouti :

- Le serveur MCP Hostinger est connecté à la session, mais les appels aux endpoints d'hébergement/VPS/facturation renvoient tous une erreur **401 (non autorisé)**. Seul l'endpoint de messagerie (`mail_listOrdersV1`) a répondu, avec une liste vide. Cela indique un jeton d'API dont le périmètre (scope) ne couvre pas l'hébergement/VPS, et non une absence de VPS.
- Aucun accès SSH n'est configuré dans cette session (pas de clé privée dans `~/.ssh/`, pas d'hôte connu, pas de variable d'environnement pointant vers le VPS).

Par conséquent, **aucune des mesures demandées (CPU, RAM, disque, services, instances Odoo, PostgreSQL, Nginx, ports, sauvegardes, sécurité) n'a pu être collectée**, et ce rapport ne contient aucune valeur inventée. Toutes les sections techniques sont marquées `[NON DISPONIBLE — ACCÈS REQUIS]`.

**Conclusion (section 17) : STOP — VPS À ADAPTER**, au sens où l'accès doit être établi avant que l'audit — puis le LOT 1 — puissent avancer. Ce n'est pas un constat d'insuffisance du VPS lui-même, qui reste `[À VALIDER PO]`.

---

## 2. Méthode et périmètre

Périmètre demandé : audit technique en lecture seule uniquement, sans aucune installation, modification, création, démarrage/arrêt/redémarrage de service, ni écriture sur le serveur.

Deux canaux d'accès étaient prévus par la mission, dans cet ordre de priorité :

1. **MCP Hostinger connecté à Claude Code** — utilisé en priorité.
2. **SSH en lecture seule**, uniquement si des informations manquaient après le MCP et si un accès autorisé était disponible.

### 2.1 Tentatives effectuées via MCP Hostinger

| Appel | Résultat | Interprétation |
|---|---|---|
| Recherche exhaustive des outils `VPS_*` exposés à cette session | 10 outils trouvés, tous des actions d'écriture (firewall, clés publiques, snapshot, enregistrement PTR, script post-install, déploiement de projet Docker) | **Aucun outil de lecture** (liste des VPS, détails d'une VM, métriques CPU/RAM/disque) n'est exposé dans le périmètre `VPS_*` de ce serveur MCP pour cette session |
| `mcp__Hostinger__billing_getSubscriptionListV1` | Erreur 401 | Périmètre du jeton insuffisant pour la facturation |
| `mcp__Hostinger__hosting_listOrdersV1` | Erreur 401 | Périmètre du jeton insuffisant pour l'hébergement |
| `mcp__Hostinger__hosting_listWebsitesV1` | Erreur 401 | Périmètre du jeton insuffisant pour l'hébergement |
| `mcp__Hostinger__mail_listOrdersV1` | Succès — `{"data": [], "total": 0}` | Confirme que la connexion MCP fonctionne bien pour le périmètre « mail », mais qu'aucun produit mail n'est associé — n'apporte aucune information sur le VPS |

Le connecteur Hostinger apparaît comme « connecté » côté session (`ListConnectors` → `connected: true`), ce qui exclut une déconnexion pure et simple. Les appels ont été **retentés plusieurs fois** (`billing_getSubscriptionListV1`, `hosting_listOrdersV1`, `agency-hosting_listOrdersV1`), à des moments différents de la session, avec le même résultat (401) à chaque fois — ce n'est donc pas un incident transitoire.

Deux causes possibles, à vérifier côté Hostinger/claude.ai :

1. Le jeton API Hostinger relié à ce connecteur n'a, dans hPanel, que le périmètre **Email** activé, sans les périmètres Hébergement / VPS / Facturation (les jetons API Hostinger sont accordés par groupe de permissions à la création).
2. Le connecteur a été (re)connecté ou son périmètre modifié **après le démarrage de cette session** — les connecteurs ne sont lus qu'au démarrage d'une session, donc un changement récent ne serait pas encore pris en compte ici et nécessiterait une nouvelle session.

Dans les deux cas, le blocage est un problème de **périmètre d'autorisation (scope) du jeton**, pas d'absence de connecteur.

### 2.2 Tentative d'accès SSH

Vérification de l'environnement de la session :
- `~/.ssh/` : vide (aucune clé privée, aucun `config`, aucun `known_hosts` pointant vers un VPS).
- Variables d'environnement : aucune référence à un hôte, une IP ou des identifiants VPS.

Conformément à la consigne de ne jamais demander de mot de passe dans le chat, **aucune tentative de connexion SSH interactive n'a été faite** et aucun secret n'a été demandé.

### 2.3 Ce qui n'a donc pas pu être vérifié

L'intégralité des sections 5 à 12 de la mission (caractéristiques VPS, services, instances Odoo, PostgreSQL, Nginx/HTTPS, ports/réseau, sauvegardes, sécurité) repose sur des commandes système (`uname`, `lscpu`, `free`, `df`, `systemctl status`, `ss`/`netstat`, `psql`, `nginx -T`, etc.) qui n'ont pas pu être exécutées, faute d'accès.

---

## 3. Caractéristiques du VPS

`[NON DISPONIBLE — ACCÈS REQUIS]`

---

## 4. CPU / RAM / disque

| Élément | Valeur |
|---|---|
| OS / distribution | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| Version Ubuntu | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| Architecture CPU | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| vCPU | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| RAM totale | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| RAM utilisée | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| RAM disponible | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| Swap | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| Disque total | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| Disque utilisé | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| Disque disponible | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| Filesystem | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| Uptime | `[NON DISPONIBLE — ACCÈS REQUIS]` |
| Load average | `[NON DISPONIBLE — ACCÈS REQUIS]` |

Rappel NSS_ERP_02 §17 : l'estimation « 512 Mo / 1 worker » ne doit **pas** être retenue comme dimensionnement de référence — elle reste à vérifier par une mesure réelle, toujours non disponible à ce stade.

---

## 5. Services actifs

`[NON DISPONIBLE — ACCÈS REQUIS]` pour Odoo, PostgreSQL, Nginx, Apache, Docker, Redis, Certbot et tout autre service.

---

## 6. Instances Odoo existantes

`[NON DISPONIBLE — ACCÈS REQUIS]`

Aucune instance Odoo n'a pu être identifiée, ni confirmée absente. Aucune donnée sensible (mot de passe admin, identifiants PostgreSQL, tokens) n'a été manipulée puisqu'aucun accès n'a eu lieu.

---

## 7. PostgreSQL

`[NON DISPONIBLE — ACCÈS REQUIS]`

---

## 8. Nginx / HTTPS

`[NON DISPONIBLE — ACCÈS REQUIS]`

---

## 9. Ports et réseau

`[NON DISPONIBLE — ACCÈS REQUIS]` pour les ports 22, 80, 443, 5432 et tout autre port. Aucun port disponible pour NSS TEST ne peut donc être proposé de façon fiable à ce stade (voir section 14 pour une proposition indicative, à confirmer).

---

## 10. Sauvegardes

`[NON DISPONIBLE — ACCÈS REQUIS]`

---

## 11. Sécurité observée

`[NON DISPONIBLE — ACCÈS REQUIS]`

---

## 12. Risques de coexistence

Sans mesure réelle, tout risque de coexistence avec des instances existantes reste **hypothétique**. Le seul risque certain à ce stade est **procédural** : lancer une installation sans audit préalable validé irait à l'encontre de la règle du LOT 0 et de la règle NSS_ERP_02 §17 (« auditer l'instance/l'environnement disponible avant déploiement »).

---

## 13. Capacité NSS TEST

**« Peut-on installer NSS ERP TEST sur ce VPS sans mettre en danger les instances Odoo existantes ? »**

**Réponse : impossible à déterminer — l'audit n'a pas pu être réalisé.**

Aucune des trois réponses attendues (OUI / OUI SOUS CONDITIONS / NON) ne peut être justifiée par des mesures réelles, puisqu'aucune mesure n'a pu être prise. Répondre par défaut « OUI » ou « NON » serait une hypothèse présentée comme un fait, ce que `CLAUDE.md` interdit explicitement (section 3).

---

## 14. Architecture proposée NSS TEST

Proposition indicative, reprenant les choix déjà validés dans NSS_ERP_02 (section 21 et 22), **à confirmer une fois l'audit réel possible** :

```text
Utilisateur système   : odoo-nss
Chemin Odoo           : /opt/odoo-nss/
Service systemd       : odoo-nss-test.service
Port                  : 8070 (à confirmer disponible — non vérifié)
Rôle PostgreSQL        : odoo_nss
Nom DB TEST            : nss_test
Fichier config         : /etc/odoo/odoo-nss-test.conf
Filestore               : /opt/odoo-nss/filestore/
Addons NSS              : nss_core (+ nss_project, nss_account si nécessaire)
Sous-domaine             : nss-test.<domaine à définir> (ARCH-06, non validé)
Reverse proxy            : bloc Nginx dédié, sans toucher aux blocs existants
HTTPS                    : Let's Encrypt via certbot, certificat dédié au sous-domaine
Sauvegardes               : pg_dump quotidien + tar du filestore, copie externe avant PROD
```

Cette proposition reprend telle quelle l'architecture cible de NSS_ERP_02 ; elle n'a **pas** été adaptée aux ressources réelles du VPS puisque celles-ci restent inconnues.

---

## 15. Pré-requis avant installation

1. Rétablir un accès en lecture au VPS, selon l'une de ces options :
   - vérifier dans hPanel que le jeton API Hostinger relié au connecteur couvre bien les périmètres Hébergement / VPS / Facturation (pas seulement Email), puis démarrer une **nouvelle session** Claude Code (les connecteurs ne sont relus qu'au démarrage d'une session) ; ou
   - ajouter une clé SSH publique de cette session au VPS, avec un compte disposant de droits de lecture seule ; ou
   - à défaut, que le PO exécute lui-même les commandes de diagnostic listées en section 2.3 et fournisse la sortie brute (sans mot de passe ni secret).
2. Réexécuter l'audit technique (sections 3 à 13) avec les données réelles.
3. Obtenir la confirmation ARCH-05 (RAM, CPU, disque, OS, PostgreSQL) et ARCH-06 (sous-domaine) déjà demandées dans NSS_ERP_02 section 25 — ce LOT 0 devait précisément produire ces réponses.

---

## 16. Points bloquants

| ID | Blocage | Impact | Action requise |
|---|---|---|---|
| AUDIT-01 | Jeton API Hostinger connecté sans périmètre hébergement/VPS/facturation (401 sur `hosting_*`, `billing_*`) | Impossible de lister le(s) VPS ou d'obtenir ses métriques via MCP | Élargir le scope du jeton côté Hostinger/claude.ai |
| AUDIT-02 | Aucun accès SSH configuré dans la session (pas de clé, pas d'hôte) | Impossible de lancer les commandes de diagnostic système en secours | Fournir une clé SSH en lecture seule à la session, ou exécuter les commandes soi-même |
| AUDIT-03 | Absence de toute mesure réelle (CPU/RAM/disque/services/Odoo/PostgreSQL/Nginx/ports/sauvegardes/sécurité) | Impossible de répondre à la question de capacité (section 13) | Résoudre AUDIT-01 ou AUDIT-02 puis relancer l'audit |

---

## 17. Recommandation LOT 1

Ne pas démarrer le LOT 1 (ni aucune installation) tant que les points bloquants AUDIT-01/02/03 ne sont pas résolus et que l'audit technique n'a pas produit de mesures réelles.

---

## Conclusion

**STOP — VPS À ADAPTER**

(Le blocage porte sur l'accès nécessaire à l'audit, pas sur une insuffisance démontrée du VPS lui-même, laquelle reste `[À VALIDER PO]`.)

---

*Fin du document NSS_ERP_03_AUDIT_VPS_HOSTINGER.md*
