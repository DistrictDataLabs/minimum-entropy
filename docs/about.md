# About Minimum Entropy     

Minimum Entropy is a fork of [Kyudo](https://github.com/mclumd/kyudo), a knowledge goal casebase management and annotation tool. Kyudo was designed to create a corpus with which to explore case-based reasoning and automatic knowledge goal solutions in an artificial intelligence setting and was set up similarly to a Q&A application like [StackExchange](http://stackexchange.com/) or [Quora](https://www.quora.com/).

### Name Origin

[Maximum Entropy](https://en.wikipedia.org/wiki/Multinomial_logistic_regression) is a classification method that is used to predict the probabilities of different possible outcomes of a categorically distributed dependent variable. It uses a principle such that the probability which best represents the current state of knowledge is the one with the largest [entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)). Entropy refers to uncertainty, and in a question and answer site, uncertainty is bad. Therefore we've named the site minimum entropy to reflect the fact that we are trying to minimize uncertainty in order to best represent the current state of knowledge.

### Contributing

Minimum Entropy is open source, and we would love your help to develop the site, particularly if you are a Django or Front-End developer! You can contribute in the following ways:

1. Add issues or bugs to the bug tracker: [https://github.com/DistrictDataLabs/minimum-entropy/issues](https://github.com/DistrictDataLabs/minimum-entropy/issues)
2. Work on a card on the dev board: [https://waffle.io/DistrictDataLabs/minimum-entropy](https://waffle.io/DistrictDataLabs/minimum-entropy)
3. Create a pull request in Github: [https://github.com/DistrictDataLabs/minimum-entropy/pulls](https://github.com/DistrictDataLabs/minimum-entropy/pulls)

The repository is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. Please make sure that all pull requests go into the _develop_ branch; pulls to master will not be considered. A typical workflow is as follows:

1. Select a card from the [dev board](https://waffle.io/DistrictDataLabs/minimum-entropy) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        ~$ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested) merge your feature into develop.

        ~$ git checkout develop
        ~$ git merge --no-ff feature-myfeature
        ~$ git branch -d feature-myfeature
        ~$ git push origin develop

4. Repeat. Releases will be routinely pushed into master via release branches, then deployed to the server.

## Contributors

Thank you for all your help contributing to make Minimum Entropy a great project!

### Maintainers

- Benjamin Bengfort: [@bbengfort](https://github.com/bbengfort/)

### Contributors

- Your name here!

## Changelog

The release versions that are sent to the Python package index (PyPI) are also tagged in Github. You can see the tags through the Github web application and download the tarball of the version you'd like. Additionally PyPI will host the various releases of Trinket (eventually).

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bug fixes or other micro changes that developers should feel free to immediately update to.

### Version 1.0 Beta 1

* **tag**: [v1.0b1](https://github.com/DistrictDataLabs/minimum-entropy/releases/tag/v1.0b1)
* **deployment**: Tuesday, July 5, 2016
* **commit**: [256a4e6](https://github.com/DistrictDataLabs/minimum-entropy/commit/256a4e6eb45d49b0e1927a3bcd201848f474b5c0)

This beta release for Version 1.0 simply moves the code over from Kyudo and modifies it to remove the research components and only present a question and answer system. Things are not perfect since the app was designed for a different research project. However, the core functionality - asking questions and answering them with Markdown, as well as up and down voting exists. This is a good start to beta to our faculty to see what they think!
