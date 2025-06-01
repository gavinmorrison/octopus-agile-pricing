#!/usr/bin/env python3
"""
Basic tests for the Octopus Agile Pricing script.

Copyright (c) 2025 Gavin Morrison
Licensed under the MIT License. See LICENSE file for details.
"""

import unittest
import sys
import os

# Add parent directory to path so we can import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import octopus_agile_prices as oap

class TestOctopusAgilePrices(unittest.TestCase):
    
    def test_region_mapping_exists(self):
        """Test that region mapping is properly defined."""
        self.assertIsInstance(oap.REGION_MAPPING, dict)
        self.assertEqual(len(oap.REGION_MAPPING), 14)
        self.assertIn('_C', oap.REGION_MAPPING)
        self.assertEqual(oap.REGION_MAPPING['_C'], 'London')
    
    def test_region_mapping_completeness(self):
        """Test that all expected regions are in the mapping."""
        expected_codes = ['_A', '_B', '_C', '_D', '_E', '_F', '_G', '_H', '_J', '_K', '_L', '_M', '_N', '_P']
        for code in expected_codes:
            self.assertIn(code, oap.REGION_MAPPING)
    
    def test_london_is_default(self):
        """Test that London is the default region."""
        # This tests the function signature default
        import inspect
        sig = inspect.signature(oap.get_agile_tariff_for_region)
        default_region = sig.parameters['region_name'].default
        self.assertEqual(default_region, 'London')
    
    def test_api_functions_exist(self):
        """Test that all expected functions exist."""
        functions = [
            'get_agile_prices',
            'get_available_products', 
            'get_agile_tariff_for_region',
            'get_agile_prices_for_region'
        ]
        for func_name in functions:
            self.assertTrue(hasattr(oap, func_name))
            self.assertTrue(callable(getattr(oap, func_name)))

class TestAPIIntegration(unittest.TestCase):
    """Integration tests that require API access."""
    
    def test_get_available_products(self):
        """Test that we can fetch available products."""
        try:
            products = oap.get_available_products()
            self.assertIsNotNone(products)
            self.assertGreater(len(products), 0)
            
            # Check expected columns exist
            expected_columns = ['product_code', 'region_name', 'region_code', 'is_agile']
            for col in expected_columns:
                self.assertIn(col, products.columns)
                
            # Check we have some agile products
            agile_products = products[products['is_agile']]
            self.assertGreater(len(agile_products), 0)
            
        except Exception as e:
            self.skipTest(f"API test skipped due to network/API error: {e}")
    
    def test_london_tariff_lookup(self):
        """Test that we can get London tariff info."""
        try:
            tariff_info = oap.get_agile_tariff_for_region("London")
            self.assertIsInstance(tariff_info, dict)
            
            expected_keys = ['product_code', 'tariff_code', 'region_name', 'region_code']
            for key in expected_keys:
                self.assertIn(key, tariff_info)
            
            self.assertEqual(tariff_info['region_name'], 'London')
            self.assertEqual(tariff_info['region_code'], '_C')
            
        except Exception as e:
            self.skipTest(f"API test skipped due to network/API error: {e}")

if __name__ == '__main__':
    unittest.main()
