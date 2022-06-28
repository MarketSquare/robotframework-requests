# How to contribute

## Setup a development environment

1) First of all make sure to have a 3.x python version installed
2) Clone the source code:
    `git clone git@github.com:MarketSquare/robotframework-requests.git`
3) I suggest to create a python virtual environment:
```sh
    cd robotframework-requests/
    python -m venv venv
    source venv/bin/activate
```
4) Install the library in editing mode and all the test dependencies:
    `python -m pip install -e '.[test]'`
5) Run acceptance tests with robot:
    `robot ./atests`
6) Run unit tests wiht pytest:
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

Keywords documentation (on Linux) can be updated running the following script:

`doc/generate_doc.sh`

# What can I do?

In this [GitHub Project Board](https://github.com/MarketSquare/robotframework-requests/projects/1)
are mainly tracked the priorities and plans for the next versions.

Of course you can always reply to issues and review pull requests.

## Robot Framework Milano Meetup
During the 17th April 2020 meetup we had the following todo list. 

### New plans for 0.8 version
- [X] **Feature:** [New On Session keywords](https://github.com/MarketSquare/robotframework-requests/issues/276)
- [X] **Experiment:** [Reorganize Keywords in classes](https://github.com/MarketSquare/robotframework-requests/issues/270)
- [X] **Documentation:** Write a better introductive documentation to keywords (session best practices, parameters description, response object)

### Early Adopters and feedback needed for pre-release versions
You can install pre-release versions in this way:

    pip install robotframework-requests --pre

### Others
- [X] **Review PR:** [Support sending arrays in query string and request body](https://github.com/MarketSquare/robotframework-requests/pull/220)
- [ ] **Review PR:** [disable cert warnings](https://github.com/MarketSquare/robotframework-requests/pull/209)
- [X] **Feature:** [Allow passing auth param to create client cert session](https://github.com/MarketSquare/robotframework-requests/issues/245)
- [X] **Tech:** [Deprecate To Json keyword in favor of response.json attribute](https://github.com/MarketSquare/robotframework-requests/issues/219)
- [ ] **Tech**: Moving all tests to local http server (Flask)
- [ ] **Challenge**: Start local http server (Flask) only once per test run instead of start/stop for each suite

### Reply / close issues as you will :)
https://github.com/MarketSquare/robotframework-requests/issues
