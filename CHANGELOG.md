# Change Log

## [v1.2.6](https://github.com/ntt-nflex/flexer/tree/v1.2.6) (Jun 29, 2017)
[Full Changelog](https://github.com/ntt-nflex/flexer/compare/v.1.2.5...v1.2.6)

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
- Fix the nFlex client _post_file method to properly handle zip file uploads

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
