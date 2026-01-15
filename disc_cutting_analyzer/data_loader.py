import pandas as pd
import streamlit as st
from typing import Dict, Any
import os


@st.cache_data
def load_data(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Load data from Excel file and return a dictionary of DataFrames.
    
    Args:
        file_path (str): Path to the Excel file containing the data
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary with sheet names as keys and DataFrames as values
    """
    try:
        # Read all sheets from the Excel file
        excel_file = pd.ExcelFile(file_path)
        data_dict = {}
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            # Clean column names to handle any special characters
            df.columns = df.columns.str.strip()
            data_dict[sheet_name] = df
            
        return data_dict
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return {}


def get_all_data() -> pd.DataFrame:
    """
    Get all data combined from all sheets in the Excel file.
    
    Returns:
        pd.DataFrame: Combined DataFrame with all data and a 'Material' column indicating the source
    """
    # Define the path to the Excel file
    file_path = os.path.join(os.path.dirname(__file__), "..", "DevelopNEW data", "База данных. Диски ADT пополнение.xlsx")
    
    # Load data from all sheets
    data_dict = load_data(file_path)
    
    # Combine all sheets into a single DataFrame
    all_data_list = []
    for sheet_name, df in data_dict.items():
        df_copy = df.copy()
        df_copy['Material'] = sheet_name  # Add material column to identify source
        all_data_list.append(df_copy)
    
    if all_data_list:
        combined_df = pd.concat(all_data_list, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()


@st.cache_data
def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    """
    Load data from an uploaded Excel file.
    
    Args:
        uploaded_file: Uploaded file object from Streamlit's file_uploader
        
    Returns:
        pd.DataFrame: Combined data from all sheets in the uploaded file
    """
    try:
        # Read all sheets from the uploaded Excel file
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        
        all_dataframes = []
        
        for sheet_name in sheet_names:
            # Read each sheet from the uploaded file
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            # Clean column names to handle any special characters
            df.columns = df.columns.str.strip()
            # Add a column to identify the material based on sheet name
            df['Material'] = sheet_name
            all_dataframes.append(df)
        
        # Combine all dataframes
        if all_dataframes:
            combined_data = pd.concat(all_dataframes, ignore_index=True)
            return combined_data
        else:
            st.error("Не удалось загрузить данные из файла. Проверьте формат файла.")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Ошибка при загрузке загруженного файла: {str(e)}")
        return pd.DataFrame()


def get_available_materials(data: pd.DataFrame) -> list:
    """
    Get unique materials from the data.
    
    Args:
        data (pd.DataFrame): Input DataFrame
        
    Returns:
        list: Unique materials in the dataset
    """
    if 'Material' in data.columns:
        unique_values = data['Material'].dropna().unique()
        return sorted(unique_values.tolist())
    else:
        return []


def get_available_cut_types(data: pd.DataFrame) -> list:
    """
    Get unique cut types from the data.
    
    Args:
        data (pd.DataFrame): Input DataFrame
        
    Returns:
        list: Unique cut types in the dataset
    """
    if 'Тип резки' in data.columns:
        unique_values = data['Тип резки'].dropna().unique()
        return sorted(unique_values.tolist())
    else:
        return []
