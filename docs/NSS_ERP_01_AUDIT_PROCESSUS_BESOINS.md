# NSS ERP — Audit des processus et besoins métier

**Référence :** NSS_ERP_01
**Version :** 1.2 — décisions PO intégrées
**Date :** 23 septembre 2026
**Auteur :** Architecte fonctionnel (Claude Opus)
**Statut :** validé pour passage à NSS-ERP-02 — certaines décisions opérationnelles restent ouvertes

---

## 1. Executive Summary

Ce document constitue la source de vérité fonctionnelle du projet ERP pour le mouvement Nous Sommes la Solution (NSS). Il couvre l'ensemble des domaines métier identifiés, distingue systématiquement les faits documentés des hypothèses, et produit un modèle fonctionnel initial avec une priorisation MVP / Phase 2 / Phase 3.

NSS est un mouvement panafricain de femmes rurales présent dans **10 pays** [VALIDÉ PO], regroupant plus de 800 associations et plus de 200 000 membres et sympathisant·es [SOURCE RÉCENTE — chiffres agrégés à valider comme indicateurs officiels]. Le mouvement opère autour de la souveraineté alimentaire, l'agroécologie, les semences paysannes et le plaidoyer.

L'ERP cible est **Odoo Community**, complété par des modules OCA si nécessaire, et du développement spécifique uniquement en dernier recours. L'objectif est un système simple, multi-pays, multi-organisations, évolutif et adapté à une ONG.

**Décisions en attente :** 24 points regroupés en section 30, dont un sous-ensemble réellement bloquant pour l'architecture sont regroupés en section 30.

---

## 2. Contexte NSS

### 2.1 Nature du mouvement

Nous Sommes la Solution (NSS) est un mouvement panafricain de femmes rurales créé en 2011. [HISTORIQUE CONFIRMÉ]

Il est né comme expression des droits des femmes au sein d'une campagne pour la souveraineté alimentaire portée par les mouvements paysans du continent. [HISTORIQUE]

### 2.2 Mission et thématiques

Thématiques centrales documentées :

- Souveraineté alimentaire
- Agriculture familiale
- Agroécologie
- Semences paysannes et biodiversité
- Plaidoyer et gouvernance agricole
- Formation et autonomisation des femmes rurales
- Accès équitable aux ressources (terre, eau, semences)

### 2.3 Structuration documentée

Selon la brochure 2019 [HISTORIQUE] :

- NSS est passé d'une campagne (2011–2014) à un mouvement structuré.
- Première assemblée générale en 2017.
- Les instances décisionnelles sont constituées à 100 % de femmes rurales.
- Chaque pays membre est représenté par une personne au Conseil d'Administration.
- Le CA élit en son sein le bureau.
- L'ONG Fahamu Africa accompagne techniquement le mouvement depuis 2011, avec un appui se réduisant progressivement.

[PROCESSUS ACTUEL DE GOUVERNANCE NON DOCUMENTÉ EN DÉTAIL — À VALIDER PO]

### 2.4 Siège / coordination centrale

Adresse documentée : 9, Cité Sonatel 2, Dakar, Sénégal. [HISTORIQUE — partagée avec Fahamu Africa]

Présidente panafricaine citée dans les sources récentes : Mariama Sonko. [SOURCE RÉCENTE — À VALIDER PO]

---

## 3. Sources analysées

| Source | Type | Date | Fiabilité |
|---|---|---|---|
| Brochure « NSS FRANCAIS » | Document officiel NSS | 2019 | [HISTORIQUE] — personnes, contacts et chiffres potentiellement obsolètes |
| NSS_ERP_00_RECHERCHE_PAYS_2026.md | Recherche projet ERP | Sept. 2026 | [SOURCE RÉCENTE] — consolidation de sources publiques, validée PO pour les pays |
| Publications WAS Africa (Bénin, Togo) | Sites officiels NSS | Juin–Juil. 2026 | [SOURCE RÉCENTE] |
| Publication Casa24 (CIFAP) | Presse | Sept. 2026 | [SOURCE RÉCENTE] |
| Page AFSA | Partenaire externe | Récente | [ÉCART DOCUMENTAIRE] — cite 14 pays sans liste nominative |
| Publication CFSI / ALIMENTERRE | Partenaire | 2023 | [SOURCE RÉCENTE pour 2023] |

---

## 4. Fiabilité des données

### Règle générale

| Catégorie | Traitement |
|---|---|
| Liste des 10 pays | [VALIDÉ PO] — source de vérité |
| Organisations listées dans la brochure 2019 | [HISTORIQUE] — existence confirmée à l'époque, statut actuel à vérifier |
| Responsables / contacts brochure 2019 | [DONNÉE HISTORIQUE À VÉRIFIER] — ne pas importer automatiquement |
| Chiffres de membres (175 000 / 180 000 / 200 000) | [HISTORIQUE] — non fiables individuellement, jamais coder en dur |
| Nombre d'associations (500+ / 800+) | [HISTORIQUE] — idem |
| Partenaires listés en 2019 | [HISTORIQUE] — relations à confirmer |
| Données récentes Bénin/Togo/Côte d'Ivoire | [SOURCE RÉCENTE — À VALIDER PO] |

### Principe

Toute donnée non revalidée par le PO reste marquée et ne doit pas être traitée comme une donnée de production ERP.

---

## 5. Périmètre géographique

### 5.1 Les 10 pays validés

[VALIDÉ PO — décision du 23 septembre 2026]

| # | Pays | Code ISO | Type | Date d'entrée | Statut |
|---|---|---|---|---|---|
| 1 | Bénin | BJ | Extension | Juin 2026 | Actif récent |
| 2 | Burkina Faso | BF | Fondateur | 2011 | Actif |
| 3 | Côte d'Ivoire | CI | Extension | Date exacte à valider — présence documentée en 2023 | Actif |
| 4 | Gambie | GM | Extension | Date exacte à valider — présence documentée en 2019 | Actif |
| 5 | Ghana | GH | Fondateur | 2011 | Actif |
| 6 | Guinée | GN | Fondateur | 2011 | Actif |
| 7 | Guinée-Bissau | GW | Extension | Date exacte à valider — présence documentée en 2019 | Actif |
| 8 | Mali | ML | Fondateur | 2011 | Actif |
| 9 | Sénégal | SN | Fondateur | 2011 | Actif |
| 10 | Togo | TG | Extension | Juillet 2026 | Actif récent |

### 5.2 Historique de l'expansion

- **2011 :** 5 pays fondateurs (BF, GH, GN, ML, SN) avec 12 organisations fondatrices [HISTORIQUE CONFIRMÉ]
- **2019 :** 7 pays sont documentés dans la brochure (GM et GW y figurent ; leur date exacte d'entrée n'est pas établie) [HISTORIQUE CONFIRMÉ]
- **2023 :** 8 pays sont documentés, avec la Côte d'Ivoire ; la date exacte de son entrée reste à valider [SOURCE RÉCENTE]
- **Juin 2026 :** 9 pays (ajout BJ) [SOURCE RÉCENTE]
- **Juillet 2026 :** 10 pays (ajout TG) [SOURCE RÉCENTE]

### 5.3 Écarts documentaires

- Des sources de juin 2026 présentent le Bénin comme le « 12e pays ». [ÉCART DOCUMENTAIRE — pas de liste nominative cohérente à 12]
- AFSA mentionne 14 pays. [ÉCART DOCUMENTAIRE — pas de liste nominative]
- **Décision ERP :** périmètre fixé à 10 pays. Les écarts sont documentés mais n'impactent pas le modèle.

### 5.4 Conséquences ERP

- La liste de pays doit être **dynamique** (table paramétrable, jamais codée en dur).
- Le modèle doit supporter l'ajout d'un 11e, 12e pays sans modification structurelle.
- Chaque pays a potentiellement une structure interne différente.

---

## 6. Objectifs de l'ERP

### 6.1 Objectif général

Centraliser progressivement la gestion interne du mouvement NSS dans un système unique, fiable et accessible.

### 6.2 Objectifs fonctionnels

[PROPOSITION — basée sur l'analyse des sources et des besoins identifiés]

1. **Connaître le réseau** — Disposer d'un annuaire structuré et à jour des pays, coordinations, organisations et responsables.
2. **Gérer les adhésions** — Suivre les organisations membres, leur statut, leurs cotisations.
3. **Piloter les programmes et projets** — Suivre les activités, résultats et budgets.
4. **Gérer les finances** — Enregistrer recettes, dépenses, suivre les budgets, produire les justificatifs.
5. **Suivre les financements** — Gérer les conventions bailleurs, montants, périodes.
6. **Centraliser les documents** — Rattacher chaque document à son contexte métier.
7. **Sécuriser les accès** — Différencier les droits par rôle et par pays.
8. **Produire du reporting** — Indicateurs réseau, financiers et projets.

---

## 7. Périmètre fonctionnel global

| Domaine | MVP | Phase 2 | Phase 3 |
|---|---|---|---|
| Réseau NSS (pays, orga, contacts) | ✓ | | |
| Adhésions organisations | ✓ | | |
| Programmes / Projets / Activités | ✓ | | |
| Finance (recettes, dépenses, justificatifs) | ✓ | | |
| Budgets | ✓ | | |
| Partenaires / Bailleurs | ✓ | | |
| Financements / Conventions | | ✓ | |
| Gestion documentaire avancée | | ✓ | |
| Reporting avancé | | ✓ | |
| Membres individuels (si décidé) | | | ✓ |
| Portail partenaires | | | ✓ |
| Multi-devise avancé | | ✓ | |

---

## 8. Gestion du réseau NSS

### Objectif métier

Disposer en permanence d'une vue fiable et à jour de la structure du mouvement : quels pays, quelles coordinations, quelles organisations, quels responsables.

### AS-IS

La brochure 2019 permet d'identifier 13 organisations nommées réparties dans 7 pays, avec un responsable et des contacts pour chacune. [HISTORIQUE]

Aucun système centralisé n'est documenté. [PROCESSUS ACTUEL NON DOCUMENTÉ — À VALIDER PO]

Il est probable que le suivi se fait via des fichiers, carnets d'adresses ou contacts téléphoniques. [HYPOTHÈSE]

### TO-BE [PROPOSITION]

Un module « Réseau NSS » centralise :

- La liste des pays membres et leur statut
- La coordination nationale par pays
- Les organisations membres rattachées à chaque pays
- Les responsables et contacts de chaque organisation
- L'historique des changements (responsables, statuts)

### Données — Entité : Pays NSS

- Nom du pays
- Code ISO 3166
- Statut NSS (fondateur / extension / observation / archivé)
- Date d'entrée dans le mouvement
- Date de sortie éventuelle
- Coordination nationale (lien vers organisation ou personne)
- Organisation point focal
- Langues officielles
- Devise locale
- Zone UEMOA / CEDEAO [HYPOTHÈSE — pertinence à valider]
- Notes
- Actif / archivé

### Données — Entité : Organisation

- Nom complet
- Sigle / acronyme
- Pays de rattachement
- Type (association de femmes rurales / fédération / ONG / coordination / autre) [À VALIDER PO]
- Statut NSS (membre actif / suspendu / archivé)
- Date d'adhésion à NSS
- Organisation fondatrice (oui/non)
- Responsable actuel (lien vers contact)
- Historique des responsables
- Adresse
- Contacts (téléphone, email)
- Documents rattachés
- Notes

### Données — Entité : Contact / Responsable

- Nom, prénom
- Fonction dans l'organisation
- Fonction NSS éventuelle (coordinatrice nationale, présidente panafricaine, membre CA…)
- Organisation(s) rattachée(s)
- Téléphone(s) [DONNÉE SENSIBLE]
- Email(s) [DONNÉE SENSIBLE]
- Période de fonction (date début / date fin)
- Statut (actif / ancien)
- Notes

### Acteurs

| Action | Qui |
|---|---|
| Créer un pays | Admin ERP / Direction NSS |
| Ajouter une organisation | Coordination NSS / Coordination pays |
| Modifier les contacts | Coordination pays / Admin |
| Consulter l'annuaire | Tous les utilisateurs autorisés |
| Archiver une organisation | Direction NSS |

### Risques

- Données de 2019 potentiellement obsolètes pour 7 des 10 pays
- Risque de doublons si import non contrôlé
- Contacts personnels (téléphones, emails) = données sensibles
- Pas de processus documenté de mise à jour des contacts

---

## 9. Pays et coordinations nationales

### Objectif métier

Chaque pays membre dispose d'une coordination nationale. L'ERP doit permettre de savoir à tout moment qui coordonne NSS dans chaque pays.

### AS-IS

La brochure 2019 ne décrit pas explicitement une entité « coordination nationale » — elle liste des organisations et leurs responsables. [HISTORIQUE]

Les sources récentes (2026) mentionnent des « coordinatrices nationales » ou « représentantes nationales » pour les nouveaux pays. [SOURCE RÉCENTE]

La distinction entre coordination nationale et organisation point focal n'est pas formellement définie. [À VALIDER PO]

### TO-BE [PROPOSITION]

Chaque pays dispose d'un enregistrement « Coordination nationale » qui peut être :

- **Option A :** une des organisations membres qui joue le rôle de coordination [HYPOTHÈSE]
- **Option B :** une personne nommée coordinatrice, indépendamment de son organisation [HYPOTHÈSE]
- **Option C :** les deux (une personne coordinatrice + une organisation point focal)

La décision métier revient au PO (cf. section 30, ERP-Q02).

### Données récentes connues par pays

| Pays | Coordination / représentation | Source |
|---|---|---|
| Bénin | Clarisse ADONSI (représentante) | [SOURCE RÉCENTE — À VALIDER PO] |
| Burkina Faso | [À VALIDER PO] | |
| Côte d'Ivoire | Monique Konan (coordinatrice) | [SOURCE RÉCENTE — À VALIDER PO] |
| Gambie | [À VALIDER PO] | |
| Ghana | [À VALIDER PO] | |
| Guinée | [À VALIDER PO] | |
| Guinée-Bissau | [À VALIDER PO] | |
| Mali | [À VALIDER PO] | |
| Sénégal | Mariama Sonko (présidente panafricaine) | [SOURCE RÉCENTE — À VALIDER PO] |
| Togo | Aku Afefa Agbeka-Adiku (coordinatrice) | [SOURCE RÉCENTE — À VALIDER PO] |

---

## 10. Organisations / associations

### Objectif métier

Gérer l'annuaire des organisations membres de NSS, leur rattachement pays, leur statut et leurs responsables.

### AS-IS

La brochure 2019 liste 13 organisations membres historiques identifiables par nom : [HISTORIQUE]

| Pays | Organisation | Sigle |
|---|---|---|
| Burkina Faso | Fédération Nationale des Organisations Paysannes | FENOP |
| Burkina Faso | Réseau d'Appui à la Citoyenneté des Femmes Rurales Ouest-Africaines et du Tchad | RESACIFROAT |
| Gambie | Catalunya Gambia Foundation | CGF |
| Ghana | Rural Women Farmers Association of Ghana | RUWFAG |
| Ghana | Assono Organic Farming Project | ABOFAB |
| Guinée | Association Guinéenne pour l'Allègement des Charges Féminines | AGACFEM |
| Guinée | Association Guinéenne pour la Sécurité et la Souveraineté Alimentaires | AGUISSA |
| Guinée-Bissau | Fédération Paysanne de KAFO | KAFO |
| Mali | Association Malienne pour la Sécurité et la Souveraineté Alimentaire | AMASSA |
| Mali | Associations des Organisations Professionnelles Paysannes | AOPP |
| Mali | Coordination des associations et ONG féminines du Mali | CAFO |
| Sénégal | Association des Jeunes Agriculteurs de Casamance | AJAC |
| Sénégal | Union des Groupements Paysans de Mékhé | UGPM |

**Note :** le chiffre de « 12 organisations fondatrices » concerne le lancement de 2011 dans 5 pays. Il ne doit pas être confondu avec la liste de 13 organisations identifiables dans la brochure 2019, qui couvre alors 7 pays. La brochure ne permet pas, à elle seule, de reconstituer avec certitude les 12 organisations fondatrices de 2011. [HISTORIQUE — À NE PAS SPÉCULER]

Pour Bénin, Côte d'Ivoire et Togo, les organisations points focaux récentes sont :

- Bénin : FAEB (Fédération Agroécologique du Bénin) [SOURCE RÉCENTE — À VALIDER PO]
- Togo : Eco-Impact [SOURCE RÉCENTE — À VALIDER PO]
- Côte d'Ivoire : [À VALIDER PO]

Le mouvement compte aujourd'hui plus de 800 associations. [SOURCE RÉCENTE — chiffre global non vérifiable individuellement]

### TO-BE [PROPOSITION]

L'ERP gère un répertoire d'organisations avec :

- Fiche complète par organisation
- Rattachement à un pays
- Statut NSS (membre actif, fondateur, suspendu, archivé)
- Historique des responsables
- Documents d'adhésion rattachés
- Possibilité de distinguer « organisation fondatrice » vs « AFR adhérente » vs « organisation point focal »

### Validations

[PROPOSITION]

- Ajout d'organisation : saisie par coordination pays → validation par coordination NSS
- Changement de responsable : saisie → validation
- Archivage : validation direction NSS

### Risques

- Volume potentiel : 800+ organisations. L'import doit être contrôlé et progressif.
- Les 14 organisations historiques sont un point de départ mais doivent être revalidées.
- Le terme « AFR » (Association de Femmes Rurales) est utilisé dans les sources mais sa définition formelle dans le contexte ERP reste à clarifier. [À VALIDER PO]

---

## 11. Membres et adhésions

### Objectif métier

Suivre quelles organisations sont membres de NSS, leur statut d'adhésion et éventuellement leurs cotisations.

### AS-IS

La brochure 2019 indique : « Pour adhérer au mouvement, il faut remplir et signer une demande d'adhésion, payer pour son adhésion et sa cotisation. » [HISTORIQUE]

Les « membres » de NSS au sens large incluent potentiellement :

- Les organisations (associations, fédérations)
- Les membres individuels de ces organisations (femmes rurales)
- Les sympathisant·es

Les chiffres varient : 175 000 (2019) → 180 000 (2023) → 200 000 (2026). [HISTORIQUE — CONFLIT DE SOURCES]

### TO-BE — Trois options

**Option A — Organisations uniquement** [PROPOSITION RECOMMANDÉE POUR LE MVP]

L'ERP gère uniquement les organisations comme entités membres. Chaque organisation a un statut d'adhésion, une date, un historique de cotisation. Le nombre de membres individuels est un champ déclaratif sur la fiche organisation.

**Option B — Organisations + statistiques**

Comme option A, mais chaque organisation déclare périodiquement un nombre de membres. L'ERP consolide les chiffres globaux sans gérer les individus.

**Option C — Membres individuels**

L'ERP gère chaque personne membre. Impact très élevé : potentiellement 200 000+ enregistrements, nécessité d'identification, de collecte de données personnelles dans des zones rurales multi-pays.

**Recommandation :** Option A pour le MVP, Option B en Phase 2. Option C uniquement si un besoin métier explicite le justifie. [PROPOSITION]

### Données — Entité : Adhésion

- Organisation
- Date de demande d'adhésion
- Date d'adhésion effective
- Statut (en cours / active / expirée / suspendue / archivée)
- Cotisation due
- Cotisation payée
- Date de dernier renouvellement
- Documents d'adhésion rattachés
- Nombre de membres déclaré (champ déclaratif)
- Notes

### Processus d'adhésion documenté partiellement [HISTORIQUE]

1. L'organisation remplit et signe une demande d'adhésion
2. Paiement de l'adhésion et de la cotisation
3. Engagement sur la vision et les objectifs NSS

[PROCESSUS DÉTAILLÉ NON DOCUMENTÉ — À VALIDER PO : qui valide l'adhésion ? quelle instance ? quel montant de cotisation ? quelle périodicité ?]

---

## 12. Programmes

### Objectif métier

NSS conduit des programmes thématiques regroupant plusieurs projets. L'ERP doit permettre de les suivre.

### AS-IS

Les sources documentent des thématiques (souveraineté alimentaire, agroécologie, semences, plaidoyer, formation) mais ne décrivent pas formellement une structure « programme ». [PROCESSUS ACTUEL NON DOCUMENTÉ — À VALIDER PO]

Le camp CIFAP de Niaguis (sept. 2026) est un exemple d'activité multi-pays documentée. [SOURCE RÉCENTE]

### TO-BE [PROPOSITION]

Entité : Programme

- Nom
- Code
- Description / objectifs
- Thématique(s)
- Date de début / fin
- Statut (planifié / en cours / clôturé / archivé)
- Responsable
- Pays concernés
- Bailleurs / financements associés
- Budget global
- Projets rattachés
- Documents

### Acteurs

| Action | Qui |
|---|---|
| Créer un programme | Direction NSS / Responsable programmes |
| Modifier | Responsable programme |
| Clôturer | Direction NSS |
| Consulter | Utilisateurs autorisés |

---

## 13. Projets

### Objectif métier

Un projet est une unité opérationnelle au sein d'un programme, avec un budget, un calendrier et des résultats attendus.

### AS-IS

[PROCESSUS ACTUEL NON DOCUMENTÉ — À VALIDER PO]

### TO-BE [PROPOSITION]

Entité : Projet

- Nom
- Code
- Programme parent
- Description / objectifs
- Pays concerné(s)
- Organisation(s) participante(s)
- Responsable projet
- Date début / fin prévue / fin réelle
- Statut (planifié / en cours / suspendu / clôturé / archivé)
- Budget alloué
- Bailleur(s)
- Activités rattachées
- Livrables attendus
- Documents

---

## 14. Activités

### Objectif métier

Une activité est une action concrète au sein d'un projet : formation, atelier, rencontre, session IEC, camp, etc.

### AS-IS

La brochure 2019 mentionne des types d'activités : séances IEC, sessions de partage de techniques, interventions en réunions. [HISTORIQUE]

Le CIFAP de Niaguis (sept. 2026) est un exemple concret d'activité multi-pays. [SOURCE RÉCENTE]

### TO-BE [PROPOSITION]

Entité : Activité

- Nom
- Projet parent
- Type (formation / atelier / rencontre / plaidoyer / camp / IEC / autre) [À VALIDER PO]
- Lieu
- Pays
- Date début / fin
- Responsable
- Participants / organisations participantes
- Budget activité
- Dépenses réalisées
- Résultats / compte-rendu
- Documents / justificatifs
- Statut

---

## 15. Finance

### Objectif métier

Gérer les flux financiers de NSS : recettes (financements, cotisations) et dépenses (activités, fonctionnement), avec pièces justificatives.

### AS-IS

[PROCESSUS FINANCIER ACTUEL NON DOCUMENTÉ — À VALIDER PO]

### Point critique — comptabilité vs gestion financière

Le besoin initial du projet mentionne explicitement la **comptabilité**. Il faut donc distinguer deux niveaux avant l'architecture Odoo :

- **Gestion financière / trésorerie / budget** : recettes, dépenses, justificatifs, budgets, suivi par projet.
- **Comptabilité complète** : journaux, plan comptable, écritures, banques, rapprochements, clôtures et états financiers selon les obligations applicables.

[À VALIDER PO — CRITIQUE] : NSS souhaite-t-il que l'ERP tienne la comptabilité officielle/statutaire, ou seulement le suivi financier et budgétaire interne ? Cette décision conditionne fortement NSS-ERP-02.

### TO-BE [PROPOSITION]

#### Recettes

- Type (financement bailleur / cotisation / don / autre)
- Source (bailleur, organisation, autre)
- Montant
- Devise
- Date
- Convention / financement rattaché
- Projet / programme rattaché
- Justificatif
- Statut (attendue / reçue / annulée)

#### Dépenses

- Libellé
- Catégorie [À VALIDER PO — plan de catégories budgétaires NSS]
- Montant
- Devise
- Date
- Bénéficiaire / fournisseur
- Projet / activité rattaché(e)
- Ligne budgétaire
- Justificatif(s) obligatoire(s)
- Statut (brouillon / soumise / validée / payée / rejetée)

#### Workflow de dépense [PROPOSITION]

1. Saisie par le porteur de l'activité / projet
2. Rattachement du justificatif
3. Contrôle par le responsable financier
4. Validation par le niveau d'autorisation requis
5. Paiement
6. Archivage

[WORKFLOW À VALIDER PO — les niveaux d'autorisation et seuils ne sont pas documentés]

### Points multi-pays

| Aspect | Conséquence ERP |
|---|---|
| Devises | Plusieurs devises possibles (XOF, GHS, GMD, GNF, USD, EUR…) |
| Comptabilité | Une ou plusieurs sociétés Odoo ? [À VALIDER PO] |
| Fiscalité | Régimes fiscaux différents selon les pays |
| Plan comptable | Potentiellement différent par zone (OHADA / anglophone / lusophone) |

**Recommandation MVP :** commencer avec une seule société Odoo (coordination centrale, Sénégal) et une comptabilité principale. Évaluer le multi-société en Phase 2. [PROPOSITION]

---

## 16. Budgets

### Objectif métier

Suivre les prévisions budgétaires et leur exécution à plusieurs niveaux.

### AS-IS

[PROCESSUS BUDGÉTAIRE ACTUEL NON DOCUMENTÉ — À VALIDER PO]

### TO-BE [PROPOSITION]

Niveaux budgétaires :

| Niveau | Description |
|---|---|
| Budget annuel NSS | Enveloppe globale annuelle |
| Budget programme | Enveloppe par programme |
| Budget projet | Enveloppe par projet |
| Budget activité | Enveloppe par activité |

Chaque niveau doit permettre le suivi :

- **Prévu** : montant budgété
- **Engagé** : dépenses approuvées non encore payées
- **Dépensé** : montants effectivement décaissés
- **Disponible** : prévu − engagé − dépensé

Et la comparaison **budget vs réalisé**.

Les budgets par bailleur peuvent coexister avec les budgets par projet (un projet peut avoir plusieurs bailleurs). [PROPOSITION]

Budget par pays : [À VALIDER PO — pertinence à confirmer]

---

## 17. Partenaires et bailleurs

### Objectif métier

Maintenir un annuaire des partenaires techniques et financiers de NSS.

### AS-IS

La brochure 2019 liste 5 partenaires : [HISTORIQUE]

| Partenaire | Localisation |
|---|---|
| Grassroots International | Jamaica Plain, MA, USA |
| AgroEcology Fund | Washington DC, USA |
| The MATCH International Women's Fund | Ottawa, Canada |
| Thousand Currents | Oakland, CA, USA |
| Fahamu Africa | Dakar, Sénégal |

Fahamu Africa a un rôle particulier : appui technique depuis 2011 et hébergement du siège NSS. [HISTORIQUE]

### TO-BE [PROPOSITION]

Entité : Partenaire

- Nom
- Type (bailleur / partenaire technique / institutionnel / autre)
- Pays / adresse
- Contact(s) principal(aux)
- Relation avec NSS (description)
- Date de début de la relation
- Statut (actif / ancien)
- Conventions rattachées
- Financements rattachés
- Documents

### Acteurs

| Action | Qui |
|---|---|
| Créer un partenaire | Direction NSS / Finance |
| Modifier | Direction NSS |
| Consulter | Responsables programmes, finance |

---

## 18. Financements

### Objectif métier

Suivre les conventions de financement : montants, devises, périodes, projets financés, décaissements.

### AS-IS

[PROCESSUS DE GESTION DES FINANCEMENTS NON DOCUMENTÉ — À VALIDER PO]

### TO-BE [PROPOSITION]

Entité : Financement / Convention

- Référence
- Bailleur (lien vers partenaire)
- Intitulé
- Montant total
- Devise
- Date de signature
- Date début / fin
- Programme(s) / projet(s) financé(s)
- Tranches de décaissement prévues
- Tranches reçues
- Conditions / livrables requis
- Documents (convention signée, avenants, rapports exigés)
- Statut (en négociation / signé / en cours / clôturé / archivé)
- Responsable suivi

---

## 19. Gestion documentaire

### Objectif métier

Chaque document doit pouvoir être rattaché à son contexte métier (organisation, projet, financement, dépense…).

### AS-IS

[PROCESSUS DOCUMENTAIRE ACTUEL NON DOCUMENTÉ — À VALIDER PO]

### TO-BE [PROPOSITION]

Types de documents envisagés :

- Conventions et contrats
- Rapports (narratifs, financiers)
- Factures et reçus
- Justificatifs de dépense
- PV (assemblées, réunions CA)
- Documents d'adhésion
- Documents administratifs (statuts, récépissés)
- Photos / médias d'activités
- Correspondances importantes

Chaque document doit être rattaché à au moins une entité métier : organisation, projet, financement, dépense, activité, pays.

Odoo gère nativement les pièces jointes sur chaque enregistrement. Pour le MVP, cette fonctionnalité native suffit. Un système de GED avancé (indexation, recherche full-text, workflows documentaires) relève de la Phase 2 ou 3. [PROPOSITION]

---

## 20. Utilisateurs et gouvernance

### Objectif métier

Définir qui accède à quoi dans l'ERP.

### AS-IS

La brochure 2019 décrit une gouvernance : CA (un représentant par pays), bureau élu par le CA, instances constituées à 100 % de femmes rurales, appui technique Fahamu Africa. [HISTORIQUE]

[ORGANIGRAMME OPÉRATIONNEL ACTUEL NON DOCUMENTÉ — À VALIDER PO]

### TO-BE — Rôles proposés [PROPOSITION]

| Rôle | Périmètre | Droits |
|---|---|---|
| Admin ERP | Système | Tout |
| Direction NSS | Global | Lecture/écriture global, validations stratégiques |
| Responsable finance | Global | Finance, budgets, dépenses, conventions |
| Responsable programmes | Programmes/projets | Création projets, suivi activités, budgets projets |
| Coordination pays | Son pays | Organisations, contacts, activités locales, dépenses locales |
| Utilisateur pays | Son pays | Saisie, consultation limitée |
| Audit / consultation | Global | Lecture seule |

**Principe clé :** les utilisateurs pays ne doivent voir que les données de leur pays, sauf autorisation explicite. [PROPOSITION]

**Nombre d'utilisateurs estimé :** [À VALIDER PO] — probablement 15–30 utilisateurs actifs pour le MVP (coordination centrale + 1–2 par pays).

---

## 21. Reporting

### Objectif métier

Produire les indicateurs nécessaires au pilotage et au reporting bailleurs.

### Indicateurs proposés [PROPOSITION]

**Réseau**

- Nombre de pays actifs
- Nombre d'organisations par pays
- Nombre total d'organisations actives
- Nombre de membres déclarés (si Option B adoptée)
- Organisations sans responsable renseigné
- Adhésions expirées ou en attente

**Projets**

- Projets actifs par programme
- Projets actifs par pays
- Activités réalisées / planifiées
- Taux de réalisation par projet

**Finance**

- Budget prévu vs engagé vs dépensé (par programme, projet, bailleur)
- Taux d'exécution budgétaire
- Dépenses en attente de validation
- Recettes attendues vs reçues

**Documents**

- Conventions expirant dans les 3 prochains mois
- Dépenses sans justificatif

---

## 22. Processus transverses

### 22.1 Langues

NSS couvre des pays francophones (BJ, BF, CI, GN, ML, SN, TG), anglophones (GH, GM) et lusophones (GW).

Conséquences ERP :

- L'interface Odoo doit être disponible au minimum en français et anglais.
- Les données (noms d'organisations, descriptions de projets) sont saisies dans la langue du pays.
- Les rapports aux bailleurs internationaux peuvent être en anglais ou français.

[À VALIDER PO : quelle est la langue de travail principale de l'ERP ?]

Odoo Community supporte nativement le multi-langue sur l'interface. Pas de développement spécifique nécessaire pour cet aspect. [PROPOSITION]

### 22.2 Multi-devise

Devises potentiellement concernées :

| Devise | Pays |
|---|---|
| XOF (Franc CFA UEMOA) | BJ, BF, CI, ML, SN, TG, GW |
| GHS (Cedi) | GH |
| GMD (Dalasi) | GM |
| GNF (Franc guinéen) | GN |
| EUR / USD | Bailleurs internationaux |

Odoo Community supporte nativement le multi-devise. [PROPOSITION : activer dès le MVP]

### 22.3 Calendrier et exercice fiscal

[À VALIDER PO : exercice fiscal NSS = année civile ?]

---

## 23. Historisation

### Principe

L'ERP ne doit jamais écraser silencieusement une donnée importante. Les changements significatifs doivent être traçables.

### Éléments à historiser [PROPOSITION]

| Élément | Mécanisme |
|---|---|
| Responsable d'un pays / coordination | Enregistrement avec dates début/fin |
| Responsable d'une organisation | Enregistrement avec dates début/fin |
| Statut d'une organisation | Log de changement ou champ avec date |
| Statut d'adhésion | Historique (renouvellements, suspensions) |
| Coordonnées (tél, email) | Ancien / nouveau avec date de changement |
| Statut d'un pays | Date d'entrée, éventuellement date de sortie |
| Documents | Versionnage si modification |

Odoo dispose d'un mécanisme natif de suivi des modifications (chatter / log). Pour les changements de responsable, un modèle relationnel avec dates est préférable au simple écrasement. [PROPOSITION]

---

## 24. Données à migrer

### Principe

Aucune donnée historique ne doit être importée automatiquement sans validation.

### Source principale : brochure 2019

| Type de donnée | Volume | Statut | Recommandation |
|---|---|---|---|
| Organisations (13 identifiables) | Faible | [HISTORIQUE] | Importer uniquement après validation du périmètre de migration, avec statut « à vérifier » |
| Responsables / contacts | 13 personnes identifiables | [DONNÉE HISTORIQUE À VÉRIFIER] | Ne pas importer les coordonnées sans validation PO |
| Partenaires (5) | Faible | [HISTORIQUE] | Importer, marquer « à vérifier » |
| Pays (7 historiques + 3 récents) | 10 | [VALIDÉ PO] | Créer les 10 pays directement |

### Source : recherche pays 2026

| Type de donnée | Volume | Statut | Recommandation |
|---|---|---|---|
| Coordinations récentes (BJ, TG, CI, SN) | 4 | [SOURCE RÉCENTE — À VALIDER PO] | Importer après validation PO |
| Organisations point focal récentes (FAEB, Eco-Impact) | 2 | [SOURCE RÉCENTE — À VALIDER PO] | Importer après validation PO |

### Processus d'import recommandé [PROPOSITION]

1. Créer les 10 pays avec leurs métadonnées validées
2. Créer les organisations historiques avec le statut « à vérifier »
3. Demander au PO la validation par pays (coordinatrice, organisations actives, contacts)
4. Mettre à jour les fiches après validation
5. Ne pas importer les téléphones et emails historiques sans accord explicite

---

## 25. Modèle métier initial

```
NSS (mouvement)
│
├── PAYS (10 — dynamique)
│   ├── Statut (fondateur / extension / archivé)
│   ├── Coordination nationale
│   │   └── Coordinatrice / responsable (avec historique)
│   │
│   └── ORGANISATIONS / ASSOCIATIONS (800+)
│       ├── Type (AFR / fédération / ONG / coordination / point focal)
│       ├── Statut NSS (actif / suspendu / archivé)
│       ├── Adhésion (date, cotisation, renouvellement)
│       ├── Responsable(s) (avec historique)
│       ├── Contacts [données sensibles]
│       ├── Nombre de membres déclaré
│       └── Documents
│
├── PROGRAMMES
│   ├── Thématique(s)
│   ├── Bailleur(s)
│   ├── Budget
│   │
│   └── PROJETS
│       ├── Pays concerné(s)
│       ├── Organisation(s) participante(s)
│       ├── Budget projet
│       │
│       └── ACTIVITÉS
│           ├── Type (formation / IEC / camp / plaidoyer…)
│           ├── Lieu, dates
│           ├── Participants
│           ├── Budget activité
│           └── Documents / justificatifs
│
├── PARTENAIRES / BAILLEURS
│   ├── Type (bailleur / technique / institutionnel)
│   └── FINANCEMENTS / CONVENTIONS
│       ├── Montant, devise, période
│       ├── Programme(s) financé(s)
│       ├── Tranches
│       └── Documents (convention, rapports)
│
├── FINANCE
│   ├── RECETTES (financements, cotisations, dons)
│   ├── DÉPENSES
│   │   ├── Catégorie
│   │   ├── Projet / activité
│   │   ├── Justificatif(s)
│   │   └── Workflow validation
│   └── BUDGETS
│       ├── Par programme / projet / activité
│       └── Prévu / Engagé / Dépensé / Disponible
│
└── GOUVERNANCE
    ├── Conseil d'Administration (1 représentant·e / pays)
    ├── Bureau (élu par le CA)
    └── Rôles ERP (admin, direction, finance, coordination pays…)
```

---

## 26. MVP

### Périmètre strict du MVP [PROPOSITION]

Le MVP doit permettre à NSS de commencer à utiliser l'ERP pour ses besoins quotidiens les plus fondamentaux.

**Inclus dans le MVP :**

1. **Annuaire réseau** — Pays, organisations, responsables, contacts. Consultation et mise à jour.
2. **Adhésions** — Statut d'adhésion des organisations, date, cotisation (suivi simple).
3. **Projets** — Création et suivi de projets avec dates, pays, responsable, statut.
4. **Activités** — Création et suivi d'activités rattachées aux projets.
5. **Partenaires** — Annuaire des bailleurs et partenaires.
6. **Finance opérationnelle** — Recettes/dépenses, justificatifs, validation simple, rattachement projet.
7. **Budgets** — Budget par projet, suivi prévu vs dépensé.
8. **Comptabilité** — périmètre exact conditionné par la décision PO sur comptabilité officielle vs suivi financier interne.
9. **Documents** — Pièces jointes sur chaque entité (fonctionnalité native Odoo).
10. **Utilisateurs** — 3 à 4 rôles : admin, direction/finance, coordination pays, consultation.
11. **Reporting de base** — Organisations par pays, budget vs dépensé par projet.

**Exclu du MVP :**

- Gestion des membres individuels
- Programmes (les projets suffisent au départ)
- Conventions de financement détaillées
- Multi-société Odoo
- Portail externe
- Reporting avancé / tableaux de bord
- Automatisations
- Workflows complexes multi-niveaux

**Estimation utilisateurs MVP :** 10–20 personnes. [HYPOTHÈSE]

**Langues MVP :** français + anglais. [PROPOSITION]

---

## 27. Phase 2

**Après stabilisation du MVP** [PROPOSITION]

1. **Programmes** — Entité programme regroupant les projets
2. **Financements / conventions** — Suivi détaillé des conventions bailleurs avec tranches
3. **Budgets avancés** — Budget programme, budget bailleur, comparaisons multi-niveaux
4. **Membres Option B** — Nombre de membres déclaré par organisation, consolidation
5. **Multi-devise** — Si non activé dans le MVP
6. **Reporting avancé** — Tableaux de bord, indicateurs bailleur
7. **Workflow de validation** — Dépenses avec seuils et niveaux d'approbation
8. **GED améliorée** — Catégorisation des documents, recherche, alertes d'expiration

---

## 28. Phase 3

**Extensions avancées** [PROPOSITION]

1. **Membres individuels** (Option C) — Uniquement si le besoin est confirmé
2. **Portail partenaires / bailleurs** — Consultation en ligne par les bailleurs
3. **Multi-société Odoo** — Si des pays ont besoin d'une comptabilité séparée
4. **Reporting consolidé multi-pays**
5. **Application mobile simplifiée** — Pour les coordinatrices pays (saisie terrain)
6. **Intégration communication** — Envoi de notifications, relances cotisations

---

## 29. Risques et points d'attention

| # | Risque | Impact | Mitigation |
|---|---|---|---|
| R01 | Données historiques importées sans validation | Erreurs en production | Import contrôlé, statut « à vérifier » |
| R02 | Contacts personnels (tél/email) exposés | Vie privée, sécurité | Droits d'accès par rôle, données sensibles |
| R03 | Écarts documentaires pays (12/14 vs 10) | Confusion utilisateurs | Périmètre fixé par PO, écarts documentés |
| R04 | Structure hétérogène entre pays | Modèle trop rigide ou trop lâche | Modèle flexible, champs optionnels |
| R05 | Volume d'organisations (800+) mal maîtrisé | Performance, qualité de données | Import progressif pays par pays |
| R06 | Processus internes non documentés | Workflows ERP inadaptés | Valider chaque workflow avec le PO avant implémentation |
| R07 | Multi-pays / multi-devise / multi-langue | Complexité technique | MVP mono-société, multi-devise natif Odoo |
| R08 | Faible connectivité dans certaines zones | Adoption difficile | Interface légère, saisie offline à évaluer en Phase 3 |
| R09 | Turnover des responsables | Perte de continuité | Historisation systématique |
| R10 | Dépendance Fahamu Africa | Risque si séparation | Documenter les processus, rendre NSS autonome sur l'ERP |

---

## 30. Points à valider par le PO

| ID | Domaine | Ce que nous savons | Décision nécessaire | Impact ERP | Priorité |
|---|---|---|---|---|---|
| ERP-Q01 | Membres | NSS compte 800+ associations et un très grand nombre de membres/sympathisant·es | **VALIDÉ PO : Option B — organisations + statistiques déclaratives, sans membres individuels dans le MVP** | Modèle de données validé pour MVP | VALIDÉ |
| ERP-Q02 | Coordination pays | Plusieurs formes existent selon les pays | **VALIDÉ PO : personne coordinatrice + organisation point focal éventuelle, indépendantes l'une de l'autre** | Modèle réseau validé | VALIDÉ |
| ERP-Q03 | Organisations | La brochure 2019 liste 14 organisations. Le réseau en compte 800+ | Confirmer la différence métier entre organisation fondatrice, AFR adhérente, fédération, point focal | Typologie, classification | CRITIQUE |
| ERP-Q04 | Adhésion | La brochure mentionne demande + adhésion + cotisation | Confirmer : qui valide l'adhésion ? Quel montant de cotisation ? Quelle périodicité ? | Workflow adhésion | HAUTE |
| ERP-Q05 | Finance | Deux architectures restent possibles | **OUVERT : étudier centralisation et multi-entités dans NSS-ERP-02, avec trajectoire progressive** | Architecture Odoo à comparer | CRITIQUE |
| ERP-Q06 | Finance | Pas de plan de catégories budgétaires documenté | Fournir la grille de catégories de dépenses utilisée par NSS | Structure budgets et dépenses | HAUTE |
| ERP-Q07 | Finance | Pas de workflow de validation documenté | Définir les niveaux d'autorisation pour les dépenses (seuils, approbateurs) | Workflow dépenses | HAUTE |
| ERP-Q08 | Budgets | Plusieurs niveaux possibles | Confirmer les niveaux budgétaires pertinents (annuel, programme, projet, activité, bailleur, pays) | Structure budgets | HAUTE |
| ERP-Q09 | Partenaires | 5 partenaires listés en 2019 | Confirmer la liste actuelle des partenaires et bailleurs actifs | Annuaire partenaires | MOYENNE |
| ERP-Q10 | Coordinations | Données récentes pour 4 pays seulement | Fournir la coordinatrice / représentante actuelle pour chacun des 10 pays | Données de référence | CRITIQUE |
| ERP-Q11 | Organisations | 14 organisations historiques identifiées | Confirmer lesquelles sont toujours actives et leur responsable actuel | Données de référence | CRITIQUE |
| ERP-Q12 | Langue | Pays FR, EN, PT | Quelle est la langue de travail principale de l'ERP ? | Configuration i18n | MOYENNE |
| ERP-Q13 | Exercice fiscal | Non documenté | L'exercice fiscal NSS correspond à l'année civile ? | Configuration comptable | MOYENNE |
| ERP-Q14 | Gouvernance | CA + bureau documentés en 2019 | Fournir l'organigramme opérationnel actuel de NSS | Rôles ERP | HAUTE |
| ERP-Q15 | Utilisateurs | Démarrage progressif | **VALIDÉ PO : environ 10–20 utilisateurs max pour le pilote/MVP, comptes de test d'abord** | Dimensionnement initial validé | VALIDÉ |
| ERP-Q16 | Activités | Types mentionnés (IEC, camps, formations) | Confirmer la typologie des activités pour l'ERP | Classification | MOYENNE |
| ERP-Q17 | Hébergement | Le PO dispose déjà d'un VPS Hostinger avec Odoo Community | **VALIDÉ PO : VPS Hostinger, avec environnement de test avant production** | Infrastructure de départ validée | VALIDÉ |
| ERP-Q18 | Import | Données 2019 disponibles | Souhaite-t-on importer les données historiques de la brochure 2019 comme point de départ ? | Migration | MOYENNE |
| ERP-Q19 | Fahamu Africa | Appui technique en réduction | Quel rôle Fahamu Africa jouera dans l'ERP ? Utilisateur ? Administrateur ? Aucun ? | Gouvernance système | HAUTE |
| ERP-Q20 | Chiffres globaux | Chiffres variables selon les sources (175k / 180k / 200k) | Les chiffres officiels actuels de NSS (associations, membres) pour les indicateurs de départ | Données de référence | MOYENNE |
| ERP-Q21 | Projets | Aucun projet/programme actuel n'est décrit dans les sources | Fournir 2–3 exemples de projets/programmes actuels pour valider le modèle | Validation du modèle | HAUTE |
| ERP-Q22 | Financement | Aucune convention n'est décrite dans les sources | Fournir 1–2 exemples de conventions/financements actuels pour valider le modèle | Validation du modèle | HAUTE |
| ERP-Q23 | Cotisation | Mentionnée mais non détaillée | Existe-t-il une cotisation différenciée selon les pays / types d'organisations ? | Modèle adhésion | MOYENNE |
| ERP-Q24 | Comptabilité | Le besoin initial inclut la comptabilité | **VALIDÉ PO : prévoir une comptabilité complète/officielle** | Architecture comptable requise dans NSS-ERP-02 | VALIDÉ |

---

## 31. Recommandations pour NSS-ERP-02

Le prochain livrable devra être l'**architecture technique fonctionnelle** du MVP :

### NSS_ERP_02 — Architecture technique

Contenu recommandé :

1. **Mapping Odoo** — Quels modules Odoo Community couvrent quels besoins identifiés dans cet audit
2. **Modules OCA recommandés** — Identification des modules OCA pertinents (contacts, projets, comptabilité analytique, etc.)
3. **Développements spécifiques** — Liste minimale des développements nécessaires (module réseau NSS, adhésions…)
4. **Modèle de données Odoo** — Traduction des entités métier en modèles Odoo
5. **Architecture multi-pays** — Mono ou multi-société, gestion des devises
6. **Rôles et droits Odoo** — Mapping des rôles métier vers les groupes Odoo
7. **Infrastructure** — Recommandation hébergement
8. **Plan d'implémentation MVP** — Phases, estimation d'effort

### Prérequis

NSS_ERP_02 peut maintenant être produit.

Décisions déjà validées :
- **ERP-Q01** — organisations + statistiques déclaratives, pas de membres individuels au MVP ;
- **ERP-Q02** — coordinatrice/représentante + organisation point focal éventuelle ;
- **ERP-Q15** — pilote d'environ 10–20 utilisateurs maximum ;
- **ERP-Q17** — VPS Hostinger avec Odoo Community ;
- **ERP-Q24** — comptabilité complète/officielle à prévoir.

Décision restant volontairement ouverte :
- **ERP-Q05** — centralisation comptable ou multi-entités. NSS-ERP-02 doit comparer les deux options et proposer une trajectoire progressive sans bloquer le pilote.

Les données de référence **ERP-Q10 / ERP-Q11** (coordinations et organisations actuelles) restent nécessaires pour la migration, mais ne bloquent pas la conception de l'architecture.

Les autres points peuvent être validés en parallèle.

---

## 32. Décisions Product Owner — 23 septembre 2026

Les décisions suivantes sont validées pour préparer l'architecture NSS-ERP-02.

### ERP-Q01 — Niveau de gestion des membres

**[VALIDÉ PO] Option B : organisations + statistiques de membres.**

Pour le MVP :
- les organisations / associations sont les entités membres principales ;
- l'ERP ne gère pas individuellement les centaines de milliers de membres ;
- chaque organisation peut déclarer un nombre de membres ;
- ces chiffres pourront être consolidés par pays et au niveau NSS.

La gestion individuelle des membres reste hors MVP.

### ERP-Q02 — Coordination par pays

**[VALIDÉ PO] Modèle recommandé : personne coordinatrice + organisation point focal éventuelle.**

Chaque pays pourra donc avoir :
- une coordinatrice / représentante NSS ;
- une organisation point focal lorsqu'elle existe ;
- un historique des changements.

Les deux éléments doivent rester indépendants afin qu'un pays puisse fonctionner avec :
- une personne seulement ;
- une organisation seulement ;
- ou les deux.

### ERP-Q24 — Périmètre comptable

**[VALIDÉ PO] L'ERP doit prévoir une comptabilité complète/officielle, et pas seulement un suivi recettes/dépenses.**

L'architecture devra donc étudier :
- journaux ;
- plan comptable ;
- banques / caisses ;
- écritures comptables ;
- rapprochements ;
- fournisseurs ;
- paiements ;
- clôtures ;
- états financiers ;
- analytique par projet / activité / bailleur ;
- obligations comptables applicables.

La configuration exacte devra être validée dans NSS-ERP-02.

### ERP-Q05 — Organisation comptable multi-pays

**[OUVERT — DEUX OPTIONS À ÉTUDIER DANS NSS-ERP-02]**

Le PO ne souhaite pas encore choisir entre :

**Option A — centralisation**
- une comptabilité principale NSS ;
- coordination centrale ;
- suivi analytique des pays.

**Option B — multi-entités**
- comptabilités séparées pour certaines coordinations / structures pays ;
- consolidation au niveau NSS.

NSS-ERP-02 doit comparer les deux architectures et recommander une trajectoire progressive.

Pour les premiers tests, privilégier l'architecture la plus simple à déployer, sans empêcher une évolution vers l'autre option.

### ERP-Q15 — Utilisateurs

**[VALIDÉ PO] Démarrage sur un petit nombre d'utilisateurs, puis extension progressive.**

Ordre de grandeur de départ retenu :
- environ 10 à 20 utilisateurs maximum pour le MVP / pilote ;
- comptes de test et données fictives avant toute mise en production ;
- ajout des utilisateurs réels uniquement après validation des rôles et droits.

### ERP-Q17 — Hébergement

**[VALIDÉ PO] Hébergement sur VPS Hostinger existant avec Odoo Community.**

Le PO dispose déjà d'un VPS Hostinger avec Odoo Community.

NSS-ERP-02 devra donc :
- auditer l'instance / l'environnement disponible avant déploiement ;
- éviter d'impacter les autres instances éventuelles ;
- recommander isolation, sauvegardes, sécurité et stratégie de déploiement ;
- définir un environnement de test avec données fictives avant production.

### Principe de test

**[VALIDÉ PO] Aucun démarrage avec les données réelles NSS.**

La première implémentation devra utiliser :
- pays fictifs ou copies anonymisées ;
- organisations fictives ;
- projets fictifs ;
- budgets et écritures fictifs ;
- utilisateurs de test.

Les données réelles ne seront intégrées qu'après validation fonctionnelle, droits d'accès, sauvegardes et processus de migration.


---

## 33. Contrôle fonctionnel ChatGPT — corrections V1.1

Les corrections suivantes ont été intégrées sans modifier l'orientation générale de l'audit :

1. La liste 2026 reste fixée à **10 pays [VALIDÉ PO]**.
2. Les dates 2019/2023 sont traitées comme des **dates de documentation**, pas comme des dates d'entrée certaines.
3. La brochure permet d'identifier **13 organisations historiques nommées**, et non 14.
4. Le chiffre des **12 organisations fondatrices de 2011** est distingué de la liste de membres visible en 2019.
5. La devise **XAF** a été retirée des devises directement liées aux 10 pays retenus.
6. Le besoin de **comptabilité** a été séparé du simple suivi recettes/dépenses/budgets et devient une décision PO critique.
7. Les noms actuels des coordinations et organisations sont considérés comme des données de migration, **pas comme des bloqueurs d'architecture**.


---

*Fin du document NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md*
