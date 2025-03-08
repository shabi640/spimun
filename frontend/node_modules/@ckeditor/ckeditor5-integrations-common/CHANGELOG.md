Changelog
=========

## [2.2.3](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v2.2.2...v2.2.3) (2025-02-12)

### Features

* Added support for loading more testing versions in CDN loader. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/af0384bdd76b49c91852cf98174a2ed76e6fd06a))


## [2.2.2](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v2.2.1...v2.2.2) (2024-11-19)

### Features

* Improved error messages in `loadCKEditorCloud` when using editor version not supporting CDN distribution. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/390bac703e2a72cd8dcac5681a8998507d3bf63a))


## [2.2.1](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v2.2.0...v2.2.1) (2024-11-04)

### Features

* Add testing versions support to injector. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/518448b1e7e9e8b8866592ff2b7daca3869f73b3))


## [2.2.0](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v2.1.0...v2.2.0) (2024-10-29)

### Features

* Added the `createCustomCdnUrl` configuration option to override default CKEditor 5 Cloud CDN URLs in `loadCKEditorCloud`. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/f13ee317b8ee65a79525824d04ebeeb27b52700b))
* Added support for passing a translations list for CKBox in the configuration for `loadCKEditorCloud`. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/29f8aaf3a82904fc1598a4f81d3803e587d639e2))
* Improved detection of already installed versions of the editor. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/adc3143d032a2501c0a5872cb92a36938d720f5a))


## [2.1.0](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v2.0.0...v2.1.0) (2024-09-26)

### Features

* Better error messages in `loadCKEditorCloud`. It now detects existing editor installations and gives migration info from NPM to CDN. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/a57de9cd4e996ff151c599e810db1d33ca380be8))

### Bug fixes

* `ckeditor5-premium-features` is no longer required to be installed. It should no longer raise TypeScript compilation errors while using this package with `tsconfig.json` file with `skipLibCheck: false` option. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/72b9b8269868cc962a19a1ebdf767b0b1b20dfaa))
* Removed aliases in `src/` files to fix incorrect `.d.ts` output. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/7fe1f75fe16b8f5e7af93a50f4a11ecabccc5087))


## [2.0.0](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v1.0.0...v2.0.0) (2024-09-12)

### BREAKING CHANGES

* The `languages` configuration property has been renamed to `translations` in `loadCKEditorCloud`.

### Features

* Add the `crossorigin=anonymous` attribute to all CDN resource tags to prevent CORS issues. Closes https://github.com/ckeditor/ckeditor5-integrations-common/issues/30. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/78587c987dc4d70154db2f1b88455a430b542ac0))
* Add the `injectedHtmlElementsAttributes` attribute to the `loadCKEditorCloud` configuration, allowing the addition of `nonce` and other custom attributes to injected elements. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/78587c987dc4d70154db2f1b88455a430b542ac0))
* `CKEditorCloudResult` now returns more narrowly typed attributes for `CKBox` and `CKEditorPremiumFeatures`, taking into account `CKEditorCloudConfig`. Closes [#24](https://github.com/ckeditor/ckeditor5-integrations-common/issues/24). ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/30de408f43b85f5f91c64b7d243ca4b773348e9a))
* The `en` language is no longer loaded when passed in `translations` as it is prebundled. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/25e41b6b199ff616b496b9ac63d610d8d35cf1ea))

### Bug fixes

* Rename the `languages` configuration property to `translations` in `loadCKEditorCloud`. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/25e41b6b199ff616b496b9ac63d610d8d35cf1ea))


## [1.0.0](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v0.2.1...v1.0.0) (2024-09-04)

We are happy to announce the first stable release of `@ckeditor/ckeditor5-integrations-common`, a package containing utility modules for integrating with CKEditor 5.

Below, you can find changes compared to the latest non-stable release.

### Features

* CSS scripts are now injected at the beginning of the document head, allowing for easier overriding of editor styles. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/cd61e7ce7baad29adefd275661c9ca7ef5006095))

### Bug fixes

* Ensure that preload link tags are injected before stylesheet link tags. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/d61b83e8ffede29debcc11c4be2798ad30d527e4))


## [0.2.1](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v0.2.0...v0.2.1) (2024-08-27)

### Bug fixes

* Export missing `CdnPluginsPacks` typing, which is used in integrations. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/43e7c51e0e3d79ae27bf3edef77a4c2991880801))


## [0.2.0](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v0.1.1...v0.2.0) (2024-08-27)

### Bug fixes

* No longer raise `export modifier cannot be applied to ambient modules` error on older TS versions. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/15bca0a5f559738558dde08603d16445cb91d349))

### Features

The API interface of the `loadCKEditorCloud` method has been simplified, and the ability to specify the `CKBox` theme has been added. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/tree/e45c569661b1686d153e12a31c146c46751396e6))

## [0.1.1](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v0.1.0...v0.1.1) (2024-08-20)

### Bug fixes

* Add missing CKEditor window variables to the final `index.d.ts` bundle. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/09e84c8270633c38c7857754219776659a4cfee2))


## [0.1.0](https://github.com/ckeditor/ckeditor5-integrations-common/compare/v0.0.1...v0.1.0) (2024-08-20)

### Features

The initial version of the cloud integration utils implementation. ([commit](https://github.com/ckeditor/ckeditor5-integrations-common/commit/c7e447058302a9f788a7a5abababe787b721b5f5))


## 0.0.1 (2024-08-19)

This is an initial package for development purposes. It does not contain code yet.
