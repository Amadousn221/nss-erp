# NSS ERP — LOT 2B Checkpoint 4B-B : configuration de base de `nss_test`

**Référence :** NSS_ERP_11
**Date :** 26 septembre 2026
**Statut :** société, pays, devise et paramètres admin de `nss_test` configurés via ORM Odoo ; aucune donnée métier NSS créée
**Prérequis :** `NSS_ERP_10` (Checkpoint 4A, filtres et UX de `nss_network`) ; backup pré-configuration créé et validé le 26 septembre 2026

---

## 1. Objectif

Configurer les paramètres de base de l'environnement `nss_test` (VPS `195.35.2.137`) via l'ORM Odoo, sans SQL direct et sans modification de `pg_hba.conf` :

- activer la langue `fr_FR` ;
- renommer la société par défaut (« My Company ») en « NSS ERP TEST » ;
- renommer le partenaire lié à la société ;
- définir le pays de la société sur le Sénégal ;
- définir la devise de la société sur XOF (si l'ORM l'autorise) ;
- définir la langue et le fuseau horaire de l'utilisateur admin.

Aucun déploiement du Checkpoint 4A, aucune copie de `nss_network`, aucun chargement des 10 pays NSS, aucune création d'organisation/adhésion/projet, aucune modification Nginx/DNS, aucune intervention sur l'instance Odoo 19 (`odoo.service`, natif).

---

## 2. Correction de contexte

Le conteneur `nss_test_odoo` ne tourne pas sur le poste Windows local : il tourne sur le VPS NSS (`195.35.2.137`, `srv1367494`). Toute commande Docker de ce checkpoint a été exécutée **sur le VPS, via SSH** (`ssh -i ~/.ssh/claude_nss_local root@195.35.2.137`), jamais localement.

---

## 3. Contrôle avant écriture

- Connexion SSH au VPS : OK.
- `nss_test_odoo` : `Up 40h` (running).
- `nss_test_db` : `Up 47h (healthy)`.
- HTTPS `/web/login` : `200`.
- `odoo.service` (Odoo 19 natif, production) : `active (running)`.
- `nginx` : `active`.
- PostgreSQL système : `active`.
- `n8n` / `n8n-connect` : conteneurs `Up`.

Aucune anomalie détectée. Poursuite autorisée.

---

## 4. Backup pré-configuration

Le backup annoncé comme déjà créé avant ce Checkpoint a été localisé et vérifié (aucune recréation nécessaire) :

`/var/backups/nss-erp/pre-checkpoint4b-config-20260926-1042/` (permissions restreintes, non versionné) :

| Fichier | Contenu |
|---|---|
| `nss_test_pre4b.dump` | Dump PostgreSQL complet de `nss_test` (format custom `pg_dump -Fc`) |
| `nss_test_filestore.tar.gz` | Archive du filestore `nss_test` |
| `manifest.json` | Métadonnées : date UTC, type `PRE-CHECKPOINT4B-CONFIG`, base, empreintes SHA256 |
| `SHA256SUMS.txt` | Empreintes SHA256 des deux fichiers |

Vérification d'intégrité (`sha256sum -c SHA256SUMS.txt`) : **OK** pour les deux fichiers.

---

## 5. Test de connexion ORM (lecture seule)

Commande exécutée sur le VPS, script Python passé via `stdin`, sans lecture ni affichage d'aucun secret :

```
ssh -i ~/.ssh/claude_nss_local root@195.35.2.137 \
  "docker exec -i nss_test_odoo /entrypoint.sh odoo shell -d nss_test --no-http"
```

Résultat : connexion réussie, `env.company.name` = `My Company` (état pré-configuration attendu). **PASS.**

---

## 6. Écritures ORM

Toutes les écritures ont été effectuées dans une seule transaction (script Python via `stdin` de `odoo shell`), avec `try/except` : en cas de refus ORM sur une étape quelconque, `env.cr.rollback()` annule l'intégralité de la transaction avant tout `commit()`.

### 6.1 Incidents rencontrés et corrigés (sans contournement)

1. **Champ `lang` invalide sur `base.language.install`** : en Odoo 18, ce wizard n'expose plus de champ `lang` (code texte). Un premier essai avec `lang_id` a également échoué. L'introspection ORM (`fields_get()`) a montré le champ réel : `lang_ids` (`many2many`). Corrigé en conséquence — aucune donnée n'a été committée lors de ces deux tentatives infructueuses (rollback automatique).
2. **Devise XOF introuvable en recherche par défaut** : `res.currency` filtre par défaut sur `active=True` ; XOF existe nativement mais était inactive. Corrigé en recherchant avec `active_test=False`, puis activée via `write({'active': True})` avant l'affectation à la société — aucun contournement SQL.

Après chacun de ces deux échecs, un contrôle en lecture seule a confirmé que le rollback avait bien annulé la totalité de la transaction, y compris l'installation partielle de `fr_FR` (`fr_FR.active` revenu à `False`).

### 6.2 Écriture réussie

| Étape | Action | Résultat |
|---|---|---|
| A | `fr_FR` installée via le wizard officiel `base.language.install` (`lang_ids`) | OK |
| E (pré) | `res.currency` XOF activée (`active_test=False` puis `write`) | OK |
| B | `res.company.name` : `My Company` → `NSS ERP TEST` | OK |
| C | `res.partner` (partenaire lié à la société) : `My Company` → `NSS ERP TEST` | OK |
| D | `res.company.country_id` → Sénégal (`res.country` natif, code `SN`) | OK |
| E | `res.company.currency_id` → XOF — l'ORM a accepté le changement sans erreur (base de test sans écritures comptables) | OK |
| F | `res.users` (admin) : `lang` → `fr_FR`, `tz` → `Africa/Dakar` (login, mot de passe et groupes non touchés) | OK |

Transaction validée par `env.cr.commit()`. Aucun SQL direct, aucune modification de `pg_hba.conf`, aucun secret lu ou affiché.

---

## 7. Validation post-écriture (ORM, lecture seule)

| Contrôle | Résultat |
|---|---|
| Nombre de sociétés | 1 |
| Société de l'admin | `NSS ERP TEST` |
| `res.company.name` | `NSS ERP TEST` |
| Partenaire lié à la société | `NSS ERP TEST` |
| Pays de la société | Sénégal |
| Devise de la société | XOF |
| Langue admin | `fr_FR` |
| Fuseau horaire admin | `Africa/Dakar` |
| `fr_FR` active | `True` |
| `en_US` active | `True` |
| `nss_network` (`ir.module.module.state`) | `installed` |

---

## 8. Contrôles de non-régression

| Élément | Résultat |
|---|---|
| `nss_test_odoo` | `Up`, jamais redémarré |
| `nss_test_db` | `Up (healthy)` |
| HTTPS `/web/login` | `200` |
| `odoo.service` (Odoo 19, natif) | `active` |
| `n8n` | `Up` |
| `n8n-connect` | `Up` |
| PostgreSQL système | `active` |
| Nginx | `active` |
| `nss_network` | `installed` (état inchangé par ce checkpoint) |

Aucune régression détectée sur les services existants.

---

## 9. Sécurité et données

- Aucun secret (mot de passe PostgreSQL, `POSTGRES_PASSWORD`, mot de passe admin Odoo, clé SSH) lu, affiché ou consigné dans ce document ou dans les commandes exécutées.
- `docker exec env` n'a jamais été utilisé.
- `.env` du VPS n'a jamais été lu.
- `pg_hba.conf` n'a pas été modifié ; PostgreSQL n'a pas été mis en `trust`.
- Aucun `SQL UPDATE` direct — uniquement des écritures ORM Odoo, validées transactionnellement.
- Aucune donnée métier NSS créée (pas d'organisation, pas d'adhésion, pas de projet, pas de chargement des 10 pays).

---

## 10. Points à valider PO

Aucun point bloquant restant pour ce checkpoint.

Rappels hors périmètre (reportés à des checkpoints dédiés, cf. `NSS_ERP_09` §10) :
- déploiement du Checkpoint 4A ;
- chargement des 10 pays NSS ;
- conception des record rules par pays.

---

*Fin du document NSS_ERP_11_LOT2B_CHECKPOINT4B_CONFIG.md*
