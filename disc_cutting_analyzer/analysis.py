import pandas as pd
from typing import List, Dict, Tuple


def filter_data(
    data: pd.DataFrame,
    selected_materials: List[str],
    selected_cut_types: List[str],
    min_thickness: float,
    max_thickness: float,
    min_kerf_width: float,
    max_kerf_width: float,
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
        (data["Материал пластины"].isin(selected_materials))
        & (data["Тип резки"].isin(selected_cut_types))
        & (data["Толщина пластины, мкм"] >= min_thickness)
        & (data["Толщина пластины, мкм"] <= max_thickness)
        & (data["Ширина реза, мкм"] >= min_kerf_width)
        & (data["Ширина реза, мкм"] <= max_kerf_width)
    ].copy()

    return filtered_data


def _convert_numeric_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Convert specified columns to numeric, handling non-numeric values.

    Args:
        df (pd.DataFrame): Input DataFrame
        columns (List[str]): List of column names to convert

    Returns:
        pd.DataFrame: DataFrame with converted columns
    """
    df_copy = df.copy()
    for col in columns:
        if col in df_copy.columns:
            df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
    return df_copy


def _calculate_material_averages(material_data: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate average statistics for a specific material.

    Args:
        material_data (pd.DataFrame): DataFrame containing data for a single material

    Returns:
        Dict[str, float]: Dictionary containing average statistics for the material
    """
    # Define column mappings for better readability
    metric_columns = {
        "Количество": len(material_data),
        "Средняя толщина пластины (мкм)": "Толщина пластины, мкм",
        "Средние сколы (лицевая сторона, мкм)": "Сколы лицевая сторона (медиана), мкм",
        "Средние сколы (обратная сторона, мкм)": "Сколы обратная сторона (медиана), мкм",
        "Средняя производительность (шт/час)": "Производительность, шт/час",
        "Средний срок службы диска (резов)": "Срок службы диска, резов",
        "Средняя скорость подачи (мм/с)": "Скорость подачи, мм/с",
        "Средняя частота оборотов шпинделя (об/мин)": "Частота оборотов шпинделя, об/мин",
    }

    averages = {"Количество": metric_columns["Количество"]}

    # Calculate means for all numeric metrics
    for metric_name, column_name in metric_columns.items():
        if metric_name != "Количество" and column_name in material_data.columns:
            averages[metric_name] = material_data[column_name].mean()

    return averages


def get_material_statistics(data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Calculate statistics for each material in the dataset.

    Args:
        data (pd.DataFrame): Input DataFrame

    Returns:
        Dict[str, Dict[str, float]]: Statistics for each material
    """
    if data.empty:
        return {}

    # Define numeric columns that need to be converted
    numeric_columns = [
        "Толщина пластины, мкм",
        "Сколы лицевая сторона (медиана), мкм",
        "Сколы обратная сторона (медиана), мкм",
        "Производительность, шт/час",
        "Срок службы диска, резов",
        "Скорость подачи, мм/с",
        "Частота оборотов шпинделя, об/мин",
    ]

    # Pre-convert all numeric columns to optimize performance
    processed_data = _convert_numeric_columns(data, numeric_columns)

    # Get unique materials
    unique_materials = processed_data["Материал пластины"].dropna().unique()

    # Calculate statistics for each material
    material_stats = {}
    for material in unique_materials:
        material_subset = processed_data[
            processed_data["Материал пластины"] == material
        ]
        material_stats[material] = _calculate_material_averages(material_subset)

    return material_stats


def get_cut_type_analysis(data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Analyze data by cut type.

    Args:
        data (pd.DataFrame): Input DataFrame

    Returns:
        Dict[str, Dict[str, float]]: Analysis for each cut type
    """
    if data.empty:
        return {}

    # Define numeric columns that need to be converted
    numeric_columns = [
        "Толщина пластины, мкм",
        "Сколы лицевая сторона (медиана), мкм",
        "Сколы обратная сторона (медиана), мкм",
        "Производительность, шт/час",
        "Срок службы диска, резов",
        "Скорость подачи, мм/с",
        "Частота оборотов шпинделя, об/мин",
    ]

    # Pre-convert all numeric columns to optimize performance
    processed_data = _convert_numeric_columns(data, numeric_columns)

    # Get unique cut types
    unique_cut_types = processed_data["Тип резки"].dropna().unique()

    # Calculate statistics for each cut type
    cut_type_stats = {}
    for cut_type in unique_cut_types:
        cut_type_subset = processed_data[processed_data["Тип резки"] == cut_type]
        cut_type_stats[cut_type] = _calculate_material_averages(cut_type_subset)

    return cut_type_stats


def get_thickness_ranges(data: pd.DataFrame) -> List[Tuple[float, float]]:
    """
    Get common thickness ranges in the dataset.

    Args:
        data (pd.DataFrame): Input DataFrame

    Returns:
        List[Tuple[float, float]]: List of (min, max) thickness ranges
    """
    thickness_values = sorted(data["Толщина пластины, мкм"].unique())

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
    data: pd.DataFrame, material: str, target_thickness: float, cut_type: str = None
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
    material_data = data[data["Материал пластины"] == material].copy()

    if cut_type:
        material_data = material_data[material_data["Тип резки"] == cut_type]

    # Calculate distance to target thickness
    material_data["thickness_distance"] = abs(
        material_data["Толщина пластины, мкм"] - target_thickness
    )

    # Sort by thickness proximity and performance
    optimal_data = material_data.sort_values(
        ["thickness_distance", "Производительность, шт/час"], ascending=[True, False]
    )

    return optimal_data.head(10)  # Return top 10 closest matches


def get_disc_recommendations(
    data: pd.DataFrame, material: str, thickness: float, cut_type: str = None
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
    material_data = data[data["Материал пластины"] == material].copy()

    if cut_type:
        material_data = material_data[material_data["Тип резки"] == cut_type]

    # Calculate distance to target thickness
    material_data["thickness_distance"] = abs(
        material_data["Толщина пластины, мкм"] - thickness
    )

    # Sort by thickness proximity and performance
    recommendations = material_data.sort_values(
        [
            "thickness_distance",
            "Производительность, шт/час",
            "Сколы лицевая сторона (медиана), мкм",
        ],
        ascending=[True, False, True],
    )

    # Take top 5 recommendations
    top_recommendations = recommendations.head(5)

    result = []
    for _, row in top_recommendations.iterrows():
        result.append(
            {
                "Артикул": row["Артикул диска"],
                "Толщина пластины (мкм)": row["Толщина пластины, мкм"],
                "Производительность (шт/час)": row["Производительность, шт/час"],
                "Сколы (лицевая сторона, мкм)": row[
                    "Сколы лицевая сторона (медиана), мкм"
                ],
                "Сколы (обратная сторона, мкм)": row[
                    "Сколы обратная сторона (медиана), мкм"
                ],
                "Срок службы диска (резов)": row["Срок службы диска, резов"],
                "Скорость подачи (мм/с)": row["Скорость подачи, мм/с"],
                "Частота оборотов шпинделя (об/мин)": row[
                    "Частота оборотов шпинделя, об/мин"
                ],
            }
        )

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
        mat_data = data[data["Материал пластины"] == material]

        if not mat_data.empty:
            # Convert relevant columns to numeric, handling non-numeric values
            numeric_cols = [
                "Толщина пластины, мкм",
                "Сколы лицевая сторона (медиана), мкм",
                "Сколы обратная сторона (медиана), мкм",
                "Производительность, шт/час",
                "Срок службы диска, резов",
            ]

            for col in numeric_cols:
                if col in mat_data.columns:
                    mat_data = mat_data.copy()  # Explicitly work on a copy
                    mat_data[col] = pd.to_numeric(mat_data[col], errors="coerce")

            comparison_data.append(
                {
                    "Материал": material,
                    "Количество": len(mat_data),
                    "Средняя толщина пластины (мкм)": mat_data[
                        "Толщина пластины, мкм"
                    ].mean(),
                    "Средние сколы (лицевая сторона, мкм)": mat_data[
                        "Сколы лицевая сторона (медиана), мкм"
                    ].mean(),
                    "Средние сколы (обратная сторона, мкм)": mat_data[
                        "Сколы обратная сторона (медиана), мкм"
                    ].mean(),
                    "Средняя производительность (шт/час)": mat_data[
                        "Производительность, шт/час"
                    ].mean(),
                    "Средний срок службы диска (резов)": mat_data[
                        "Срок службы диска, резов"
                    ].mean(),
                    "Минимальные сколы (лицевая сторона, мкм)": mat_data[
                        "Сколы лицевая сторона (медиана), мкм"
                    ].min(),
                    "Максимальные сколы (лицевая сторона, мкм)": mat_data[
                        "Сколы лицевая сторона (медиана), мкм"
                    ].max(),
                    "Лучшая производительность (шт/час)": mat_data[
                        "Производительность, шт/час"
                    ].max(),
                }
            )

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
        data_for_trends["Толщина пластины, мкм"] = pd.to_numeric(
            data_for_trends["Толщина пластины, мкм"], errors="coerce"
        )
        data_for_trends["Производительность, шт/час"] = pd.to_numeric(
            data_for_trends["Производительность, шт/час"], errors="coerce"
        )

        # Drop rows with NaN values for grouping
        clean_data = data_for_trends.dropna(
            subset=["Толщина пластины, мкм", "Производительность, шт/час"]
        )

        thickness_perf = clean_data.groupby("Толщина пластины, мкм")[
            "Производительность, шт/час"
        ].mean()
        trends["thickness_vs_performance"] = list(thickness_perf.items())

        # Material vs Average Performance
        material_perf = clean_data.groupby("Материал пластины")[
            "Производительность, шт/час"
        ].mean()
        trends["material_vs_performance"] = list(material_perf.items())

        # Cut Type vs Average Performance
        cut_perf = clean_data.groupby("Тип резки")["Производительность, шт/час"].mean()
        trends["cut_type_vs_performance"] = list(cut_perf.items())

    return trends
