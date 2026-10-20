# Addons NSS

Ce répertoire contient les modules Odoo spécifiques développés pour NSS.

## État actuel

**Un seul module : `nss_network`** (LOT 2B, Checkpoint 2), conformément à la
décision définitive du Product Owner du 24 septembre 2026 — voir
`docs/NSS_ERP_02_ARCHITECTURE_ODOO.md` section 21. Aucun autre addon
spécifique (`nss_core`, `nss_project`, `nss_account`, etc.) ne doit être créé
sans nouvelle validation PO explicite.

`nss_network` est **installé** sur l'environnement NSS TEST (base `nss_test`,
version `18.0.1.0.0`) ; le Checkpoint 4A (filtres métier et UX) y est déployé
depuis le 20 octobre 2026 (voir
`docs/implementation/NSS_ERP_09_LOT2B_CHECKPOINT3_INSTALLATION.md` et
`docs/implementation/NSS_ERP_12_LOT2B_CHECKPOINT4A_DEPLOIEMENT.md`). Il ne
contient aucune donnée réelle NSS : aucun pays NSS n'est encore chargé.

Ce répertoire sert de point de montage pour le conteneur `nss-odoo` défini
dans `deploy/nss-test/compose.yaml` :

```yaml
volumes:
  - ../../addons:/mnt/extra-addons:ro
```

Il est monté **en lecture seule** dans le conteneur, à l'emplacement
`/mnt/extra-addons`, référencé dans `addons_path` du fichier de
configuration Odoo NSS (`deploy/nss-test/config/odoo.local.conf`, non
versionné).

## Structure

```
addons/
├── README.md
└── nss_network/
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    ├── security/
    ├── views/
    └── tests/
```
