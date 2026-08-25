
# Greenstand System Overview & Master Glossary

<details>
<summary><strong>Overview & Framework Abstract</strong></summary>

<br>

### Overview
Users take photos and “capture” the state of trees, or other environmental indicators, using a mobile app. These captures are sent from mobile phones to the cloud where they are linked to tokens in wallets. Tokens are exchanged or transferred via the wallet system. Token owners tag attributes that either add or subtract the validity of claims for environmental and social impact and ownership of that impact. 

The relative value of a token is calculated and weighted against other tokens using its tagged attributes. 

The token life cycle ends when it is either deleted by a user, permanently claimed for its impact, or minted into an immutable token. These tokens by nature are non-fungible; however, using relative value claims, they may be converted into fungible tokens.

### Framework Abstract
This framework finances environmental restoration efforts using non-fungible and fungible environmental monitoring and verification tokens derived from data on ecological impact ownership claims.

The model creates, trades, and retires the Greenstand Impact Tokens, which are non-fungible Tokens (NFT), and enables the conversion of this token into fungible tokens through the creation and use of **Relative Value Indexes (RVI)**. Its first primary use case converts the act of monitoring and verifying tree growth into tokens that enable a localized regenerative economy rooted in creating environmental wealth.

In this framework, **‘Greenstand’** refers to any technologically independent entity acting as a sealing node and writing to a shared decentralized ledger.
</details>

## System Domains & Database Schema

### Architectural Domains
* **Treetracker Domain:** Encompasses planters, planter identifiers, smart contracts, sessions, trees, and captures.
* **Field Data Domain:** Covers planter registrations, raw captures, raw sessions, and field data collection.
* **Stakeholder Domain:** Defines individual growers, planting organizations, and hierarchical stakeholder relationships.
* **Wallet Domain:** Manages accounts, tokens, transactions, transfer requests, action tokens, and wallet balances.

---

## Core System Concept

**Greenstand Node:** A replica of the Greenstand platform that executes data verification, maintains wallet ledgers, seals blocks, and mints tokens according to network data standards.


## Captures
### **Capture:**
* Captures support claims for *environmental impact and ownership of that impact* by producing data on interactions between an entity (such as a grower) and the environment.
* A capture is a data package derived from a ground-based monitoring event that ‘captures’ the environmental state at a specific time to provide proof of the existence of a new or previously existing ecological asset or evidence of an activity linked to the creation of such an asset. 

Capture data contains a timestamp, location, image, user info, and additional metadata. It is sent to the cloud for analysis and verification. 
  
  * **Raw Capture:** (Synonymous with a basic token) A capture that has not been accepted into or minted by any wallet.
  * **Accepted Capture:** A capture that has been accepted into a wallet *(Note: This does not automatically imply financial or environmental value)*.
  * **Capture Life Cycle:** A capture originates from a user “ground truthing” with a mobile phone. It is sent to the cloud where it is minted as a token into a wallet (if accepted)
    * If sent to the **Origin Wallet**, it can be **Deleted** or **Accepted**.
    * If sent to **another wallet**, it can be **Rejected** or **Accepted** *(if rejected, it is traded in token form from one wallet to another)*.
    * It travels through the wallet system until retired or deleted by a user.
* **Capture Matching:** 
The process of establishing a relationship between two or more captures, based on geo-location, attributes, and relationship to other captures. Matches previous tree data points to new data points based on location, image recognition, species, and timestamp to value the incremental growth of individual trees.
~~* **Tracking Session**~~
---

## Token States & Lifecycle
### Token Definitions
* **Token:** A capture and its related data, that has been placed in a wallet for trading.(often representing the incremental growth of a tree).
* **Greenstand Impact Token:** A non-fungible, environmentally backed digital reference to a capture and its attributes that facilitates the trade of social and ecological impact. It is a Mature, Immutable, or Locked token on a Greenstand node or network.
* **TRing:**  A fungible token (Identical, mutually exchangeable tokens) minted from the conversion of the non-fungible Greenstand Impact Token using the network's master RVI
* **Parent Token ID:** A database reference linking a token to an earlier historical token representing the same environmental asset, or specific geo location.

### Token States
* **Token State:** The operational state that governs which actions (e.g., trading, tag modifications) can be performed on a token:
  * **Basic Token:** (Synonymous with raw capture) This is a token created during a field monitoring session that exists only in isolated networks (typically on the mobile device that created it) before verification by a Greenstand node.
  * **Mature Token:** A token ingested into a Greenstand node and placed in an API-based wallet after initial data gateway checks. It is subject to further evaluation, tag adjustments, trading, retirement, or conversion.
  * **Blocked Token:** A token placed in a holding state and blocked from trading due to missing initial ownership data, flagged origin sources, or conflicting impact/ownership claims.
  * **Immutable Token:** A token whose attributes/tags can no longer be modified because they have been permanently "baked" or hard-coded into a blockchain ledger or exported.
  * **Locked Token:** A token that can no longer be modified or traded because it has been securely retired via an impact claim or exported to an external ledger/blockchain system.

---

## Attributes, Tags & Claims

### **Claims** 
Claims concern the type and quality of impact provided, impact responsibility, and ownership. Claims differ in validity. Data contained within a capture that validates or invalidates claims of environmental/social impact and ownership (e.g., *"This is an indigenous tree," "I am growing this tree"*).
* Claims may be considered false, conflicting, or true.
* **Conflicting Claim:** A claim flagged as contradictory due to unestablished responsible entities, overlapping geographical data, contract/lien violations, or disputed ownership of the impact creation.

### **Tags** 
An attribute ascribed to a capture/token by a wallet owner or verification system.
  * **Environmental Tags:** Attributes related to ecological change (e.g., location, species, carbon mass, biodiversity ratings).
  * **Social Impact Tags:** Attributes proving impact ownership and social benefit (e.g., payment to grower, refugee status, gender, indigenous status).
  * **Processing Tags:** Metadata documenting token creation, data sources, validation algorithms, and modification records.
* **Tagging Permission:** The authority to add or remove tags from a capture, accessible exclusively through token ownership in a wallet.
* **Tagging Permanence:** The immutable historical record of all tags added or removed during a capture’s life cycle.
* **Token Change Log:** An immutable audit log stored using blockchain technology that details all transactions and attribute modifications for a given token.

---

## Valuation & Relative Value Index

Algorithms that compute a relative impact value of each token based on tagged attributes.

* **Value / Relative Impact Value (RVI):** A numeral attached to a Greenstand Impact Token that is derived from the relative value calculation using tagged attributes attached to capture data. [Example](https://drive.google.com/file/d/1_jHzPogVokJJ9uLEPD_EYhvi2pvnS0WE/view)
* **Relative Impact Value Index (RVI):** An algorithm or framework that computes or weighs the value of each token based on its attributes (e.g., carbon sequestration, biodiversity, social impact) to place a comparative score or value on an NFT relative to others.
* **Master Relative Value Index:** The standardized RVI maintained by consensus across the Greenstand network used to compute native network currency.
* **Relative Value Tool:** A utility enabling system users to generate custom RVI values using the specific tags attached to captures in their wallets.
* **Value Factor (`value_factor`):** A database field calculating relative value based on ascribed tree capture tags (such as `tree_species`).
* **TRing:** The native ~~ERC-20 network~~ currency minted by depositing Greenstand Tokens based on the Master RVI calculation.
* ~~**Grain:** The smallest subunit of the TRing network currency (1 Grain = 1/100 TRing).~~

---

## Assets & Environmental Entities

~~* **Impact Asset:** An entity with quantifiable social and ecological value.~~
~~  * **Fundamental Impact Asset:** A synonym for an individual Impact Token.~~ 
~~  * **Aggregate Impact Asset:** Formed when multiple impact tokens are attached to a single conservation entity over time. ~~
* **Tree:** A woody perennial plant and the primary impact asset tracked by the Treetracker platform. In the Greenstand token model, "tree planting" is represented by a Greenstand Token without a `parent_id`.
* **Environmental Building Block:** A tangible, codifiable ecosystem asset that facilitates land restoration.

---

## Stakeholder Roles & Organizations
* **Account:** A user-based permission on the Greenstand platform.
* **Organizational Account:** an account that has granted permission for other users to access and manage its data. 
* **Stakeholder:** An individual or organization involved in the ecosystem (`{ Person, Planting Organization }`):
  * **Creators:** Entities performing direct token creation activities, including land restoration, planting, ground truthing, data collection, aggregation, and verification.
  * **Brokers:** Individuals or organizations involved in trading, transferring, marketing, or exchanging tokens.
  * **Offsetters:** Entities that permanently retire tokens to make final claims for carbon sequestration or ecosystem service credits.
* **Planter / Grower:** The entity on the ground claiming responsibility for the environmental impact, typically a field worker or farmer using the app to collect data on trees and restore land. 
~~* **Smallholder Farmer:** Individuals whose primary income derives from small-scale agricultural practices on small land plots.~~
~~* **Impact Manager:** An organization coordinating physical and operational responsibility for tree growth and restoration projects.~~
~~* **Organization:** An organization planting trees, managing growers, and monetizing environmental impact.~~
~~* **Project**~~
* **Grower Registration** The registration of an independent grower wallet that has no independent access to the system.
~~* **Grower** .~~
* **Entity_id** Wallet identifier associated with a `person_id` or `planting_organization`. 
* **Person_id** The entity ID linked to a `planter_id` within the main database `Trees` table. 

---

## System Architecture, Wallets & Transfers

### **Wallet** 
A container account in a chain-of-custody ledger system that holds tokens and enables exchanges between parties. 
  * **Origin Wallet:** The first wallet into which a token is minted upon upload.
  * **Root Wallet:** A high-permission wallet state on a node that enables API calls to create new wallets, manage sub-wallets, and execute batch transfer requests.
~~* **Clique Proof of Authority (EIP-225):** An energy-efficient consensus protocol used on Greenstand's Ethereum side-chain where authorized nodes seal canonical blocks instead of mining.~~
* **Impact Wallet Map:** A public map interface linking supported trees to a specific wallet holder.

### **Transfer Types:**
  * **Transfer:** The movement of a token from one wallet to another.
  * **Transfer Request:** A formalized request to move one or more tokens between wallets.
  * **Field Transfer:** A request, attached to a raw capture(s), that, upon upload, directs the transfer of a token or group of tokens from the origin wallet to a specific wallet. It allows peer-to-peer token movement offline prior to cloud ingestion and network verification.
  * **Action Token:** A special token issued to enable specific actions, workflows, or system permissions. Used to gift tokens to new wallets via a link. 
* **Grower Payment Verification:** Digital proof of payment attached to a token's initial transfer, verifying direct grower compensation. 
~~* **Impact Manager Map:** An organizational map displaying all trees coordinated under a specific project.~~

---


## References & System Documentation

* [Greenstand Token Whitepaper Google](https://github.com/Greenstand/Greenstand-Overview/blob/master/Greenstand-Token.md)
