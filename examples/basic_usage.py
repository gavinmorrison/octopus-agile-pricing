#!/usr/bin/env python3
"""
Basic usage examples for the Octopus Agile Pricing script.

Copyright (c) 2025 Gavin Morrison
Licensed under the MIT License. See LICENSE file for details.
"""

import sys
import os

# Add parent directory to path so we can import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from octopus_agile_prices import get_agile_prices_for_region, get_available_products

def main():
    print("🔌 Octopus Energy Agile Pricing Examples")
    print("=" * 50)
    
    # Example 1: Get London prices for last 3 days
    print("\n📍 Example 1: London prices (last 3 days)")
    try:
        london_prices = get_agile_prices_for_region("London", days=3)
        print(f"Retrieved {len(london_prices)} price points for London")
        print(f"Price range: {london_prices['price_gbp'].min():.4f} to {london_prices['price_gbp'].max():.4f} £/kWh")
        
        # Find cheapest and most expensive periods
        cheapest = london_prices.loc[london_prices['price_gbp'].idxmin()]
        most_expensive = london_prices.loc[london_prices['price_gbp'].idxmax()]
        
        print(f"Cheapest: {cheapest['price_gbp']:.4f} £/kWh at {cheapest['valid_from']}")
        print(f"Most expensive: {most_expensive['price_gbp']:.4f} £/kWh at {most_expensive['valid_from']}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Compare multiple regions
    print("\n🗺️  Example 2: Compare regions (last 1 day)")
    regions_to_compare = ["London", "Yorkshire", "Southern Scotland"]
    
    for region in regions_to_compare:
        try:
            prices = get_agile_prices_for_region(region, days=1)
            avg_price = prices['price_gbp'].mean()
            print(f"{region:20}: {avg_price:.4f} £/kWh average")
        except Exception as e:
            print(f"{region:20}: Error - {e}")
    
    # Example 3: Show all available regions
    print("\n🌍 Example 3: All available regions")
    try:
        products = get_available_products()
        agile_products = products[products['is_agile']]
        regions = sorted(agile_products['region_name'].unique())
        
        print("Available regions:")
        for i, region in enumerate(regions, 1):
            print(f"  {i:2d}. {region}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n✅ Examples completed!")

if __name__ == "__main__":
    main()
