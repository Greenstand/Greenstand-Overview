# Welcome to GreenStand's Tree Tracker project

We are here to make the world a cooler, richer and greener place.  

**Basic Overview:** The [treetracker-android](https://github.com/Greenstand/treetracker-android) app is a tool to allow planters to verify tree planting and tree survival with geo-tagged, time-stamped images. The tree images are to be analyzed using the [treetracker-admin](https://github.com/Greenstand/treetracker-admin) and then displayed and shared via tokens/links on the [treetracker-web-map](https://github.com/Greenstand/treetracker-web-map). This map is embedded on other organizations websites. 

## Development needs as of 10/08/2018

Here are immediate and long-term needs. Here are a few, if you don’t see a project that fits, come check in on [Slack link](https://join.slack.com/t/greenstand/shared_invite/enQtMjcyMzgyMjk4NzU3LWZmNjM3YzY5N2Q0MzQ5YTM4OGZkMWJhM2U4MTkyYjI2NjhkN2YxNTRiMDIwNWQ5ZTVlNDczYzBjZmMxYzM2ZjU) and let’s figure out how to leverage your skills, don’t be shy there are lots to a do and great community to plug into!

- HTML/JS - Both our web map and our admin panel need HTML and Javascript support on the frontend (React.js, google maps, query).  And API work on backend (node.js).

- Android - The app is functioning well, but we needs a UX overhaul to make it rock solid and easy to use for our users in the Africa field. It needs more testing and crash debugging. 

- DevOps - Currently taken up by @MattK. We have Jenkins in place and could use more support getting our CI/CD pipelines dialed in for node.js and Android.

- Node.js unit testing - We only have partial coverage of our API in our unit tests, which means we cannot reliability validate new commits for continuous deployment.  We are using Mocha/Chai to write automated tests, and this should be straightforward for anyone with basic unit testing experience.

- Cloud - Docker, chef, or your favorite deployment tools, help us automate the rollout of new features to our production infrastructure.

- Database - Treetracker is currently powered by postGRES/postGIS.  As our database grows to millions of trees, our clustering algorithms are going to need aggressive optimization.

- Image processing - blurred/invalid image detection, duplicate image detection. Let's get our analysis pipeline rolling.

- Security Review

## [Roadmap](https://github.com/Greenstand/Development-Overview/blob/master/Roadmap.md) for our long term development plans

# Contributing to The Cause
Help us star and fork our repositories.

### Join The team
* Fill out the [Join-the-team-form](https://docs.google.com/forms/d/e/1FAIpQLSe61HDJKVH16vtTxhXpbwCH-wTVN1e6XoVU1riWjJ-ne5SIiA/viewform?usp=sf_link)

* Ask to be added to the team on Github. 

* If you already know how, feel free to just fork, build and pull.

* If the words 'fork and pull' doesn't make sense, please read up on Github below. 

**Think Agile - Small Iterations - Clearly Defined Commits.**
  
 * Keep your commits small - if you worked on three issues make three commits etc. 
 
 * Small commites help the reviewer
 
 * Lots of small commits make your profile look cooler.
 
* When in doubt, ask.

## Your first contribution
* Find a task you would like to work on by browsing the repositories' issue lists below. 
* Let others know what you are working on - post your intentions in the relevant slack channel or Github comments. 
* If you don't find something now, be persistent. 

## Complete list of [Issues/Tickets](https://github.com/Greenstand/Development-Overview/blob/master/Issues-lndex.md)**

   * [General Issues](https://github.com/Greenstand/Development-Overview/issues)
   * Kotlin Issues: [Android](https://github.com/Greenstand/treetracker-android/issues)
       
   * Java Script Issues:
          [Admin Panel](https://github.com/Greenstand/treetracker-admin/issues), 
          [Web map issues](https://github.com/Greenstand/treetracker-web/issues), 
          [Mobile App API](https://github.com/Greenstand/treetracker-mobile-api/issues), 
          

## Project Repositories

*In its most basic form this platform is designed to collect tree images from an android application and display these images on web-maps that can be served on other organizations' websites. In its more advanced form, we are verifying individual planter's efforts by tracking individual trees over time and creating results-based employment.*

#### [Treetracker-Android Application](https://github.com/Greenstand/treetracker-android)
- [Treetracker_Android User Story](https://github.com/Greenstand/treetracker-android/wiki/User-Story)
- [Treetracker Android Project Board](https://github.com/orgs/Greenstand/projects/5)
- [Treetracker Android Wiki](https://github.com/Greenstand/treetracker-android/wiki)
#### [Treetracker-Web Map](https://github.com/Greenstand/treetracker-web)
- [Treetracker-Web-Map User Story](https://github.com/Greenstand/treetracker-web-map/wiki)
- [Treetracker Web Map Project Board](https://github.com/orgs/Greenstand/projects/4)
- [Treetracker Web Map Wiki](https://github.com/Greenstand/treetracker-web-map/wiki)
#### [Treetracker-Admin panel](Https://github.com/Greenstand/treetracker-admin)
- [Treetracker-Admin User Story]
- [Treetracker Admin Project Board](https://github.com/orgs/Greenstand/projects/6)
- [Treetracker Admin Wiki](https://github.com/Greenstand/treetracker-admin/wiki)
#### [Database Migrations](https://github.com/Greenstand/treetracker-database-migrations)
- [Database Migrations Docs](https://db-migrate.readthedocs.io/en/latest/Getting%20Started/configuration/)
#### [Design Basics and Assets](https://github.com/Greenstand/Design)
- [Design Wiki](https://github.com/Greenstand/Design/wiki)
#### [Development overview](https://github.com/Greenstand/Development-Overview)
- [Development Overview Project Board]
- [Development Overview Wiki](https://github.com/Greenstand/Development-Overview/wiki)

API's 
* [Repository - Api for working with the android mobile segment](https://github.com/Greenstand/treetracker-mobile-api)
* [Repository - Api for working with admin-panel](https://github.com/Greenstand/treetracker-admin-api)
* [Some json and scripts for working with the API](https://github.com/Greenstand/treetracker-json)
* [Tree tracker server scripts](https://github.com/Greenstand/treetracker-server-scripts)

## Basic Git Hub skills required!
If you have not heard of a **pull request** it is time for you to join over 27 million developers and learn this version control platform. There are lots of cool articles to get you up to speed: [Github Introduction](https://guides.github.com/introduction/flow/) [Forking a Repository in Github](https://help.github.com/articles/fork-a-repo/), [Synicing a Fork in Github](https://help.github.com/articles/syncing-a-fork/)

**We use the Fork and Pull model.**

Basics: 
* Fork the repository
* All changes you make must be submitted for review via a pull request to the appropriate branch.
* Ask for clarification if needed (via Git pull requests or Slack). 
* Report problems.

### Slack Basics
[Slack link](https://join.slack.com/t/greenstand/shared_invite/enQtMjcyMzgyMjk4NzU3LWZmNjM3YzY5N2Q0MzQ5YTM4OGZkMWJhM2U4MTkyYjI2NjhkN2YxNTRiMDIwNWQ5ZTVlNDczYzBjZmMxYzM2ZjU)
Slack is our main form of communication. Here are some Slack basics: 
To add yourself to the desired channels: on the left window in Slack find **channel +**... 

Our popular channels are #development, #android, #nodejs-api, #tree-talk etc..

* Speak out! Public messages build our team and keep us motivated. Use Public channels as much as possible. 
* Keep your messages in the relevant channels - talk about android in the android channel etc..
* Ask any question - we are friendly and all learning together. General tech questions go in #development, other questions in #general, Android questions in #android etc.
* Pointless chatter goes in #random channel
* Opening *Threads* to reply keeps channels cleaner.

## Helpful Links: 

[GreenStand Coding Style Guide](https://github.com/Greenstand/Development-Overview/blob/master/StyleGuide.md) for coding style rules 

## Contacts: 
- [Slack Link](https://join.slack.com/t/greenstand/shared_invite/enQtMjcyMzgyMjk4NzU3LWZmNjM3YzY5N2Q0MzQ5YTM4OGZkMWJhM2U4MTkyYjI2NjhkN2YxNTRiMDIwNWQ5ZTVlNDczYzBjZmMxYzM2ZjU)

- Info@greenstand.org
