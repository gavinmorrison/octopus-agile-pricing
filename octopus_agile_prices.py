"""
Octopus Energy Agile Pricing Data Fetcher

This script fetches historic pricing data for Octopus Energy Agile tariffs.
It supports all UK regions and defaults to London.

Copyright (c) 2025 Gavin Morrison
Licensed under the MIT License. See LICENSE file for details.

Example usage:
    # Get London prices for last 7 days (default)
    prices = get_agile_prices_for_region("London")

    # Get Yorkshire prices for last 14 days
    prices = get_agile_prices_for_region("Yorkshire", days=14)

    # Get all available regions
    products = get_available_products()
    regions = products['region_name'].unique()
"""

import requests
from datetime import datetime, timedelta
import pandas as pd
import os
import argparse

# Octopus Energy region mapping
REGION_MAPPING = {
    '_A': 'Eastern England',
    '_B': 'East Midlands',
    '_C': 'London',
    '_D': 'Merseyside and Northern Wales',
    '_E': 'West Midlands',
    '_F': 'North Eastern England',
    '_G': 'North Western England',
    '_H': 'Southern England',
    '_J': 'South Eastern England',
    '_K': 'Southern Wales',
    '_L': 'South Western England',
    '_M': 'Yorkshire',
    '_N': 'Southern Scotland',
    '_P': 'Northern Scotland'
}

def get_agile_prices(product_code="AGILE-FLEX-22-11-25", tariff_code="E-1R-AGILE-FLEX-22-11-25-E", 
                     period_from=None, period_to=None):
    """
    Fetch historic pricing data for Octopus Energy Agile tariff.
    
    Args:
        product_code: The Agile product code
        tariff_code: The specific tariff code
        period_from: Start date (defaults to 1 day ago)
        period_to: End date (defaults to now)
    
    Returns:
        DataFrame with timestamp and price data
    """
    # Set default date range if not provided
    if not period_from:
        period_from = (datetime.now() - timedelta(days=1)).isoformat()
    if not period_to:
        period_to = datetime.now().isoformat()
    
    # Construct API URL
    base_url = "https://api.octopus.energy/v1/products"
    url = f"{base_url}/{product_code}/electricity-tariffs/{tariff_code}/standard-unit-rates/"
    
    # Parameters for the request
    params = {
        'period_from': period_from,
        'period_to': period_to,
        'page_size': 1500  # Get more results per page
    }
    
    # Make the request
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    
    # Extract the results
    data = response.json()['results']
    
    # Convert to DataFrame
    df = pd.DataFrame(data)



    # Convert timestamps to datetime and set as index
    if 'valid_from' in df.columns:
        df['valid_from'] = pd.to_datetime(df['valid_from'])
    if 'valid_to' in df.columns:
        df['valid_to'] = pd.to_datetime(df['valid_to'])

    # Convert value_inc_vat from pence to pounds
    if 'value_inc_vat' in df.columns:
        df['price_gbp'] = df['value_inc_vat'] / 100
    
    return df

def get_available_products():
    """
    Fetch all available products and their tariffs from Octopus Energy API.
    
    Returns:
        DataFrame with product information
    """
    base_url = "https://api.octopus.energy/v1/products/"
    
    # Make the request
    response = requests.get(base_url, params={'is_variable': True})
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    
    # Extract the results
    products = response.json()['results']
    
    # Create a list to store product details
    product_details = []
    
    # Process each product
    for product in products:
        product_code = product['code']
        
        # Get detailed product info including tariffs
        product_url = f"{base_url}{product_code}"
        product_response = requests.get(product_url)
        
        if product_response.status_code == 200:
            product_data = product_response.json()
            
            # Extract tariff codes
            if 'single_register_electricity_tariffs' in product_data:
                for region, tariff in product_data['single_register_electricity_tariffs'].items():
                    # Try to get tariff code from different payment methods
                    tariff_code = None
                    if 'direct_debit_monthly' in tariff:
                        tariff_code = tariff['direct_debit_monthly']['code']
                    elif 'direct_debit_quarterly' in tariff:
                        tariff_code = tariff['direct_debit_quarterly']['code']
                    elif 'varying' in tariff:
                        tariff_code = tariff['varying']['code']
                    else:
                        # If none of the expected payment methods exist, skip this tariff
                        continue

                    product_details.append({
                        'product_code': product_code,
                        'product_name': product['full_name'],
                        'tariff_code': tariff_code,
                        'region_code': region,
                        'region_name': REGION_MAPPING.get(region, region),
                        'is_variable': product['is_variable'],
                        'is_green': product['is_green'],
                        'is_tracker': product['is_tracker'],
                        'is_agile': 'agile' in product_code.lower()
                    })
    
    # Convert to DataFrame
    df = pd.DataFrame(product_details)
    return df

def get_agile_prices_for_region(region_name="London", days=7):
    """
    Convenience function to get Agile prices for a specific region.

    Args:
        region_name: Human-readable region name (default: "London")
        days: Number of days of historical data to fetch (default: 7)

    Returns:
        DataFrame with pricing data for the region
    """
    tariff_info = get_agile_tariff_for_region(region_name)

    from_date = (datetime.now() - timedelta(days=days)).isoformat()
    to_date = datetime.now().isoformat()

    prices = get_agile_prices(
        product_code=tariff_info['product_code'],
        tariff_code=tariff_info['tariff_code'],
        period_from=from_date,
        period_to=to_date
    )

    # Add region info to the dataframe
    prices['region_name'] = tariff_info['region_name']
    prices['region_code'] = tariff_info['region_code']

    return prices

def get_agile_tariff_for_region(region_name="London"):
    """
    Get the most recent Agile tariff for a specific region.

    Args:
        region_name: Human-readable region name (default: "London")

    Returns:
        Dictionary with product_code and tariff_code for the region
    """
    products_df = get_available_products()
    agile_products = products_df[products_df['is_agile']]

    # Filter for the specified region
    region_products = agile_products[agile_products['region_name'] == region_name]

    if len(region_products) == 0:
        raise ValueError(f"No Agile products found for region: {region_name}")

    # Get the most recent product (assuming newer product codes are better)
    # Filter out outgoing tariffs for consumption pricing
    consumption_products = region_products[~region_products['product_code'].str.contains('OUTGOING')]

    if len(consumption_products) > 0:
        latest_product = consumption_products.iloc[0]
    else:
        latest_product = region_products.iloc[0]

    return {
        'product_code': latest_product['product_code'],
        'tariff_code': latest_product['tariff_code'],
        'region_name': latest_product['region_name'],
        'region_code': latest_product['region_code']
    }

def main():
    """Main function with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Fetch Octopus Energy Agile pricing data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Get London prices for last 7 days
  %(prog)s --region Yorkshire        # Get Yorkshire prices for last 7 days
  %(prog)s --region London --days 14 # Get London prices for last 14 days
  %(prog)s --list-regions            # Show all available regions
        """
    )

    parser.add_argument(
        '--region', '-r',
        default='London',
        help='Region name (default: London)'
    )

    parser.add_argument(
        '--days', '-d',
        type=int,
        default=7,
        help='Number of days of historical data (default: 7)'
    )

    parser.add_argument(
        '--list-regions',
        action='store_true',
        help='List all available regions and exit'
    )

    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for CSV files (default: output)'
    )

    args = parser.parse_args()

    # Handle list regions
    if args.list_regions:
        print("🌍 Available regions:")
        for code, name in sorted(REGION_MAPPING.items(), key=lambda x: x[1]):
            print(f"  {name} ({code})")
        return

    # Main execution
    run_main_script(args.region, args.days, args.output_dir)

def run_main_script(region_name="London", days=7, output_dir="output"):
    """Run the main script logic."""
    # Get all available products and tariffs
    print("Fetching available products and tariffs...")
    products_df = get_available_products()

    # Filter for Agile products
    agile_products = products_df[products_df['is_agile']]
    print(f"\nFound {len(agile_products)} Agile products across all regions")

    # Show unique products with region names
    unique_products = agile_products[['product_code', 'product_name', 'region_name']].drop_duplicates()
    print("\nAvailable Agile products by region:")
    for region in sorted(unique_products['region_name'].unique()):
        region_products = unique_products[unique_products['region_name'] == region]
        print(f"  {region}: {len(region_products)} products")

    # Get pricing data for specified region
    print(f"\n{'='*50}")
    print(f"Getting pricing data for {region_name}...")
    try:
        prices = get_agile_prices_for_region(region_name, days=days)

        print(f"Region: {prices['region_name'].iloc[0]} ({prices['region_code'].iloc[0]})")

        print(f"\nRetrieved {len(prices)} price points for {region_name}")
        print("\nSample pricing data:")
        print(prices[['valid_from', 'value_inc_vat', 'price_gbp']].head(10))

        # Show some statistics
        if len(prices) > 0:
            print(f"\nPricing statistics (last {days} days):")
            print(f"  Minimum price: {prices['price_gbp'].min():.4f} £/kWh")
            print(f"  Maximum price: {prices['price_gbp'].max():.4f} £/kWh")
            print(f"  Average price: {prices['price_gbp'].mean():.4f} £/kWh")

            # Check for negative prices
            negative_prices = prices[prices['price_gbp'] < 0]
            if len(negative_prices) > 0:
                print(f"  🎉 Found {len(negative_prices)} periods with negative prices!")

        # Save to CSV with region info in output folder
        os.makedirs(output_dir, exist_ok=True)
        region_safe = region_name.lower().replace(' ', '_')
        filename = f'{output_dir}/octopus_agile_prices_{region_safe}.csv'
        prices.to_csv(filename, index=False)
        print(f"\nData saved to: {filename}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Available regions:", sorted(agile_products['region_name'].unique()))

if __name__ == "__main__":
    main()
