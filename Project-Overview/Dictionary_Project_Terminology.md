# Terminology for the project. Please revise as you see fit

- Active = A true/false database field that displays or hides a data point on the treetracker.org tree maps
- Certificate = A database table that allows a number of tree id's to be linked together on a map (consider changing to tree_token_accont

- Cluster = A group of trees on the treetracker.org map that is clustered together under one pin
- Cluster Size = The radius size that determines what trees join individual clusters???
- Datapoint = a small packet of data sent from the planters phone to the database that contains: timestamp, location, image, user and more
- Duplicate = a data point or verified tree that has multiple records

- Donor = an individual (or entity) whos monetary contribution has linked to a specific tree or set of trees. 
- Donor = a database field that links a certificate to a specific organization (this should be removed)
- Donor = a third party broker for tree tokens (interacting directly with the consumer/funders)
- Dead = A database field that identifies trees that are obviously dead
- Entity_id = The wallet (requiers a person or a planting_organization)
- Funder = (also referred to as investor) referring to the individual consumer or any third party buying tree's not directly from the planting organization or Greenstand (Donor being a step closer to the planting org or Greenstand, and being a conduit to collect funder money, more like a booker)
- 
- Greenstander = someone who willingly spends considerable time or money to create this system 
- Grower = A better term for a planter???
- GPS Accuracy = A database field that captures the phones reported GPS Accuracy level (at the time of the photo) in meters. (33% error)
- Missing = A database field for trees that have not been relocated for an extended period of time
- Mobile money = Financial systems, like Mpesa, that allow funds to be sent to a users sim card
- Organization = A database field that places a group of Donors and their Tree Tokens under the umbrella of a specific organization 
- Planting organization = referring specifically to an organization that is planting trees and selling that environmental impact. 
- 
- Priority = A database field that can be set to make an individual pin on the planters phone flash red
- Planter = A user using the Tree Tracker Planter app to collect data on trees
- Person (Table in the DB) has a planter mode or a 
- Planter_identifier = a felid that users enter into the app to create a user account (email or phone #)
- Tree = a woody perennial plant, typically having a single stem or trunk growing to a considerable height and bearing lateral branches at some distance from the ground
- Tree Token = the incremental growth of a tree (as set in the tree token creation document) 
 1. Base codable information from incoming data (and value factor adjustment)
 2. Image
 3. Initial Entity_ID

- /?token = Currently a set of tree_ids linked to a certificate in the database and displayed on a map
- Update Feature = A feature that matches previous data points to a new data point, based on location, image recognition, species and time stamp
Value_factor = a database field that allows different tree_species to have different value for token creation.
- Verified Tree = A tree with a high probability of existence, based on image
