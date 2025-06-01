# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-01-01

### Changed
- Updated minimum Python version requirement from 3.7 to 3.8 for GitHub Actions compatibility
- Updated CI/CD pipeline to use Ubuntu 22.04 for broader Python version support
- Relaxed pandas version requirement from >=2.2.0 to >=2.0.0 for Python 3.8 compatibility
- Updated requests version requirement from >=2.32.0 to >=2.28.0 for better compatibility

### Technical
- Removed Python 3.7 from CI test matrix (not available on Ubuntu 24.04)
- Updated package classifiers and requirements
- Fixed pandas dependency issue where pandas 2.2.0+ requires Python 3.9+

## [1.0.0] - 2025-01-01

### Added
- Initial release of Octopus Energy Agile Pricing Data Fetcher
- Support for all 14 UK regions with human-readable names
- London as default region
- Automatic detection of current Agile tariff codes
- CSV export functionality with output directory structure
- Comprehensive error handling for API responses
- Statistics calculation (min, max, average prices)
- Negative price detection and reporting
- Region mapping from Octopus codes to human-readable names
- Convenience functions for easy region-based data fetching
- Complete documentation and examples

### Features
- `get_agile_prices_for_region()` - Easy region-based price fetching
- `get_agile_prices()` - Low-level API for specific tariff codes
- `get_available_products()` - Fetch all available Octopus products
- `get_agile_tariff_for_region()` - Get tariff info for specific regions
- Automatic output directory creation
- Robust API error handling
- Support for custom date ranges

### Technical
- Python 3.7+ compatibility
- Minimal dependencies (requests, pandas)
- Clean code structure with proper documentation
- MIT License
- GitHub-ready repository structure
