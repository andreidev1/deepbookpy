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