# Addons NSS

Ce répertoire est destiné aux modules Odoo spécifiques développés pour NSS
(ex. `nss_core`, `nss_project`, `nss_account` — voir
`docs/NSS_ERP_02_ARCHITECTURE_ODOO.md` section 21 pour le détail de ces
modules et leur périmètre).

## État actuel

**Vide.** Aucun module n'a encore été développé à ce stade (LOT 1A —
préparation de l'environnement uniquement). Ce répertoire sert de point
de montage pour le conteneur `nss-odoo` défini dans
`deploy/nss-test/compose.yaml` :

```yaml
volumes:
  - ../../addons:/mnt/extra-addons:ro
```

Il est monté **en lecture seule** dans le conteneur, à l'emplacement
`/mnt/extra-addons`, référencé dans `addons_path` du template versionné
`deploy/nss-test/config/odoo.conf.example` — et donc, en LOT 1B, du
fichier réellement monté `deploy/nss-test/config/odoo.local.conf` (non
versionné, créé à partir de ce template).

## Convention future

Chaque module NSS sera un sous-répertoire de `addons/`, au format standard
d'un module Odoo (`__manifest__.py`, `models/`, `views/`, `security/`,
etc.), par exemple :

```
addons/
├── README.md
├── nss_core/
├── nss_project/
└── nss_account/       (si nécessaire, cf. NSS_ERP_02 §21)
```

Aucun module n'est créé dans ce lot. La création des modules NSS suivra
les décisions d'architecture déjà validées dans `NSS_ERP_02` et sera
traitée dans un lot dédié, après validation du Product Owner.
