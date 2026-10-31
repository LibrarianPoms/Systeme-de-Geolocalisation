# Gisgraphy - Open Source Geocoder

Source: https://github.com/gisgraphy/gisgraphy

**Free, open source, and ready to use geocoder, reverse geocoder and geolocalisation webservices**

---

## Présentation

Depuis 2006, Gisgraphy est un framework gratuit et open source qui offre la possibilité de faire de la géolocalisation et du géocodage via des APIs Java ou des webservices REST.

### Caractéristiques principales :
- **100+ millions d'entrées** (OpenStreetMap, Openaddresses, Geonames, Quattroshapes)
- **Production ready** : scalable, performant, load balanced
- **Multi-format** : XML, JSON, PHP, Python, Ruby, YAML, GeoRSS, Atom
- **243 pays** supportés avec pagination
- **Intégration OpenGTS/Traccar** : client Gisgraphy inclus

---

## Webservices Disponibles

### 1. Geocoding
Fournir une adresse (structurée ou non) et obtenir sa position GPS.
- Couverture mondiale
- +410 millions d'adresses avec numéros de rue

### 2. Reverse Geocoding
Fournir une position GPS et obtenir l'adresse correspondante.
- Couverture mondiale
- +410 millions d'adresses

### 3. Street Search
Trouver des rues pour un point GPS donné (et un nom optionnel).
- Limite de vitesse, nombre de voies, péage, type de surface, azimut
- Pour logiciels de tracking GPS (OpenGTS, Traccar)

### 4. Nearby
Trouver des lieux, POIs, villes, rues autour d'un point GPS pour un rayon donné.
- 230+ types de POIs (restaurant, station, ATM, PostOffice, Doctor, Parking...)
- Résultats triés par distance

### 5. Fulltext Search / Autocompletion
Pour un texte donné et un point GPS optionnel, trouver des lieux, POIs, villes, rues, codes postaux.
- Autocomplétion (as you type)
- Location bias, fuzzy, spell checking
- Filtrage par type de lieu

### 6. Address Parser
Diviser une adresse en composants individuels :
- Numéro de rue, type de rue, nom de rue
- Unité (apt, building), code postal, état, pays, ville
- Support de 60+ pays

---

## Base de Données

Base de données unique et mondiale :
- **500+ millions d'entrées**
- Adresses, POIs, rues, villes, divisions administratives
- Format CSV ou SQL
- Sources : OpenStreetMap, Openaddresses, Geonames, Quattroshapes

---

## Intégrations

### Gisgraphoid (Android)
Bibliothèque pour faire du géocodage sur mobile/tablette Android.
- Même API Geocoder que Google
- Fonctionne sur toutes les versions Android
- Gratuit, pas de clé API, pas de limite
- Affichage sur OpenStreetMap ou Google Maps

### Leaflet Plugins
- **Geocoding** : Input avec autocomplétion sur carte Leaflet
- **Reverse Geocoding** : Clic droit sur la carte pour obtenir l'adresse

---

## Installation

- **Docker** : Images Docker disponibles
- **Scripts d'installation** : Pour serveur local
- Documentation : http://www.gisgraphy.com/documentation/installation/index.php

---

## Démo

- Démo sur carte (Leaflet) : http://services.gisgraphy.com
- Webservices : http://services.gisgraphy.com/public/geocoding.html

---

## Caractéristiques Techniques

- REST WebServices
- Recherche fulltext basée sur Lucene/Solr
- Interface admin avec statistiques
- Services répliqués / scalables / haute performance / cachés
- Support des alphabets cyrillique, arabe, chinois...
- Widgets Dojo / Prototype / Ajax
- Module OpenSearch
- Drapeaux de tous les pays en SVG et PNG

---

## Licence

- **LGPL v3** (open source)
- Données : voir attributions sur https://www.gisgraphy.com/attributions.html

---

## Liens

- **Site web** : https://www.gisgraphy.com
- **GitHub** : https://github.com/gisgraphy/gisgraphy
- **Documentation** : https://www.gisgraphy.com/documentation/quick-start.php
- **Accès gratuit** : https://www.gisgraphy.com/free-access.php
