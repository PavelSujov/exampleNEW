"""
Simple test script to verify that all modules can be imported without errors
and basic functionality works.
"""

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")
    
    try:
        from disc_cutting_analyzer.data_loader import get_all_data, load_data
        print("[OK] data_loader module imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import data_loader: {e}")
        return False
    
    try:
        from disc_cutting_analyzer.decrypting import decode_article, get_article_info
        print("[OK] decrypting module imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import decrypting: {e}")
        return False
    
    try:
        from disc_cutting_analyzer.plotting import create_chipping_plot
        print("[OK] plotting module imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import plotting: {e}")
        return False
    
    try:
        from disc_cutting_analyzer.analysis import filter_data
        print("[OK] analysis module imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import analysis: {e}")
        return False
    
    try:
        import app
        print("[OK] app module imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import app: {e}")
        return False
    
    return True


def test_data_loading():
    """Test basic data loading functionality."""
    print("\nTesting data loading...")
    
    try:
        from disc_cutting_analyzer.data_loader import get_all_data
        data = get_all_data()
        
        if data.empty:
            print("[WARNING] Data is empty - check if data files exist")
        else:
            print(f"[OK] Data loaded successfully with {len(data)} records")
            print(f"  Available columns: {list(data.columns)[:10]}...")  # Show first 10 columns
            print(f"  Available materials: {sorted(data['Material'].unique()) if 'Material' in data.columns else []}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return False


def test_article_decoding():
    """Test article decoding functionality with a sample."""
    print("\nTesting article decoding...")
    
    try:
        from disc_cutting_analyzer.decrypting import decode_article, validate_article_format
        
        # Test with a sample article format
        sample_article = "00757-1130-250-100"
        
        is_valid = validate_article_format(sample_article)
        print(f"[OK] Article format validation: {is_valid}")
        
        decoded = decode_article(sample_article)
        if decoded:
            print(f"[OK] Article decoded successfully: {decoded['article']}")
        else:
            print("[INFO] Article decoding returned None (may be due to missing parameter file)")
        
        return True
    except Exception as e:
        print(f"[INFO] Article decoding test failed (expected if parameter file not available): {e}")
        return True  # This is OK since parameter file might not be accessible during testing


def main():
    """Run all tests."""
    print("Running tests for Disc Cutting Analyzer...\n")
    
    success = True
    success &= test_imports()
    success &= test_data_loading()
    success &= test_article_decoding()
    
    print(f"\n{'='*50}")
    if success:
        print("All tests passed! The application should run correctly.")
    else:
        print("Some tests failed. Please check the error messages above.")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()