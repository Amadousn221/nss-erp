# NSS ERP — LOT 2B Checkpoint 1 : socle fonctionnel natif (contacts, mail, project)

**Référence :** NSS_ERP_07
**Date :** 24 septembre 2026
**Statut :** installation native réalisée — **aucun développement `nss_network`, aucune donnée métier**
**Prérequis :** LOT 2A clôturé et fusionné dans `main` (`NSS_ERP_06_LOT2A_BASELINE_MODULE_AUDIT.md`)

---

## 1. État avant intervention

| Élément | État constaté |
|---|---|
| `nss_test_odoo` | RUNNING |
| `nss_test_db` | HEALTHY |
| `https://erp-test.wasafrica.org/web/login` | HTTP 200 |
| Odoo 19 (existant) | actif, inchangé |
| n8n / n8n-connect | actifs, inchangés |
| PostgreSQL système | actif, inchangé |
| Nginx | actif, inchangé |
| Baseline LOT 2A (`/var/backups/nss-erp/baseline-20260924-1855/`) | présente, intacte |

**Modules installés avant ce lot (12) :** `auth_totp`, `base`, `base_import`, `base_import_module`, `base_setup`, `bus`, `html_editor`, `iap`, `web`, `web_editor`, `web_tour`, `web_unsplash` — hérités de l'initialisation `base` du LOT 1B (Checkpoint 3).

Aucune anomalie détectée avant installation.

---

## 2. Modules installés

Installation demandée : `contacts`, `mail`, `project` (module `base` déjà présent, non réinstallé explicitement).

**Modules à l'état `installed` après ce lot (38 au total) :**

`analytic`, `auth_signup`, `auth_totp`, `auth_totp_mail`, `auth_totp_portal`, `base`, `base_import`, `base_import_module`, `base_install_request`, `base_setup`, `bus`, `contacts`, `digest`, `google_gmail`, `html_editor`, `http_routing`, `iap`, `iap_mail`, `mail`, `mail_bot`, `partner_autocomplete`, `phone_validation`, `portal`, `portal_rating`, `privacy_lookup`, `project`, `project_sms`, `project_todo`, `rating`, `resource`, `resource_mail`, `sms`, `snailmail`, `uom`, `web`, `web_editor`, `web_tour`, `web_unsplash`.

---

## 3. Dépendances automatiquement ajoutées

26 modules ont été installés automatiquement par la résolution de dépendances d'Odoo (non demandés explicitement) :

`analytic`, `auth_signup`, `auth_totp_mail`, `auth_totp_portal`, `base_install_request`, `digest`, `google_gmail`, `http_routing`, `iap_mail`, `mail_bot`, `partner_autocomplete`, `phone_validation`, `portal`, `portal_rating`, `privacy_lookup`, `project_sms`, `project_todo`, `rating`, `resource`, `resource_mail`, `sms`, `snailmail`, `uom`.

**Point d'attention documenté explicitement (conformément à la consigne du checkpoint) :** le module **`analytic`** figure dans cette liste alors qu'il était nommément dans les modules interdits pour ce checkpoint. Vérification faite sur le manifest officiel `odoo/odoo` (branche `18.0`) : `analytic` est une **dépendance obligatoire et directe du module `project`** (`'depends': ['analytic', 'base_setup', 'mail', 'portal', 'rating', 'resource', 'web', 'web_tour', 'digest', ...]`). Il est techniquement impossible d'installer `project` sans `analytic` en Odoo 18 Community. Ce module ne contient que le **framework technique** des comptes/plans analytiques (modèles `account.analytic.account`, `account.analytic.plan`) — **aucune écriture comptable, aucun journal, aucun plan de comptes, aucune dépendance vers `account`** n'a été ajoutée. Il ne s'agit donc pas d'une installation de comptabilité, mais d'une dépendance technique normale, non bloquante au sens de la consigne (« documente-la mais ne bloque pas si elle est normale »).

Tous les autres modules ajoutés automatiquement sont des dépendances natives standards de `mail`/`project` (SMS, notifications, portail, évaluations, ressources, etc.), sans lien avec la comptabilité ni avec un module OCA.

---

## 4. Méthode d'installation

Depuis `/opt/nss-erp/deploy/nss-test` sur le VPS :

1. `docker compose stop nss-odoo` (arrêt temporaire, `nss_test_db` non arrêté).
2. `docker compose run --rm nss-odoo odoo --config /etc/odoo/odoo.conf -d nss_test -i contacts,mail,project --without-demo=all --stop-after-init` — conteneur éphémère d'installation, sans port publié, `--stop-after-init` (pas de serveur HTTP démarré pendant l'installation).
3. `docker compose start nss-odoo` — redémarrage normal après succès.

Résultat : **38 modules chargés en 18,63 s, aucune erreur, arrêt propre** (« Modules loaded. » puis « Initiating shutdown »).

---

## 5. Résultat

| Vérification | Résultat |
|---|---|
| `contacts` | `installed` |
| `mail` | `installed` |
| `project` | `installed` |
| Menu racine « Contacts » | présent (`ir.ui.menu` id 108) |
| Menu racine « Project » | présent (`ir.ui.menu` id 131) |
| Traceback dans les logs après redémarrage | aucun |
| Module OCA installé | aucun |
| Module NSS (`nss_network` ou autre) installé | aucun |

L'accessibilité des applications a été vérifiée par requête directe en base (état des modules + présence des menus racine), **sans tentative de connexion à l'interface** (le mot de passe administrateur, changé manuellement par le PO au Checkpoint 6 du LOT 1B, n'est ni connu ni utilisé par Claude Code).

---

## 6. Non-régression

| Vérification | Résultat |
|---|---|
| `https://erp-test.wasafrica.org/web/login` | HTTP 200 |
| `nss_test_odoo` | RUNNING |
| `nss_test_db` | HEALTHY |
| Port `8070` | `127.0.0.1:8070` uniquement (inchangé) |
| PostgreSQL NSS exposé sur l'hôte | NON |
| Odoo 19 | actif, inchangé |
| n8n / n8n-connect | actifs, inchangés |
| PostgreSQL système | actif, inchangé |
| Nginx | actif, inchangé |

Aucune anomalie détectée.

---

## 7. Modules explicitement non installés

Conformément aux interdictions du checkpoint, **aucun** des modules suivants n'a été installé : `account`, `l10n_syscohada`, `l10n_sn`, `account_budget_oca`, `account_financial_report`, `account_reconcile_oca`, `account_reconcile_model_oca`, ni aucun autre addon OCA ou tiers. Aucun addon spécifique NSS (`nss_network` ou autre) n'a été créé. Aucun pays, organisation, coordinatrice, projet métier, utilisateur métier ou donnée réelle n'a été créé.

---

## 8. Préparation du futur `nss_network`

Le socle natif requis par `NSS_ERP_02` (§21, addon unique `nss_network`) est maintenant disponible sur `nss_test` : `contacts` (`res.partner`), `mail` (chatter/pièces jointes), `project` (`project.project`/`project.task`), ainsi que `analytic` (dépendance technique de `project`, potentiellement réutilisable pour les plans analytiques Pays/Projet/Bailleur prévus en Phase comptable ultérieure — sans qu'aucune décision comptable ne soit prise ou anticipée ici).

Aucun code, modèle, vue ou donnée `nss_network` n'a été créé dans ce lot. Le développement de `nss_network` reste un lot distinct, à démarrer uniquement sur nouvelle instruction PO explicite.

---

*Fin du document NSS_ERP_07_LOT2B_NATIVE_FOUNDATION.md*
