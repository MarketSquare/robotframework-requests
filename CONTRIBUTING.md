# How to contribute

## Setup a development environment

1) First of all make sure to have a 3.x python version installed
2) I suggest to create a python virtual environment
3) Install the library in editing mode and all the test dependencies:
    `python -m pip install -e .[test]`
4) Run acceptance tests with robot:
    `robot ./atests`
5) Run unit tests wiht pytest:
    `pytest ./utests`

If everything went well now you're ready to go!

## Coding guidelines

Many checks and tests are automatically performed in Continuous Integration with the
GitHub Actions.

Have a look at the file `.github/workflows/pythonapp.yml` to see the commands used. 

#### Linting

The project uses flake8 for linting the source code.

#### Unit tests

PyTest is integrated for unit tests that located in `utests/` folder.

#### Acceptance tests

Obviously for acceptance tests Robot Framework is used, files are located in `atests/`.
   
#### Test Coverage

Test coverage is evaluated for unit and acceptance tests, after test execution 
`coverage report` command shows you the statistics. 

#### Documentation

Keywords documentation can be updated running the following command:

`python -m robot.libdoc src/RequestsLibrary doc/RequestsLibrary.html`

# What can I do?

In this [GitHub Project Board](https://github.com/MarketSquare/robotframework-requests/projects/1)
are mainly tracked the priorities and plans for the next versions.

Of course you can always reply to issues and review pull requests.

## Robot Framework Milano Meetup
During the 17th April 2020 meetup we had the following todo list. 

### New upcoming 0.7 version
- [X] **Review PR:** [Add a post method that allows sending binary data ](https://github.com/MarketSquare/robotframework-requests/pull/224) [Nello]
- [ ] **Feature:** [New On Session keywords](https://github.com/MarketSquare/robotframework-requests/issues/276) [Angelo, Nicola, Roberta]
- [X] **Fix:** [Continuous Integration on Windows](https://github.com/MarketSquare/robotframework-requests/issues/271) [Vincenzo, Diego]
- [X] **Tech:** [Integrate PyTest in CI](https://github.com/MarketSquare/robotframework-requests/issues/277) [Luca, Andrea, Kiro]

### New plans for 1.0 major version
- [ ] **Experiment:** [Reorganize Keywords in classes](https://github.com/MarketSquare/robotframework-requests/issues/270)

### Others
- [ ] **Review PR:** [Support sending arrays in query string and request body](https://github.com/MarketSquare/robotframework-requests/pull/220)
- [ ] **Review PR:** [disable cert warnings](https://github.com/MarketSquare/robotframework-requests/pull/209)
- [ ] **Feature:** [Allow passing auth param to create client cert session](https://github.com/MarketSquare/robotframework-requests/issues/245)
- [ ] **Tech:** [Deprecate To Json keyword in favor of response.json attribute](https://github.com/MarketSquare/robotframework-requests/issues/219)
- [ ] **Tech**: Moving all tests to local http server (Flask)
- [ ] **Challenge**: Start local http server (Flask) only once per test run instead of start/stop for each suite [Vincenzo, Diego]

### Reply / close issues as you will :)
https://github.com/MarketSquare/robotframework-requests/issues
