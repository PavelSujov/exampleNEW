import pandas as pd
import streamlit as st
from typing import Dict, Optional
import os


# Remove the Excel loading function as we're using CSV directly


def decode_article(article: str) -> Optional[Dict[str, str]]:
    """
    Decode a disc article to extract its parameters based on the naming convention.
    
    Args:
        article (str): The disc article string (e.g., "00757-1130-250-100")
        
    Returns:
        Optional[Dict[str, str]]: Decoded parameters or None if invalid
    """
    # Load the parameter mapping from the CSV file
    file_path = os.path.join(os.path.dirname(__file__), "..", "DevelopNEW data", "Условные обозначения.csv")
    try:
        params_df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')  # Use utf-8-sig to handle BOM
    except Exception as e:
        st.error(f"Error loading disc parameters from CSV: {str(e)}")
        return None
    
    # Initialize result dictionary
    decoded_params = {
        'article': article,
        'product_family': 'Hub blade (фланцевый/корпусной диск)',
        'grit_size': '',
        'diamond_percent': '',
        'blade_thickness': '',
        'blade_exposure': '',
        'bond_hardness': ''
    }
    
    # Validate article format: 00757-GCTT-EEE-HXX
    # where G – Grit size, C – Diamond %, TT – Blade thickness, EEE – Blade exposure, H – Bond Hardness, XX – Constant
    if len(article) != 18 or not article.startswith('00757-'):
        return decoded_params
    
    # Split the article into parts: 00757, GCTT, EEE, HXX
    try:
        parts = article.split('-')
        if len(parts) != 4:
            return decoded_params
        
        gc_part = parts[1]  # GCTT - G=Grit size, C=Diamond%, TT=Blade thickness
        eee_part = parts[2]  # EEE - Blade exposure
        hxx_part = parts[3]  # HXX - H=Bond Hardness, XX=constant (could be 00, 0, etc.)
        
        # Extract individual components
        grit_part = gc_part[0]  # G - Grit size (1 symbol: digit 1-9 or A/B)
        diamond_part = gc_part[1]  # C - Diamond % (1 symbol: digit 1-5)
        blade_thickness_part = gc_part[2:4]  # TT - Blade thickness (2 symbols: digits or A0/A1/A2)
        blade_exposure_part = eee_part  # EEE - Blade exposure (3 digits)
        bond_hardness_part = hxx_part[0]  # H - Bond hardness (1 symbol: digit 1/2/3)
        
        # Find corresponding values in the parameters dataframe
        # Using positional column indices due to encoding issues with Cyrillic column names
        # Column 0: Параметр, Column 1: Условное обозначение в артикуле, Column 2: Значение, Column 3: Единица измерения
        grit_row = params_df[(params_df.iloc[:, 0] == 'Grit Size (Размер алмазного зерна)') &
                             (params_df.iloc[:, 1] == grit_part)]
        if not grit_row.empty:
            decoded_params['grit_size'] = str(grit_row.iloc[0, 2])  # Use column index 2 for Значение
        
        diamond_row = params_df[(params_df.iloc[:, 0] == 'Diamond % (Концентрация алмазного зерна)') &
                                (params_df.iloc[:, 1] == diamond_part)]
        if not diamond_row.empty:
            decoded_params['diamond_percent'] = str(diamond_row.iloc[0, 2])  # Use column index 2 for Значение
        
        thickness_row = params_df[(params_df.iloc[:, 0] == 'Blade thickness (Толщина лезвия)') &
                                  (params_df.iloc[:, 1] == blade_thickness_part)]
        if not thickness_row.empty:
            decoded_params['blade_thickness'] = str(thickness_row.iloc[0, 2])  # Use column index 2 for Значение
        
        exposure_row = params_df[(params_df.iloc[:, 0] == 'Blade exposure (Вылет лезвия)') &
                                 (params_df.iloc[:, 1] == blade_exposure_part)]
        if not exposure_row.empty:
            decoded_params['blade_exposure'] = str(exposure_row.iloc[0, 2])  # Use column index 2 for Значение
        
        hardness_row = params_df[(params_df.iloc[:, 0] == 'Bond hardness (Твёрдость связки)') &
                                 (params_df.iloc[:, 1] == bond_hardness_part)]
        if not hardness_row.empty:
            decoded_params['bond_hardness'] = str(hardness_row.iloc[0, 2])  # Use column index 2 for Значение
        
        return decoded_params
    except Exception as e:
        st.error(f"Error decoding article: {str(e)}")
        return None


def get_article_info(article: str) -> Dict[str, str]:
    """
    Get detailed information about a disc article.
    
    Args:
        article (str): The disc article string
        
    Returns:
        Dict[str, str]: Detailed information about the disc
    """
    decoded = decode_article(article)
    if decoded:
        return decoded
    else:
        return {
            'article': article,
            'product_family': 'Unknown',
            'grit_size': 'Unknown',
            'diamond_percent': 'Unknown',
            'blade_thickness': 'Unknown',
            'blade_exposure': 'Unknown',
            'bond_hardness': 'Unknown'
        }


def validate_article_format(article: str) -> bool:
    """
    Validate if the article follows the expected format.
    
    Args:
        article (str): The article to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if the article has the correct length and prefix
    if len(article) != 18 or not article.startswith('00757'):
        return False
    
    # Check if it follows the expected pattern (with hyphens in the right places)
    parts = article.split('-')
    if len(parts) != 4:
        return False
    
    # Validate individual parts
    if len(parts[0]) != 5 or len(parts[1]) != 4 or len(parts[2]) != 3 or len(parts[3]) != 3:
        return False
    
    return True