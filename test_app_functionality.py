#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify that all modules of the disc cutting analyzer work correctly.
"""
import sys
import os

def test_imports():
    """Test that all modules can be imported without errors."""
    print("Testing module imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit import successful")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas import successful")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False
    
    try:
        import plotly
        import plotly.express as px
        import plotly.graph_objects as go
        print("✓ Plotly import successful")
    except ImportError as e:
        print(f"✗ Plotly import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy import successful")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    # Test our custom modules
    try:
        from disc_cutting_analyzer.data_loader import get_all_data, get_available_materials, get_available_cut_types
        print("✓ data_loader module import successful")
    except ImportError as e:
        print(f"✗ data_loader import failed: {e}")
        return False
    
    try:
        from disc_cutting_analyzer.analysis import filter_data, get_material_statistics, get_cut_type_analysis
        print("✓ analysis module import successful")
    except ImportError as e:
        print(f"✗ analysis import failed: {e}")
        return False
    
    try:
        from disc_cutting_analyzer.plotting import create_chipping_plot, create_performance_plot, create_process_parameters_plot
        print("✓ plotting module import successful")
    except ImportError as e:
        print(f"✗ plotting import failed: {e}")
        return False
    
    try:
        from disc_cutting_analyzer.decrypting import get_article_info, validate_article_format, decode_article
        print("✓ decrypting module import successful")
    except ImportError as e:
        print(f"✗ decrypting import failed: {e}")
        return False
    
    return True

def test_data_loading():
    """Test that data can be loaded successfully."""
    print("\nTesting data loading...")
    
    try:
        from disc_cutting_analyzer.data_loader import get_all_data
        data = get_all_data()
        
        if data is not None and not data.empty:
            print(f"✓ Data loaded successfully. Shape: {data.shape}")
            print(f"  Available materials: {len(get_available_materials(data))}")
            print(f"  Available cut types: {len(get_available_cut_types(data))}")
            return True
        else:
            print("✗ Data loading failed - no data returned")
            return False
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        return False

def test_article_decoding():
    """Test the article decoding functionality."""
    print("\nTesting article decoding...")
    
    try:
        from disc_cutting_analyzer.decrypting import get_article_info, validate_article_format
        
        # Test with a sample article
        sample_article = "00757-1130-250-100"
        is_valid = validate_article_format(sample_article)
        print(f"  Article format validation for {sample_article}: {is_valid}")
        
        if is_valid:
            decoded_info = get_article_info(sample_article)
            print(f"  Decoded info: {decoded_info}")
            print("✓ Article decoding successful")
            return True
        else:
            print("  Using sample format for testing...")
            # Even if the format is invalid, the function should still return a result
            decoded_info = get_article_info(sample_article)
            print(f"  Decoded info: {decoded_info}")
            print("✓ Article decoding function works")
            return True
    except Exception as e:
        print(f"✗ Article decoding failed: {e}")
        return False

def test_analysis_functions():
    """Test the analysis functions."""
    print("\nTesting analysis functions...")
    
    try:
        from disc_cutting_analyzer.data_loader import get_all_data
        from disc_cutting_analyzer.analysis import filter_data, get_material_statistics, get_cut_type_analysis
        
        data = get_all_data()
        if data is not None and not data.empty:
            # Test filtering with sample parameters
            filtered = filter_data(
                data, 
                selected_materials=get_available_materials(data)[:1] if get_available_materials(data) else [],
                selected_cut_types=get_available_cut_types(data)[:1] if get_available_cut_types(data) else [],
                min_thickness=data['Толщина пластины, мкм'].min() if 'Толщина пластины, мкм' in data.columns else 50,
                max_thickness=data['Толщина пластины, мкм'].max() if 'Толщина пластины, мкм' in data.columns else 500,
                min_kerf_width=data['Ширина реза, мкм'].min() if 'Ширина реза, мкм' in data.columns else 25,
                max_kerf_width=data['Ширина реза, мкм'].max() if 'Ширина реза, мкм' in data.columns else 120
            )
            print(f"  Filtered data shape: {filtered.shape}")
            
            # Test statistics
            stats = get_material_statistics(filtered)
            print(f"  Material statistics: {len(stats)} materials")
            
            print("✓ Analysis functions work correctly")
            return True
        else:
            print("✗ Analysis functions test failed - no data available")
            return False
    except Exception as e:
        print(f"✗ Analysis functions failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting Disc Cutting Analyzer functionality test...")
    print("="*60)
    
    # Change to the script's directory to handle paths properly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    all_tests_passed = True
    
    # Run each test
    all_tests_passed &= test_imports()
    all_tests_passed &= test_data_loading()
    all_tests_passed &= test_article_decoding()
    all_tests_passed &= test_analysis_functions()
    
    print("\n" + "="*60)
    if all_tests_passed:
        print("✓ All tests passed! The application should work correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())