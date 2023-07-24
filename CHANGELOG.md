## [0.3.0] - 2023-07-25

### Added

- `flaky` test dependency
-  Compatible query methods for clob_v2 module ( partially fixes #4 )
-  new integration tests for querying clob_v2 module

### Changed

- 0.2.1 to 0.3.0 version

### Fixed


### Removed


## [0.2.1] - 2023-07-22

### Added

- Integrate Sphinx Documentation (#3)
- Upload Deepbookpy to PyPi (#7)
- version.py 
- readthedocs.yml

### Changed

- upgrade pysui 0.26.0 to 0.29.0

### Fixed

- [bug](https://github.com/andreidev1/deepbookpy/issues/8) Fix `deepbookpy` package installation

### Removed



## [0.1.0] - 2023-06-29

### Added

- CHANGELOG.md
- README.md
- `docs/` directory for documentation
- `deepbook_query.py` that covers 100% of Query API
- `deepbook_sdk.py` that covers 90% of Writable API
- `tests/` that contain simplest integration test and configuration test file

### Changed

- Changed `DeepBookQuery` constructor design - `provider` and `current_address` were replaced with `client` object
- Changed `DeepBookSDK` constructor design - `provider` and `current_address` were replaced with `client` object
- Renamed `deepbookpy_query.py` to `deepbook_query.py`
- Upgrade `pytest` to `7.4.0`

### Removed

- `dto.py` module
- `config.py` module