# Roadmap for Treetracker Project (Reviewed March 2020)

This project coordinates tree planting employment for people living in extreme poverty.

See https://greenstand.gitbook.io/engineering/#welcome

## Immediate Development Targets (Core Functionality)

### Android Tree Tracker

+ Deploy data pipeline into production (Complete)
+ Integrate messages/feedback API for planter feedback (Complete)
+ GPS coordinate accuracy enhancement
+ Continue iterative improvements to UI/UX
+ Refine build automation / dev ops
+ Unit tests 
+ Run UI tests on our CI system
+ Continued work to reduce tracking time

### Android Greenstand Token Trading App
+ Credial creation
+ Basic send feature to exisisting walllet
+ Send/Gift to non exisiting wallet


### iOS Greenstand Token Trading App 
+ Credial creation
+ Basic send feature to exisisting walllet
+ Send/Gift to non exisiting wallet

### iOS Tree Tracker
+ Add Notes Feature
+ Add token sending feature

### Web Map

+ Sharing, Bill of value (TRings), and UI/UX enhancements to web map wallet view
+ Impact panels for planters and organizations
+ Integrate Wallet 
+ 
### Token Trading API
 
+ Implement generic trading between wallets (Complete)
+ Streamline process for wallet creation (Complete)
+ Automate credential creation and delivery

### General API Needs

+ Complete Domain Migraiton
+ Improve unit & integration test coverage
+ Automated testing during our deployment pipeline
+ Continue MVC factoring of R&D codes

### Cloud

+ Monitoring and alerting, log analysis
+ Develop and improve ansible scripting for deployment automation
+ Improve blue/green deployment process
+ Manage and migration of dev & test infrastructures
+ Cdn optimization in the prod environment
+ Keycloak
+ Solr

### Data Analysis

+ R&D for tree data point matching feature (Capture matching feature)
+ R&D for improving GPS accuracy using kalman filtering and planter movement scripting
+ Analysis of planter activity patterns
+ Automated duplicate screening
+ Cloud image analysis to sort images based on tags (grown, hole, etc..)
+ Machine learning species verification (80% Accuracy)
+ Modeling ecological value of planted trees

### Admin Panel
+ Planter quality control and management, activity metrics
+ Duplicate identification
+ Planter image management
+ additional filters
+ advanced species management (merge)
+ Integrate Wallet tools

### Technical Operations
+ Quality control
+ Identifying optimal phones/hardware
+ Create planter accounts
+ Assign planters to projects / organizations
+ Project configuration / organization whitelabel
+ Payout management for planters / collectors
