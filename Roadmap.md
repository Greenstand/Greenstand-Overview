# Roadmap for Treetracker Project
Technology that enables payments for the creation of environmental impact.
Contributors may also review the following:
- [Engineering Handbook](https://greenstand.gitbook.io/engineering/#welcome)
- [Visual Road Map](https://www.figma.com/file/n3pRXTcU7znsCiqZciewZE/Roadmap-2023?node-id=0-1)
- [The Project Boards](https://github.com/orgs/Greenstand/projects?query=is%3Aopen)

## Development Targets (Core Functionality)

See individual project boards and communicate with Project Managers for priorities and ticket status.

## Privacy Enhancements
  + Advance all data privacy issues
  + Deletes option (app)
  + Privacy option (app)
  + Audit all public API access for exposeing PII
  + Review, evaluate, and upgrad polices concerning access to any PII
  + Audit and document all user info exposed via integration API's
  + Implement an ossification option for PUU and Geo Location
  + Review and implement privacy protocol for token minting

### Android Tree Tracker
See Android Documentation and [Project board](https://github.com/orgs/Greenstand/projects/109)

### Android Greenstand Token Trading App
+ Credential creation / Key Cloak Integration
+ Basic send feature to an existing wallet
+ Send/Gift to a non-existing wallet

### iOS Greenstand Token Trading App
+ Login via Keycloak
+ Credential creation
+ Basic send feature to an existing wallet
+ Send/Gift to a non-existing wallet

### iOS Tree Tracker
[Project Board](https://github.com/orgs/Greenstand/projects/33)
+ Add Notes Feature
+ Add token field-transfer-request/send feature
+ Deep Link
+ Integrate Token Trading

### Web Map

+ Sharing, Bill of value (TRings), and UI/UX enhancements to web map wallet view
+ Impact panels for planters and organizations
+ Integrate Wallet 
+ Time Line Feature
+ Map loading Speed. To any tree in 2 seconds
+ Map 2.0
+ Add Geo-spatial Data layers such as  https://ctrees.org/
+ Flag /Like Feature
+ Supports Tree Capture
  - View trees on Map
  - View captures on map
  - Trees can jump to all captures
+ Customizable Map
  - Organization can custom map
  - Theme
  - Color
  -  Logo
  - Font
+ Close old webmap services
    - SEO analysis and optimization
    - Search features - (org, name, species, country, city)
    - Web Map performance up - for org map, tree point, wallet map, and timeline
    - Like Button
 
  +  Connect to Webmap wallet UI
  +  Connect to wallet ApI
    + GEO Linking
      
### Greenstand Token Trading API
 
+ Implement generic trading between wallets (Complete)
+ Streamline the process for wallet creation (Complete)
+ Automate credential creation and delivery

### General API Needs

+ Complete Domain Migraiton
+ Improve unit & integration test coverage
+ Automated testing during our deployment pipeline
+ Continue MVC factoring of R&D codes

### Cloud

+ Monitoring and alerting, log analysis
+ Develop and improve ansible scripting for deployment automation
+ Improve the blue/green deployment process
+ Manage and migration of dev & test infrastructures
+ Cdn optimization in the prod environment
+ Keycloak- integrate into all microservices 
+ Solr Implementation
+ Load Testing on services
+ Performance Reporting, (limitations, consumption and tuning performance)
+ Isolate core Services
+ Migrate requests from partners to dedicated DB + API environment
  
### Data Analysis 

+ Introduce Data Analytics tool dashboard
+  Auto Species ID
+  Auto Capture Matching
+ Adress High Resolution image issue
+ R&D for tree data point matching algorything (Capture matching feature)
+ R&D for improving GPS accuracy using kalman filtering and planter movement scripting
+ Analysis of planter activity patterns
+ Automated duplicate screening
+ Cloud image analysis to sort images based on tags (grown, hole, etc..)
+ Machine learning species verification (80% Accuracy)
+ Modeling the ecological value of planted trees

## Capture Matching Tool
+ Capture Matching advancement 80% accuracy with machine learning
+ Capture Matching to a "Usable place"
+ Capture Matching Tool being able to generate a new tree for all organizations (MILESTONE)
  
 ## Track File Tool 
+  Track Tool
+  GIS tracking and boundary layer tools
 
## Database Denormalization Project
 + Implement tagging structure (like the Habarium)

## Dev OPs
+ Upgrade Release Channel
+ Upgrade development workflow
+ Dedicated env for different features / Versions of API's for clients and testers
+ Easier way to maintain different /legacy versions
+ Integrate ML Species tagging
    
## Admin Panel
+ Self sign in sign up
+ Sign in via the app notification for on the ground trackers
+ Payment Verification Function

+ Automate access control
+ Button to Admin Panel to Wallet Tool
+ Planter quality control and management, activity metrics
+ [Capture Matching Full deployment](https://github.com/orgs/Greenstand/projects/35)
+ Duplicate identification
+ Planter image management
+ Additional filters
+ [Advanced species management (merge)](https://github.com/orgs/Greenstand/projects/64)
+ Integrate Wallet tools
+ [Messages pages for administrators](https://github.com/Greenstand/treetracker-admin-client/issues/503)
## Key Cloak Projet
+ Authentication system
+ Self Server Key Cloak Project
+ Integrate Keycloak into all Microservices
+ Auth System
+ Key cloak Users system and Authentication to all Microservices

## Wallet Admin Client

**Individual Signup and Wallet Creation**

* **Send a token via a link:** A wallet can send tokens (one or many) through a link. Unregistered users can claim the tokens by creating a new account or adding them to an existing one.

**Acceptance Criteria:**

* A token or set of tokens can be sent via a web link.
* Users with access to the link can claim the token.
* Release: Version 1.2

**Token Tax System**

* Implement a tax on all minted and traded tokens.

**Buy Token Function**

* Allow users to purchase tokens.

**Sell Token Function**

* Allow users to sell tokens.

**Freeze Function**

(Functionality details not provided)

**MVP 1.2 (Requires Keycloak Integration)**

This MVP introduces the following functionalities:

**1. Create a New Managed Wallet by Unregistered User**

Unregistered users can create a sub-account under a managed wallet by following these steps:

1. Accessing the wallet link.
2. Selecting "create new account."
3. Entering email, password, and wallet handle name.

**Acceptance Criteria:**

* User can create a new account.
* User can create a "non-trust relationship" send request to any other wallet.
* Release: Version 1.2

**2. Send a token via a link**

(Functionality and acceptance criteria are duplicated from "Individual Signup and Wallet Creation")

**Wallet Management**

* **Users' Wallet Management and Profiles:**
    * Internet users can create their own managed wallets.
    * Users can manage their wallet profiles and display them on a map.
+  **New Token Assignment Approach:**
    * Users can:
        * Register via social media platforms (e.g., Facebook).
        * Have Greenstand create a wallet for them.
        * Receive tokens assigned through the Wallet API.
* **Wallet Binding Operation**
+ (Functionality details not provided)
## Data Pipeline
+ Data pipeline Stabilization and Optimization

## RVI Tool
+ RVI tool - individual's ability to apply an RVI to any capture in their wallet by using tags related to the trees or pending transfer
+ Release Basic RVI tool: ability to have a preset formula for tree value = Name of RVI, Tags considered, value or function per tag (example Tring = zero if   Token has no valid tags, if token is valid tags = 1 * (is indigious =5) * is linked to other token
+ Design Fungible Coin

 ##   Domain Migration
 + Stop All Legacy Domain services/tables
 + Api and Tile Server, Migration to new domain
 + Migrate Admin Panel to new domain
 
 ## Payment for SAAS
+ Membership account link for autopayments based on number of tokens transferred
+ Autopayments to the use of Tools such as (Capture matching, RVI, Token Minting, messaging, Herbarium access, Data processing fees)
+ Giving our Clients/organizations/ different services based on level of payments
## Greenstand Blockchain Network
+ Beta release of modified Etheium Sidechain
+ * 7 Nodes operating
+ **Mint Token on Blockchain**
+ **First Trade from Third-Party App via Blockchain:**
* Define what can be minted as a token.
**Release 3 Primary Blockchain Nodes**
**Release RVI Protocols**
**Bridge to Ethereum Blockchain**
  * Ethereum mainnet bridge established.

 ##

### Operational 
+ Quality control
+ Identifying optimal phones/hardware
+ Automated creation and verification of planter accounts
+ Project configuration / organization whitelabel
+ Payout management for planters / collectors
+ Rewards System (trading tokens for Swag - Wallet admin dependent)

## Documentation 
+ Clean up All Readme's
+ Wallet API published Public
+ Review Audit of open links
+ Android Documentation
+ Document Image Size History and Strategies
+ Contributor Porthole - Operational Info for Contributors
+ Link all documentation from Greenstand.org
+ Auto updates to documentation for Yaml files etc..
+ Define Private and Public Docs Task New Normal
+ Web map api (published)
+ Earnings API (Private)
+ Document all main project tools we use
+ Defining public and private docs..
+ Define Gitbook versus Github uses.
+ Considering implementing Stoplight Studio Stoplight.io
+ Refine documentation on the documentation process.
+ Removal of legacy API's don't need specs.
+ Figure out how to turning a YAML into a readable file on the web
+ Keep current links to api documentation, and keep links to old documentation (production version versus test)
+ Wallet Integration API - published with access control
+ Web map API published
+ Access controlled document portal HTML documents
+ Establish sharing protocol and systems for Private Docs (gitbook versus website?)
+ Version control for Documentation_ only the live API's should be on our website, others shall be back side documents- Query only data api (when in doubt lock it up.)


# Miles Stones: 
+ Completion of all Self Service functions required for Growers and Brokers to sell and transfer tokens from mobile app to marketplace integrations
+ Automating integration for token sales and services for mass purchasing of tokens
+ Automating validation and tagging of tokens.
+ Grower Proof of payment module - a required module to enable the creation and generation of tokens off line
+ Automated workflows for direct payments via Mobile Money in 10 African Countries
+ Release To Production - Deployment of Greenstand Impact Token Blockchain Network
