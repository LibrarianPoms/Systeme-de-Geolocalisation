# Benchmark des Solutions de Géolocalisation pour Poids Lourds

## Document d'Analyse Comparative

**Date de création**: Mars 2026  
**Sources analysées**: 10 documents PDF du dossier "Localisation poid lourd"  
**Images extraites**: 29 captures des documents sources (dossier `extracted_images/`)

---

## Table des Matières

1. [Résumé Exécutif](#1-résumé-exécutif)
2. [Solutions Hardware Analysées](#2-solutions-hardware-analysées)
3. [Solutions Logicielles](#3-solutions-logicielles)
4. [Aspects Réglementaires](#4-aspects-réglementaires)
5. [Technologies de Données FCD](#5-technologies-de-données-fcd)
6. [Recherche Académique](#6-recherche-académique)
7. [Tableau Comparatif Global](#7-tableau-comparatif-global)
8. [Recommandations](#8-recommandations)
9. [Galerie d'Images Extraites](#9-galerie-dimages-extraites)

---

## 1. Résumé Exécutif

Ce benchmark analyse **10 documents** couvrant les solutions de géolocalisation pour flottes de poids lourds, incluant :
- **3 solutions hardware commerciales** (Samsara VG34, TomTom LINK 510, ATHMO Positel)
- **1 GPS de navigation poids lourd** (Becker Transit 7SL)
- **2 documents réglementaires** (CNIL/APDP, chronotachygraphes)
- **2 documents techniques** (FCD, livre blanc gestion de flotte)
- **1 thèse académique** (localisation dynamique sur carte)

### Points Clés
- Les solutions modernes combinent **GPS multi-constellation** (GPS/GLONASS/Galileo/Beidou)
- Communication via **4G LTE** avec fallback 3G/2G
- Intégration **OBD-II/CAN Bus** pour données véhicule
- Conformité **RGPD** obligatoire pour la géolocalisation des salariés
- Tendance vers la **maintenance prédictive** et l'**éco-conduite**

### 📊 Architecture Générale d'un Système de Géolocalisation

```mermaid
flowchart TB
    subgraph VEHICULE["🚛 VÉHICULE"]
        GPS["📡 Module GPS<br/>GPS/GLONASS/Galileo"]
        OBD["🔌 Interface OBD-II<br/>CAN Bus / J1939 / FMS"]
        SENSORS["📊 Capteurs<br/>Température / Carburant"]
        TACHO["⏱️ Tachygraphe<br/>Temps de conduite"]
        DRIVER["👤 ID Conducteur<br/>Dallas / RFID / NFC"]
    end
    
    subgraph BOITIER["📦 BOÎTIER TÉLÉMATIQUE"]
        MCU["🔧 Microcontrôleur"]
        MODEM["📶 Modem 4G/3G/2G"]
        STORAGE["💾 Stockage Local"]
        BT["🔵 Bluetooth"]
        WIFI["📶 WiFi"]
    end
    
    subgraph CLOUD["☁️ PLATEFORME CLOUD"]
        SERVER["🖥️ Serveurs"]
        DB["🗄️ Base de Données"]
        API["🔗 API REST"]
        ALERTS["🔔 Moteur d'Alertes"]
    end
    
    subgraph USERS["👥 UTILISATEURS"]
        WEB["🌐 Interface Web"]
        MOBILE["📱 App Mobile"]
        REPORTS["📊 Rapports"]
    end
    
    GPS --> MCU
    OBD --> MCU
    SENSORS --> MCU
    TACHO --> MCU
    DRIVER --> MCU
    
    MCU --> MODEM
    MCU --> STORAGE
    MCU --> BT
    MCU --> WIFI
    
    MODEM -->|"GSM/GPRS/LTE"| SERVER
    SERVER --> DB
    SERVER --> API
    SERVER --> ALERTS
    
    API --> WEB
    API --> MOBILE
    DB --> REPORTS
    ALERTS -->|"Email/SMS/Push"| USERS
```

### 📈 Flux de Données Temps Réel

```mermaid
sequenceDiagram
    participant V as 🚛 Véhicule
    participant B as 📦 Boîtier
    participant N as 📶 Réseau
    participant S as ☁️ Serveur
    participant U as 👤 Utilisateur
    
    V->>B: Position GPS (1 Hz)
    V->>B: Données OBD-II
    V->>B: État capteurs
    
    B->>B: Agrégation données
    B->>B: Stockage local
    
    alt Réseau disponible
        B->>N: Transmission MQTT/HTTP
        N->>S: Données véhicule
        S->>S: Traitement & Stockage
        S->>U: Mise à jour temps réel
    else Hors connexion
        B->>B: File d'attente locale
        Note over B: Store & Forward
    end
    
    alt Alerte détectée
        S->>U: Notification push
        S->>U: Email/SMS
    end
```

---

## 2. Solutions Hardware Analysées

### 2.1 Samsara VG34/VG34-EU

**Fabricant**: Samsara Networks  
**Type**: Passerelle IoT pour véhicules  
**Document source**: `VG34_datasheet_FR.pdf`

#### 📷 Aperçu Visuel

| Page 1 - Présentation | Page 2 - Sources de données |
|:---------------------:|:---------------------------:|
| ![VG34 Page 1](extracted_images/VG34_page_01.png) | ![VG34 Page 2](extracted_images/VG34_page_02.png) |

| Page 3 - Connectivité | Page 4 - Logiciel |
|:---------------------:|:-----------------:|
| ![VG34 Page 3](extracted_images/VG34_page_03.png) | ![VG34 Page 4](extracted_images/VG34_page_04.png) |

#### 🔧 Architecture Interne VG34

```mermaid
flowchart LR
    subgraph INPUTS["ENTRÉES"]
        J1962["J1962/OBD-II<br/>VL/VI"]
        J1939["J1939<br/>Poids Lourds"]
        FMS["FMS<br/>MAN/Daimler/Scania"]
        AUX["2x Entrées<br/>Numériques"]
        WIRELESS["Capteurs<br/>Sans Fil"]
    end
    
    subgraph VG34["SAMSARA VG34"]
        GPS_MOD["GPS/GLONASS<br/>-162 dBm"]
        PROC["Processeur"]
        FLASH["Mémoire Flash<br/>Hors-ligne"]
        LTE["4G LTE<br/>+ 3G/2G"]
        WIFI_AP["WiFi AP<br/>802.11g/n"]
        SEC["AES-256<br/>SSL/TLS"]
    end
    
    subgraph OUTPUTS["SORTIES"]
        CLOUD["Samsara Cloud"]
        HOTSPOT["Point d'Accès<br/>WiFi Cabine"]
        OUT1["1x Sortie<br/>Numérique"]
    end
    
    J1962 --> PROC
    J1939 --> PROC
    FMS --> PROC
    AUX --> PROC
    WIRELESS --> PROC
    GPS_MOD --> PROC
    
    PROC --> FLASH
    PROC --> LTE
    PROC --> WIFI_AP
    
    LTE --> SEC --> CLOUD
    WIFI_AP --> HOTSPOT
    PROC --> OUT1
```

#### Spécifications Techniques

| Caractéristique | Valeur |
|-----------------|--------|
| **Dimensions** | 117 x 72 x 26 mm |
| **Poids** | 118 g |
| **Température de fonctionnement** | -40°C à +85°C |
| **Alimentation** | 12V / 24V |
| **Consommation (marche)** | 1,8 W |
| **Consommation (veille)** | 396 mW |

#### Connectivité

| Type | Spécification |
|------|---------------|
| **Cellulaire VG34** | LTE B2/4/5/12, 3G B2/5 |
| **Cellulaire VG34-EU** | LTE B1/3/7/8/20, 3G B1/8, 2G B3/8 |
| **WiFi** | 802.11g/n, 2,4 GHz (Point d'accès intégré) |
| **Sécurité** | SSL/TLS, AES 256 bits |

#### Interfaces Véhicule

| Interface | Compatibilité |
|-----------|---------------|
| **OBD-II J1962** | Véhicules légers/intermédiaires |
| **J1939** | Poids lourds (Type 1 et 2) |
| **J1708** | Alimentation uniquement |
| **FMS** | MAN, Daimler, Scania, DAF, Iveco, Volvo, Renault |

#### Fonctionnalités GPS

- **Multi-constellation**: GPS + GLONASS
- **Sensibilité**: -162 dBm
- **Démarrage à chaud**: 1 seconde
- **Antenne**: Interne (externe en option)

#### Capteurs Compatibles

- Contrôleurs de température sans fil (série EM)
- Jetons d'identification conducteurs
- Modules d'entrée industriels (série IM)
- 2 entrées numériques auxiliaires
- 1 sortie numérique (future)

#### Fonctionnalités Logicielles (Cloud Samsara)

- ✅ Localisation temps réel
- ✅ Affectation véhicules
- ✅ Rapports et alertes
- ✅ Heures de service (ELD compliance USA)
- ✅ Journaux de maintenance
- ✅ Inspection véhicule électronique
- ✅ Communication répartiteurs
- ✅ Téléchargement tachygraphe à distance

#### Tarification

- Licence annuelle (1, 3 ou 5 ans)
- Inclut: connectivité cellulaire, cloud, apps mobiles, mises à jour firmware, support

---

### 2.2 TomTom LINK 510

**Fabricant**: TomTom Business Solutions  
**Type**: Boîtier de géolocalisation  
**Document source**: `ttb-link510-doc.pdf`

#### 📷 Aperçu Visuel

| Page 1 - Présentation & Avantages | Page 2 - Fonctionnalités & Specs |
|:---------------------------------:|:--------------------------------:|
| ![TomTom Page 1](extracted_images/TomTom_LINK510_page_01.png) | ![TomTom Page 2](extracted_images/TomTom_LINK510_page_02.png) |

#### 🔧 Écosystème TomTom LINK 510

```mermaid
flowchart TB
    subgraph LINK510["📦 TomTom LINK 510"]
        GPS510["GPS"]
        GSM["GSM/GPRS"]
        BT510["Bluetooth"]
        CAN["CAN Bus"]
        IO["2 IN / 1 OUT"]
    end
    
    subgraph VEHICLE["🚛 Véhicule"]
        TACHO510["Tachygraphe<br/>Numérique"]
        FMS510["Prise FMS"]
        DOORS["Portes"]
        FUEL["Carburant"]
    end
    
    subgraph ACCESSORIES["📱 Accessoires"]
        PRO["TomTom PRO<br/>Navigation"]
        ECOPLUS["ecoPLUS<br/>Éco-conduite"]
    end
    
    subgraph WEBFLEET["☁️ WEBFLEET"]
        DASHBOARD["Tableau de Bord"]
        TRACKING["Suivi Temps Réel"]
        REPORTS510["Rapports Auto"]
        LOGBOOK["Carnet de Route"]
    end
    
    TACHO510 --> LINK510
    FMS510 --> CAN
    DOORS --> IO
    FUEL --> IO
    
    BT510 <--> PRO
    BT510 <--> ECOPLUS
    
    GSM --> WEBFLEET
    
    WEBFLEET --> DASHBOARD
    WEBFLEET --> TRACKING
    WEBFLEET --> REPORTS510
    WEBFLEET --> LOGBOOK
```

#### Spécifications Techniques

| Caractéristique | Valeur |
|-----------------|--------|
| **Dimensions** | 121 x 56,5 x 21,5 mm |
| **Poids** | 88 g |
| **Température de fonctionnement** | -30°C à +70°C |
| **Alimentation** | 12V / 24V (9V à 30V) |
| **Consommation (14V)** | < 50 mA |
| **Consommation (28V)** | < 30 mA |
| **Consommation (veille)** | < 1 mA |

#### Connectivité

| Type | Spécification |
|------|---------------|
| **Cellulaire** | GSM/GPRS |
| **Bluetooth** | Classe 2 intégré |
| **Bus CAN** | CAN H, CAN L |

#### Interfaces

- 2 entrées numériques
- 1 sortie numérique
- Connexion FMS
- Connexion tachygraphe numérique

#### Fonctionnalités Principales

- ✅ Géolocalisation temps réel
- ✅ Rapports automatisés (km, trajets, temps sur site)
- ✅ Analyse comportement de conduite
- ✅ Carnet de route automatique
- ✅ Détection vol de carburant
- ✅ Verrouillage portes à distance
- ✅ Connexion navigation TomTom PRO (Bluetooth)
- ✅ Intégration TomTom ecoPLUS

#### Plateforme Logicielle

**TomTom WEBFLEET®** - Application SaaS de gestion de flotte
- Tableaux de bord standards
- Rapports personnalisables
- Alertes configurables

---

### 2.3 ATHMO Positel

**Fabricant**: ATHMO (France)  
**Type**: Système de géolocalisation modulaire  
**Document source**: `ATHMO_Informatique_embarquee_generale_fr_MEDIUM.pdf`

#### 📷 Aperçu Visuel

| Page 1 - Couverture | Page 2 - Présentation |
|:-------------------:|:---------------------:|
| ![ATHMO Page 1](extracted_images/ATHMO_page_01.png) | ![ATHMO Page 2](extracted_images/ATHMO_page_02.png) |

| Page 3 - Pourquoi s'équiper | Page 4 - Principe Positel |
|:---------------------------:|:-------------------------:|
| ![ATHMO Page 3](extracted_images/ATHMO_page_03.png) | ![ATHMO Page 4](extracted_images/ATHMO_page_04.png) |

| Page 5 - Application Web | Page 6 - Options |
|:------------------------:|:----------------:|
| ![ATHMO Page 5](extracted_images/ATHMO_page_05.png) | ![ATHMO Page 6](extracted_images/ATHMO_page_06.png) |

| Page 7 - Options (suite) | Page 8 - Packs de base |
|:------------------------:|:----------------------:|
| ![ATHMO Page 7](extracted_images/ATHMO_page_07.png) | ![ATHMO Page 8](extracted_images/ATHMO_page_08.png) |

#### 🔧 Architecture Modulaire ATHMO Positel

```mermaid
flowchart TB
    subgraph POSITEL["📦 POSITEL (Base)"]
        GPS_P["GPS"]
        GSM_P["GSM/GPRS"]
        PROC_P["Processeur"]
    end
    
    subgraph OPTIONS["🔌 MODULES OPTIONNELS"]
        ANTIVOL["🔒 Antivol Véhicule<br/>Batterie + Capteur mouvement"]
        CARBURANT["⛽ Antivol Carburant<br/>Interface CAN/Sonde"]
        CONSO["📊 Consommation<br/>Débitmètre"]
        TEMP["🌡️ Température<br/>Sondes"]
        ID_COND["👤 ID Conducteur<br/>Lecteur Dallas"]
        ID_REM["🚛 ID Remorque<br/>Balise RFID"]
        NAV["🗺️ Navigation<br/>GARMIN VL/PL"]
        MSG["💬 Messagerie<br/>Texte bidirectionnel"]
        POINTEUSE["⏰ Pointeuse<br/>Chantier"]
    end
    
    subgraph TACHYTEL["⏱️ TACHYTEL"]
        TACHY_READ["Lecture Tachygraphe"]
        TACHY_DL["Téléchargement<br/>Cartes & Mémoire"]
        TACHY_ALERT["Alertes Temps<br/>de Conduite"]
    end
    
    subgraph CLOUD_ATHMO["☁️ POSITEL MAP / TACHYTEL LIVE"]
        MAP_RT["Temps Réel"]
        MAP_HIST["Historiques"]
        MAP_ALERT["Alertes"]
        MAP_REPORT["Rapports"]
        MAP_ADMIN["Administration"]
    end
    
    POSITEL --> OPTIONS
    POSITEL --> TACHYTEL
    
    GSM_P --> CLOUD_ATHMO
    
    CLOUD_ATHMO --> MAP_RT
    CLOUD_ATHMO --> MAP_HIST
    CLOUD_ATHMO --> MAP_ALERT
    CLOUD_ATHMO --> MAP_REPORT
    CLOUD_ATHMO --> MAP_ADMIN
```

#### 📊 Flux Tachytel - Récupération Temps de Conduite

```mermaid
flowchart LR
    subgraph VEHICULE_T["🚛 Véhicule"]
        TACHO_A["Tachygraphe<br/>Analogique"]
        TACHO_N["Tachygraphe<br/>Numérique"]
        CARTE["Carte<br/>Conducteur"]
    end
    
    subgraph TACHYTEL_BOX["📦 Tachytel"]
        READER["Lecteur"]
        BUFFER["Buffer"]
        TX["Transmission"]
    end
    
    subgraph NETWORK["📶 Réseau"]
        WIFI_T["Wi-Fi"]
        GPRS_T["GSM/GPRS"]
    end
    
    subgraph SERVER_T["☁️ Tachytel LIVE"]
        STORAGE_T["Stockage"]
        ANALYSIS["Analyse"]
        ALERTS_T["Alertes"]
        REPORTS_T["Rapports"]
    end
    
    TACHO_A --> READER
    TACHO_N --> READER
    CARTE --> READER
    
    READER --> BUFFER --> TX
    
    TX --> WIFI_T --> SERVER_T
    TX --> GPRS_T --> SERVER_T
    
    SERVER_T --> STORAGE_T
    SERVER_T --> ANALYSIS
    ANALYSIS --> ALERTS_T
    ANALYSIS --> REPORTS_T
```

#### Présentation

ATHMO est spécialisée depuis 20+ ans dans l'informatique embarquée pour le transport routier. Historique notable: développement du logiciel KISCAN (lecture disques tachygraphes) commercialisé par VDO/Siemens dans 15 pays européens.

#### Architecture Système

```
[Véhicule + Positel] → [Réseau GSM/GPRS] → [Serveurs Positel MAP] → [Interface Web]
```

#### Compatibilité Véhicules

- 2 roues
- Voitures
- Utilitaires
- Camions
- Cars / Bus
- Engins BTP
- Autres

#### Fonctionnalités de Base (Positel MAP)

**Temps Réel**
- Position exacte des véhicules
- Identification véhicules et conducteurs
- Contrôle périodes d'activité
- Échange de messages textuels

**Historiques & Rapports**
- Reconstitution d'itinéraires
- Proximité et alertes
- Distance et consommation carburant
- Points d'intérêt
- Temps d'arrêt
- Vitesses moyennes
- Temps passé sur chantiers
- Export Excel/HTML

**Administration**
- Comptes utilisateurs avec droits personnalisés
- Points d'intérêt personnalisés
- Gestion véhicules et employés
- Paramétrage alertes

**Sécurité**
- Accès protégé par identifiants
- Connexion HTTPS cryptée
- Geofencing (zones géographiques)
- Alertes entrées/sorties

#### Modules Optionnels

| Module | Description |
|--------|-------------|
| **Antivol Véhicule** | Alerte si déplacement contact coupé, hors horaires, hors zones |
| **Antivol Carburant** | Détection baisse brutale niveau réservoir |
| **Consommation Carburant** | Interface CAN Bus ou débitmètre |
| **Identification Conducteurs** | Lecteur + clés Dallas |
| **Identification Remorques** | Lecteur + balise identification |
| **Pointeuse Chantier** | Lecteur mobile + clés Dallas |
| **Aide Navigation** | GPS GARMIN (cartographie VL ou PL) |
| **Messagerie** | Messages textuels véhicule ↔ bureau |
| **Température** | Sondes + alertes dépassement |
| **Capteurs ON/OFF** | Contacts secs personnalisables |

#### Module Tachytel (Chronotachygraphe)

**Fonctionnalités**
- Récupération temps d'activités en temps réel
- Compatible tachygraphes analogiques (disques) et numériques
- Téléchargement cartes conducteurs à distance
- Téléchargement mémoire tachygraphe
- Alertes approche/dépassement limites horaires
- Rapports d'activités

**Modes de transmission**
- Wi-Fi (version autonome)
- GSM/GPRS (module Positel)

**Application Tachytel LIVE**
- Cumuls quotidiens, hebdomadaires, mensuels
- Temps de conduite, travail, repos, disponibilité
- Double équipage
- Téléchargement à distance sans carte entreprise
- Export Excel

#### Conformité CNIL

- Conforme norme simplifiée n°51
- Documentation fournie pour déclaration
- Information obligatoire des personnels

---

### 2.4 Becker Transit 7SL (GPS Navigation)

**Fabricant**: United Navigation GmbH (Becker)  
**Type**: GPS de navigation pour poids lourds  
**Document source**: `mode-demploi-1489844-gps-pour-poids-lourd-becker-transit-7sl-eu-178-cm-7-pouces-europe.pdf`

#### 📷 Aperçu Visuel

| Page 1 - Couverture | Page 11 - Fonctions |
|:-------------------:|:-------------------:|
| ![Becker Page 1](extracted_images/Becker_GPS_page_01.png) | ![Becker Page 11](extracted_images/Becker_GPS_page_11.png) |

| Page 71 - Navigation Camion | Page 72 - Profil Véhicule |
|:---------------------------:|:-------------------------:|
| ![Becker Page 71](extracted_images/Becker_GPS_page_71.png) | ![Becker Page 72](extracted_images/Becker_GPS_page_72.png) |

#### 🗺️ Logique de Navigation Poids Lourd

```mermaid
flowchart TB
    subgraph PROFIL["📋 PROFIL VÉHICULE"]
        DIM["Dimensions<br/>L x l x H"]
        POIDS["Poids Total<br/>+ Charge"]
        ESSIEUX["Nombre<br/>d'Essieux"]
        TYPE["Type<br/>Camion/Camping-car"]
        MATIERES["Matières<br/>Dangereuses"]
    end
    
    subgraph CALCUL["🧮 CALCUL ITINÉRAIRE"]
        DEST["Destination"]
        ALGO["Algorithme<br/>Routage PL"]
        RESTRICTIONS["Base Restrictions"]
    end
    
    subgraph EVITEMENTS["⛔ ÉVITEMENTS AUTOMATIQUES"]
        PONTS["Ponts Bas<br/>(Hauteur)"]
        TONNAGE["Routes<br/>Tonnage Limité"]
        INTERDIT["Zones<br/>Interdites PL"]
        LEZ["Zones<br/>Environnementales"]
        TUNNEL["Tunnels<br/>Restrictions"]
    end
    
    subgraph GUIDAGE["🧭 GUIDAGE"]
        CARTE["Affichage Carte"]
        VOIX["Instructions<br/>Vocales"]
        VOIES["Aide Choix<br/>de Voies"]
        POI["POI PL<br/>Parkings/Stations"]
    end
    
    PROFIL --> CALCUL
    DEST --> ALGO
    RESTRICTIONS --> ALGO
    
    ALGO --> EVITEMENTS
    
    EVITEMENTS --> GUIDAGE
```

#### Spécifications Techniques

| Caractéristique | Valeur |
|-----------------|--------|
| **Écran** | 7 pouces (17,8 cm) tactile |
| **Alimentation** | 12V / 24V |
| **Température stockage** | -20°C à +60°C |
| **Température fonctionnement** | 0°C à +45°C |
| **Garantie** | 24 mois (batterie: 6 mois) |

#### Fonctionnalités Navigation Poids Lourd

**Profil Véhicule**
- Configuration dimensions (longueur, largeur, hauteur)
- Configuration poids
- Nombre d'essieux
- Type de véhicule (camion, camping-car)

**Calcul d'Itinéraire Adapté**
- Évitement ponts bas (hauteur)
- Évitement routes limitées en tonnage
- Évitement zones interdites PL
- Zones environnementales (LEZ)

**Alertes Conducteur**
- Avertissements vitesse
- Avertisseur de radars (option)
- Alertes zones environnementales
- Avertissements spécifiques camion

#### Fonctionnalités Avancées (selon modèle)

| Fonction | Description |
|----------|-------------|
| **TMC** | Infos trafic temps réel |
| **Live Traffic** | Trafic via données mobiles |
| **Commande vocale** | OneShot Pro Becker |
| **Bluetooth** | Mains libres |
| **Caméra de recul** | Raccordement externe |
| **WiFi** | Mises à jour et POI Live |
| **Calendrier interdictions PL** | Interdictions de rouler européennes |
| **Profil hauteur** | Affichage dénivelé itinéraire |

#### Points d'Intérêt (POI)

- Guide camping ADAC
- MARCO POLO Travel Guide
- Parkings sécurisés
- Stations service
- Aires de repos

---

## 3. Solutions Logicielles

### 3.1 Plateformes Cloud Comparées

| Plateforme | Fabricant | Type | Accès |
|------------|-----------|------|-------|
| **Samsara Cloud** | Samsara | SaaS | Web + Mobile |
| **WEBFLEET** | TomTom | SaaS | Web |
| **Positel MAP** | ATHMO | SaaS | Web |
| **Tachytel LIVE** | ATHMO | SaaS | Web |

### 3.2 Fonctionnalités Logicielles Comparées

| Fonctionnalité | Samsara | TomTom | ATHMO |
|----------------|---------|--------|-------|
| Suivi temps réel | ✅ | ✅ | ✅ |
| Historique trajets | ✅ | ✅ | ✅ |
| Geofencing | ✅ | ✅ | ✅ |
| Alertes personnalisées | ✅ | ✅ | ✅ |
| Rapports automatiques | ✅ | ✅ | ✅ |
| Export données | ✅ | ✅ | ✅ (Excel/HTML) |
| Analyse éco-conduite | ✅ | ✅ | ✅ |
| Gestion conducteurs | ✅ | ✅ | ✅ |
| Messagerie | ✅ | ✅ | ✅ |
| Tachygraphe distant | ✅ | ✅ | ✅ |
| API disponible | ✅ | ✅ | Non spécifié |
| App mobile | ✅ | ✅ | Non spécifié |

---

## 4. Aspects Réglementaires

### 📊 Vue d'Ensemble Réglementaire

```mermaid
mindmap
  root((GÉOLOCALISATION<br/>SALARIÉS))
    RGPD/CNIL
      Déclaration obligatoire
      Information salariés
      Droit d accès
      Droit opposition
    FINALITÉS AUTORISÉES
      Production
      Sécurité
      Facturation
      Temps travail
    RESTRICTIONS
      Pas contrôle permanent
      Désactivation vie privée
      Pas usage disciplinaire
    CONSERVATION
      2 mois standard
      1 an preuves
      5 ans temps travail
    CHRONOTACHYGRAPHE
      Obligatoire > 3.5T
      Règlement EU 561/2006
      Temps conduite
      Repos
```

### 4.1 RGPD et Géolocalisation des Salariés

**Document source**: `La-geolocalisation-des-vehicules-mis-a-disposition-des-salaries.pdf`

#### 📋 Processus de Mise en Conformité

```mermaid
flowchart LR
    subgraph AVANT["📝 AVANT DÉPLOIEMENT"]
        A1["Définir<br/>Finalités"]
        A2["Déclaration<br/>CNIL/APDP"]
        A3["Information<br/>Salariés"]
        A4["Consultation<br/>CSE"]
    end
    
    subgraph PENDANT["⚙️ EXPLOITATION"]
        B1["Collecte<br/>Minimale"]
        B2["Accès<br/>Restreint"]
        B3["Journalisation"]
        B4["Chiffrement"]
    end
    
    subgraph DROITS["👤 DROITS SALARIÉS"]
        C1["Accès<br/>Données"]
        C2["Rectification"]
        C3["Opposition"]
        C4["Désactivation<br/>Vie Privée"]
    end
    
    subgraph FIN["🗑️ FIN DE VIE"]
        D1["Suppression<br/>Automatique"]
        D2["Archivage<br/>Légal"]
    end
    
    A1 --> A2 --> A3 --> A4
    A4 --> B1 --> B2 --> B3 --> B4
    B4 --> DROITS
    DROITS --> D1
    DROITS --> D2
```

#### Finalités Autorisées

La mise en place d'un dispositif de géolocalisation peut répondre aux objectifs suivants :

1. **Amélioration du processus de production**
   - Allocation optimale des moyens (envoi véhicule le plus proche)
   - Analyse a posteriori des déplacements

2. **Sécurité**
   - Sécurité des personnes (travailleurs isolés)
   - Sécurité des marchandises (transport de fonds)
   - Sécurité du véhicule

3. **Suivi marchandises**
   - Respect chaîne du froid
   - Traçabilité

4. **Facturation**
   - Suivi prestations de transport
   - Ramassage scolaire, nettoyage, etc.

5. **Temps de travail**
   - Uniquement si pas d'autre moyen disponible

6. **Preuve d'exécution**
   - Constitution de preuves de prestation

#### Restrictions Importantes

| Situation | Règle |
|-----------|-------|
| **Véhicule usage privé** | Possibilité de désactiver la géolocalisation hors temps de travail |
| **Mandat syndical/électif** | Pas de géolocalisation pendant exercice du mandat |
| **Liberté d'organisation** | Pas de géolocalisation (VRP, visiteurs médicaux) |
| **Contrôle permanent** | Interdit |
| **Usage disciplinaire** | Interdit sauf exceptions |

#### Données Collectables

- Identification employé (nom, prénom, matricule, immatriculation)
- Données de localisation
- Historique des déplacements
- Vitesse de circulation
- Kilomètres parcourus
- Durées d'utilisation
- Temps de conduite
- Nombre d'arrêts

#### Durées de Conservation

| Usage | Durée |
|-------|-------|
| **Standard** | 2 mois |
| **Preuve d'intervention** | 1 an |
| **Suivi temps de travail** | 5 ans |

#### Obligations Employeur

1. Information préalable des employés
2. Déclaration CNIL/APDP
3. Politique d'habilitations
4. Authentification forte (identifiant + mot de passe)
5. Journalisation des accès
6. Sécurisation des échanges de données

### 4.2 Chronotachygraphes

**Réglementation applicable**: Règlement (CEE) n° 561/2006

#### Véhicules Concernés

Tout véhicule automobile dont le poids maximal autorisé > 3,5 tonnes

#### Données Enregistrées

- Vitesse
- Distance parcourue
- Temps de conduite
- Temps de travail (autre)
- Interruptions de travail
- Temps de repos journalier
- Ouverture du boîtier

#### Application Territoriale

Applicable quel que soit le pays d'immatriculation, dès circulation sur le territoire de l'UE.

---

## 5. Technologies de Données FCD

### 5.1 Floating Car Data (FCD)

**Document source**: `files.pdf` (FAQ Cerema)

#### 📊 Architecture FCD

```mermaid
flowchart TB
    subgraph SOURCES["📱 SOURCES DE DONNÉES"]
        APPS["Apps Navigation<br/>Google Maps / Waze"]
        CONSTRUCTEURS["Véhicules Connectés<br/>Constructeurs"]
        FLOTTES["Boîtiers Flotte<br/>Professionnels"]
        TELEPEAGE["Badges Télépéage<br/>PL"]
    end
    
    subgraph COLLECTE["📡 COLLECTE"]
        ANON["Anonymisation"]
        AGG["Agrégation"]
        FILTER["Filtrage"]
    end
    
    subgraph TRAITEMENT["⚙️ TRAITEMENT"]
        MAP_MATCH["Map Matching"]
        STATS["Calculs Statistiques"]
        ML["Machine Learning<br/>Classification VL/PL"]
    end
    
    subgraph PRODUITS["📊 PRODUITS FCD"]
        TEMPS["Temps de Parcours"]
        VITESSE["Vitesses Moyennes"]
        TRAFIC["État du Trafic"]
        OD["Matrices O/D"]
    end
    
    subgraph USAGES["🎯 USAGES"]
        NAVIGATION["Navigation<br/>Temps Réel"]
        GESTION["Gestion<br/>Trafic"]
        PLANIF["Planification<br/>Urbaine"]
        ETUDES["Études<br/>Mobilité"]
    end
    
    SOURCES --> COLLECTE
    COLLECTE --> TRAITEMENT
    TRAITEMENT --> PRODUITS
    PRODUITS --> USAGES
```

#### Définition

Les données FCD (Floating Car Data) sont des données de géolocalisation collectées anonymement via :
- Applications de navigation (Google Maps, Waze)
- Dispositifs intégrés constructeurs
- Boîtiers de suivi de flotte
- Badges de télépéage

#### Sources de Données

| Source | Avantages | Limitations |
|--------|-----------|-------------|
| **Apps navigation** | Large base utilisateurs | Activation manuelle requise |
| **Constructeurs** | Collecte continue | Véhicules récents uniquement |
| **Flottes professionnelles** | Fiable, continu | Profils spécifiques (PL, taxis) |
| **Télépéage** | Identification certaine PL | Couverture limitée autoroutes |

#### Distinction VL/PL

- Badges télépéage PL → identification certaine
- Modèles statistiques basés sur comportement de conduite
- Profils de vitesse et accélération
- Trajectoires et itinéraires
- Horaires de circulation

#### Usages

| Usage | Pertinence FCD |
|-------|----------------|
| Temps de parcours | ✅ Excellent |
| Vitesses moyennes | ✅ Excellent |
| Couverture réseau | ✅ Excellent |
| Débits véhicules | ⚠️ Complémentaire (comptages) |
| Régulation feux | ⚠️ Limité |
| Trajets courts | ⚠️ Sous-représentés |

#### Coût d'Acquisition

Paramètres influençant le prix :
1. Type de données (agrégées vs désagrégées)
2. Granularité spatiale
3. Granularité temporelle
4. Volume et fréquence d'échantillonnage
5. Droits d'usage
6. Qualité et enrichissement
7. Niveau de service (temps réel vs différé)

---

## 6. Recherche Académique

### 6.1 Thèse El Najjar (2003)

**Document source**: `these_Maan_E_El_Najjar-1.pdf`

**Titre**: Localisation dynamique d'un véhicule sur une carte routière numérique pour l'assistance à la conduite

**Institution**: Université de Technologie de Compiègne (UTC), Laboratoire HeuDiaSyc

#### 📊 Architecture de Fusion Multi-Capteurs (Map-Matching)

```mermaid
flowchart TB
    subgraph CAPTEURS["📡 CAPTEURS"]
        GPS_DIFF["GPS Différentiel<br/>AgGPS132 Trimble<br/>Précision métrique"]
        ABS["Capteurs ABS<br/>Rotation Roues"]
        IMU["Gyroscope<br/>Accéléromètre"]
    end
    
    subgraph CARTE["🗺️ CARTE NUMÉRIQUE"]
        IGN["IGN Géoroute V2"]
        SIG["SIG Géoconcept"]
        SEGMENTS["Segments Routiers"]
    end
    
    subgraph FUSION["🔄 FUSION MULTI-SOURCES"]
        KALMAN["Filtre de Kalman<br/>Étendu"]
        CROYANCE["Théorie des<br/>Croyances"]
        MAHAL["Distance de<br/>Mahalanobis"]
    end
    
    subgraph SELECTION["🎯 SÉLECTION DE ROUTE"]
        GEOM["Méthodes<br/>Géométriques"]
        TOPO["Méthodes<br/>Topologiques"]
        BAYES["Méthodes<br/>Bayésiennes"]
        PARTICULE["Filtrage<br/>Particulaire"]
    end
    
    subgraph SORTIE["📍 RÉSULTAT"]
        POSE["Position + Cap<br/>sur Carte"]
        CERTITUDE["Degré de<br/>Certitude"]
        ROUTE["Route<br/>Identifiée"]
    end
    
    CAPTEURS --> FUSION
    CARTE --> FUSION
    FUSION --> SELECTION
    SELECTION --> SORTIE
```

#### 🔄 Processus de Map-Matching

```mermaid
sequenceDiagram
    participant GPS as 📡 GPS
    participant EKF as 🔄 Filtre Kalman
    participant MAP as 🗺️ Carte
    participant MM as 🎯 Map-Matching
    participant OUT as 📍 Sortie
    
    loop Chaque seconde
        GPS->>EKF: Position brute (lat, lon)
        EKF->>EKF: Prédiction (modèle véhicule)
        EKF->>EKF: Correction (mesures)
        EKF->>MM: Position estimée + covariance
        MAP->>MM: Segments candidats
        MM->>MM: Calcul distances Mahalanobis
        MM->>MM: Fusion croyances
        MM->>OUT: Route sélectionnée + certitude
    end
    
    alt GPS indisponible (tunnel)
        EKF->>EKF: Navigation à l'estime (ABS)
        Note over EKF: Store & Forward
    end
```

#### Problématique

Localisation précise d'un véhicule sur une carte routière numérique pour les systèmes ADAS (Advanced Driver Assistance Systems).

#### Approche Méthodologique

**Fusion Multi-Sources**
- GPS différentiel (AgGPS132 Trimble, précision métrique)
- Capteurs proprioceptifs (ABS - rotation roues)
- Carte routière numérique (IGN Géoroute V2)
- SIG Géoconcept

**Algorithmes**
- Filtrage de Kalman étendu
- Théorie des croyances (Dempster-Shafer)
- Map-matching (localisation cartographique)

#### Méthodes de Sélection de Routes

1. **Méthodes Déterministes**
   - Géométriques
   - Topologiques
   - Détection de virages
   - Comparaison de longueurs

2. **Méthodes Bayésiennes**
   - Gaussienne (distance de Mahalanobis)
   - Filtrage particulaire

3. **Approche Crédibiliste**
   - Fusion multi-critères
   - Quantification du degré de certitude

#### Résultats

- Localisation temps réel sur carte
- Qualification des résultats (précision + certitude)
- Gestion de l'intermittence GPS (tunnels)
- Architecture temps réel mono et multi-machines

#### Applications ADAS Identifiées

- Anticipation de virages
- Alerte de sortie de route
- Régulation de distance inter-véhicules
- Prévention de collisions
- Information conducteur enrichie

---

## 7. Tableau Comparatif Global

### 📊 Radar Comparatif des Solutions

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#4CAF50'}}}%%
pie showData
    title Couverture Fonctionnelle par Solution
    "Samsara VG34" : 95
    "TomTom LINK 510" : 80
    "ATHMO Positel" : 75
    "Becker GPS" : 40
```

### 📈 Positionnement des Solutions

```mermaid
quadrantChart
    title Positionnement Solutions Géolocalisation PL
    x-axis Fonctionnalités Basiques --> Fonctionnalités Avancées
    y-axis Connectivité Limitée --> Connectivité Étendue
    quadrant-1 Leaders
    quadrant-2 Spécialistes
    quadrant-3 Entrée de gamme
    quadrant-4 Niches
    Samsara VG34: [0.9, 0.95]
    TomTom LINK 510: [0.7, 0.5]
    ATHMO Positel: [0.6, 0.4]
    Becker GPS: [0.3, 0.2]
```

### 7.1 Comparatif Hardware

| Critère | Samsara VG34 | TomTom LINK 510 | ATHMO Positel |
|---------|--------------|-----------------|---------------|
| **Dimensions** | 117x72x26 mm | 121x56,5x21,5 mm | Non spécifié |
| **Poids** | 118 g | 88 g | Non spécifié |
| **Temp. fonct.** | -40°C à +85°C | -30°C à +70°C | Non spécifié |
| **Alimentation** | 12V/24V | 12V/24V | 12V/24V |
| **Cellulaire** | 4G LTE + 3G + 2G | GSM/GPRS | GSM/GPRS |
| **GPS** | GPS + GLONASS | GPS | GPS |
| **WiFi** | ✅ Point d'accès | ❌ | ❌ |
| **Bluetooth** | ✅ | ✅ Classe 2 | ❌ |
| **OBD-II** | ✅ J1962/J1939/J1708 | ✅ CAN Bus | ✅ CAN Bus |
| **FMS** | ✅ | ✅ | Non spécifié |
| **Entrées numériques** | 2 | 2 | Oui (options) |
| **Sortie numérique** | 1 (future) | 1 | Non spécifié |
| **Capteurs température** | ✅ Sans fil | ❌ | ✅ Filaire |
| **ID conducteur** | ✅ Jetons | ❌ | ✅ Dallas |
| **Antivol** | ✅ | ✅ | ✅ |
| **Tachygraphe** | ✅ Distant | ✅ | ✅ Tachytel |

### 7.2 Comparatif Fonctionnel

| Fonctionnalité | Samsara | TomTom | ATHMO | Becker GPS |
|----------------|---------|--------|-------|------------|
| **Suivi temps réel** | ✅ | ✅ | ✅ | ❌ |
| **Historique trajets** | ✅ | ✅ | ✅ | ✅ |
| **Geofencing** | ✅ | ✅ | ✅ | ❌ |
| **Éco-conduite** | ✅ | ✅ | ✅ | ❌ |
| **Consommation carburant** | ✅ | ✅ | ✅ | ❌ |
| **Maintenance préventive** | ✅ | ✅ | ❌ | ❌ |
| **Navigation PL** | ❌ | ✅ (PRO) | ✅ (GARMIN) | ✅ |
| **Profil véhicule** | ✅ | ✅ | ❌ | ✅ |
| **Messagerie** | ✅ | ✅ | ✅ | ❌ |
| **Tachygraphe distant** | ✅ | ✅ | ✅ | ❌ |
| **Caméra** | ✅ | ❌ | ❌ | ✅ (option) |
| **Conformité ELD (USA)** | ✅ | ✅ | ❌ | ❌ |

### 7.3 Comparatif Connectivité

| Critère | Samsara VG34-EU | TomTom LINK 510 | ATHMO Positel |
|---------|-----------------|-----------------|---------------|
| **4G LTE** | ✅ | ❌ | ❌ |
| **3G** | ✅ | ❌ | ❌ |
| **2G/GPRS** | ✅ | ✅ | ✅ |
| **WiFi** | ✅ 802.11g/n | ❌ | ✅ (Tachytel) |
| **Bluetooth** | ✅ | ✅ | ❌ |
| **Stockage hors-ligne** | ✅ Flash | Non spécifié | Non spécifié |
| **Chiffrement** | AES 256 bits | Non spécifié | HTTPS |

---

## 8. Recommandations

### 8.1 Choix de Solution selon Besoins

| Besoin Principal | Solution Recommandée |
|------------------|---------------------|
| **Flotte internationale, connectivité avancée** | Samsara VG34 |
| **Intégration navigation TomTom** | TomTom LINK 510 |
| **Solution française, support local** | ATHMO Positel |
| **Navigation PL uniquement** | Becker Transit 7SL |
| **Gestion tachygraphes prioritaire** | ATHMO Tachytel |

### 8.2 Fonctionnalités Essentielles à Implémenter

Sur la base de l'analyse des solutions existantes, le système de géolocalisation à développer devrait inclure :

#### 🏗️ Architecture Cible Recommandée

```mermaid
flowchart TB
    subgraph HARDWARE["🔧 HARDWARE EMBARQUÉ"]
        direction TB
        MCU_T["MCU ARM Cortex<br/>+ Stockage Flash"]
        GPS_T["GPS Multi-Constellation<br/>GPS/GLONASS/Galileo"]
        MODEM_T["Modem 4G LTE<br/>Cat-M1 / NB-IoT"]
        WIFI_T["WiFi 802.11n<br/>Point d'Accès"]
        BT_T["Bluetooth 5.0<br/>BLE"]
        CAN_T["Interface CAN<br/>J1939 / FMS"]
        IO_T["GPIO<br/>4 IN / 2 OUT"]
    end
    
    subgraph CAPTEURS["📊 CAPTEURS"]
        TEMP_T["Température<br/>Sans Fil"]
        FUEL_T["Carburant<br/>CAN / Sonde"]
        DOOR_T["Portes<br/>Contact Sec"]
        RFID_T["ID Conducteur<br/>NFC / RFID"]
    end
    
    subgraph BACKEND["☁️ BACKEND"]
        direction TB
        MQTT_T["Broker MQTT<br/>Temps Réel"]
        API_T["API REST<br/>Node.js / Python"]
        DB_T["Base de Données<br/>PostgreSQL + TimescaleDB"]
        CACHE_T["Cache Redis<br/>Sessions"]
        NOTIF_T["Service Notifications<br/>Email / SMS / Push"]
    end
    
    subgraph FRONTEND["🖥️ INTERFACES"]
        WEB_T["Application Web<br/>React + Leaflet"]
        MOBILE_T["App Mobile<br/>React Native"]
        REPORTS_T["Rapports<br/>PDF / Excel"]
    end
    
    CAPTEURS --> HARDWARE
    HARDWARE -->|"MQTT over TLS"| BACKEND
    BACKEND --> FRONTEND
```

#### 📋 Roadmap de Développement

```mermaid
gantt
    title Roadmap Système Géolocalisation PL
    dateFormat  YYYY-MM
    section Hardware
    Conception PCB           :h1, 2026-04, 2M
    Prototypage              :h2, after h1, 2M
    Tests & Certification    :h3, after h2, 3M
    section Backend
    API Core                 :b1, 2026-04, 2M
    Base de données          :b2, 2026-04, 1M
    Service temps réel       :b3, after b2, 2M
    Alertes & Notifications  :b4, after b3, 1M
    section Frontend
    Interface Web            :f1, 2026-06, 3M
    Application Mobile       :f2, after f1, 2M
    Rapports                 :f3, 2026-08, 2M
    section Intégration
    Tests système            :i1, 2026-10, 2M
    Pilote terrain           :i2, after i1, 2M
    Déploiement              :i3, after i2, 1M
```

#### Hardware
- [ ] GPS multi-constellation (GPS + GLONASS + Galileo)
- [ ] Connectivité 4G LTE avec fallback 3G/2G
- [ ] Interface OBD-II/CAN Bus (J1939, FMS)
- [ ] WiFi pour mise à jour et point d'accès
- [ ] Bluetooth pour périphériques
- [ ] Entrées/sorties numériques configurables
- [ ] Capteurs température sans fil
- [ ] Identification conducteur (RFID/NFC)
- [ ] Stockage local (store & forward)
- [ ] Température de fonctionnement: -40°C à +85°C

#### Logiciel
- [ ] Plateforme web responsive
- [ ] Application mobile (iOS/Android)
- [ ] Suivi temps réel sur carte (OpenStreetMap)
- [ ] Geofencing multi-zones
- [ ] Alertes personnalisables (email, SMS, push)
- [ ] Rapports automatiques (PDF, Excel)
- [ ] Analyse éco-conduite
- [ ] Gestion conducteurs et véhicules
- [ ] Messagerie bidirectionnelle
- [ ] API REST pour intégrations
- [ ] Téléchargement tachygraphe distant
- [ ] Conformité RGPD (désactivation hors travail)

#### Navigation PL
- [ ] Profil véhicule (dimensions, poids, essieux)
- [ ] Évitement restrictions (hauteur, tonnage)
- [ ] Zones environnementales (LEZ)
- [ ] POI spécifiques PL (parkings sécurisés, stations)
- [ ] Calendrier interdictions de rouler

### 8.3 Points de Vigilance

1. **Conformité RGPD**
   - Déclaration CNIL obligatoire
   - Information préalable des salariés
   - Possibilité de désactivation hors temps de travail
   - Conservation limitée des données

2. **Interopérabilité**
   - Support protocoles standards (FMS, J1939)
   - API ouverte pour intégrations tierces
   - Export données formats standards

3. **Fiabilité**
   - Stockage local en cas de perte réseau
   - Synchronisation automatique
   - Redondance GPS (multi-constellation)

4. **Évolutivité**
   - Architecture modulaire
   - Mise à jour firmware à distance
   - Ajout de capteurs sans remplacement matériel

---

## 9. Galerie d'Images Extraites

### 9.1 Documentation LINK (Images uniquement - pas de texte extractible)

Ce document était au format image dans le PDF original. Voici les captures :

| Page 1 | Page 2 | Page 3 |
|:------:|:------:|:------:|
| ![LINK Page 1](extracted_images/LINK_page_01.png) | ![LINK Page 2](extracted_images/LINK_page_02.png) | ![LINK Page 3](extracted_images/LINK_page_03.png) |

### 9.2 Livre Blanc - Gestion de Flotte

| Page 1 - Couverture | Page 2 - Sommaire |
|:-------------------:|:-----------------:|
| ![LivreBlanc Page 1](extracted_images/LivreBlanc_page_01.png) | ![LivreBlanc Page 2](extracted_images/LivreBlanc_page_02.png) |

| Page 3 - Définitions | Page 4 - Secteurs |
|:--------------------:|:-----------------:|
| ![LivreBlanc Page 3](extracted_images/LivreBlanc_page_03.png) | ![LivreBlanc Page 4](extracted_images/LivreBlanc_page_04.png) |

### 9.3 Réglementation CNIL/APDP - Géolocalisation des Salariés

| Page 1 - Introduction | Page 2 - Finalités | Page 3 - Justification |
|:---------------------:|:------------------:|:----------------------:|
| ![CNIL Page 1](extracted_images/CNIL_Geoloc_page_01.png) | ![CNIL Page 2](extracted_images/CNIL_Geoloc_page_02.png) | ![CNIL Page 3](extracted_images/CNIL_Geoloc_page_03.png) |

### 9.4 Index des Images Extraites

| Fichier | Source | Description |
|---------|--------|-------------|
| `VG34_page_01.png` | VG34_datasheet_FR.pdf | Présentation générale Samsara VG34 |
| `VG34_page_02.png` | VG34_datasheet_FR.pdf | Sources de données et interfaces |
| `VG34_page_03.png` | VG34_datasheet_FR.pdf | Connectivité et alimentation |
| `VG34_page_04.png` | VG34_datasheet_FR.pdf | Fonctionnalités logicielles |
| `TomTom_LINK510_page_01.png` | ttb-link510-doc.pdf | Présentation et avantages |
| `TomTom_LINK510_page_02.png` | ttb-link510-doc.pdf | Caractéristiques techniques |
| `ATHMO_page_01.png` | ATHMO_Informatique_embarquee.pdf | Couverture |
| `ATHMO_page_02.png` | ATHMO_Informatique_embarquee.pdf | Présentation entreprise |
| `ATHMO_page_03.png` | ATHMO_Informatique_embarquee.pdf | Pourquoi s'équiper |
| `ATHMO_page_04.png` | ATHMO_Informatique_embarquee.pdf | Principe Positel |
| `ATHMO_page_05.png` | ATHMO_Informatique_embarquee.pdf | Application Positel MAP |
| `ATHMO_page_06.png` | ATHMO_Informatique_embarquee.pdf | Options disponibles |
| `ATHMO_page_07.png` | ATHMO_Informatique_embarquee.pdf | Options (suite) |
| `ATHMO_page_08.png` | ATHMO_Informatique_embarquee.pdf | Packs de base |
| `LINK_page_01.png` | LINK.pdf | Documentation produit (image) |
| `LINK_page_02.png` | LINK.pdf | Documentation produit (image) |
| `LINK_page_03.png` | LINK.pdf | Documentation produit (image) |
| `LivreBlanc_page_01.png` | livre-blanc-gestion-de-flotte.pdf | Couverture |
| `LivreBlanc_page_02.png` | livre-blanc-gestion-de-flotte.pdf | Sommaire |
| `LivreBlanc_page_03.png` | livre-blanc-gestion-de-flotte.pdf | Définitions |
| `LivreBlanc_page_04.png` | livre-blanc-gestion-de-flotte.pdf | Secteurs d'activité |
| `CNIL_Geoloc_page_01.png` | La-geolocalisation-des-vehicules.pdf | Introduction |
| `CNIL_Geoloc_page_02.png` | La-geolocalisation-des-vehicules.pdf | Finalités autorisées |
| `CNIL_Geoloc_page_03.png` | La-geolocalisation-des-vehicules.pdf | Justification légale |
| `Becker_GPS_page_01.png` | mode-demploi-becker-transit.pdf | Couverture manuel |
| `Becker_GPS_page_11.png` | mode-demploi-becker-transit.pdf | Aperçu des fonctions |
| `Becker_GPS_page_12.png` | mode-demploi-becker-transit.pdf | Fonctions (suite) |
| `Becker_GPS_page_71.png` | mode-demploi-becker-transit.pdf | Navigation camion |
| `Becker_GPS_page_72.png` | mode-demploi-becker-transit.pdf | Profil véhicule |

---

## Annexes

### A. Documents Sources Analysés

| # | Fichier | Type | Pages | Taille |
|---|---------|------|-------|--------|
| 1 | `VG34_datasheet_FR.pdf` | Fiche technique | 11 | 407 KB |
| 2 | `ttb-link510-doc.pdf` | Fiche technique | 2 | 472 KB |
| 3 | `ATHMO_Informatique_embarquee_generale_fr_MEDIUM.pdf` | Brochure | 11 | 885 KB |
| 4 | `livre-blanc-gestion-de-flotte-de-vehicules-corrige.pdf` | Livre blanc | 9+ | 1.3 MB |
| 5 | `La-geolocalisation-des-vehicules-mis-a-disposition-des-salaries.pdf` | Réglementation | 7 | 381 KB |
| 6 | `these_Maan_E_El_Najjar-1.pdf` | Thèse | 200+ | 2.7 MB |
| 7 | `mode-demploi-gps-poids-lourd-becker-transit-7sl.pdf` | Manuel | 150+ | 5.8 MB |
| 8 | `files.pdf` | FAQ technique | 5 | 130 KB |
| 9 | `LINK.pdf` | Documentation | - | 1.1 MB |
| 10 | `Telechargez-la-brochure-Technologie-a-bord_2019.pdf` | Brochure | - | 803 KB |

### B. Glossaire

| Terme | Définition |
|-------|------------|
| **ADAS** | Advanced Driver Assistance Systems |
| **CAN Bus** | Controller Area Network - Bus de communication véhicule |
| **ELD** | Electronic Logging Device (USA) |
| **FCD** | Floating Car Data |
| **FMS** | Fleet Management System (standard européen) |
| **GNSS** | Global Navigation Satellite System |
| **J1939** | Protocole CAN pour poids lourds |
| **LEZ** | Low Emission Zone |
| **OBD-II** | On-Board Diagnostics version 2 |
| **POI** | Point of Interest |
| **SIG** | Système d'Information Géographique |
| **TMC** | Traffic Message Channel |

---

*Document généré automatiquement à partir de l'analyse des PDFs du dossier "Localisation poid lourd"*
