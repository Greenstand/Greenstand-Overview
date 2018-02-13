# Roadmap for TreeTracker Project

This project coordinates tree planting employment for people living in extreme poverty.

See [Contributing](https://github.com/Greenstand/Development-Overview/blob/master/Contributing.md) 

## Immediate Development Targets (Core Functionality)

### Android
~~+ Integrate with API~~

~~+ Fix GPS Location Tracking~~

~~+ Upload images to cloud object storage and integrate URLS with API (**Underway**)~~

~~+ UI Fixes and Updates~~

~~+ Repackage with new key~~

+ Implement RPC for stream upload/downloading trees

~~+ Remove remind to sync ~~

### Web
+ Design and Implement an Awesome web map background 

~~+ Switch to JSONP endpoints~~ CANCELLED

+ Design location markers, etc

+ ~~Tweak for embedding in other platforms ~~

+ Stylize dialog

### API
~~+ Clean or Rewrite the Api (**Underway**)~~

+ Access control on the API  (**Underway**)
+ ~~First work on new web map API in node.js ->~~ JEM
+ Authentication for new android API in node.js
+ ~~Implement clustering inside postGIS~~ Anuja
+ ~~Create development infrastructure~~ Zaven

+ Create tree endpoints filtered by location or user

~~+ JSONP endpoints for Map~~

### Cloud
+ Scalable Infrastructure / Load Balancing

+ Backups

+ ~~SSL (https)~~ Jon

+ SSL (https) Dev Server

### Dev Ops
+ Deployments

+ Automated unit testing

## Targets for February 2018 (Deployable System)

### Admin Panel
+ List and filter plants by time and planter
+ Remove tree records from list

### Embed maps in external websites
+ Filter by project / organizations
+ Filter by region
+ Filter by date

### Donor Panel 
+ Map
+ Click on trees and see something
+ A charts page

## Long Term Feature Targets  (Full System)

### Admin Panel
#### Project management
+ Create planter accounts
+ Assign planters to projects / organizations
+ Project configuration / organization whitelabel
+ Payout management for planters / collectors
#### Planting planning
+ Notify planters to check on particular trees
+ Species mixture and layout
+ Collection of forest products
+ Coordination of collection
+ Coordination of pickup

#### Tree Updates
+ Data quality / linking tree updates to correct tree using GPS

### Android
+ Money earned counter for the planter
+ Whitelabel deployments

### Link to mobile money

### Link donations to individual trees or groups of trees

### Advanced GIS features and Data Analysis

### Species recognition

