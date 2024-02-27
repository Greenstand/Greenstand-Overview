# Roadmap for Treetracker Project (Reviewed APR 2023)

Technology that enables payments for the creation of environmental impact.
Contributrors may also review the following:
- [Engineering Handbook](https://greenstand.gitbook.io/engineering/#welcome)
- [Visual Road Map](https://www.figma.com/file/n3pRXTcU7znsCiqZciewZE/Roadmap-2023?node-id=0-1)
- [The Project Boards](https://github.com/orgs/Greenstand/projects?query=is%3Aopen)

## Immediate Development Targets (Core Functionality)

### Android Tree Tracker
+ UX/UI - Standardize icons (14)
+ Clear Current Bug Reports (15)
+ Deeplinks (16)
 - Organization send link for custom app to users (17)
 - Custom Setup for deeplinks (18)
 - Introduce config file adjustments based on phone performance / Org needs (46)
+ Ux/UI - New Token Field Transfer Page (19)
+ Create Wireframes for new landing page (20)
+ Privacy options (21)
+ Delete Options (22)
+ Users can send and receive messages (25)
+ Feedback for planter feedback at tree level (26)
+ Refine build automation/dev ops (27)
+ Run UI tests on our CI system (28)
+ Unit tests (29)
+ Tracking time to below 2 seconds (31)
+ GPS coordinate accuracy enhancement (ongoing) (33)
+ Adjust and Optimize Convergence time out (44)
+ Reduce Decimal point to tangible number (47)
+ Adjust and optimize Image Sizes (43)
+ Adjust and Optimize processing times for saving / Displaying images (43)
+ Adjust and Optimize UX flows and reduce number of clicks) (45)
+ Integrate Token trading App (34)
+ Planters Can Transfer Tokens to another Wallet/ USER account (36)
      
### Android Greenstand Token Trading App
+ Credential creation / Key Cloak Integration
+ Basic send feature to an existing wallet
+ Send/Gift to a non-existing wallet

### iOS Greenstand Token Trading App
+ Credial creation
+ Basic send feature to an existing wallet
+ Send/Gift to a non-existing wallet

### iOS Tree Tracker
[Project Board](https://github.com/orgs/Greenstand/projects/33)
+ Add Notes Feature
+ Add token field-transfer-request/send feature

### Web Map

+ Sharing, Bill of value (TRings), and UI/UX enhancements to web map wallet view
+ Impact panels for planters and organizations
+ Integrate Wallet 


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
+ Solr

### Data Analysis 

+ R&D for tree data point matching feature (Capture matching feature)
+ R&D for improving GPS accuracy using kalman filtering and planter movement scripting
+ Analysis of planter activity patterns
+ Automated duplicate screening
+ Cloud image analysis to sort images based on tags (grown, hole, etc..)
+ Machine learning species verification (80% Accuracy)
+ Modeling the ecological value of planted trees

### Admin Panel

+ Planter quality control and management, activity metrics
+ [Capture Matching Full deployment](https://github.com/orgs/Greenstand/projects/35)
+ Duplicate identification
+ Planter image management
+ Additional filters
+ [Advanced species management (merge)](https://github.com/orgs/Greenstand/projects/64)
+ Integrate Wallet tools
+ [Messages pages for administrators](https://github.com/Greenstand/treetracker-admin-client/issues/503)

### Admin Wallet Client 
+ Beta Release

### Greenstand Block Chain Network
+ Beta release of modified Etheium Sidechain

### Operational 
+ Quality control
+ Identifying optimal phones/hardware
+ Automated creation and verification of planter accounts
+ Project configuration / organization whitelabel
+ Payout management for planters / collectors

Greenstand Block Chain Network
+ Beta release of modified Etheium Sidechain
