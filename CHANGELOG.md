## [0.5.0] - 2025-04-28

### Added

- compatibility with Deepbook v3 smart contract calls

### Changed

- upgraded pysui to `0.82.0`

### Removed

- v2 smart contract calls
- v2 docs

## [0.4.2] - 2023-10-27


### Changed

- upgraded pysui from `0.35.0` to `0.38.0`

### Fixed


## [0.4.1] - 2023-09-13


### Changed

- upgraded pysui from `0.32.0` to `0.35.0`

### Fixed


## [0.4.0] - 2023-08-23

### Added

- create_customized_pool(), create_child_account_cap(), clean_up_expired_orders()


### Changed

- `deepbookpy.deepbook_query` & `deepbookpy.deepbook_sdk` -> `deepbook_client.py`

### Fixed



### Removed



## [0.3.1] - 2023-08-07

### Added

- `get_all_pools()` - returns all available pools that live in `dee9` package
- `get_pool_info()` - returns `pool_id`, `base_asset` and `quote_asset`
- `get_pool_type_args()` that retrives `base_asset_type` and `quote_asset_type`
- `types/` directory that contains `LimitOrderType` and `SelfMatchingPreventionStyle` interfaces
- `utils.helpers` module that contains different helper functions
- new constants that live in `utils.constants` module

### Changed

- `pysui 0.29.0` to `pysui 0.32.0`
- `token_1` & `token_2` parameters of methods that live in `deepbookpy.deepbook_query` to `base_asset_type`, `quote_asset_type`
- `swap` internal design functions
- `SuiTransction` pysui import

### Fixed

- [pysui latest version incompatibility](https://github.com/andreidev1/deepbookpy/issues/11)
- cancel order functions argument types


### Removed

- `_mint()` method

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