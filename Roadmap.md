# Roadmap for Treetracker Project (Reviewed APR 2023)

Technology that enables payments for the creation of environmental impact.

Also, see https://greenstand.gitbook.io/engineering/#welcome

See the latest [Road Map](https://www.figma.com/file/n3pRXTcU7znsCiqZciewZE/Roadmap-2023?node-id=0-1)

## Immediate Development Targets (Core Functionality)

### Android Tree Tracker

+ Deploy data pipeline into production (Complete)
+ Integrate messages/feedback API for planter feedback (Complete)
+ GPS coordinate accuracy enhancement (ongoing)
+ Continue iterative improvements to UI/UX (ongoing)
+ Reduced tracking time per tree (ongoing)
+ Refine build automation/dev ops
+ Unit tests 
+ Run UI tests on our CI system

### Android Greenstand Token Trading App
+ Credial creation
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

### Token Trading API
 
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

### Operational Challenges to Overcome 
+ Quality control
+ Identifying optimal phones/hardware
+ Automated creation and verification of planter accounts
+ Project configuration / organization whitelabel
+ Payout management for planters / collectors

### Greenstand Block Chain Network
+ Beta release of modified Etheium Sidechain
