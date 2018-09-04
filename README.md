# Welcome to GreenStand's Tree Tracker project

## Contributing See [Contributing](https://github.com/Greenstand/Development-Overview/blob/master/Contributing.md) 

## Roadmap See [Roadmap](https://github.com/Greenstand/Development-Overview/blob/master/Roadmap.md) for our long term development plans.

## Development needs as of 09/04/2018

Here are immediate and long-term needs. Here are a few, if you don’t see a project that fits, come check in on [Slack link](https://join.slack.com/t/greenstand/shared_invite/enQtMjcyMzgyMjk4NzU3LWZmNjM3YzY5N2Q0MzQ5YTM4OGZkMWJhM2U4MTkyYjI2NjhkN2YxNTRiMDIwNWQ5ZTVlNDczYzBjZmMxYzM2ZjU) and let’s figure out how to leverage your skills, don’t be shy there are lots to a do and great community to plug into!

- HTML/JS - Both our web map and our admin panel need HTML and Javascript support on the frontend (React.js, google maps, query).  And API work on backend (node.js).

- Android - The app is functioning well, but we need to make it rock solid for our users in the Africa field with an intensive round of testing and crash debugging.  Either you are an app breaker or an app fixer —  we need both!

- DevOps - Currently taken up by, we have Jenkins in place and could use more support getting our CI/CD pipelines dialed in for node.js and Android.

- Node.js unit testing - We only have partial coverage of our API in our unit tests, which means we cannot reliability validate new commits for continuous deployment.  We are using Mocha/Chai to write automated tests, and this should be straightforward for anyone with basic unit testing experience.

- Cloud - Docker, chef, or your favorite deployment tools, help us automate the rollout of new features to our production infrastructure.

- Database - Treetracker is currently powered by postGRES/postGIS.  As our database grows to millions of trees, our clustering algorithms are going to need aggressive optimization.

- Image processing - blurred/invalid image detection, duplicate image detection, seedling image recognition - in Java or AWS Lambda - let's get our analysis pipeline rolling.

- Security Review

- Complete list of [Issues/Tickets](https://github.com/Greenstand/Development-Overview/blob/master/Issues-lndex.md)

### Contacts: 
[Slack Link](https://join.slack.com/t/greenstand/shared_invite/enQtMjcyMzgyMjk4NzU3LWZmNjM3YzY5N2Q0MzQ5YTM4OGZkMWJhM2U4MTkyYjI2NjhkN2YxNTRiMDIwNWQ5ZTVlNDczYzBjZmMxYzM2ZjU)

Info@greenstand.org
