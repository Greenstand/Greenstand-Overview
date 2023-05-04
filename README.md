---
description: Resources and context for Greenstand Engineers
---

# Overview



![](https://lh3.googleusercontent.com/t9i8Puyxha\_y1G3VibmyP7B3mMYrvIp4uROd8KH9x-9z13mzMR8HI4meNrkp-XL8GdMfONjfwbaMHMp2-11bcq\_WcA8HT2JbymGXanOFNd4dru0RH8-IRzSv\_xPAE9iYAZRjYIU)

This is a “living document” and will continue to be updated! You can access the most recent version of this document at [https://app.gitbook.com/@greenstand/s/engineering/](https://app.gitbook.com/@greenstand/s/engineering/)

## **Welcome!**

Thanks for volunteering as a Greenstand Engineer!  Greenstand Engineers build the treetracker platform, a powerful and integrated set of applications and software services that employs some of the world’s poorest people to regrow forests by paying them for the positive impacts they create.  This guide explains our motivations, organizational culture, software projects, and tools that we use to collaborate, build, and run our platform.  [https://greenstand.org](https://greenstand.org) \


We are so glad to have you on board.  This is a large project and we have many tasks ahead of us - ensuring a quality software service that can verify the growth and success of billions of trees as we collaborate with tens of third party reforestation organizations to rebuild our global forests.  It’s a big dream, but by working together that vision is already becoming reality.  There is a place in this effort for every software engineer!\


### **What is Treetracker?** 

Treetracker is a platform that enables proof of reforestation impact (such as tree plantings, or tree survivorship) to be collected, verified, and exchanged for financial compensation.  Growers capture timestamped, geotagged images using mobile applications to demonstrate impacts that are relayed to our cloud via an ingestion pipeline.  These data are reviewed using our admin panel, and shown in context via our web map.  Ownership of impacts are tradable through our wallet service, which enables diverse funding sources to fund these activities through a transparent chain of custody.\


A huge gap exists between the good intentions of global reforestation efforts and verified, new forest growth on the ground.  Treetracker enables the radical transparency and collaboration necessary to turn intentions into outcomes.\
\


### **Treetracker Platform High Level Overview** 

![](<.gitbook/assets/Screen Shot 2021-04-07 at 6.53.52 PM.png>)

A visual review of our technical capabilities is available here: &#x20;

{% file src=".gitbook/assets/TechCapabilitiesWinter2021.pdf" %}

###

### **Test Environment**

One of the best ways to understand our platform is to try it out.  We recommend that you use our test environment to do so.   Do not worry about damaging data in the test environment, it is all test data.

**Admin Panel:** [http://test-admin.treetracker.org/](http://test-admin.treetracker.org/)\
User: demo\
Password: hxRSxG63a8

**Android Application:** [https://appdistribution.firebase.dev/i/8d0c18f52fc10af9](https://appdistribution.firebase.dev/i/8d0c18f52fc10af9)

**Web Map:** [http://test.treetracker.org](http://test.treetracker.org)

**Wallet API:** Come to the wallet team meeting and request access!\


→  TODO: Location Accuracy Test Case\
\


### **Domain Model**

We use standardized language to talk about the logical units involved in our technical and operational systems. &#x20;

An evolving document is maintained at the following link, and changes are suggested and reviewed via Pull Request: [https://github.com/Greenstand/system-design-docs/blob/master/domain-model/domain\_model.md](https://github.com/Greenstand/system-design-docs/blob/master/domain-model/domain\_model.md)

[https://medium.com/spotlight-on-javascript/domain-driven-design-for-javascript-developers-9fc3f681931a](https://medium.com/spotlight-on-javascript/domain-driven-design-for-javascript-developers-9fc3f681931a)\


**Our Engineering Organization**\



Building treetracker requires diverse technical skills and many projects working together to build a functional whole.  As such, we have organized the Greenstand Engineers as a microservices enterprise.  We operate on the principle of creating many small, focused teams.  Each team organizes an (optional) weekly meeting, has team leads, and receives technical support and coordination from engineering leadership.  New volunteers are encouraged to choose one project to contribute to at first.  Over time, as you learn more about our platform, there are many opportunities to  learn new technologies, attend other team meetings, or collaborate in cross team working groups.\


### **Structure of Greenstand** 

Greenstand currently has three divisions: Engineering, Operations, and Programs.  Each division is led by a VP who collaborates with the President on the high level guidance of Greenstand.  Individuals in these roles currently are:

President: Ezra Jay\
VP Engineering: OPEN\
VP Operations: OPEN\
VP Programs: Sebastian Gaertner\


Greenstand engineering division is working on filling the roles of VP Engineering and Director of Engineering.\


### **Roles**

We define role levels to facilitate organizing our teams and decision making. &#x20;

All new volunteers enter as Contributors.  Core Contributors in the engineering division are individuals who have contributed 50 hours of engineering work to the project.  Lead and Coordinator roles are reserved for individuals that have made outstanding contributions to the platform and desire leadership opportunities and experience. &#x20;

In certain cases roles may have funding available.\


### **Teams**

The engineering division is divided into many small teams.  In some cases we also organize cross-team working groups to address special concerns.  We add and delete teams as needed and deemed appropriate.  Some teams also have squads tasked with specific responsibilities within the team, such as guidance, testing, or challenging engineering problems**.**

#### **Current Teams:**

Admin Panel Application\
Impact Map Web Application\
Wallet Application\
Mobile ( composed of Android and iOS teams)\
Machine Learning\
Wallet Microservice\
Application Platform\
GIS

[**https://app.gitbook.com/@greenstand/s/engineering/teams**](https://app.gitbook.com/@greenstand/s/engineering/teams)

**Current Working Groups:**

Microservices\
Load Testing\
Airflow\
\
**Coding Partners**

TODO



### **Team Meetings**

Greenstand Engineers meet weekly at a variety of team meetings to coordinate efforts. These meetings are optional - if you are comfortable working alone and communicating via slack we are completely on board with that process - but we do find that face time and verbal discussion help coordinate and move the project forward effectively.   Please it’s a good way to meet other collaborators.  The team calendar can be found at:

[Greenstand Team Calendar ](https://calendar.google.com/calendar/embed?src=greenstand.org\_fc0daljnbpsupt6skbb77mkuq0%40group.calendar.google.com\&ctz=America%2FAnchorage)

Ask to be invited to meetings you are interested, and you will receive updates to the meeting details via google calendar automatically.\


**Developer Roundtables** are forums for tech/organizational questions, group debugging, help for junior devs, and also presentation of items of interest including system architectures and technical training. &#x20;

**Coworking Sessions** are times when many Greenstand Engineers may be online at the same time and can collaborate or experience community support. \


Note that Greenstand is an international project and your ability to attend some meetings may be defined somewhat by your time zone.  In particular we have a developer roundtable that runs at 10AM London / 6 PM Beijing time to support our international team members in Europe, India, Africa, and China. &#x20;

### **Volunteer Enterprise Perspective**

As a volunteer enterprise, we need to meet the demands of a full scale technical operation with an often heavily part time and large rotating set of collaborators.  This means that working on Treetracker will feel different than working for a corporation with many full time, retained, and robustly funded engineers.  **Our strength as Greenstand Engineers comes from working together,** each of us focusing on small coordinated pieces of a big project.  This often means considerably more ‘hand off’ in terms of tech leadership, troubleshooting, and availability than some engineers might be used to.  It’s also a strength though and a lot of fun, because Greenstand’s large community of like minded individuals is a great place to make new connections, networks, and friends.\
\
