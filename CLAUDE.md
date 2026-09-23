# CLAUDE.md — NSS ERP

## 1. Rôle de Claude Code

Tu interviens comme **développeur / intégrateur technique** du projet ERP de **Nous Sommes la Solution (NSS)**.

Tu n'es pas le Product Owner et tu ne dois pas inventer de règles métier.

Le Product Owner est l'utilisateur.
Claude Opus intervient comme architecte fonctionnel.
ChatGPT intervient comme contrôleur fonctionnel / UX / cadrage.
Claude Code intervient uniquement lorsque les décisions nécessaires ont été validées.

---

## 2. État actuel du projet

Le projet est en **phase de recherche et d'audit fonctionnel**.

Solution envisagée :
- Odoo Community ;
- modules OCA si réellement nécessaires ;
- développements spécifiques seulement lorsqu'un besoin validé n'est pas couvert proprement.

### Interdiction actuelle

**Ne pas installer, configurer ou développer l'ERP tant que `NSS_ERP_02` n'a pas validé l'architecture technique.**

Avant cette validation, le travail autorisé concerne uniquement :
- lecture des sources ;
- audit du repo ;
- documentation ;
- préparation de structures non exécutables ;
- vérification de compatibilité ;
- propositions techniques sans implémentation.

---

## 3. Sources de vérité

Ordre de priorité :

1. décisions explicites et récentes du Product Owner ;
2. données internes NSS validées par le Product Owner ;
3. documents NSS récents et officiels ;
4. publications récentes du site NSS / WAS Africa ;
5. sources partenaires crédibles ;
6. documentation historique ;
7. hypothèses.

Une hypothèse ne devient jamais un fait.

Utiliser systématiquement :
- `[À VALIDER PO]` pour une donnée non confirmée ;
- `[HYPOTHÈSE]` pour une proposition ;
- `[CONFLIT DE SOURCES]` lorsqu'une information est contradictoire.

Ne jamais résoudre silencieusement un conflit documentaire.

---

## 4. Baseline géographique NSS — septembre 2026

La brochure historique 2019 documente notamment :
- Burkina Faso
- Gambie
- Ghana
- Guinée
- Guinée-Bissau
- Mali
- Sénégal

Les recherches récentes permettent d'ajouter de façon nominative :
- Côte d'Ivoire
- Bénin
- Togo

### Liste officielle validée par le Product Owner

1. Bénin
2. Burkina Faso
3. Côte d'Ivoire
4. Gambie
5. Ghana
6. Guinée
7. Guinée-Bissau
8. Mali
9. Sénégal
10. Togo

**Décision PO du 23 septembre 2026 : cette liste de 10 pays est la source de vérité fonctionnelle actuelle du projet ERP NSS.**

Elle reste une donnée métier dynamique : de nouveaux pays pourront être ajoutés ultérieurement sans modifier le code.

Des sources publiques mentionnent également :
- Bénin comme « 12e pays » ;
- NSS comme réseau de « 14 pays ».

Ces affirmations ne donnent pas une liste nominative cohérente avec les autres sources.

Elles doivent donc rester comme :

`[ÉCART DOCUMENTAIRE EXTERNE — NON BLOQUANT]`

Elles ne doivent pas modifier la liste officielle ERP tant qu'une nouvelle décision explicite du Product Owner n'est pas donnée.

### Règle absolue

**Ne jamais coder `10`, `12` ou `14` comme nombre fixe dans la logique applicative.**

Le nombre actuel validé est **10**, mais il doit être obtenu depuis les données.

Les pays doivent être des enregistrements de données ajoutables, modifiables, activables et archivables.

Lire également :

`NSS_ERP_00_RECHERCHE_PAYS_2026.md`

---

## 5. Évolution géographique connue

### 2011
5 pays fondateurs :
- Burkina Faso
- Ghana
- Guinée
- Mali
- Sénégal

### Documentation 2019
Présence également documentée :
- Gambie
- Guinée-Bissau

### 2023
Présence documentée en Côte d'Ivoire.

### 13 juin 2026
Implantation officielle au Bénin.

Données récentes à conserver comme provisoires :
- Représentante : Clarisse ADONSI
- Structure citée : FAEB

Statut :
`[À VALIDER PO avant import de production]`

### 18 juillet 2026
Lancement officiel NSS Togo.

Données récentes à conserver comme provisoires :
- Coordinatrice : Aku Afefa Agbeka-Adiku
- Point focal cité : Eco-Impact
- Responsable Eco-Impact cité : Jean-Charles Sossou

Statut :
`[À VALIDER PO avant import de production]`

### Côte d'Ivoire
Coordinatrice citée en 2026 :
- Monique Konan

Statut :
`[À VALIDER PO avant import de production]`

---

## 6. Principe de modèle de données

Le modèle cible devra pouvoir représenter au minimum :

```text
NSS
│
├── Pays
│   ├── Coordination nationale
│   │   ├── Responsable(s)
│   │   └── Historique
│   │
│   └── Organisations / associations
│       ├── Responsable(s)
│       ├── Contacts
│       ├── Adhésion
│       ├── Documents
│       └── Membres éventuels
│
├── Programmes
│   └── Projets
│       └── Activités
│
├── Partenaires / bailleurs
│   └── Financements
│
└── Finance
    ├── Budgets
    ├── Recettes
    ├── Dépenses
    └── Justificatifs
```

Ce schéma est fonctionnel et provisoire.
Il ne doit pas être transformé en modèle Odoo définitif avant validation de `NSS_ERP_01` et `NSS_ERP_02`.

---

## 7. Règles critiques de conception

### 7.1 Multi-pays

Le système doit permettre l'ajout d'un pays sans modification du code.

Interdit :
- enum métier figée contenant les pays NSS ;
- conditions du type `if country == Senegal`;
- dashboards supposant un nombre fixe de pays.

### 7.2 Historisation

Ne jamais écraser un ancien responsable sans conserver l'historique si le besoin métier est validé.

Prévoir l'historisation potentielle de :
- responsable pays ;
- responsable organisation ;
- statut organisation ;
- adhésion ;
- rattachement ;
- coordonnées officielles.

### 7.3 Membres

Ne pas supposer que NSS souhaite gérer individuellement plus de 180 000 / 200 000 membres.

La décision entre :
- suivi des organisations uniquement ;
- suivi d'agrégats ;
- suivi individuel des membres

est **[À VALIDER PO]**.

Aucune table massive de membres individuels ne doit être créée avant cette décision.

### 7.4 Comptabilité

Ne pas supposer :
- une devise unique ;
- un seul plan comptable ;
- un seul pays fiscal ;
- une consolidation comptable complète.

Le mouvement est multi-pays et les besoins comptables doivent être définis dans l'audit.

### 7.5 Langues

Ne pas supposer que l'ERP sera uniquement en français.

Présence de pays francophones, anglophones et lusophones dans le réseau.

La stratégie linguistique ERP est :
`[À VALIDER PO]`.

### 7.6 Données personnelles

Les données suivantes sont sensibles :
- téléphones ;
- emails personnels ;
- documents d'identité ;
- pièces financières ;
- justificatifs ;
- informations bancaires.

Appliquer le principe du moindre privilège.

Ne jamais exposer ces données dans :
- logs ;
- données de démonstration ;
- fixtures publiques ;
- captures ;
- exports non protégés.

---

## 8. Règles Odoo

Lorsque l'architecture sera validée :

1. privilégier Odoo Community natif ;
2. vérifier les modules OCA avant tout développement spécifique ;
3. documenter chaque module ajouté ;
4. éviter les dépendances inutiles ;
5. ne jamais modifier directement le core Odoo ;
6. créer les personnalisations dans des modules NSS séparés ;
7. prévoir migrations et désinstallation propres ;
8. ne pas ajouter de module simplement parce qu'il existe.

Pour chaque fonctionnalité, documenter :

```text
Besoin métier
→ Odoo natif ?
→ OCA ?
→ paramétrage ?
→ développement NSS ?
→ rejet / hors périmètre ?
```

---

## 9. Principe MVP

Le MVP doit rester petit.

Domaines actuellement envisagés :
- réseau / pays / organisations ;
- adhésions essentielles ;
- projets / activités ;
- budgets ;
- recettes / dépenses ;
- justificatifs ;
- partenaires / bailleurs ;
- reporting essentiel ;
- utilisateurs / rôles.

Ne pas ajouter sans validation :
- IA ;
- application mobile native ;
- CRM commercial complexe ;
- RH complète ;
- automatisations gadgets ;
- fonctionnalités marketing ;
- portail sophistiqué ;
- intégrations externes non justifiées.

---

## 10. Workflow documentaire

Les livrables sont nommés :

```text
NSS_ERP_00_...
NSS_ERP_01_...
NSS_ERP_02_...
```

Ordre prévu :

```text
NSS_ERP_00_RECHERCHE_PAYS_2026.md
        ↓
NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md
        ↓
Validation PO + contrôle ChatGPT
        ↓
NSS_ERP_02_ARCHITECTURE_ODOO.md
        ↓
Validation PO
        ↓
Implémentation Claude Code
```

Ne sauter aucune étape structurante.

---

## 11. Comportement attendu de Claude Code

Avant toute modification :

1. lire `CLAUDE.md` ;
2. lire les documents `NSS_ERP_*` disponibles ;
3. auditer l'existant ;
4. identifier ce qui est validé et ce qui ne l'est pas ;
5. annoncer les fichiers qui seront touchés ;
6. effectuer seulement les modifications nécessaires ;
7. vérifier le résultat ;
8. fournir un résumé court des changements.

Ne pas :
- inventer des données ;
- modifier des fichiers hors périmètre ;
- lancer une refonte globale non demandée ;
- créer 10 variantes d'une même solution ;
- supprimer des données ;
- importer des contacts historiques sans validation ;
- transformer une donnée web en donnée de production automatiquement.

---

## 12. Règle anti allers-retours

Lorsque des informations sont manquantes :

- ne pas interrompre le travail pour poser une question à chaque manque ;
- regrouper les blocages dans une section unique `POINTS_A_VALIDER_PO`;
- continuer tout ce qui peut être fait sans hypothèse dangereuse.

Exception :
si une action est destructive, irréversible, financière ou de production, demander validation avant exécution.

---

## 13. Import des anciennes données

La brochure 2019 contient des associations, responsables, téléphones et emails.

Ces informations sont des **données historiques**.

Avant import :
- vérifier si l'organisation est toujours membre ;
- vérifier le responsable actuel ;
- vérifier l'adresse email ;
- vérifier le téléphone ;
- conserver la provenance et la date de la source.

Ne jamais remplacer automatiquement une donnée récente par une donnée de 2019.

---

## 14. Qualité des données

Toute donnée structurante importée doit idéalement disposer de :

```text
source
source_date
verification_status
verified_at
verified_by
notes
```

Valeurs possibles de `verification_status` :

```text
historical
unverified
po_confirmed
source_confirmed
conflict
archived
```

Les noms techniques définitifs seront décidés lors de l'architecture.

---

## 15. Critère de réussite

Le futur ERP NSS doit être :

- simple ;
- compréhensible par l'équipe ;
- maintenable ;
- évolutif ;
- multi-pays ;
- peu dépendant de développements spécifiques ;
- sécurisé ;
- capable de conserver l'historique ;
- capable d'évoluer si NSS accueille de nouveaux pays.

La priorité n'est pas de maximiser le nombre de fonctionnalités.

La priorité est d'obtenir une **source de vérité interne fiable pour NSS**.
