import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import List, Optional
import numpy as np


def create_chipping_plot(
    data: pd.DataFrame,
    selected_materials: List[str],
    selected_cut_types: List[str],
    min_thickness: float,
    max_thickness: float,
    min_kerf_width: float,
    max_kerf_width: float
) -> go.Figure:
    """
    Create an interactive plot showing chipping metrics vs wafer thickness by material.
    
    Args:
        data (pd.DataFrame): Filtered data to plot
        selected_materials (List[str]): Selected materials
        selected_cut_types (List[str]): Selected cut types
        min_thickness (float): Minimum thickness for filtering
        max_thickness (float): Maximum thickness for filtering
        min_kerf_width (float): Minimum kerf width for filtering
        max_kerf_width (float): Maximum kerf width for filtering
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Apply filters
    filtered_data = data[
        (data['Материал пластины'].isin(selected_materials)) &
        (data['Тип резки'].isin(selected_cut_types)) &
        (data['Толщина пластины, мкм'] >= min_thickness) &
        (data['Толщина пластины, мкм'] <= max_thickness) &
        (data['Ширина реза, мкм'] >= min_kerf_width) &
        (data['Ширина реза, мкм'] <= max_kerf_width)
    ].copy()
    
    if filtered_data.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available for selected filters", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font_size=16)
        return fig
    
    # Create subplots for different chipping metrics
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=['Front Side Chipping (Median)', 'Back Side Chipping (Median)'],
        vertical_spacing=0.2
    )
    
    for material in selected_materials:
        for cut_type in selected_cut_types:  # Loop through cut types to differentiate them visually
            material_cut_data = filtered_data[
                (filtered_data['Материал пластины'] == material) &
                (filtered_data['Тип резки'] == cut_type)
            ]
            
            if not material_cut_data.empty:
                # Ensure data is numeric for both axes
                material_cut_data = material_cut_data.copy()
                material_cut_data['Толщина пластины, мкм'] = pd.to_numeric(material_cut_data['Толщина пластины, мкм'], errors='coerce')
                material_cut_data['Сколы лицевая сторона (медиана), мкм'] = pd.to_numeric(material_cut_data['Сколы лицевая сторона (медиана), мкм'], errors='coerce')
                
                # Clean the data by removing NaN values
                clean_front_data = material_cut_data[
                    material_cut_data['Толщина пластины, мкм'].notna() &
                    material_cut_data['Сколы лицевая сторона (медиана), мкм'].notna()
                ]
                
                if not clean_front_data.empty:
                    # Front side chipping
                    fig.add_trace(
                        go.Scatter(
                            x=clean_front_data['Толщина пластины, мкм'],
                            y=clean_front_data['Сколы лицевая сторона (медиана), мкм'],
                            mode='markers',
                            name=f'{material} ({cut_type}) - Front Side',
                            legendgroup=f'{material}-{cut_type}',
                            showlegend=True
                        ),
                        row=1, col=1
                    )
                    
                    # Add trend line for front side chipping
                    if len(clean_front_data) > 1:
                        x_vals = clean_front_data['Толщина пластины, мкм'].values
                        y_vals = clean_front_data['Сколы лицевая сторона (медиана), мкм'].values
                        # Ensure both arrays have same length and no NaN values
                        mask = ~(np.isnan(x_vals) | np.isnan(y_vals))
                        x_clean = x_vals[mask]
                        y_clean = y_vals[mask]
                        
                        if len(x_clean) > 1:
                            z = np.polyfit(x_clean, y_clean, 1)
                            p = np.poly1d(z)
                            fig.add_trace(
                                go.Scatter(
                                    x=x_clean,
                                    y=p(x_clean),
                                    mode='lines',
                                    name=f'{material} ({cut_type}) - Front Side Trend',
                                    legendgroup=f'{material}-{cut_type}',
                                    showlegend=False,
                                    line=dict(dash='dash', width=1)
                                ),
                                row=1, col=1
                            )
                
                # Back side chipping (if available)
                if 'Сколы обратная сторона (медиана), мкм' in material_cut_data.columns:
                    # Ensure data is numeric for back side
                    material_cut_data['Сколы обратная сторона (медиана), мкм'] = pd.to_numeric(material_cut_data['Сколы обратная сторона (медиана), мкм'], errors='coerce')
                    
                    # Clean the data by removing NaN values
                    clean_back_data = material_cut_data[
                        material_cut_data['Толщина пластины, мкм'].notna() &
                        material_cut_data['Сколы обратная сторона (медиана), мкм'].notna()
                    ]
                    
                    if not clean_back_data.empty:
                        fig.add_trace(
                            go.Scatter(
                                x=clean_back_data['Толщина пластины, мкм'],
                                y=clean_back_data['Сколы обратная сторона (медиана), мкм'],
                                mode='markers',
                                name=f'{material} ({cut_type}) - Back Side',
                                legendgroup=f'{material}-{cut_type}',
                                showlegend=True
                            ),
                            row=2, col=1
                        )
                        
                        # Add trend line for back side chipping
                        if len(clean_back_data) > 1:
                            x_vals = clean_back_data['Толщина пластины, мкм'].values
                            y_vals = clean_back_data['Сколы обратная сторона (медиана), мкм'].values
                            # Ensure both arrays have same length and no NaN values
                            mask = ~(np.isnan(x_vals) | np.isnan(y_vals))
                            x_clean = x_vals[mask]
                            y_clean = y_vals[mask]
                            
                            if len(x_clean) > 1:
                                z = np.polyfit(x_clean, y_clean, 1)
                                p = np.poly1d(z)
                                fig.add_trace(
                                    go.Scatter(
                                        x=x_clean,
                                        y=p(x_clean),
                                        mode='lines',
                                        name=f'{material} ({cut_type}) - Back Side Trend',
                                        legendgroup=f'{material}-{cut_type}',
                                        showlegend=False,
                                        line=dict(dash='dash', width=1)
                                    ),
                                    row=2, col=1
                                )
    
    fig.update_xaxes(title_text="Wafer Thickness (μm)", row=1, col=1)
    fig.update_xaxes(title_text="Wafer Thickness (μm)", row=2, col=1)
    fig.update_yaxes(title_text="Chipping (μm)", row=1, col=1)
    fig.update_yaxes(title_text="Chipping (μm)", row=2, col=1)
    
    fig.update_layout(
        title="Chipping Metrics vs Wafer Thickness by Material",
        height=800,
        hovermode='x unified'
    )
    
    return fig


def create_performance_plot(
    data: pd.DataFrame,
    selected_materials: List[str],
    selected_cut_types: List[str],
    min_thickness: float,
    max_thickness: float,
    min_kerf_width: float,
    max_kerf_width: float
) -> go.Figure:
    """
    Create an interactive plot showing performance metrics vs wafer thickness by material.
    
    Args:
        data (pd.DataFrame): Filtered data to plot
        selected_materials (List[str]): Selected materials
        selected_cut_types (List[str]): Selected cut types
        min_thickness (float): Minimum thickness for filtering
        max_thickness (float): Maximum thickness for filtering
        min_kerf_width (float): Minimum kerf width for filtering
        max_kerf_width (float): Maximum kerf width for filtering
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Apply filters
    filtered_data = data[
        (data['Материал пластины'].isin(selected_materials)) &
        (data['Тип резки'].isin(selected_cut_types)) &
        (data['Толщина пластины, мкм'] >= min_thickness) &
        (data['Толщина пластины, мкм'] <= max_thickness) &
        (data['Ширина реза, мкм'] >= min_kerf_width) &
        (data['Ширина реза, мкм'] <= max_kerf_width)
    ].copy()
    
    if filtered_data.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available for selected filters", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font_size=16)
        return fig
    
    # Create subplots for performance and blade life
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=['Performance (pcs/hour)', 'Blade Life (cuts)'],
        vertical_spacing=0.2
    )
    
    for material in selected_materials:
        for cut_type in selected_cut_types:  # Loop through cut types to differentiate them visually
            material_cut_data = filtered_data[
                (filtered_data['Материал пластины'] == material) &
                (filtered_data['Тип резки'] == cut_type)
            ]
            
            if not material_cut_data.empty:
                # Ensure data is numeric for performance
                material_cut_data = material_cut_data.copy()
                material_cut_data['Толщина пластины, мкм'] = pd.to_numeric(material_cut_data['Толщина пластины, мкм'], errors='coerce')
                material_cut_data['Производительность, шт/час'] = pd.to_numeric(material_cut_data['Производительность, шт/час'], errors='coerce')
                
                # Clean the data by removing NaN values
                clean_perf_data = material_cut_data[
                    material_cut_data['Толщина пластины, мкм'].notna() &
                    material_cut_data['Производительность, шт/час'].notna()
                ]
                
                if not clean_perf_data.empty:
                    # Performance
                    fig.add_trace(
                        go.Scatter(
                            x=clean_perf_data['Толщина пластины, мкм'],
                            y=clean_perf_data['Производительность, шт/час'],
                            mode='markers',
                            name=f'{material} ({cut_type}) - Performance',
                            legendgroup=f'{material}-{cut_type}',
                            showlegend=True
                        ),
                        row=1, col=1
                    )
                    
                    # Add trend line for performance
                    if len(clean_perf_data) > 1:
                        x_vals = clean_perf_data['Толщина пластины, мкм'].values
                        y_vals = clean_perf_data['Производительность, шт/час'].values
                        # Ensure both arrays have same length and no NaN values
                        mask = ~(np.isnan(x_vals) | np.isnan(y_vals))
                        x_clean = x_vals[mask]
                        y_clean = y_vals[mask]
                        
                        if len(x_clean) > 1:
                            z = np.polyfit(x_clean, y_clean, 1)
                            p = np.poly1d(z)
                            fig.add_trace(
                                go.Scatter(
                                    x=x_clean,
                                    y=p(x_clean),
                                    mode='lines',
                                    name=f'{material} ({cut_type}) - Performance Trend',
                                    legendgroup=f'{material}-{cut_type}',
                                    showlegend=False,
                                    line=dict(dash='dash', width=1)
                                ),
                                row=1, col=1
                            )
                
                # Blade life
                # Ensure data is numeric for blade life
                material_cut_data['Срок службы диска, резов'] = pd.to_numeric(material_cut_data['Срок службы диска, резов'], errors='coerce')
                
                # Clean the data by removing NaN values
                clean_blade_data = material_cut_data[
                    material_cut_data['Толщина пластины, мкм'].notna() &
                    material_cut_data['Срок службы диска, резов'].notna()
                ]
                
                if not clean_blade_data.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=clean_blade_data['Толщина пластины, мкм'],
                            y=clean_blade_data['Срок службы диска, резов'],
                            mode='markers',
                            name=f'{material} ({cut_type}) - Blade Life',
                            legendgroup=f'{material}-{cut_type}',
                            showlegend=True
                        ),
                        row=2, col=1
                    )
                    
                    # Add trend line for blade life
                    if len(clean_blade_data) > 1:
                        x_vals = clean_blade_data['Толщина пластины, мкм'].values
                        y_vals = clean_blade_data['Срок службы диска, резов'].values
                        # Ensure both arrays have same length and no NaN values
                        mask = ~(np.isnan(x_vals) | np.isnan(y_vals))
                        x_clean = x_vals[mask]
                        y_clean = y_vals[mask]
                        
                        if len(x_clean) > 1:
                            z = np.polyfit(x_clean, y_clean, 1)
                            p = np.poly1d(z)
                            fig.add_trace(
                                go.Scatter(
                                    x=x_clean,
                                    y=p(x_clean),
                                    mode='lines',
                                    name=f'{material} ({cut_type}) - Blade Life Trend',
                                    legendgroup=f'{material}-{cut_type}',
                                    showlegend=False,
                                    line=dict(dash='dash', width=1)
                                ),
                                row=2, col=1
                            )
    
    fig.update_xaxes(title_text="Wafer Thickness (μm)", row=1, col=1)
    fig.update_xaxes(title_text="Wafer Thickness (μm)", row=2, col=1)
    fig.update_yaxes(title_text="Performance (pcs/hour)", row=1, col=1)
    fig.update_yaxes(title_text="Blade Life (cuts)", row=2, col=1)
    
    fig.update_layout(
        title="Performance Metrics vs Wafer Thickness by Material",
        height=800,
        hovermode='x unified'
    )
    
    return fig


def create_process_parameters_plot(
    data: pd.DataFrame,
    selected_materials: List[str],
    selected_cut_types: List[str],
    min_thickness: float,
    max_thickness: float,
    min_kerf_width: float,
    max_kerf_width: float
) -> go.Figure:
    """
    Create an interactive plot showing process parameters vs wafer thickness by material.
    
    Args:
        data (pd.DataFrame): Filtered data to plot
        selected_materials (List[str]): Selected materials
        selected_cut_types (List[str]): Selected cut types
        min_thickness (float): Minimum thickness for filtering
        max_thickness (float): Maximum thickness for filtering
        min_kerf_width (float): Minimum kerf width for filtering
        max_kerf_width (float): Maximum kerf width for filtering
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Apply filters
    filtered_data = data[
        (data['Материал пластины'].isin(selected_materials)) &
        (data['Тип резки'].isin(selected_cut_types)) &
        (data['Толщина пластины, мкм'] >= min_thickness) &
        (data['Толщина пластины, мкм'] <= max_thickness) &
        (data['Ширина реза, мкм'] >= min_kerf_width) &
        (data['Ширина реза, мкм'] <= max_kerf_width)
    ].copy()
    
    if filtered_data.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available for selected filters", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font_size=16)
        return fig
    
    # Create subplots for process parameters
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=['Kerf Width (μm)', 'Feed Rate (mm/s)', 'Spindle Speed (RPM)'],
        vertical_spacing=0.15
    )
    
    for material in selected_materials:
        for cut_type in selected_cut_types:  # Loop through cut types to differentiate them visually
            material_cut_data = filtered_data[
                (filtered_data['Материал пластины'] == material) &
                (filtered_data['Тип резки'] == cut_type)
            ]
            
            if not material_cut_data.empty:
                # Ensure data is numeric for all parameters
                material_cut_data = material_cut_data.copy()
                material_cut_data['Толщина пластины, мкм'] = pd.to_numeric(material_cut_data['Толщина пластины, мкм'], errors='coerce')
                material_cut_data['Ширина реза, мкм'] = pd.to_numeric(material_cut_data['Ширина реза, мкм'], errors='coerce')
                
                # Clean the data by removing NaN values
                clean_kerf_data = material_cut_data[
                    material_cut_data['Толщина пластины, мкм'].notna() &
                    material_cut_data['Ширина реза, мкм'].notna()
                ]
                
                if not clean_kerf_data.empty:
                    # Kerf width
                    fig.add_trace(
                        go.Scatter(
                            x=clean_kerf_data['Толщина пластины, мкм'],
                            y=clean_kerf_data['Ширина реза, мкм'],
                            mode='markers',
                            name=f'{material} ({cut_type}) - Kerf Width',
                            legendgroup=f'{material}-{cut_type}',
                            showlegend=True
                        ),
                        row=1, col=1
                    )
                    
                    # Add trend line for kerf width
                    if len(clean_kerf_data) > 1:
                        x_vals = clean_kerf_data['Толщина пластины, мкм'].values
                        y_vals = clean_kerf_data['Ширина реза, мкм'].values
                        # Ensure both arrays have same length and no NaN values
                        mask = ~(np.isnan(x_vals) | np.isnan(y_vals))
                        x_clean = x_vals[mask]
                        y_clean = y_vals[mask]
                        
                        if len(x_clean) > 1:
                            z = np.polyfit(x_clean, y_clean, 1)
                            p = np.poly1d(z)
                            fig.add_trace(
                                go.Scatter(
                                    x=x_clean,
                                    y=p(x_clean),
                                    mode='lines',
                                    name=f'{material} ({cut_type}) - Kerf Width Trend',
                                    legendgroup=f'{material}-{cut_type}',
                                    showlegend=False,
                                    line=dict(dash='dash', width=1)
                                ),
                                row=1, col=1
                            )
                
                # Feed rate
                material_cut_data['Скорость подачи, мм/с'] = pd.to_numeric(material_cut_data['Скорость подачи, мм/с'], errors='coerce')
                
                # Clean the data by removing NaN values
                clean_feed_data = material_cut_data[
                    material_cut_data['Толщина пластины, мкм'].notna() &
                    material_cut_data['Скорость подачи, мм/с'].notna()
                ]
                
                if not clean_feed_data.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=clean_feed_data['Толщина пластины, мкм'],
                            y=clean_feed_data['Скорость подачи, мм/с'],
                            mode='markers',
                            name=f'{material} ({cut_type}) - Feed Rate',
                            legendgroup=f'{material}-{cut_type}',
                            showlegend=False
                        ),
                        row=2, col=1
                    )
                    
                    # Add trend line for feed rate
                    if len(clean_feed_data) > 1:
                        x_vals = clean_feed_data['Толщина пластины, мкм'].values
                        y_vals = clean_feed_data['Скорость подачи, мм/с'].values
                        # Ensure both arrays have same length and no NaN values
                        mask = ~(np.isnan(x_vals) | np.isnan(y_vals))
                        x_clean = x_vals[mask]
                        y_clean = y_vals[mask]
                        
                        if len(x_clean) > 1:
                            z = np.polyfit(x_clean, y_clean, 1)
                            p = np.poly1d(z)
                            fig.add_trace(
                                go.Scatter(
                                    x=x_clean,
                                    y=p(x_clean),
                                    mode='lines',
                                    name=f'{material} ({cut_type}) - Feed Rate Trend',
                                    legendgroup=f'{material}-{cut_type}',
                                    showlegend=False,
                                    line=dict(dash='dash', width=1)
                                ),
                                row=2, col=1
                            )
                
                # Spindle speed
                material_cut_data['Частота оборотов шпинделя, об/мин'] = pd.to_numeric(material_cut_data['Частота оборотов шпинделя, об/мин'], errors='coerce')
                
                # Clean the data by removing NaN values
                clean_spindle_data = material_cut_data[
                    material_cut_data['Толщина пластины, мкм'].notna() &
                    material_cut_data['Частота оборотов шпинделя, об/мин'].notna()
                ]
                
                if not clean_spindle_data.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=clean_spindle_data['Толщина пластины, мкм'],
                            y=clean_spindle_data['Частота оборотов шпинделя, об/мин'],
                            mode='markers',
                            name=f'{material} ({cut_type}) - Spindle Speed',
                            legendgroup=f'{material}-{cut_type}',
                            showlegend=False
                        ),
                        row=3, col=1
                    )
                    
                    # Add trend line for spindle speed
                    if len(clean_spindle_data) > 1:
                        x_vals = clean_spindle_data['Толщина пластины, мкм'].values
                        y_vals = clean_spindle_data['Частота оборотов шпинделя, об/мин'].values
                        # Ensure both arrays have same length and no NaN values
                        mask = ~(np.isnan(x_vals) | np.isnan(y_vals))
                        x_clean = x_vals[mask]
                        y_clean = y_vals[mask]
                        
                        if len(x_clean) > 1:
                            z = np.polyfit(x_clean, y_clean, 1)
                            p = np.poly1d(z)
                            fig.add_trace(
                                go.Scatter(
                                    x=x_clean,
                                    y=p(x_clean),
                                    mode='lines',
                                    name=f'{material} ({cut_type}) - Spindle Speed Trend',
                                    legendgroup=f'{material}-{cut_type}',
                                    showlegend=False,
                                    line=dict(dash='dash', width=1)
                                ),
                                row=3, col=1
                            )
    
    fig.update_xaxes(title_text="Wafer Thickness (μm)", row=1, col=1)
    fig.update_xaxes(title_text="Wafer Thickness (μm)", row=2, col=1)
    fig.update_xaxes(title_text="Wafer Thickness (μm)", row=3, col=1)
    fig.update_yaxes(title_text="Width (μm)", row=1, col=1)
    fig.update_yaxes(title_text="Rate (mm/s)", row=2, col=1)
    fig.update_yaxes(title_text="Speed (RPM)", row=3, col=1)
    
    fig.update_layout(
        title="Process Parameters vs Wafer Thickness by Material",
        height=1000,
        hovermode='x unified'
    )
    
    return fig


def create_disc_parameters_plot(
    data: pd.DataFrame,
    selected_materials: List[str],
    selected_cut_types: List[str],
    min_thickness: float,
    max_thickness: float,
    min_kerf_width: float,
    max_kerf_width: float
) -> go.Figure:
    """
    Create an interactive plot showing disc parameters vs wafer thickness by material.
    
    Args:
        data (pd.DataFrame): Filtered data to plot
        selected_materials (List[str]): Selected materials
        selected_cut_types (List[str]): Selected cut types
        min_thickness (float): Minimum thickness for filtering
        max_thickness (float): Maximum thickness for filtering
        min_kerf_width (float): Minimum kerf width for filtering
        max_kerf_width (float): Maximum kerf width for filtering
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Apply filters
    filtered_data = data[
        (data['Материал пластины'].isin(selected_materials)) &
        (data['Тип резки'].isin(selected_cut_types)) &
        (data['Толщина пластины, мкм'] >= min_thickness) &
        (data['Толщина пластины, мкм'] <= max_thickness) &
        (data['Ширина реза, мкм'] >= min_kerf_width) &
        (data['Ширина реза, мкм'] <= max_kerf_width)
    ].copy()
    
    if filtered_data.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available for selected filters", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font_size=16)
        return fig
    
    # Create subplots for disc parameters
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=['Grit Size (mesh)', 'Diamond Concentration (%)'],
        vertical_spacing=0.1
    )
    
    for material in selected_materials:
        material_data = filtered_data[filtered_data['Материал пластины'] == material]
        
        if not material_data.empty:
            # Note: We can't plot disc parameters directly from the main data
            # because the disc parameters are encoded in the article number
            # So we'll just show a placeholder for now
            fig.add_trace(
                go.Scatter(
                    x=[min_thickness, max_thickness],
                    y=[0, 0],
                    mode='lines',
                    name=f'{material}',
                    showlegend=False,
                    line=dict(color='rgba(0,0,0,0)')
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=[min_thickness, max_thickness],
                    y=[0, 0],
                    mode='lines',
                    name=f'{material}',
                    showlegend=False,
                    line=dict(color='rgba(0,0,0,0)')
                ),
                row=2, col=1
            )
    
    fig.update_xaxes(title_text="Wafer Thickness (μm)", row=1, col=1)
    fig.update_xaxes(title_text="Wafer Thickness (μm)", row=2, col=1)
    fig.update_yaxes(title_text="Value", row=1, col=1)
    fig.update_yaxes(title_text="Value", row=2, col=1)
    
    fig.update_layout(
        title="Disc Parameters vs Wafer Thickness by Material (Decode articles for actual values)",
        height=600,
        annotations=[
            dict(
                x=0.5, y=0.75,
                xref="paper", yref="paper",
                text="Grit size and diamond concentration are encoded in the disc article number",
                showarrow=False, font_size=12
            ),
            dict(
                x=0.5, y=0.25,
                xref="paper", yref="paper",
                text="Use the article decoder to get specific disc parameter values",
                showarrow=False, font_size=12
            )
        ]
    )
    
    return fig


def create_summary_metrics(
    data: pd.DataFrame,
    selected_materials: List[str],
    selected_cut_types: List[str],
    min_thickness: float,
    max_thickness: float,
    min_kerf_width: float,
    max_kerf_width: float
) -> dict:
    """
    Calculate summary metrics for the selected data.
    
    Args:
        data (pd.DataFrame): Filtered data to calculate metrics for
        selected_materials (List[str]): Selected materials
        selected_cut_types (List[str]): Selected cut types
        min_thickness (float): Minimum thickness for filtering
        max_thickness (float): Maximum thickness for filtering
        min_kerf_width (float): Minimum kerf width for filtering
        max_kerf_width (float): Maximum kerf width for filtering
        
    Returns:
        dict: Dictionary containing calculated metrics
    """
    # Apply filters
    filtered_data = data[
        (data['Материал пластины'].isin(selected_materials)) &
        (data['Тип резки'].isin(selected_cut_types)) &
        (data['Толщина пластины, мкм'] >= min_thickness) &
        (data['Толщина пластины, мкм'] <= max_thickness) &
        (data['Ширина реза, мкм'] >= min_kerf_width) &
        (data['Ширина реза, мкм'] <= max_kerf_width)
    ].copy()
    
    if filtered_data.empty:
        return {
            'avg_front_chipping': 0,
            'avg_back_chipping': 0,
            'avg_performance': 0,
            'avg_blade_life': 0,
            'total_records': 0
        }
    
    # Calculate metrics - convert to numeric first, handling non-numeric values
    front_chipping_col = 'Сколы лицевая сторона (медиана), мкм'
    performance_col = 'Производительность, шт/час'
    blade_life_col = 'Срок службы диска, резов'
    back_chipping_col = 'Сколы обратная сторона (медиана), мкм'
    
    # Convert columns to numeric, coercing errors to NaN
    filtered_data[front_chipping_col] = pd.to_numeric(filtered_data[front_chipping_col], errors='coerce')
    filtered_data[performance_col] = pd.to_numeric(filtered_data[performance_col], errors='coerce')
    filtered_data[blade_life_col] = pd.to_numeric(filtered_data[blade_life_col], errors='coerce')
    filtered_data[back_chipping_col] = pd.to_numeric(filtered_data[back_chipping_col], errors='coerce')
    
    avg_front_chipping = filtered_data[front_chipping_col].mean()
    avg_performance = filtered_data[performance_col].mean()
    avg_blade_life = filtered_data[blade_life_col].mean()
    
    # Handle back chipping separately as it might not be available for all records
    back_chipping_data = filtered_data[
        filtered_data[back_chipping_col].notna()
    ]
    avg_back_chipping = back_chipping_data[back_chipping_col].mean() if not back_chipping_data.empty else 0
    
    return {
        'avg_front_chipping': round(avg_front_chipping, 2) if pd.notna(avg_front_chipping) else 0,
        'avg_back_chipping': round(avg_back_chipping, 2) if pd.notna(avg_back_chipping) else 0,
        'avg_performance': round(avg_performance, 2) if pd.notna(avg_performance) else 0,
        'avg_blade_life': round(avg_blade_life, 2) if pd.notna(avg_blade_life) else 0,
        'total_records': len(filtered_data)
    }