# CKEditor 5 - Common Integration Utils

[![npm version](https://badge.fury.io/js/%40ckeditor%2Fckeditor5-integrations-common.svg)](https://www.npmjs.com/package/@ckeditor/ckeditor5-integrations-common)
[![CircleCI](https://circleci.com/gh/ckeditor/ckeditor5-integrations-common.svg?style=shield)](https://app.circleci.com/pipelines/github/ckeditor/ckeditor5-integrations-common?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/ckeditor/ckeditor5-integrations-common/badge.svg?branch=master)](https://coveralls.io/github/ckeditor/ckeditor5-integrations-common?branch=master)
![Dependency Status](https://img.shields.io/librariesio/release/npm/@ckeditor/ckeditor5-integrations-common)

Official [CKEditor 5](https://ckeditor.com/ckeditor-5/) common integration utils. This package contains a set of utilities that are shared between CKEditor 5 framework integrations such like:

- [CKEditor 5 Vue integration](https://github.com/ckeditor/ckeditor5-vue)
- [CKEditor 5 React integration](https://github.com/ckeditor/ckeditor5-react)
- [CKEditor 5 Angular integration](https://github.com/ckeditor/ckeditor5-angular)

The prime example of such shared utility might be the CKEditor 5 Cloud integration loader that is used by all integrations to dynamically load the editor from the CDN.

It's highly recommended to not use this package directly in your application because it's intended to be used by through the integrations listed above. However, if you need to use it directly (because you are using framework that is not supported by the integrations), you can use it as a standalone package, but keep in mind that the API is designed to be used by the integrations and might not be user-friendly.

## Contributing

After cloning this repository, install the necessary dependencies:

```bash
npm install
```

You can also use [Yarn](https://yarnpkg.com/).

### Running the development server

You can start the development server using the command below:

```bash
npm run dev
```

### Executing tests

To test the editor integration against a set of automated tests, run the following command:

```bash
npm run test
```

If you want to run the tests in watch mode, use the following command:

```bash
npm run test:watch
```

### Building the package

To build the package that is ready to publish, use the following command:

```bash
npm run build
```

## Releasing package

CircleCI automates the release process and can release both channels: stable (`X.Y.Z`) and pre-releases (`X.Y.Z-alpha.X`, etc.).

Before you start, you need to prepare the changelog entries.

1. Make sure the `#master` branch is up-to-date: `git fetch && git checkout master && git pull`.
1. Prepare a release branch: `git checkout -b release-[YYYYMMDD]` where `YYYYMMDD` is the current day.
1. Generate the changelog entries: `yarn run changelog --branch release-[YYYYMMDD] [--from [GIT_TAG]]`.
    * By default, the changelog generator uses the latest published tag as a starting point for collecting commits to process.

      The `--from` modifier option allows overriding the default behavior. It is required when preparing the changelog entries for the next stable release while the previous one was marked as a prerelease, e.g., `@alpha`.

      **Example**: Let's assume that the `v40.5.0-alpha.0` tag is our latest and that we want to release it on a stable channel. The `--from` modifier should be equal to `--from v40.4.0`.
    * This task checks what changed in each package and bumps the version accordingly. It won't create a new changelog entry if nothing changes at all. If changes were irrelevant (e.g., only dependencies), it would make an "_internal changes_" entry.
    * Scan the logs printed by the tool to search for errors (incorrect changelog entries). Incorrect entries (e.g., ones without the type) should be addressed. You may need to create entries for them manually. This is done directly in CHANGELOG.md (in the root directory). Make sure to verify the proposed version after you modify the changelog.
1. Commit all changes and prepare a new pull request targeting the `#master` branch.
1. Ping the `@ckeditor/ckeditor-5-devops` team to review the pull request and trigger the release process.

## License

Licensed under a dual-license model, this software is available under:

* the [GNU General Public License Version 2 or later](http://www.gnu.org/licenses/gpl.html),
* or commercial license terms from CKSource Holding sp. z o.o.

For more information, see: [https://ckeditor.com/legal/ckeditor-licensing-options](https://ckeditor.com/legal/ckeditor-licensing-options).
