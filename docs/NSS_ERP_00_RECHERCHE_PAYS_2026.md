# NSS ERP — Recherche pays & mise à jour 2026

**Statut :** source de travail pré-ERP
**Date de mise à jour :** 23 septembre 2026
**Objectif :** établir une base factuelle récente sur l'implantation géographique de Nous Sommes la Solution (NSS) avant l'audit fonctionnel ERP.

---

## 1. Principe de lecture

Les informations historiques NSS ne doivent pas être considérées comme automatiquement valides en 2026.

Pour le projet ERP, on distingue :

- **[VÉRIFIÉ RÉCENT]** : confirmé par une source récente identifiant explicitement le pays.
- **[HISTORIQUE]** : confirmé par une ancienne documentation NSS.
- **[À VALIDER PO]** : information plausible ou revendiquée par une source, mais non suffisamment documentée pour devenir une donnée de référence ERP.
- **[CONFLIT DE SOURCES]** : plusieurs sources donnent des chiffres incompatibles.

La donnée validée par le Product Owner NSS prévaut toujours sur les sources publiques.

---

## 2. Évolution documentée du réseau

### 2011 — 5 pays fondateurs

La documentation historique NSS indique que le mouvement est lancé en 2011 par 12 organisations de femmes rurales dans :

1. Burkina Faso
2. Ghana
3. Guinée
4. Mali
5. Sénégal

Répartition historique :
- Burkina Faso : 2 organisations
- Ghana : 2
- Guinée : 2
- Mali : 3
- Sénégal : 3

**Statut : [HISTORIQUE CONFIRMÉ]**

### Vers 2019 — 7 pays documentés

La brochure NSS de 2019 mentionne également des organisations membres en :

6. Gambie
7. Guinée-Bissau

La brochure liste notamment CGF pour la Gambie et KAFO pour la Guinée-Bissau.

**Statut : [HISTORIQUE CONFIRMÉ]**

### 2023–2025 — 8 pays

Des publications de 2023–2025 décrivent NSS comme un réseau d'environ 800 associations dans huit pays :

1. Burkina Faso
2. Côte d'Ivoire
3. Gambie
4. Ghana
5. Guinée
6. Guinée-Bissau
7. Mali
8. Sénégal

La Côte d'Ivoire est donc une extension postérieure à la brochure 2019.

**Statut : [VÉRIFIÉ]**

### Juin 2026 — Bénin

Le lancement officiel de NSS au Bénin a eu lieu le 13 juin 2026.

Éléments récents :
- Représentante nationale : **Clarisse ADONSI**
- Appui cité : **Fédération Agroécologique du Bénin (FAEB)**
- Implantation / siège annoncé : Cotonou, secteur de Fidjrossè
- lancement avec plus de 200 participantes et participants selon les publications disponibles.

**Statut : [VÉRIFIÉ RÉCENT]**

### Juillet 2026 — Togo

La branche togolaise a été officiellement lancée le 18 juillet 2026 à Kpalimé.

Éléments récents :
- Coordinatrice nationale : **Aku Afefa Agbeka-Adiku**
- Point focal / organisation membre citée : **Eco-Impact**
- Directeur exécutif Eco-Impact cité : **Jean-Charles Sossou**
- Coordinatrice NSS Côte d'Ivoire citée : **Monique Konan**

Plusieurs sources de juillet 2026 décrivent explicitement le Togo comme le dixième pays et énumèrent les neuf précédents.

**Statut : [VÉRIFIÉ RÉCENT]**

---

## 3. Base pays opérationnelle à utiliser pour l'ERP

À la date du 23 septembre 2026, la liste la mieux étayée par des sources qui **nomment explicitement les pays** est :

| # | Pays | Statut ERP initial | Remarque |
|---|---|---|---|
| 1 | Burkina Faso | Actif / historique | Pays fondateur |
| 2 | Ghana | Actif / historique | Pays fondateur |
| 3 | Guinée | Actif / historique | Pays fondateur |
| 4 | Mali | Actif / historique | Pays fondateur |
| 5 | Sénégal | Actif / historique | Pays fondateur |
| 6 | Gambie | Actif | Documenté dans la brochure 2019 |
| 7 | Guinée-Bissau | Actif | Documenté dans la brochure 2019 |
| 8 | Côte d'Ivoire | Actif | Documenté comme membre du réseau à partir des sources 2023 |
| 9 | Bénin | Actif récent | Implantation officielle juin 2026 |
| 10 | Togo | Actif récent | Lancement officiel juillet 2026 |

Une publication de septembre 2026 sur le camp CIFAP de Niaguis cite précisément des participantes venues de ces **10 pays** :
Bénin, Burkina Faso, Côte d'Ivoire, Gambie, Ghana, Guinée, Guinée-Bissau, Mali, Sénégal et Togo.

**BASE ERP VALIDÉE PAR LE PO : 10 pays.**

Décision du Product Owner du 23 septembre 2026 : **la liste officielle retenue pour le projet ERP NSS est fixée à 10 pays**.

---

## 4. Conflits de sources à ne pas masquer

### Bénin décrit comme « 12e pays »

Le site NSS / WAS Africa et plusieurs reprises de presse publiées en juin 2026 présentent le Bénin comme le **12e pays d'implantation**.

Cela entre en conflit avec :
- les listes nominatives récentes ;
- les sources de juillet 2026 présentant le Togo comme le **10e pays** ;
- la liste des 10 pays représentés au CIFAP de septembre 2026.

**Décision ERP après validation PO :**
la liste officielle du projet ERP reste fixée à **10 pays**. Les mentions publiques de 12 pays ne modifient pas la donnée de référence ERP.

Créer la mention :

> **[À VALIDER PO] Des sources publiques parlent de 12 pays au moment de l'arrivée du Bénin, mais elles ne fournissent pas une liste nominative cohérente.**

### AFSA décrit NSS comme présent dans 14 pays

Une page récente de l'Alliance for Food Sovereignty in Africa (AFSA) présente NSS comme un mouvement de femmes rurales de **14 pays d'Afrique de l'Ouest**.

Cette page ne donne pas la liste nominative des 14 pays dans le contenu consulté.

**Décision ERP après validation PO :**
- ne pas créer quatre pays supplémentaires sur cette seule base ;
- conserver cette mention uniquement comme **écart documentaire externe** ;
- la donnée de référence ERP est **10 pays**.

### Chiffres de membres et d'associations

Plusieurs périodes donnent des chiffres différents :
- brochure historique : plus de 500 AFR, environ 175 000 membres et sympathisant·es ;
- sources 2023 : environ 800 associations, plus de 180 000 membres ;
- lancement Togo 2026 : plus de 800 associations, plus de 200 000 membres et sympathisants.

**Décision ERP :**
les chiffres globaux ne doivent jamais être codés en dur.

Ils doivent être :
- calculés depuis les données ERP lorsque possible ;
- ou stockés comme indicateurs datés avec une source et un statut de validation.

---

## 5. Conséquences directes pour le modèle ERP

### 5.1 Pays dynamique

Ne jamais créer une liste fermée codée en dur.

Entité minimale proposée :

`country_membership`

Champs fonctionnels envisagés :
- pays
- code ISO
- statut NSS
- date d'entrée / lancement
- date de sortie éventuelle
- type : fondateur / extension / observation / à confirmer
- coordination nationale
- organisation point focal
- source de validation
- date de vérification
- vérifié par
- notes
- actif / archivé

### 5.2 Coordination nationale

Le modèle doit permettre :

`Pays`
→ `Coordination NSS nationale`
→ `Organisation(s) membre(s)`
→ `Responsables / contacts`
→ éventuellement `Membres individuels`

Ne pas présumer que tous les pays ont exactement la même structure.

### 5.3 Organisations

Une organisation peut avoir :
- plusieurs responsables dans le temps ;
- une date d'adhésion ;
- un statut ;
- plusieurs contacts ;
- plusieurs projets ;
- plusieurs pièces/documentations ;
- une relation avec un ou plusieurs financements.

Les anciennes listes de contacts ne doivent pas écraser les responsables actuels.

### 5.4 Historisation obligatoire

Prévoir un historique pour :
- responsables pays ;
- responsables d'associations ;
- statut d'une organisation ;
- adhésion ;
- coordonnées ;
- rattachement pays ;
- documents officiels.

### 5.5 Données sensibles

Téléphones, emails personnels, pièces administratives et informations financières doivent être protégés par des droits d'accès.

Les contacts historiques de la brochure 2019 ne doivent pas être importés automatiquement sans validation.

---

## 6. Données récentes identifiées

### Bénin

- Pays : Bénin
- Statut : actif récent
- Date de lancement : 13 juin 2026
- Représentante nationale : Clarisse ADONSI
- Appui / structure citée : Fédération Agroécologique du Bénin (FAEB)
- Ville / zone citée : Cotonou / Fidjrossè
- Validation finale ERP : [À VALIDER PO]

### Togo

- Pays : Togo
- Statut : actif récent
- Date de lancement : 18 juillet 2026
- Coordinatrice nationale : Aku Afefa Agbeka-Adiku
- Point focal cité : Eco-Impact
- Responsable Eco-Impact cité : Jean-Charles Sossou
- Lieu du lancement : Kpalimé
- Validation finale ERP : [À VALIDER PO]

### Côte d'Ivoire

- Pays : Côte d'Ivoire
- Statut : actif
- Coordinatrice citée en 2026 : Monique Konan
- Validation finale ERP : [À VALIDER PO]

### Sénégal

- Pays : Sénégal
- Statut : fondateur / actif
- Présidente panafricaine NSS citée dans les sources récentes : Mariama Sonko
- Validation finale ERP : [À VALIDER PO]

---

## 7. Points à confirmer avec NSS

| ID | Question | Importance ERP |
|---|---|---|
| GEO-01 | Liste officielle des pays membres au 23/09/2026 | **VALIDÉ PO : 10 pays** |
| GEO-02 | Écart documentaire « 12e pays » pour le Bénin | Non bloquant — conserver comme note de source |
| GEO-03 | Mentions externes de 12/14 pays | Non bloquant — ne pas intégrer à la base ERP |
| GEO-04 | Confirmer la coordinatrice / représentante actuelle de chaque pays | Critique |
| GEO-05 | Confirmer l'organisation point focal par pays | Critique |
| GEO-06 | Confirmer les associations réellement actives par pays | Critique |
| GEO-07 | Confirmer le nombre actuel d'associations membres | Moyenne |
| GEO-08 | Confirmer le nombre actuel de membres et sympathisant·es | Moyenne |
| GEO-09 | Définir la différence métier entre association, organisation, coordination pays et membre | Critique |
| GEO-10 | Déterminer si le suivi individuel des membres est nécessaire dans l'ERP | Critique |

---

## 8. Sources principales consultées

### Source historique
- Brochure « NSS FRANCAIS » de 2019 fournie au projet.

### Sources récentes
- WAS Africa / NSS — lancement officiel du Bénin, 15 juin 2026
  https://wasafrica.org/fr/implantation-officielle-du-mouvement-panafricain-nous-sommes-la-solution-au-benin-ce-samedi-13-juin-2026/

- WAS Africa / NSS — implantation NSS au Bénin
  https://wasafrica.org/fr/agroecologie-et-souverainete-alimentaire-au-benin-le-mouvement-nss-mis-sur-pied/

- Société Civile Médias — lancement NSS Togo, 20 juillet 2026
  https://societecivilemedias.com/2026/07/20/agriculture-durable-le-mouvement-nous-sommes-la-solution-lance-sa-branche-togolaise-pour-porter-la-voix-des-femmes-paysannes/

- Agridigitale — Togo présenté comme dixième pays, 18 juillet 2026
  https://agridigitale.net/article/le-mouvement-nous-sommes-la-solution-pose-ses-valises-au-togo

- CFSI / ALIMENTERRE — réseau de 8 pays en 2023
  https://www.alimenterre.org/mariama-sonko-le-soulevement-des-femmes-rurales

- AFSA — page membres présentant NSS comme actif dans 14 pays
  https://afsafrica.org/fr/nos-membres/

- Casa24 — CIFAP 2026, participantes de 10 pays
  https://www.casa24.sn/Agroecologie-en-Afrique-de-l-Ouest-Quand-les-femmes-rurale-reprennent-le-controle-de-l-assiette-et-des-terroirs_a6724.html

---

## 9. Règle pour la suite du projet

Pour `NSS_ERP_01_AUDIT_PROCESSUS_BESOINS.md` :

- utiliser **10 pays validés par le PO** comme baseline officielle et opérationnelle ;
- conserver les mentions 12/14 pays uniquement comme **écarts documentaires externes non bloquants** ;
- ne jamais inventer les pays manquants ;
- toute donnée de personne, organisation ou chiffre non confirmée par le PO reste `[À VALIDER PO]`;
- la structure ERP doit être extensible à de nouveaux pays sans modification du code.
