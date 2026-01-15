import sys
import os

# Add the current directory to Python path to handle imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    import streamlit as st
    print("[OK] Streamlit imported")
except ImportError as e:
    print(f"[ERROR] Streamlit import failed: {e}")

try:
    import pandas as pd
    print("[OK] Pandas imported")
except ImportError as e:
    print(f"[ERROR] Pandas import failed: {e}")

try:
    import plotly
    import plotly.express as px
    print("[OK] Plotly imported")
except ImportError as e:
    print(f"[ERROR] Plotly import failed: {e}")

try:
    import numpy as np
    print("[OK] NumPy imported")
except ImportError as e:
    print(f"[ERROR] NumPy import failed: {e}")

# Test our modules
try:
    from disc_cutting_analyzer.data_loader import get_all_data
    print("[OK] data_loader module imported")
except ImportError as e:
    print(f"[ERROR] data_loader import failed: {e}")

try:
    from disc_cutting_analyzer.analysis import filter_data
    print("[OK] analysis module imported")
except ImportError as e:
    print(f"[ERROR] analysis import failed: {e}")

try:
    from disc_cutting_analyzer.plotting import create_chipping_plot
    print("[OK] plotting module imported")
except ImportError as e:
    print(f"[ERROR] plotting import failed: {e}")

try:
    from disc_cutting_analyzer.decrypting import get_article_info
    print("[OK] decrypting module imported")
except ImportError as e:
    print(f"[ERROR] decrypting import failed: {e}")

print("Import tests completed.")