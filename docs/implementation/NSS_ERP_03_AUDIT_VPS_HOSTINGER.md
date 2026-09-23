# NSS ERP — Audit VPS Hostinger

**Référence :** NSS_ERP_03
**Version :** 1.0
**Date :** 23 septembre 2026
**Auteur :** Claude Code (intégrateur technique)
**Statut :** Audit non concluant — accès en lecture indisponible
**Périmètre :** LOT 0 — audit technique en lecture seule du VPS Hostinger

---

## 1. Résumé exécutif

Cet audit avait pour objectif de déterminer, à partir de mesures réelles et en lecture seule, si le VPS Hostinger existant peut accueillir une instance NSS ERP TEST (Odoo 18 Community) sans mettre en danger les instances Odoo déjà en place.

**Constat principal : l'audit n'a pas pu être réalisé.** Aucune donnée technique réelle sur le VPS (OS, CPU, RAM, disque, services, instances Odoo, PostgreSQL, Nginx, ports, sauvegardes, sécurité) n'a pu être collectée, pour deux raisons cumulatives :

1. Le connecteur **MCP Hostinger** disponible dans cette session **n'expose aucun outil de lecture/inventaire pour les VPS** (pas de « liste des VPS », pas de « détails VPS », pas d'exécution de commande). Les seuls outils `VPS_*` disponibles sont des actions d'écriture (attacher une clé SSH, créer/activer/désactiver un pare-feu, créer une règle de pare-feu, créer un snapshot, créer un enregistrement PTR, créer un script post-install, déployer un projet Docker) — toutes interdites dans le cadre de cet audit en lecture seule.
2. Les quelques appels de lecture disponibles côté compte Hostinger (abonnements, domaines) ont échoué avec une erreur **401 Unauthorized** : le connecteur Hostinger n'est pas authentifié pour cette session, ou n'a pas la portée nécessaire.
3. Aucun accès SSH n'est configuré dans cet environnement d'exécution (aucune variable d'environnement d'hôte/identifiants, aucune clé dans `~/.ssh`).

Conformément à `CLAUDE.md` (section 3 et section 11 : ne jamais inventer de données), **aucune caractéristique du VPS n'est indiquée comme un fait** dans ce document. Toutes les sections d'audit ci-dessous sont marquées `[À VALIDER PO]` faute de mesure réelle.

**Conclusion de ce LOT 0 : STOP — accès à adapter avant tout audit exploitable.** Voir section 17.

---

## 2. Méthode et périmètre

Actions réalisées, toutes en lecture seule, sans aucune modification du VPS :

- Inventaire exhaustif des outils exposés par le connecteur MCP Hostinger connecté à cette session (recherche par mots-clés : VPS, virtual machine, instance, metrics, list, get, execute, SSH, recovery…).
- Tentative d'appel de deux endpoints de lecture Hostinger non liés au VPS (`billing_getSubscriptionListV1`, `domains_getDomainListV1`) pour vérifier l'état d'authentification du connecteur.
- Vérification de la présence d'un accès SSH dans l'environnement d'exécution (variables d'environnement, répertoire `~/.ssh`).
- Lecture de `CLAUDE.md`, `docs/NSS_ERP_02_ARCHITECTURE_ODOO.md` (section 17 « Architecture VPS Hostinger », section 25 points ARCH-05/ARCH-07) et vérification (recherche mot-clé) de `docs/NSS_ERP_00_RECHERCHE_PAYS_2026.md` et `docs/NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md` pour tout élément déjà validé sur l'hébergement.

**Ce qui n'a PAS été fait**, conformément aux interdictions du mandat :

- Aucune commande d'installation, de mise à jour système, de modification de service, de configuration réseau, de base de données ou de fichier.
- Aucune tentative de connexion SSH avec des identifiants devinés, générés ou demandés à l'utilisateur.
- Aucun appel aux outils Hostinger d'écriture (`VPS_attachPublicKeyV1`, `VPS_createSnapshotV1`, `VPS_activateFirewallV1`, `VPS_createNewFirewallV1`, `VPS_createFirewallRuleV1`, `VPS_createPTRRecordV1`, `VPS_createPostInstallScriptV1`, `VPS_createPublicKeyV1`, `VPS_createNewProjectV1`).

**Ce qui est déjà validé PO** (source : `docs/NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md`, ERP-Q17) :

> Le PO dispose déjà d'un VPS Hostinger avec Odoo Community, avec la volonté d'un environnement de test avant production.

Cette information est une décision PO déjà actée — elle confirme l'existence du VPS et d'au moins une instance Odoo — mais ne fournit aucune mesure technique exploitable pour le dimensionnement.

---

## 3. Caractéristiques du VPS

`[À VALIDER PO]` — non disponible. Aucun accès en lecture n'a permis d'identifier le système d'exploitation, la version, ni l'identifiant de la machine virtuelle Hostinger (`virtualMachineId`), pourtant requis par tous les outils `VPS_*` disponibles.

---

## 4. CPU / RAM / disque

`[À VALIDER PO]` — non disponible :

- vCPU : inconnu
- RAM totale / utilisée / disponible : inconnu
- Swap : inconnu
- Disque total / utilisé / disponible : inconnu
- Filesystem : inconnu
- Uptime : inconnu
- Load average : inconnu

Aucune commande de mesure (`nproc`, `free -h`, `df -h`, `uptime`) n'a pu être exécutée, faute de canal d'accès (ni MCP, ni SSH) vers le VPS.

---

## 5. Services actifs

`[À VALIDER PO]` — non disponible. Statut et consommation d'Odoo, PostgreSQL, Nginx, Apache, Docker, Redis, Certbot ou tout autre service ne peuvent pas être vérifiés sans accès en lecture au VPS.

---

## 6. Instances Odoo existantes

`[À VALIDER PO]` — non disponible. La seule information certaine (source `NSS_ERP_01`, ERP-Q17) est qu'**au moins une instance Odoo Community existe déjà** sur ce VPS. Version, service systemd, port, utilisateur système, chemins, fichier de configuration, nombre de workers, consommation et statut restent à relever lors d'un audit réel.

**Rappel de sécurité déjà respecté :** même en cas d'accès, ce document ne devra jamais afficher `admin_passwd`, mot de passe PostgreSQL, token ou secret.

---

## 7. PostgreSQL

`[À VALIDER PO]` — non disponible. Version, statut, port, nombre de bases, bases liées à Odoo, rôles PostgreSQL et espace disque utilisé restent à vérifier.

---

## 8. Nginx / HTTPS

`[À VALIDER PO]` — non disponible. Version, server blocks, domaines/sous-domaines liés à Odoo, ports proxyfiés, présence HTTPS et certificats existants restent à vérifier.

---

## 9. Ports et réseau

`[À VALIDER PO]` — non disponible. Impossible de lister les ports en écoute (22, 80, 443, 5432, ports Odoo existants, autres) ni de proposer un port réellement libre pour NSS TEST sans données réelles. La proposition de port en section 14 est donc une hypothèse à confirmer, pas une vérification.

---

## 10. Sauvegardes

`[À VALIDER PO]` — non disponible. Sauvegardes Hostinger, snapshots, scripts de backup, fréquence, emplacement et présence d'une sauvegarde externe restent à vérifier.

---

## 11. Sécurité observée

`[À VALIDER PO]` — non disponible côté VPS (SSH, authentification par clé, accès root direct, firewall Hostinger, UFW, fail2ban, HTTPS, ports exposés, permissions).

**Constat côté accès Claude Code (celui-ci est vérifié) :**

- Le connecteur MCP Hostinger connecté à cette session ne fournit aucun outil de lecture/inventaire pour les VPS (uniquement des actions d'écriture).
- Les appels de lecture testés sur d'autres ressources Hostinger du même compte (abonnements, domaines) retournent `401 Unauthorized`.
- Aucune clé SSH ni information de connexion (hôte, utilisateur, identifiants) n'est présente dans cet environnement d'exécution.

---

## 12. Risques de coexistence

Non évaluables sans mesures réelles. Le risque principal identifié à ce stade est **méthodologique, pas technique** : sans marge CPU/RAM/disque mesurée, toute tentative d'installation d'une seconde instance Odoo serait une action non couverte par des données, ce que `CLAUDE.md` interdit explicitement (ne jamais transformer une hypothèse en donnée de production, ne jamais deviner).

---

## 13. Capacité NSS TEST

**Question :** « Peut-on installer NSS ERP TEST sur ce VPS sans mettre en danger les instances Odoo existantes ? »

**Réponse : NON — pas dans l'état actuel de l'audit.**

Justification : cette réponse ne repose **pas** sur une mesure démontrant un VPS insuffisant (aucune mesure n'a pu être obtenue), mais sur l'absence totale de mesure réelle de CPU, RAM, disque et charge des instances Odoo existantes. `docs/NSS_ERP_02_ARCHITECTURE_ODOO.md` (section 17) est explicite : « Ne pas retenir l'estimation… comme dimensionnement de référence » et exige un audit réel avant toute installation. En l'absence de cet audit, installer quoi que ce soit serait une action non couverte par des données, donc refusée par construction — indépendamment de ce que seraient les vraies mesures.

Cette réponse devra être réévaluée dès qu'un accès en lecture (MCP corrigé ou SSH en lecture seule autorisé) sera disponible.

---

## 14. Architecture proposée NSS TEST

Sans rien créer sur le VPS, et sous réserve d'adaptation une fois les vrais chemins/ports connus (l'exemple ci-dessous reprend celui déjà documenté dans `NSS_ERP_02` section 17, non vérifié contre le VPS réel) :

```text
Utilisateur système     : odoo-nss                         [HYPOTHÈSE — à adapter]
Chemin Odoo NSS          : /opt/odoo-nss/                   [HYPOTHÈSE — à adapter]
Service systemd          : odoo-nss-test.service            [HYPOTHÈSE — à adapter]
Port                      : 8070 (à confirmer libre)         [HYPOTHÈSE — à confirmer]
Rôle PostgreSQL           : odoo_nss                         [HYPOTHÈSE — à adapter]
Nom DB TEST               : nss_test                         [HYPOTHÈSE — à adapter]
Fichier config            : /etc/odoo/odoo-nss-test.conf     [HYPOTHÈSE — à adapter]
Filestore                 : /opt/odoo-nss/filestore/         [HYPOTHÈSE — à adapter]
Addons NSS                : /opt/odoo-nss/addons/nss_core, nss_project, nss_account (si besoin) [HYPOTHÈSE]
Sous-domaine               : nss-test.<domaine>.tld           [À VALIDER PO — domaine non défini, cf. ARCH-06 dans NSS_ERP_02]
Reverse proxy              : bloc Nginx dédié → localhost:8070 [HYPOTHÈSE — à adapter à la conf Nginx réelle]
HTTPS                      : Let's Encrypt / certbot          [HYPOTHÈSE — à vérifier si certbot déjà utilisé]
Stratégie de sauvegarde    : pg_dump + tar filestore quotidien, rétention 30 j, copie externe avant PROD (reprise NSS_ERP_02 section 19) [PROPOSITION]
```

Isolation prévue par rapport à l'instance existante : utilisateur système dédié, base de données et rôle PostgreSQL dédiés, répertoire filestore séparé, fichier de configuration séparé, service systemd séparé — conformément à `NSS_ERP_02` section 17. Ces éléments restent des propositions tant que l'architecture réelle du VPS n'est pas connue.

---

## 15. Pré-requis avant installation

1. Rétablir un accès en lecture au VPS : soit un connecteur/outil MCP Hostinger avec des endpoints de lecture VPS (liste des VM, détails, métriques) correctement authentifié, soit un accès SSH en lecture seule explicitement autorisé par le PO (clé fournie hors chat, jamais de mot de passe demandé dans la conversation).
2. Réaliser l'audit réel des sections 3 à 11 de ce document avec des mesures effectives.
3. Confirmer le sous-domaine à utiliser pour NSS TEST (point ARCH-06, déjà en attente dans `NSS_ERP_02`).
4. Confirmer qu'aucune modification n'est faite sur l'instance Odoo existante pendant tout le processus.
5. Revalider la section 13 (capacité NSS TEST) à partir des mesures réelles avant toute installation.

---

## 16. Points bloquants

| ID | Blocage | Impact | Action nécessaire |
|---|---|---|---|
| AUDIT-01 | Le connecteur MCP Hostinger connecté à cette session n'expose aucun outil de lecture/inventaire pour les VPS (seulement des outils d'écriture : clés, pare-feu, snapshot, PTR, post-install, projet Docker) | Impossible d'obtenir CPU/RAM/disque/services/instances via MCP | Le PO vérifie si un outil de lecture VPS existe côté Hostinger (hPanel / API) et, si oui, si le connecteur MCP peut être reconnecté avec ce périmètre |
| AUDIT-02 | Les appels de lecture Hostinger testés (abonnements, domaines) retournent 401 Unauthorized | Le connecteur semble non authentifié ou hors périmètre pour cette session | Le PO reconnecte/ré-autorise le connecteur Hostinger dans les paramètres Claude (capture d'écran fournie par le PO montre la page Connecteurs — le connecteur Hostinger y apparaît comme « Communauté », ce qui peut expliquer un périmètre de lecture limité) |
| AUDIT-03 | Aucun accès SSH configuré dans cet environnement (pas d'hôte, pas d'identifiants, pas de clé) | Impossible de basculer sur la méthode SSH prévue en secours | Si le PO souhaite un accès SSH en lecture seule, il l'ajoute via les paramètres de l'environnement (jamais collé dans le chat) et indique le nom de variable utilisé |
| AUDIT-04 | Sous-domaine NSS TEST non défini (ARCH-06, déjà ouvert dans NSS_ERP_02) | Bloque la configuration Nginx/HTTPS proposée en section 14 | Décision PO |

---

## 17. Recommandation LOT 1

**Ne pas démarrer le LOT 1.** Aucune mesure réelle du VPS n'a été obtenue ; recommander un LOT 1 sur cette base reviendrait à s'appuyer sur des hypothèses, ce que `CLAUDE.md` interdit.

Prochaine étape recommandée : résoudre AUDIT-01/02/03 (section 16), puis relancer un audit LOT 0 avec un accès en lecture fonctionnel avant toute décision GO/NO-GO réelle.

---

## Conclusion

**STOP — VPS À ADAPTER**

Précision : ce STOP ne signifie pas que le VPS est techniquement insuffisant — cela reste inconnu. Il signifie que **l'accès nécessaire pour auditer le VPS n'est pas encore fonctionnel** et doit être « adapté » (reconnexion/portée du connecteur Hostinger, ou accès SSH en lecture seule autorisé) avant qu'un audit exploitable, puis une décision LOT 1, ne soient possibles.

Le LOT 1 n'est pas lancé.
