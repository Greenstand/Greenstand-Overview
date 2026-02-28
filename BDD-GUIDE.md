# BDD Guide for the Treetracker Admin Platform

This platform uses **Behaviour-Driven Development (BDD)** as the shared language between product, QA, and engineering. A feature's lifecycle flows in one direction:

```
Product Stakeholder          Test Engineer              Developer
writes .feature file   →   implements steps   →   implements feature
(Gherkin spec)              (WebdriverIO)           runs tests, ships report
```

The result is a living specification: the same file that describes a feature also proves it works, and a recorded video of the browser run is attached to every pull request so reviewers can see the behaviour without running the suite themselves.

---

## For Product Stakeholders

Your job is to write `.feature` files. These live in `features/` and are the authoritative description of what the software should do. Test engineers and developers implement against them — no feature file, no feature.

### Gherkin format

```gherkin
Feature: <name of the capability>

  Scenario: <one concrete situation>
    Given <the starting state>
    When  <the action the user takes>
    And   <additional action, if needed>
    Then  <the observable outcome>
```

Use `And` to chain steps of the same type. Each `Scenario` must be independently runnable — do not assume state from a previous scenario.

### Real example: `features/login.feature`

```gherkin
Feature: Login

  Scenario: Login with wrong credentials shows an error message
    Given I am on the login page
    When I enter username "admin" and password "wrongpwd"
    And I click the login button
    Then I should see an error message

  Scenario: Login with valid credentials succeeds
    Given I am on the login page
    When I enter username "test-dev" and password "5Z5971uQXV"
    And I click the login button
    Then I should be redirected away from the login page
```

### Rules for writing good scenarios

- **Write from the user's point of view.** "I click the login button", not "the submit handler is called".
- **One behaviour per scenario.** A scenario that tests both happy path and error state is hard to diagnose when it fails.
- **Use concrete values.** Parameterised strings like `"admin"` and `"wrongpwd"` give test engineers something to wire up without guessing.
- **Describe the observable outcome.** `Then I should see an error message` — something the user sees, not an internal state.
- **Avoid implementation detail.** The feature file should remain valid even if the UI is redesigned.

### Reviewing test results

After a developer runs the BDD suite and pushes the `reports/` folder, the Allure HTML report is published and accessible without any local setup:

**[https://greenstand.github.io/treetracker-admin-client/reports/allure-html/](https://greenstand.github.io/treetracker-admin-client/reports/allure-html/)**

Open this link to see every scenario listed by name, its pass/fail status, and a step-by-step breakdown. The test video (`reports/video/test-run.mp4`) is also in the same `reports/` folder on GitHub Pages and shows a live browser recording of the full test run.

**[https://greenstand.github.io/treetracker-admin-client/reports/video/test-run.mp4](https://greenstand.github.io/treetracker-admin-client/reports/video/test-run.mp4)**

As a stakeholder, you can use this to verify that the feature you described behaves exactly as written — no access to a development environment needed.

### Where to put new feature files

```
features/
  login.feature          ← existing
  verify-captures.feature   ← new file you create
  grower-search.feature
```

One file per feature area. Name it after the capability, lowercase with hyphens.

---

## For Test Engineers

You receive `.feature` files from stakeholders and turn each step into executable code. The toolchain is **WebdriverIO + Cucumber**.

### File layout

```
features/
  login.feature                          ← from stakeholder
  step-definitions/
    login.steps.js                       ← you write this
  page-objects/
    LoginPage.js                         ← you write this
```

Each feature should have a matching step-definitions file and (usually) a page object for the UI elements it touches.

### Step definitions

Import the Cucumber step helpers and wire each step text to a function. The string in `Given/When/Then` must match the feature file **exactly** (WebdriverIO uses it as a pattern).

```js
// features/step-definitions/login.steps.js
const { Given, When, Then } = require('@cucumber/cucumber');
const loginPage = require('../page-objects/LoginPage');

Given('I am on the login page', async () => {
  await browser.url('/');
});

When('I enter username {string} and password {string}', async (username, password) => {
  await loginPage.usernameInput.setValue(username);
  await loginPage.passwordInput.setValue(password);
});

When('I click the login button', async () => {
  await loginPage.submitButton.click();
});

Then('I should see an error message', async () => {
  await expect(loginPage.errorMessage).toBeDisplayed();
});

Then('I should be redirected away from the login page', async () => {
  await browser.waitUntil(
    async () => !(await browser.getUrl()).includes('/login'),
    { timeout: 10000, timeoutMsg: 'Expected URL to leave /login after login' }
  );
});
```

Use `{string}` (with curly braces) in step text to capture quoted values from the feature file as function arguments.

### Page objects

Keep all element selectors in page objects, not in step definitions. This makes reskinning the UI a one-file change.

```js
// features/page-objects/LoginPage.js
class LoginPage {
  get usernameInput() { return $('#userName'); }
  get passwordInput() { return $('#password'); }
  get submitButton()  { return $('button[type="submit"]'); }
  get errorMessage()  { return $('h6'); }

  async login(username, password) {
    await this.usernameInput.setValue(username);
    await this.passwordInput.setValue(password);
    await this.submitButton.click();
  }
}

module.exports = new LoginPage();
```

Use WebdriverIO's `$()` with CSS selectors. Prefer stable attributes (`id`, `data-testid`, `type`) over positional selectors like `nth-child`.

### Running the suite

The app must be running before you start WebdriverIO:

```bash
# Terminal 1 — start the app
npm start          # runs on http://localhost:3001

# Terminal 2 — run all BDD tests
npm run wdio
```

To run a single feature file while building out steps:

```bash
npx wdio run wdio.conf.js --spec features/login.feature
```

If a step has no implementation yet, WebdriverIO prints a snippet — copy it into your step definitions file and fill in the body.

### What the runner does automatically

- Captures screenshots at 2 fps during the entire run
- Stitches them into `reports/video/test-run.mp4` via ffmpeg after the run completes
- Writes Allure result data to `reports/allure-results/`

You do not need to configure any of this — it is handled by `wdio.conf.js`.

---

## For Developers

You receive a feature file (and possibly partially-written step definitions) and your job is to:

1. Implement the feature in the React app
2. Make the BDD tests pass
3. Generate a report and video
4. Attach the video to your pull request

### Prerequisites

| Tool | How to get it |
|------|--------------|
| Node ≥ 18 | `nvm use` or install from nodejs.org |
| ChromeDriver | Place the matching binary at `.drivers/chromedriver` |
| ffmpeg | Required to produce `test-run.mp4`; update the path in `wdio.conf.js` if not at `/Users/deanchen/soft/ffmpeg` |

### Development loop

```bash
# Start the app
npm start

# In another terminal — run just the feature you're working on
npx wdio run wdio.conf.js --spec features/login.feature
```

Iterate until all scenarios are green. The runner exits non-zero on any failure, so you can rely on the exit code in scripts.

### Generate the Allure HTML report

After a successful run:

```bash
npm run wdio:report
```

This generates `reports/allure-html/` and opens it in your browser. The report shows each scenario, its steps, pass/fail status, and timestamps.

### The test video

`reports/video/test-run.mp4` is produced automatically at the end of every `npm run wdio` run. It is a 2 fps screen capture of the full browser session — enough to see each page transition and form interaction.

### Pull request checklist

Before opening a PR for any change involving a new or modified feature:

1. Run `npm run wdio` — all scenarios must be green.
2. Run `npm run wdio:report` — confirm the HTML report looks correct.
3. Commit or upload `reports` to the PR, please remove the old one before generate a new one, otherwise the PR will be too large to review.
4. Reference the `.feature` file in the PR description so reviewers know which scenario is being validated.

Reviewers can watch the video without pulling the branch or running a local environment.

### Conventional commit for BDD work

```
test(login): add BDD scenarios for invalid credentials

Implements step definitions and page object for the login feature.
All 2 scenarios pass; video attached.
```

Use `test` as the type for commits that add or fix test/BDD coverage. Use `feat` when you are also shipping application code alongside the test.
