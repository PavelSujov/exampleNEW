import pandas as pd
import streamlit as st
from typing import List, Dict, Tuple
import numpy as np


def filter_data(
    data: pd.DataFrame,
    selected_materials: List[str],
    selected_cut_types: List[str],
    min_thickness: float,
    max_thickness: float,
    min_kerf_width: float,
    max_kerf_width: float
) -> pd.DataFrame:
    """
    Filter the data based on user selections.
    
    Args:
        data (pd.DataFrame): Input DataFrame to filter
        selected_materials (List[str]): Selected materials
        selected_cut_types (List[str]): Selected cut types
        min_thickness (float): Minimum thickness for filtering
        max_thickness (float): Maximum thickness for filtering
        min_kerf_width (float): Minimum kerf width for filtering
        max_kerf_width (float): Maximum kerf width for filtering
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    filtered_data = data[
        (data['Материал пластины'].isin(selected_materials)) &
        (data['Тип резки'].isin(selected_cut_types)) &
        (data['Толщина пластины, мкм'] >= min_thickness) &
        (data['Толщина пластины, мкм'] <= max_thickness) &
        (data['Ширина реза, мкм'] >= min_kerf_width) &
        (data['Ширина реза, мкм'] <= max_kerf_width)
    ].copy()
    
    return filtered_data


def get_material_statistics(data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Calculate statistics for each material in the dataset.
    
    Args:
        data (pd.DataFrame): Input DataFrame
        
    Returns:
        Dict[str, Dict[str, float]]: Statistics for each material
    """
    stats = {}
    
    for material in data['Материал пластины'].unique():
        material_data = data[data['Материал пластины'] == material]
        
        # Convert relevant columns to numeric, handling non-numeric values
        numeric_cols = [
            'Толщина пластины, мкм',
            'Сколы лицевая сторона (медиана), мкм',
            'Сколы обратная сторона (медиана), мкм',
            'Производительность, шт/час',
            'Срок службы диска, резов',
            'Скорость подачи, мм/с',
            'Частота оборотов шпинделя, об/мин'
        ]
        
        for col in numeric_cols:
            if col in material_data.columns:
                material_data = material_data.copy()  # Explicitly work on a copy
                material_data[col] = pd.to_numeric(material_data[col], errors='coerce')
        
        stats[material] = {
            'Количество': len(material_data),
            'Средняя толщина пластины (мкм)': material_data['Толщина пластины, мкм'].mean(),
            'Средние сколы (лицевая сторона, мкм)': material_data['Сколы лицевая сторона (медиана), мкм'].mean(),
            'Средние сколы (обратная сторона, мкм)': material_data['Сколы обратная сторона (медиана), мкм'].mean(),
            'Средняя производительность (шт/час)': material_data['Производительность, шт/час'].mean(),
            'Средний срок службы диска (резов)': material_data['Срок службы диска, резов'].mean(),
            'Средняя скорость подачи (мм/с)': material_data['Скорость подачи, мм/с'].mean(),
            'Средняя частота оборотов шпинделя (об/мин)': material_data['Частота оборотов шпинделя, об/мин'].mean()
        }
    
    return stats


def get_cut_type_analysis(data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Analyze data by cut type.
    
    Args:
        data (pd.DataFrame): Input DataFrame
        
    Returns:
        Dict[str, Dict[str, float]]: Analysis for each cut type
    """
    analysis = {}
    
    for cut_type in data['Тип резки'].unique():
        cut_data = data[data['Тип резки'] == cut_type]
        
        # Convert relevant columns to numeric, handling non-numeric values
        numeric_cols = [
            'Толщина пластины, мкм',
            'Сколы лицевая сторона (медиана), мкм',
            'Сколы обратная сторона (медиана), мкм',
            'Производительность, шт/час',
            'Срок службы диска, резов',
            'Скорость подачи, мм/с',
            'Частота оборотов шпинделя, об/мин'
        ]
        
        for col in numeric_cols:
            if col in cut_data.columns:
                cut_data = cut_data.copy()  # Explicitly work on a copy
                cut_data[col] = pd.to_numeric(cut_data[col], errors='coerce')
        
        analysis[cut_type] = {
            'Количество': len(cut_data),
            'Средняя толщина пластины (мкм)': cut_data['Толщина пластины, мкм'].mean(),
            'Средние сколы (лицевая сторона, мкм)': cut_data['Сколы лицевая сторона (медиана), мкм'].mean(),
            'Средние сколы (обратная сторона, мкм)': cut_data['Сколы обратная сторона (медиана), мкм'].mean(),
            'Средняя производительность (шт/час)': cut_data['Производительность, шт/час'].mean(),
            'Средний срок службы диска (резов)': cut_data['Срок службы диска, резов'].mean(),
            'Средняя скорость подачи (мм/с)': cut_data['Скорость подачи, мм/с'].mean(),
            'Средняя частота оборотов шпинделя (об/мин)': cut_data['Частота оборотов шпинделя, об/мин'].mean()
        }
    
    return analysis


def get_thickness_ranges(data: pd.DataFrame) -> List[Tuple[float, float]]:
    """
    Get common thickness ranges in the dataset.
    
    Args:
        data (pd.DataFrame): Input DataFrame
        
    Returns:
        List[Tuple[float, float]]: List of (min, max) thickness ranges
    """
    thickness_values = sorted(data['Толщина пластины, мкм'].unique())
    
    if len(thickness_values) < 2:
        return [(thickness_values[0], thickness_values[0])] if thickness_values else []
    
    # Group thickness values into ranges
    ranges = []
    start = thickness_values[0]
    prev = thickness_values[0]
    
    for val in thickness_values[1:]:
        if val - prev > 50:  # If gap is larger than 50 μm, start a new range
            ranges.append((start, prev))
            start = val
        prev = val
    
    ranges.append((start, prev))
    
    return ranges


def find_optimal_settings(
    data: pd.DataFrame,
    material: str,
    target_thickness: float,
    cut_type: str = None
) -> pd.DataFrame:
    """
    Find optimal cutting settings for a given material and thickness.
    
    Args:
        data (pd.DataFrame): Input DataFrame
        material (str): Target material
        target_thickness (float): Target thickness
        cut_type (str, optional): Specific cut type to consider
        
    Returns:
        pd.DataFrame: Optimal settings sorted by performance
    """
    material_data = data[data['Материал пластины'] == material].copy()
    
    if cut_type:
        material_data = material_data[material_data['Тип резки'] == cut_type]
    
    # Calculate distance to target thickness
    material_data['thickness_distance'] = abs(material_data['Толщина пластины, мкм'] - target_thickness)
    
    # Sort by thickness proximity and performance
    optimal_data = material_data.sort_values([
        'thickness_distance', 
        'Производительность, шт/час'
    ], ascending=[True, False])
    
    return optimal_data.head(10)  # Return top 10 closest matches


def get_disc_recommendations(
    data: pd.DataFrame,
    material: str,
    thickness: float,
    cut_type: str = None
) -> List[Dict[str, any]]:
    """
    Get disc recommendations based on material and thickness.
    
    Args:
        data (pd.DataFrame): Input DataFrame
        material (str): Target material
        thickness (float): Target thickness
        cut_type (str, optional): Specific cut type to consider
        
    Returns:
        List[Dict[str, any]]: List of recommended disc settings
    """
    material_data = data[data['Материал пластины'] == material].copy()
    
    if cut_type:
        material_data = material_data[material_data['Тип резки'] == cut_type]
    
    # Calculate distance to target thickness
    material_data['thickness_distance'] = abs(material_data['Толщина пластины, мкм'] - thickness)
    
    # Sort by thickness proximity and performance
    recommendations = material_data.sort_values([
        'thickness_distance', 
        'Производительность, шт/час',
        'Сколы лицевая сторона (медиана), мкм'
    ], ascending=[True, False, True])
    
    # Take top 5 recommendations
    top_recommendations = recommendations.head(5)
    
    result = []
    for _, row in top_recommendations.iterrows():
        result.append({
            'Артикул': row['Артикул диска'],
            'Толщина пластины (мкм)': row['Толщина пластины, мкм'],
            'Производительность (шт/час)': row['Производительность, шт/час'],
            'Сколы (лицевая сторона, мкм)': row['Сколы лицевая сторона (медиана), мкм'],
            'Сколы (обратная сторона, мкм)': row['Сколы обратная сторона (медиана), мкм'],
            'Срок службы диска (резов)': row['Срок службы диска, резов'],
            'Скорость подачи (мм/с)': row['Скорость подачи, мм/с'],
            'Частота оборотов шпинделя (об/мин)': row['Частота оборотов шпинделя, об/мин']
        })
    
    return result


def compare_materials(data: pd.DataFrame, materials: List[str]) -> pd.DataFrame:
    """
    Compare key metrics across different materials.
    
    Args:
        data (pd.DataFrame): Input DataFrame
        materials (List[str]): Materials to compare
        
    Returns:
        pd.DataFrame: Comparison table
    """
    comparison_data = []
    
    for material in materials:
        mat_data = data[data['Материал пластины'] == material]
        
        if not mat_data.empty:
            # Convert relevant columns to numeric, handling non-numeric values
            numeric_cols = [
                'Толщина пластины, мкм',
                'Сколы лицевая сторона (медиана), мкм',
                'Сколы обратная сторона (медиана), мкм',
                'Производительность, шт/час',
                'Срок службы диска, резов'
            ]
            
            for col in numeric_cols:
                if col in mat_data.columns:
                    mat_data = mat_data.copy()  # Explicitly work on a copy
                    mat_data[col] = pd.to_numeric(mat_data[col], errors='coerce')
            
            comparison_data.append({
                'Материал': material,
                'Количество': len(mat_data),
                'Средняя толщина пластины (мкм)': mat_data['Толщина пластины, мкм'].mean(),
                'Средние сколы (лицевая сторона, мкм)': mat_data['Сколы лицевая сторона (медиана), мкм'].mean(),
                'Средние сколы (обратная сторона, мкм)': mat_data['Сколы обратная сторона (медиана), мкм'].mean(),
                'Средняя производительность (шт/час)': mat_data['Производительность, шт/час'].mean(),
                'Средний срок службы диска (резов)': mat_data['Срок службы диска, резов'].mean(),
                'Минимальные сколы (лицевая сторона, мкм)': mat_data['Сколы лицевая сторона (медиана), мкм'].min(),
                'Максимальные сколы (лицевая сторона, мкм)': mat_data['Сколы лицевая сторона (медиана), мкм'].max(),
                'Лучшая производительность (шт/час)': mat_data['Производительность, шт/час'].max()
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    return comparison_df


def get_performance_trends(data: pd.DataFrame) -> Dict[str, List[Tuple]]:
    """
    Analyze performance trends across different parameters.
    
    Args:
        data (pd.DataFrame): Input DataFrame
        
    Returns:
        Dict[str, List[Tuple]]: Trends for different parameters
    """
    trends = {}
    
    # Thickness vs Performance trend
    if not data.empty:
        # Convert relevant columns to numeric
        data_for_trends = data.copy()
        data_for_trends['Толщина пластины, мкм'] = pd.to_numeric(data_for_trends['Толщина пластины, мкм'], errors='coerce')
        data_for_trends['Производительность, шт/час'] = pd.to_numeric(data_for_trends['Производительность, шт/час'], errors='coerce')
        
        # Drop rows with NaN values for grouping
        clean_data = data_for_trends.dropna(subset=['Толщина пластины, мкм', 'Производительность, шт/час'])
        
        thickness_perf = clean_data.groupby('Толщина пластины, мкм')['Производительность, шт/час'].mean()
        trends['thickness_vs_performance'] = list(thickness_perf.items())
        
        # Material vs Average Performance
        material_perf = clean_data.groupby('Материал пластины')['Производительность, шт/час'].mean()
        trends['material_vs_performance'] = list(material_perf.items())
        
        # Cut Type vs Average Performance
        cut_perf = clean_data.groupby('Тип резки')['Производительность, шт/час'].mean()
        trends['cut_type_vs_performance'] = list(cut_perf.items())
    
    return trends