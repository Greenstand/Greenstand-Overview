# Welcome to Greenstand's Treetracker project

We are here to make the world a cooler, richer and greener place.  

**Basic Overview:** The [treetracker-android](https://github.com/Greenstand/treetracker-android) app is a tool to allow planters to verify tree planting and tree survival with geo-tagged, time-stamped images. The tree images and data points are analyzed using the [treetracker-admin-client](https://github.com/Greenstand/treetracker-admin-client) and displayed and shared via tokens/links on the [treetracker-web-map-client](https://github.com/Greenstand/treetracker-web-map-client). This map can be embedded on other organizations' websites displaying their planted and mapped trees. The [wallet-api](https://github.com/Greenstand/treetracker-wallet-api) is a service that allows people to create/register wallet and transfer tokens. These token are created from data linked to a claim of having created a ecological impact, though the tending and caring of trees. The tokens and the wallet system can be used to trade tokens via an API. [Postman](https://github.com/Greenstand/treetracker-wallet-api#set-up-postman-to-operate-wallet-api) is a helpful tool for interacting with the wallet API

Also see:

- [Greenstand Engineering Handbook](https://greenstand.gitbook.io/engineering)

- [Greenstand Operations Handbook](https://app.gitbook.com/o/-MXNadx4i6aOZ12XcStA/s/-MgvgPeo6NdZWFJ-Vzv0/)

- [Greenstand Token](https://github.com/Greenstand/Development-Overview/blob/master/Greenstand-Token.md)

## [Roadmap](https://github.com/Greenstand/Development-Overview/blob/master/Roadmap.md) for our feature development plans

# Contributing to The Cause

Help us star and fork our repositories.


### Join The team
* Fill out the [Engineering Sign Up](https://greenstand.org/contribute/volunteer)

* Ask to be added to the team on Github.

* If you already know how, feel free to just fork and pull.

* If the words 'fork and pull' doesn't make sense, please read up on Github below.

**Think Agile - Small Iterations - Clearly Defined Commits.**

 * Keep your commits small - if you worked on three issues make three commits etc.

 * Small commits help the reviewer

 * Lots of small commits make your profile look cooler.

 * When in doubt, ask. (Via Slack or Github)

## Your first contribution

Don't be shy. There are lots to a do and a great community to plug into!

* Find a task you would like to work on by browsing the repositories' issue lists below.
* Let others know what you are working on - post your intentions in the Github comments or relevant Slack channel.
* If you don't find something now, be persistent - keep asking!


### Ongoing Needs

- Quality Control - Need quality control engineers to understand use cases and be available for robust testing on builds before rollout. This is often testing new features on our admin panel, webmap or mobile app. If you can find a broken link or a button that doesn't work, you have found a great way to contribute and get to know the project.

- Documentation - help Update and sync all documentation

- General Decisions - take part in the general decision making process: https://github.com/Greenstand/treetracker-decisions

### Development needs as of Aug 2022

Here are a few immediate and long-term needs. If you don’t see a project that fits, keep looking, come check in on Slack link and let’s figure out how to leverage your skills.


- General Project Boards: https://github.com/orgs/Greenstand/projects

- Tree tracker Web Map Client Project Beta https://github.com/orgs/Greenstand/projects/49

- Customizable Web Map Tool: https://github.com/orgs/Greenstand/projects/56

- Search Service on Greenstand: https://github.com/orgs/Greenstand/projects/57

- React.js, Next.js - Our admin panel is build using React.js, Next.js. We have new designs for the web map that need to be implemented and made mobile compliant.

- Node.js, - our APIs are build on node.js express.  We need API engineers with some database experience to add features.  We also need engineers to improve our testing coverage.

- Android - Need Android UI/UX engineers and individuals with experience working with cloud integrations in offline scenarios.  Experience with enhancing GPS accuracy on the Android platform is also useful.

- iOS - We need to build a clone of our Android app in iOS.  

- DevOps - We use Github Action, Kubernetes, ArgoCD for build and deployment automation.  Our automation coverage is partial and we need engineer with experience on these platforms to fix problems and streamline the process.

- Cloud - Scaling and security analysis is needed.

- Database - Database administration is need to continue refining our backend systems. We use PostgreSQL + PostGIS.

- Image processing - Duplicate image detection, species detection. Let's get our analysis pipeline rolling.

## Complete list of [Issues/Tickets](https://github.com/Greenstand/Development-Overview/blob/master/Issues-lndex.md)**

   * [General Issues](https://github.com/Greenstand/Development-Overview/issues)
   * Kotlin Issues: [Android App](https://github.com/Greenstand/treetracker-android/issues)

   * JavaScript Issues:
          [Admin Panel Client](https://github.com/Greenstand/treetracker-admin-client/issues),
          [Web Map Client](https://github.com/Greenstand/treetracker-web-map-client/issues),
          [Mobile App API](https://github.com/Greenstand/treetracker-mobile-api/issues),

   * Micro-services Issues:
       [treetracker-api](https://github.com/Greenstand/treetracker-api)
       [treetracker-field-data](https://github.com/Greenstand/treetracker-field-data)
       [treetracker-query-api](https://github.com/Greenstand/treetracker-query-api)

## Project Repositories

*In its most basic form, this platform is designed to collect tree images from an android application and display these images on web-maps that can be served on other organizations' websites. In its more advanced form, we are verifying individual planter's efforts by tracking individual trees over time and creating results-based employment. Each Data point or "capture" gets turned into a tradeable token*

#### [Treetracker-Android Application](https://github.com/Greenstand/treetracker-android)
- [Treetracker_Android User Story](https://github.com/Greenstand/treetracker-android/wiki/User-Story)
- [Treetracker Android Project Board](https://github.com/orgs/Greenstand/projects/5)
- [Treetracker Android Wiki](https://github.com/Greenstand/treetracker-android/wiki)
#### [Treetracker-Web Map](https://github.com/Greenstand/treetracker-web-client)
- [Treetracker-Web-Map User Story](https://app.gitbook.com/@greenstand/s/impact-map/)
- [Treetracker Web Map Project Board](https://github.com/orgs/Greenstand/projects/49)
- [Treetracker Web Map Wiki](https://docs.greenstand.org/wallet-web-app/crsWWEYzLFNFCLaLwZ4s/)
#### [Treetracker-Admin panel](Https://github.com/Greenstand/treetracker-admin-client)
- [Treetracker-Admin User Story]
- [Treetracker Admin Project Board]
- [Treetracker Admin Wiki](https://docs.greenstand.org/admin-panel/)

#### [Development overview](https://github.com/Greenstand/Development-Overview)
- [Development Overview Project Board]
- [Development Overview Wiki](https://github.com/Greenstand/Development-Overview/wiki)

API's
* [Repository - Api for working with the android mobile segment](https://github.com/Greenstand/treetracker-mobile-api)
* [Repository - Api for working with admin-panel](https://github.com/Greenstand/treetracker-api)
* [Repository - API for wallet](https://github.com/Greenstand/treetracker-wallet-api)

## Basic Git Hub skills required!

**We use the Fork and Pull model.**
Pro Tip: Keep pull requests small and focused on the issue you are solving. (Large changes in code are much harder to accept)

If you have not heard of a **pull request** it is time for you to join over 27 million developers and learn this version control platform. There are lots of cool articles to get you up to speed: [Github Introduction](https://guides.github.com/introduction/flow/) [Forking a Repository in Github](https://help.github.com/articles/fork-a-repo/), [Synicing a Fork in Github](https://help.github.com/articles/syncing-a-fork/)
More links can be found here in [Github Basics:project-overview/github](https://github.com/Greenstand/Project_Overview/Resources/Github-basics)

### Slack Basics
For Slack channel link email info@greenstand.org

Slack is our main form of communication. Here are some Slack basics:
To add yourself to the desired channels: on the left window in Slack find **channel +**...

Our popular channels are #development, #android, #nodejs-api, #tree-talk etc..

* Speak out! Public messages build our team and keep us motivated. Use Public channels as much as possible.
* Keep your messages in the relevant channels - talk about android in the android channel etc..
* Ask any question - we are friendly and all learning together. General tech questions go in #development, other questions in #general, Android questions in #android etc.
* Pointless chatter goes in #random channel
* Use *Threads* to reply keeps channels cleaner.
* A list of ALL channels is found pinned to the Genneral Channel if you are not in a channel that you think you need access to, reach out.
## Building Time Channel
* By logging your time (in minutes) this channel is helpful for seeing who is doing what. It is also used to:
- Reward contributors with Greenstand tokens.
- Help prevent duplicated efforts.
- Help coordinate efforts
- Gage development velocity and calculate contributions metrics.

## Helpful Links:

[treetracker.org](https://map.treetracker.org) Tree map
[Gitbook](https://app.gitbook.com/o/-MXNadx4i6aOZ12XcStA/c/-MXNhFFcuj1FVrahC56a)
[Operations Handbook](https://app.gitbook.com/o/-MXNadx4i6aOZ12XcStA/s/-MgvgPeo6NdZWFJ-Vzv0/)

## Contacts:
- [Slack Link](https://join.slack.com/t/greenstand/shared_invite/enQtMjcyMzgyMjk4NzU3LWZmNjM3YzY5N2Q0MzQ5YTM4OGZkMWJhM2U4MTkyYjI2NjhkN2YxNTRiMDIwNWQ5ZTVlNDczYzBjZmMxYzM2ZjU)

- Info@greenstand.org
