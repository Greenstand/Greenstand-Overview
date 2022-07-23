[Also See System-design-docs](https://github.com/Greenstand/system-design-docs)

[See Domain Model](https://github.com/Greenstand/system-design-docs/blob/master/domain-model/domain_model.md)


# Terminology for the project. Please revise as you see fit

- Active = A true/false database field that displays or hides a data point on the treetracker.org treemaps
- Capture Matching Feature = A feature that matches previous tree data points to a new data point, based on location, image recognition, species and time stamp
- Certificate = A database table that allows several tree id's to be linked together on a map (depreciating)
- Cluster = A group of trees on the treetracker.org map that is clustered together under one pin
- Datapoint = a small packet of data sent from the planter's phone to the database that contains: timestamp, location, image, user and more.
- Duplicate = a data point or verified tree that has multiple records
- Donor = a database field that links a certificate to a specific organization (depreciating use case)
- Dead = A database field that identifies trees that are likely dead.
- Entity_id = The wallet (requires a person_id or a planting_organization)
- Greenstander = someone who willingly spends considerable time or money to create this system
- Grower = A better term for a planter
- GPS Accuracy = A database field that captures the phones reported GPS Accuracy level (at the time of the photo) in meters. (33% error)
- Missing = A database field for trees that have not been relocated for an extended period of time
- Mobile money = payment and money trasnfer systems, like Mpesa, that allow funds to be sent to a users phone or sim card
- Organization = A database field that places a group of Donors and their Tree Tokens under the umbrella of a specific organization
- Planting organization = referring specifically to an organization that is planting trees and selling that environmental impact.
- Priority = A database field that can be set to make an individual pin on the planters phone flash red (inactive field)
- Planter = A user using the Tree Tracker Planter app to collect data on trees
- Person_id = (From the Trees Table in the DB) is the entity_id that is linked to that planter_id
- Planter_identifier = a felid that users enter into the app to create a user account (email or phone #)
- Tree = a woody perennial plant, typically having a single stem or trunk growing to a considerable height and bearing lateral branches at some distance from the ground
- Tree Capture = a tree picture under the `tree table` that can be converted into a token.
- Token = a tree capture and it's related data, that has been placed in a wallet and can be traded. Often used to represent incremental growth of a tree (as set in the tree token creation document). May have a value factor attached.
   1. Base codable information from incoming data (and value factor)
   2. Image
   3. Initial Entity_ID

- Value_factor = a database field that calculates relative value using different tags ascribed to each tree capture, such as tree_species.
- Verified Tree = A capture that has been accepted by a verification protocol - assumed to be a tree with a high probability of existence, based on image and collected data sets. (note these verification and acceptance criteria are specific to use cases)
