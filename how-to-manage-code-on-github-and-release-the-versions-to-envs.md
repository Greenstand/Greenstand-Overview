# How to manage code on Github and release the versions to envs



## The Goal

* Define a workflow to handle developing multi-features at the same time, parallelly.
* A workflow and tool to deliver the code to users: to give it to tester, end user, and partial end users for early trying.&#x20;
  * For those parallel features, we should find a way to easily deploy it to dev, and test, prod version without impact the current main version (master)
* A workflow to handle legacy, maintenance version.
  * When newer version released, it is possible we need to maintain the older version for a while, so we need to find a solution to deploy the old version, fix bugs and so on.

## The Solution

We already used semantic release, Github Action, and k8s, we don't need to introduce any new thing, just need to define a specification on steps for development and release.

By the way, I don't we need to adapt this solution for every single features, sometimes evolving features at \`master\` or other branch combined with other things is fine, and using separate branch has cost, we need to maintain multiple branches, sync them frequently, and resolve conflicts from time to time. So just pick this solution when it is really needed.&#x20;

### Prerequisites

* Install and setup semantic release: [https://github.com/semantic-release/semantic-release](https://github.com/semantic-release/semantic-release) (We have almost done this for all repos)
* Set \`main\` or \`master\` branch as the default branch, take it as the current production version. (Basically this is our case for all repos)
* Set up the Github Action to deploy the code to dev/test/prod. (Currently we have done it for all apps/services)
* Besides the prod release channel, prepare two release channel for \`beta\` and \`alpha\` release channel, it could be a domain (alpha-admin.treetracker.org, alpha-web.treetracker.org) and corresponding s3 bucket or a router ([https://prod-k8s.treetracker.org/alpha/wallet/](https://prod-k8s.treetracker.org/alpha/wallet/)), depending on the situation on the repos/apps.

### Workflow for Developing Multi-feature

To deploy a new feature, say, customizable web map (CWM), so the goal is that we want to develop this feature on a dedicated branch (cwm), and deploy it to the alpha channel on our dev/test/prod env, so our user can test, use it on that channel, say, alpha-web.treetracer.org for prod, and [https://dev-k8s.treetracker.org/alpha/webmap/](https://dev-k8s.treetracker.org/alpha/webmap/) for dev env, [https://test-k8s.treetracker.org/alpha/webmap/](https://dev-k8s.treetracker.org/alpha/webmap/) for test env.

1. Assuming current version on \`main\` is 1.1.1
2.  Create branch \`cwm\` from \`main\`, set semantic release (.releaserc config file) as below:

    ```
    {
      "branches": [
        '+([0-9])?(.{+([0-9]),x}).x',
        'main',
        'next',
        'next-major',
        { name: 'cwm', channel: 'alpha', prerelease: true },
      ],
        "plugins": [
          ...
        ]
    }
    ```

    By this setting, semantic release will take the \`cwm\` as a releasable version and deploy it to dev env when code merged to \`cwm\`, and deploy to test and prod when some Github Action is executed manually. at the \`alpha\` channel, in this case, it is: [https://dev-k8s.treetracker.org/alpha/webmap/](https://dev-k8s.treetracker.org/alpha/webmap/)
3. Develop and push code to \`cwm\` will trigger the release:
   1. Calculate the version according to the commit comment (feat, fix), and attach the word \`pre-release\`, for example: 1.2.0-cwm.1&#x20;
   2. All following pushs will not change the version (1.2.0) anymore but increase the number after cwm (e.g. 1.2.0-cwm.2), so in this way, the release will not conflict the prod channel's version which grows as 1.2.0, 1.3.0, 1.4.0.
4. We can manually run Github Action to release 1.2.0-cwm.2 to test and prod env on the \`alpha\` channel (alpha-map.treetracker.org), so people can test it.
5.  When this feature is finished and we are ready to normally release it, merge the \`cwm\` to \`main\`, this will trigger semantic release to calculate the version and do a release to dev env.

    Say, at this moment, the \`main\` 's version is 1.3.1, the semantic release will analyze the commits from the \`cwm\` and get the final version, say, 1.4.0
6. New version 1.4.0 with the new feature is ready now, can can be release to prod default channel (map.treetracker.org)

Some other consideration/scenarios:

* We should frequently merge the \`main\` to \`cwm\` to avoid big conflicts at the final merge, and sync the newest feature/fix from master to \`cwm\`.
* Because release channel requires resources, for example, domain, so we just set two channels: beta, alpha, so at the same time, for one channel, there only is one active branch that could be used/visited. It is possible there are more than 1 branch that are set in the config as \`beta\`, but the beta channel will run the code of the branch that was deployed most recently. So maybe we should just set one branch for using one channel (beta/alpha) at the same time, which means there is only one \`beta/alpha\` in the release config, which means we can just has two branch set as prerelease, so for more branch/features, we are free to create new feature branches, and code and push and co-work on it, the only limitation is that we can not release it to dev/test/prod channel.

### Workflow for maintaining legacy version

We need to maintain a specific version of code for some reason, for example, the micro-service developed version v1 and v2, we can not directly remove v1 when we release v2, we need to give the clients time to upgrade to v2.

Assuming we want to upgrade the wallet api from v1 to v2, the API for v1 is deployed to [https://prod-k8s.treetracker.org/wallet/](https://prod-k8s.treetracker.org/wallet/) and v2 is about to deploy to [https://prod-k8s.treetracker.org/wallet/](https://prod-k8s.treetracker.org/wallet/)v2, currently, the semantic release setting is (.releaserc)

```
{
  "branches": [
    '+([0-9])?(.{+([0-9]),x}).x',
    'main',
    'next',
    'next-major',
  ],
    "plugins": [
      ...
    ]
}
```

The code for v2 is in branch \`v2\`.&#x20;

Now, to release the v2, and switch v1 to maintenance:

1. Say, the current \`main\` version is 1.10.0, now create branch \`1.x\` from \`main\` branch.
2.  Change the release setting to:

    ```
    {
      "branches": [
        {name: '1.x', range: '1.x', channel: '1.x'},
        'main',
        'next',
        'next-major',
      ],
        "plugins": [
          ...
        ]
    }
    ```

    So the branch \`1.x\` will be taken as maintenance branch, and deployed to \`1.x\` channel. So we need to set the 1.x channel to point to [https://prod-k8s.treetracker.org/wallet/](https://prod-k8s.treetracker.org/wallet/)  (the current online url, by changing the Github Action) and we also need to change the default deployment to point to [https://prod-k8s.treetracker.org/wallet/](https://prod-k8s.treetracker.org/wallet/)v2, so the \`main\` branch will be deployed to that url.
3. Merge the branch \`v2\` to \`main\` branch, then the semantic release will calculate the version number, say, 2.0.0, and deploy the code to default channel, according to the change above, it would be [https://prod-k8s.treetracker.org/wallet/](https://prod-k8s.treetracker.org/wallet/)v2.
4. The following push to \`main\` will increate the version number, e.g. 2.1.0 and deploy to [https://prod-k8s.treetracker.org/wallet/](https://prod-k8s.treetracker.org/wallet/)v2 continuously.
5. If we want to fix a bug on 1.10.0:
   1. Push a commit with comment: "fix: a bug" to \`1.x\`.
   2. Get the new version number: 1.10.1
   3. Deploy 1.10.1 to 1.x channel: [https://prod-k8s.treetracker.org/wallet/](https://prod-k8s.treetracker.org/wallet/)
6. If we want to add a new feature on 1.x:
   1. Push a commit with comment: "feat: a feature" to \`1.x\`
   2. Get the new version number: 1.11
   3. Deploy 1.11 to [https://prod-k8s.treetracker.org/wallet/](https://prod-k8s.treetracker.org/wallet/)
7. If we accidentally add a break change on 1.x:
   1. Push a commit with comment: "... BREAKING CHANGE"
   2. Semantic release will throw an error and deny to generate new release.
   3. CAN NOT deploy 2.0.0 (according the rule of SR) to \`1.x\` channel.

So in this way, we can evolve new version on the branch \`main\` and maintain the version 1.x at the same time.

Some other consideration or scenarios:

* If we fixed a bug on \`main\` and now we also want to adapt it in the \`1.x\` because that the bug is also impact the 1.x version, and the opposite operation is also possible (to adopt change from 1.x to main)
  1. Cherry-pic the commit from the source and commit it to target.
  2. Semantic release calculate the version.
  3. Deploy it
