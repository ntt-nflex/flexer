# Change Log

## [v1.7.5](https://github.com/ntt-nflex/flexer/tree/v1.7.5) (June 10, 2021)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.7.4...v1.7.5)

### Changes:

- Add the property `extra-headers` in `.flexer.yaml` to specify additional headers.
- Add `--extra-header` param to `flexer config add-region` to specify the above.

## [v1.7.4](https://github.com/ntt-nflex/flexer/tree/v1.7.4) (July 30, 2020)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.7.3...v1.7.4)

### Changes:

- Fixed bug causing the message `execute() got an unexpected keyword argument 'async'`

## [v1.7.3](https://github.com/ntt-nflex/flexer/tree/v1.7.3) (Feb 14, 2020)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.7.2...v1.7.3)

### Changes:

- Testing credential validation now allows exception to be returned

## [v1.7.2](https://github.com/ntt-nflex/flexer/tree/v1.7.2) (Nov 05, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.7.1...v1.7.2)

### Changes:

- Add support for handlers file on flexer upload

## [v1.7.1](https://github.com/ntt-nflex/flexer/tree/v1.7.1) (Oct 02, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.7.0...v1.7.1)

### Changes:

- Print the payload of API error responses in the CLI tool

## [v1.7.0](https://github.com/ntt-nflex/flexer/tree/v1.7.0) (Sep 27, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.11...v1.7.0)

### Changes:

- Remove result validation

## [v1.6.11](https://github.com/ntt-nflex/flexer/tree/v1.6.11) (Sep 04, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.10...v1.6.11)

### Changes:

- Update `event_sources`, `languages` and `sync` parameters.

## [v1.6.10](https://github.com/ntt-nflex/flexer/tree/v1.6.10) (Aug 12, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.9...v1.6.10)

### Changes:

- Update metric pattern to allow specialisations

## [v1.6.9](https://github.com/ntt-nflex/flexer/tree/v1.6.9) (Aug 12, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.8...v1.6.9)

### Changes:

- Update requirements.txt

## [v1.6.8](https://github.com/ntt-nflex/flexer/tree/v1.6.8) (Aug 12, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.7...v1.6.8)

### Changes:

- Only import MongoClient from pymongo

## [v1.6.7](https://github.com/ntt-nflex/flexer/tree/v1.6.7) (Aug 12, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.6...v1.6.7)

### Changes:

- Pinning pymongo version to 3.6.0 ([@surbias](https://github.com/surbias))

## [v1.6.6](https://github.com/ntt-nflex/flexer/tree/v1.6.6) (Aug 9, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.5...v1.6.6)

### Changes:

- Add metric name pattern [\#73](https://github.com/ntt-nflex/flexer/pull/73) ([@surbias](https://github.com/surbias))

## [v1.6.5](https://github.com/ntt-nflex/flexer/tree/v1.6.5) (Apr 26, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.4...v1.6.5)

### Changes:

- Use new PyYAML 5.1 loader method to remove warning [\#72](https://github.com/ntt-nflex/flexer/pull/72) ([@lukewallis](https://github.com/lukewallis))

## [v1.6.4](https://github.com/ntt-nflex/flexer/tree/v1.6.4) (Apr 18, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.3...v1.6.4)

### Changes:

- Add a new `resource-action` event source [\#70](https://github.com/ntt-nflex/flexer/pull/70) ([@ka0riito](https://github.com/ka0riito))
- Pin jsonschema to the last working version before the major version jump [\#71](https://github.com/ntt-nflex/flexer/pull/71) ([@twosevenska](https://github.com/twosevenska))

## [v1.6.3](https://github.com/ntt-nflex/flexer/tree/v1.6.3) (Feb 09, 2019)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.2...v1.6.3)

### Changes:

- Add user_name to the Context object

## [v1.6.2](https://github.com/ntt-nflex/flexer/tree/v1.6.2) (Dec 04, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.1...v1.6.2)

### Changes:

- Send a useful User-Agent header from the CMP client [\#69](https://github.com/ntt-nflex/flexer/pull/69) ([@benpaxton-hf](https://github.com/benpaxton-hf))

## [v1.6.1](https://github.com/ntt-nflex/flexer/tree/v1.6.1) (Oct 29, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.6.0...v1.6.1)

### Changes:

- Rename async variables to prevent invalid syntax in Python3 [\#67](https://github.com/ntt-nflex/flexer/pull/67) ([@lcayolap](https://github.com/lcayolap))
- Fixed issue with filter len for Python3 [\#68](https://github.com/ntt-nflex/flexer/pull/68) ([@lcayolap](https://github.com/lcayolap))

## [v1.6.0](https://github.com/ntt-nflex/flexer/tree/v1.6.0) (Sep 06, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.5.2...v1.6.0)

### Changes:

- Change the rest-api response header values validation from a list of strings to a string

## [v1.5.2](https://github.com/ntt-nflex/flexer/tree/v1.5.2) (Aug 08, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.5.1...v1.5.2)

### Changes:

- Fix pip v10 missing main module issue [\#66](https://github.com/ntt-nflex/flexer/pull/66) ([@s-kashif](https://github.com/s-kashif))

## [v1.5.1](https://github.com/ntt-nflex/flexer/tree/v1.5.1) (July 24, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.5.0...v1.5.1)

### Changes:

- Unpin jsonschema

## [v1.5.0](https://github.com/ntt-nflex/flexer/tree/v1.5.0) (June 29, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.4.3...v1.5.0)

### Changes:

- Add region, platform and version (flexer version) fields to the Context object
- Add customer_id and user_id fields to the Context object from the module execution request

## [v1.4.3](https://github.com/ntt-nflex/flexer/tree/v1.4.3) (June 18, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.4.2...v1.4.3)

### Changes:

- Remove validation of resource_type

## [v1.4.2](https://github.com/ntt-nflex/flexer/tree/v1.4.2) (May 23, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.4.1...v1.4.2)

### Changes:

- Allow 1-6 digits in timestamp microseconds [\#64](https://github.com/ntt-nflex/flexer/pull/64) ([@boncheff](https://github.com/boncheff))

## [v1.4.1](https://github.com/ntt-nflex/flexer/tree/v1.4.1) (Apr 30, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.4.0...v1.4.1)

### Changes:

- Do not use parse_requirements from pip as its no longer exposed after version 10 [\#63](https://github.com/ntt-nflex/flexer/pull/63) ([@praveenabraham](https://github.com/praveenabraham))

## [v1.4.0](https://github.com/ntt-nflex/flexer/tree/v1.4.0) (Feb 21, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.31...v1.4.0)

### Changes:

- Add validation for the MongoDB connection strings in the `context.database` method

## [v1.3.31](https://github.com/ntt-nflex/flexer/tree/v1.3.31) (Jan 30, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.30...v1.3.31)

### Changes:

- Add nflex scheduler base data to event on test set up [\#62](https://github.com/ntt-nflex/flexer/pull/62) ([@Surbias](https://github.com/Surbias))

## [v1.3.30](https://github.com/ntt-nflex/flexer/tree/v1.3.30) (Jan 29, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.29...v1.3.30)

### Changes:

- Support account_id in single resource / per account schedule environment [\#61](https://github.com/ntt-nflex/flexer/pull/61) ([@Surbias](https://github.com/Surbias))

## [v1.3.29](https://github.com/ntt-nflex/flexer/tree/v1.3.29) (Jan 25, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.28...v1.3.29)

### Changes:

- Explicitly skip logs tests [\#60](https://github.com/ntt-nflex/flexer/pull/60) ([@Surbias](https://github.com/Surbias))

## [v1.3.28](https://github.com/ntt-nflex/flexer/tree/v1.3.28) (Jan 25, 2018)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.27...v1.3.28)

### Changes:

- Add the ability to explicitly skip logs testing on config.yaml [\#59](https://github.com/ntt-nflex/flexer/pull/59) ([@Surbias](https://github.com/Surbias))

## [v1.3.27](https://github.com/ntt-nflex/flexer/tree/v1.3.27) (Dec 22, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.26...v1.3.27)

### Changes:

- Add validation for currencies in the spend connectors [\#58](https://github.com/ntt-nflex/flexer/pull/58) ([@praveenabraham](https://github.com/praveenabraham))

## [v1.3.26](https://github.com/ntt-nflex/flexer/tree/v1.3.26) (Nov 22, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.25...v1.3.26)

### Changes:

- Update the expected level values for status connectors
- Run the validators for connector result payload in the base tests

## [v1.3.25](https://github.com/ntt-nflex/flexer/tree/v1.3.25) (Nov 22, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.24...v1.3.25)

### Changes:

- Update the expected format of the metrics, logs and status connectors event

## [v1.3.24](https://github.com/ntt-nflex/flexer/tree/v1.3.24) (Oct 24, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.23...v1.3.24)

### Changes:

- Add a new `cmp-connector.status` event source and base connector tests for it
- Add a new `rest-api` event source

## [v1.3.23](https://github.com/ntt-nflex/flexer/tree/v1.3.23) (Oct 11, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.22...v1.3.23)

### Changes:

- Don't require the `body` field in the result of `rest-api` modules if the `status_code` is 204

## [v1.3.22](https://github.com/ntt-nflex/flexer/tree/v1.3.22) (Oct 10, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.21...v1.3.22)

### Changes:

- Change `last_update` field in the logs connector result to be either a timestamp or a number

## [v1.3.21](https://github.com/ntt-nflex/flexer/tree/v1.3.21) (Oct 5, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.20...v1.3.21)

### Changes:

- Fix spend validation schemas [\#53](https://github.com/ntt-nflex/flexer/pull/53) ([@praveenabraham](https://github.com/praveenabraham))

## [v1.3.20](https://github.com/ntt-nflex/flexer/tree/v1.3.20) (Sep 29, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.19...v1.3.20)

### Changes:

- Add an `--event-source` parameter to `flexer run` and update the spend validation [\#52](https://github.com/ntt-nflex/flexer/pull/52) ([@praveenabraham](https://github.com/praveenabraham))

## [v1.3.19](https://github.com/ntt-nflex/flexer/tree/v1.3.19) (Sep 22, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.18...v1.3.19)

### Changes:

- Make `expected_metrics` and `expected_logs` config fields optional [\#49](https://github.com/ntt-nflex/flexer/pull/49) ([@k-yoshihara](https://github.com/k-yoshihara))
- Simplify the assertions in the logs and metrics connector tests [\#50](https://github.com/ntt-nflex/flexer/pull/50) ([@k-yoshihara](https://github.com/k-yoshihara))
- Support the `--auth` parameter in the `test` command

## [v1.3.18](https://github.com/ntt-nflex/flexer/tree/v1.3.18) (Sep 22, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.17...v1.3.18)

### Changes:

- Add `amount_accumulative` into the spend schema and test it [\#46](https://github.com/ntt-nflex/flexer/pull/46) ([@victorliun](https://github.com/victorliun))

## [v1.3.17](https://github.com/ntt-nflex/flexer/tree/v1.3.17) (Sep 20, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.16...v1.3.17)

### Changes:

- Try to get env variables with "AUTH\_" prefix first in the base connector tests [\#45](https://github.com/ntt-nflex/flexer/pull/45) ([@boncheff](https://github.com/boncheff))

## [v1.3.16](https://github.com/ntt-nflex/flexer/tree/v1.3.16) (Sep 19, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.15...v1.3.16)

### Changes:

- Add spend JSON schema validator [\#44](https://github.com/ntt-nflex/flexer/pull/44) ([@victorliun](https://github.com/victorliun))

## [v1.3.15](https://github.com/ntt-nflex/flexer/tree/v1.3.15) (Sep 19, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.14...v1.3.15)

### Changes:

- Change the format of the expected logs in the base connector tests [\#43](https://github.com/ntt-nflex/flexer/pull/43) ([@Surbias](https://github.com/Surbias))

## [v1.3.14](https://github.com/ntt-nflex/flexer/tree/v1.3.14) (Sep 15, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.13...v1.3.14)

### Changes:

- Add support to test `get_logs` in multiple regions. `resource` and `logs_resource` are now optional [\#41](https://github.com/ntt-nflex/flexer/pull/41) ([@Surbias](https://github.com/Surbias))

## [v1.3.13](https://github.com/ntt-nflex/flexer/tree/v1.3.13) (Sep 13, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.12...v1.3.13)

### Changes:

- Add validation for the serverity key in the `get_logs` result [\#39](https://github.com/ntt-nflex/flexer/pull/39) ([@k-yoshihara](https://github.com/k-yoshihara))

## [v1.3.12](https://github.com/ntt-nflex/flexer/tree/v1.3.12) (Sep 11, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.11...v1.3.12)

### Changes:

- Add base connector tets for the `get_logs` handler [\#38](https://github.com/ntt-nflex/flexer/pull/38) ([@k-yoshihara](https://github.com/k-yoshihara))

## [v1.3.11](https://github.com/ntt-nflex/flexer/tree/v1.3.11) (Sep 05, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.10...v1.3.11)

### Changes:

- Add SSL and timeout options to the pymongo client (context.database)
- Fix the context.log error handling [\#36](https://github.com/ntt-nflex/flexer/pull/36) ([@Surbias](https://github.com/Surbias))
- Add `original_metric` property to the metrics connector results [\#37](https://github.com/ntt-nflex/flexer/pull/37) ([@Surbias](https://github.com/Surbias))

## [v1.3.10](https://github.com/ntt-nflex/flexer/tree/v1.3.10) (Aug 30, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.9...v1.3.10)

### Changes:

- Add monitoring_system to the metrics result [\#35](https://github.com/ntt-nflex/flexer/pull/35) ([@han](https://github.com/han))

## [v1.3.9](https://github.com/ntt-nflex/flexer/tree/v1.3.9) (Aug 29, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.8...v1.3.9)

### Changes:

- Add support for NflexDB, via context.database method

## [v1.3.8](https://github.com/ntt-nflex/flexer/tree/v1.3.8) (Aug 25, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.7...v1.3.8)

### Changes:

- Support multiple resources in config.yaml [\#34](https://github.com/ntt-nflex/flexer/pull/34) ([@SafariMonkey](https://github.com/SafariMonkey))

## [v1.3.7](https://github.com/ntt-nflex/flexer/tree/v1.3.7) (Aug 24, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.6...v1.3.7)

### Changes:

- Add --keywords option to flexer test command to allow selecting which test cases to run
- Send a `nosync=true` parameter when patching zip modules as uploading the zip file will trigger a notification anyway

## [v1.3.6](https://github.com/ntt-nflex/flexer/tree/v1.3.6) (Aug 07, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.5...v1.3.6)

### Changes:

- Relax timestamp validation for `get_logs()`

## [v1.3.5](https://github.com/ntt-nflex/flexer/tree/v1.3.5) (Aug 07, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.4...v1.3.5)

### Changes:

- Add `context.state.delete` and `context.state.delete_multi` methods to clean up keys from the module state

## [v1.3.4](https://github.com/ntt-nflex/flexer/tree/v1.3.4) (Aug 01, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.3...v1.3.4)

### Changes:

- Unified error messaging [\#33](https://github.com/ntt-nflex/flexer/pull/33) ([@burbon](https://github.com/burbon))
- Relax the timestamp regex for metrics validation

## [v1.3.3](https://github.com/ntt-nflex/flexer/tree/v1.3.3) (Jul 28, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.2...v1.3.3)

### Changes:

- Add validation for rest-api modules
- Fix the runner to return a null value if there are validation errors

## [v1.3.2](https://github.com/ntt-nflex/flexer/tree/v1.3.2) (Jul 28, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.1...v1.3.2)

### Changes:

- Add environment variable to enable log on stdout [\#32](https://github.com/ntt-nflex/flexer/pull/32) ([@ukinau](https://github.com/ukinau))

## [v1.3.1](https://github.com/ntt-nflex/flexer/tree/v1.3.1) (Jul 26, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.3.0...v1.3.1)

### Changes:

- Add CLI tool support for go (Go 1.8.3)

## [v1.3.0](https://github.com/ntt-nflex/flexer/tree/v1.3.0) (Jul 21, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.10...v1.3.0)

### Changes:

- Add support for python3

## [v1.2.10](https://github.com/ntt-nflex/flexer/tree/v1.2.10) (Jul 20, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.9...v1.2.10)

### Changes:

- Added circuit resource type to flexer [\#31](https://github.com/ntt-nflex/flexer/pull/31) ([@emlynfelix](https://github.com/emlynfelix))

## [v1.2.9](https://github.com/ntt-nflex/flexer/tree/v1.2.9) (Jul 12, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.8...v1.2.9)

### Changes:

- Add optional attributes to metrics return value [\#30](https://github.com/ntt-nflex/flexer/pull/30) ([@han](https://github.com/han))

## [v1.2.8](https://github.com/ntt-nflex/flexer/tree/v1.2.8) (Jul 03, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.7...v1.2.8)

### Fixes:

- Fix the error handling in the FlexerRemoteState object

## [v1.2.7](https://github.com/ntt-nflex/flexer/tree/v1.2.7) (Jun 29, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.6...v1.2.7)

### Changes:

- Added dummy resource information

## [v1.2.6](https://github.com/ntt-nflex/flexer/tree/v1.2.6) (Jun 29, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.5...v1.2.6)

### Changes:

- Exit with 1 error code if there are any test failures
- Add Hush parameters to flexer test
- Add Hush parameters to flexer run cli

## [v1.2.5](https://github.com/ntt-nflex/flexer/tree/v1.2.5) (Jun 08, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v.1.2.4...v1.2.5)

### Changes:

- Added more connector credentials validation tests
- Moved module lib path before system lib when running the flexer cli

## [v1.2.4](https://github.com/ntt-nflex/flexer/tree/v.1.2.4) (Jun 01, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.3...v.1.2.4)

### Changes:

- Automatically generate a config file with no credentials if not present

## [v1.2.3](https://github.com/ntt-nflex/flexer/tree/v1.2.3) (Jun 01, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.2...v1.2.3)

### Changes:

- Add a `flexer config add-region` sub-command
- Add a `--version` parameter

### Fixes:

- Print the results from executions to stdout instead of stderr
- Add the six requirement so the tool can be successfully installed in a virtual environment with setuptools>=34.0.0
- Fix a typo in the module update command output

## [v1.2.2](https://github.com/ntt-nflex/flexer/tree/v1.2.2) (May 31, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.1...v1.2.2)

### Fixes:

- Update the config cmp credentials keys in the base connector tests

## [v1.2.1](https://github.com/ntt-nflex/flexer/tree/v1.2.1) (May 31, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.2.0...v1.2.1)

### Fixes:

- Run `flexer config` if a config file is not found

## [v1.2.0](https://github.com/ntt-nflex/flexer/tree/v1.2.0) (May 31, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.1.7...v1.2.0)

### Changes:

- **BREAKING**: Add support for multiple CMP regions to the config file and change the format to YAML. This requires running `flexer config` again
- Add a `flexer delete` command for deleting modules from nFlex
- Add a `flexer show` command for showing nFlex module details
- Add a `flexer logs` command for showing nFlex module execution logs
- Add a `flexer build` command for building module zip files from requirements.txt files
- Add a `flexer execute` command for running nFlex modules remotely on a CMP region
- Add a `flexer test` command to run base connector tests against a connector in development
- Update the list of allowed event sources
- Allow updating module descriptions with the `flexer update` command
- Redirect any output from the tool or the local module execution to stderr
- Redirect the return value of a module execution to stdout, useful for piping to curl and similar commands
- Display the module description in the `flexer list` output
- Update the help messages for all flexer commands

### Fixes:

- Fix the error handling for failed API requests to CMP
- Fix the `context.mail` method crashing when an exception is raised

## [v1.1.7](https://github.com/ntt-nflex/flexer/tree/v1.1.7) (Apr 24, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.1.6...v1.1.7)

### Changes:

- Fix the nFlex client \_post_file method to properly handle zip file uploads

## [v1.1.6](https://github.com/ntt-nflex/flexer/tree/v1.1.6) (Apr 18, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.1.5...v1.1.6)

### Changes:

- Add an optional resource_id to the get_metrics validation schema [\#16](https://github.com/ntt-nflex/flexer/pull/16) ([@ukinau](https://github.com/ukinau))
- Update the get_resources validation

## [v1.1.5](https://github.com/ntt-nflex/flexer/tree/v1.1.5) (Apr 12, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.1.4...v1.1.5)

### Changes:

- Add resource_id to the context.log request payload so logs would appear in the module details page
- Add context.api.put_file method and rename the context.api.post_file method parameters

## [v1.1.4](https://github.com/ntt-nflex/flexer/tree/v1.1.4) (Mar 22, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.1.3...v1.1.4)

### Changes:

- Add locations to get_resources validation [\#15](https://github.com/ntt-nflex/flexer/pull/15) ([@freewilll](https://github.com/freewilll))

## [v1.1.3](https://github.com/ntt-nflex/flexer/tree/v1.1.3) (Mar 20, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.1.2...v1.1.3)

### Changes:

- Add support for CMP access tokens to the CMP client

## [v1.1.2](https://github.com/ntt-nflex/flexer/tree/v1.1.2) (Mar 16, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.1.1...v1.1.2)

### Changes:

- Update the validation for data returned from the get_resources handler of cmp-connectors [\#13](https://github.com/ntt-nflex/flexer/pull/13) ([@prav-ab](https://github.com/prav-ab))

## [v1.1.1](https://github.com/ntt-nflex/flexer/tree/v1.1.1) (Mar 16, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.1.0...v1.1.1)

### Changes:

- Add feature: --config parameter to "flexer run"
- Update the list of supported event sources

## [v1.1.0](https://github.com/ntt-nflex/flexer/tree/v1.1.0) (Feb 15, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.13...v1.1.0)

### Changes:

- Add feature: "flexer new" command to create working examples of modules [\#7](https://github.com/ntt-nflex/flexer/pull/7) ([@tintoy](https://github.com/tintoy))

## [v1.0.13](https://github.com/ntt-nflex/flexer/tree/v1.0.13) (Jan 25, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.12...v1.0.13)

### Fixes:

- Add client for new nFlex state API, falling back to a local dictionary if not running via nFlex

## [v1.0.12](https://github.com/ntt-nflex/flexer/tree/v1.0.12) (Jan 19, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.11...v1.0.12)

### Fixes:

- Add "application/json" Content-Type to the CMP client

## [v1.0.11](https://github.com/ntt-nflex/flexer/tree/v1.0.11) (Jan 18, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.10...v1.0.11)

### Fixes:

- Fix for Windows

## [v1.0.10](https://github.com/ntt-nflex/flexer/tree/v1.0.10) (Jan 17, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.9...v1.0.10)

### Fixes:

- Fix the module upload command

## [v1.0.9](https://github.com/ntt-nflex/flexer/tree/v1.0.9) (Jan 17, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.8...v1.0.9)

### Changes:

- Add validation for data returned from metrics connectors and monitors

### Fixes:

- Add a config field to the flexer context so local executions don't fail

## [v1.0.8](https://github.com/ntt-nflex/flexer/tree/v1.0.8) (Jan 12, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.7...v1.0.8)

### Changes:

- Update the list of supported event sources
- Update the module list view to display the owner and the language of the modules
- Rename the cmp_username and cmp_password keys in the config file to cmp_api_key and cmp_api_secret respectively (Breaking change! You will have to modify the keys in the ~/.flexer.json config file or re-run the config command)

### Fixes:

- Fix the list command to show all modules using the nFlex API pagination

## [v1.0.7](https://github.com/ntt-nflex/flexer/tree/v1.0.7) (Jan 12, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.6...v1.0.7)

### Improvements:

- Add colo to get_resources validation [\#5](https://github.com/ntt-nflex/flexer/pull/5) ([@freewilll](https://github.com/freewilll))

## [v1.0.6](https://github.com/ntt-nflex/flexer/tree/v1.0.6) (Jan 09, 2017)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.5...v1.0.6)

### Improvements:

- Add validation for data returned from the get_resources handler of cmp-connectors [\#4](https://github.com/ntt-nflex/flexer/pull/4) ([@prav-ab](https://github.com/prav-ab))

## [v1.0.5](https://github.com/ntt-nflex/flexer/tree/v1.0.5) (Dec 12, 2016)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.4...v1.0.5)

### Improvements:

- Add state for nFlex modules

## [v1.0.4](https://github.com/ntt-nflex/flexer/tree/v1.0.4) (Oct 26, 2016)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.3...v1.0.4)

### Improvements:

- Add delete method to the CMP client [\#1](https://github.com/ntt-nflex/flexer/pull/1) ([@shin-chang](https://github.com/shin-chang))
- Add examples for cmp-connectors

## [v1.0.3](https://github.com/ntt-nflex/flexer/tree/v1.0.3) (Oct 13, 2016)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.2...v1.0.3)

### Fixes:

- Fix the default CMP URL to use the https scheme

## [v1.0.2](https://github.com/ntt-nflex/flexer/tree/v1.0.2) (Oct 13, 2016)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.1...v1.0.2)

### Improvements:

- Remove the pager from the print_modules method
- Disable SSL warnings of the urllib3 library
- Add README.md to the MANIFEST.in file

## [v1.0.1](https://github.com/ntt-nflex/flexer/tree/v1.0.1) (Oct 13, 2016)

[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v1.0.0...v1.0.1)

### Fixes:

- Fix the upload Make target

## [v1.0.0](https://github.com/ntt-nflex/flexer/tree/v1.0.0) (Oct 13, 2016)

### Initial release
