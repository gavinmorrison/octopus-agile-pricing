# Octopus Energy Agile Pricing Data Fetcher

A Python script to fetch and analyse historic pricing data from Octopus Energy's Agile tariff across all UK regions.

## 🚀 Features

- **All UK Regions Supported**: Fetch pricing data for any of the 14 UK regions
- **London Default**: Defaults to London pricing for convenience
- **Historic Data**: Get pricing data for any date range
- **Negative Price Detection**: Automatically identifies periods with negative pricing
- **CSV Export**: Saves data to CSV files for further analysis
- **Statistics**: Provides min, max, and average pricing statistics

## 📋 Requirements

- Python 3.7+
- Internet connection to access Octopus Energy API

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gavinmorrison/octopus-agile-pricing.git
   cd octopus-agile-pricing
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Quick Start

### Command Line Interface
```bash
# Get London prices for last 7 days (default)
python octopus_agile_prices.py

# Get Yorkshire prices for last 14 days
python octopus_agile_prices.py --region Yorkshire --days 14

# List all available regions
python octopus_agile_prices.py --list-regions

# Get help
python octopus_agile_prices.py --help
```

### CLI Options
- `--region, -r`: Region name (default: London)
- `--days, -d`: Number of days of historical data (default: 7)
- `--list-regions`: List all available regions and exit
- `--output-dir`: Output directory for CSV files (default: output)

### Use as a Python module
```python
from octopus_agile_prices import get_agile_prices_for_region

# Get London prices for last 7 days (default)
london_prices = get_agile_prices_for_region("London")

# Get Yorkshire prices for last 14 days
yorkshire_prices = get_agile_prices_for_region("Yorkshire", days=14)

# Get Southern Scotland prices for last 30 days
scotland_prices = get_agile_prices_for_region("Southern Scotland", days=30)
```

## 🗺️ Supported Regions

| Region Code | Region Name |
|-------------|-------------|
| A | Eastern England |
| B | East Midlands |
| C | London |
| D | Merseyside and Northern Wales |
| E | West Midlands |
| F | North Eastern England |
| G | North Western England |
| H | Southern England |
| J | South Eastern England |
| K | Southern Wales |
| L | South Western England |
| M | Yorkshire |
| N | Southern Scotland |
| P | Northern Scotland |

## 📊 Output

The script generates CSV files in the `output/` directory with the following columns:

- `value_exc_vat`: Price excluding VAT (pence/kWh)
- `value_inc_vat`: Price including VAT (pence/kWh)
- `valid_from`: Start time of pricing period
- `valid_to`: End time of pricing period
- `payment_method`: Payment method (usually null)
- `price_gbp`: Price in pounds per kWh
- `region_name`: Human-readable region name
- `region_code`: Octopus region code

## 🔧 API Functions

### `get_agile_prices_for_region(region_name="London", days=7)`
Convenience function to get Agile prices for a specific region.

**Parameters:**
- `region_name` (str): Human-readable region name (default: "London")
- `days` (int): Number of days of historical data to fetch (default: 7)

**Returns:** DataFrame with pricing data

### `get_agile_prices(product_code, tariff_code, period_from=None, period_to=None)`
Fetch historic pricing data for specific product and tariff codes.

### `get_available_products()`
Fetch all available Octopus Energy products and their tariffs.

### `get_agile_tariff_for_region(region_name="London")`
Get the most recent Agile tariff information for a specific region.

## 📈 Example Output

```
Found 56 Agile products across all regions

Available Agile products by region:
  East Midlands: 4 products
  Eastern England: 4 products
  London: 4 products
  ...

==================================================
Getting pricing data for London...
Region: London (_C)

Retrieved 337 price points for London

Pricing statistics (last 7 days):
  Minimum price: -0.0798 £/kWh
  Maximum price: 0.3529 £/kWh
  Average price: 0.1227 £/kWh
  🎉 Found 23 periods with negative prices!

Data saved to: output/octopus_agile_prices_london.csv
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Gavin Morrison

## ⚠️ Disclaimer

This tool is not affiliated with Octopus Energy. It uses their public API to fetch pricing data. Please use responsibly and in accordance with their terms of service.

## 🔗 Links

- [Octopus Energy](https://octopus.energy/)
- [Octopus Energy API Documentation](https://developer.octopus.energy/docs/api/)
- [Agile Octopus Tariff](https://octopus.energy/agile/)
