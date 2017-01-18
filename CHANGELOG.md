# Change Log

## [v1.0.10](https://github.com/ntt-nflex/flexer/tree/v1.0.11) (Jan 18, 2017)
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
