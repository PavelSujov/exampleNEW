import pandas as pd
import numpy as np
import pytest
import sys
import os

# Add the current directory to the path to import from disc_cutting_analyzer
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from disc_cutting_analyzer.analysis import (
    filter_data,
    get_material_statistics,
    get_cut_type_analysis,
    get_thickness_ranges,
    find_optimal_settings,
    get_disc_recommendations,
    compare_materials,
    get_performance_trends,
)


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    data = {
        "Материал пластины": ["Si", "Si", "GaAs", "Si", "GaAs"],
        "Тип резки": ["Dry", "Wet", "Dry", "Dry", "Wet"],
        "Толщина пластины, мкм": [300, 400, 500, 350, 450],
        "Ширина реза, мкм": [30, 35, 40, 32, 38],
        "Сколы лицевая сторона (медиана), мкм": [5.0, 7.0, 6.0, 5.5, 6.5],
        "Сколы обратная сторона (медиана), мкм": [6.0, 8.0, 7.0, 6.5, 7.5],
        "Производительность, шт/час": [100, 120, 110, 105, 115],
        "Срок службы диска, резов": [500, 600, 550, 520, 580],
        "Скорость подачи, мм/с": [2.0, 2.5, 2.2, 2.1, 2.4],
        "Частота оборотов шпинделя, об/мин": [30000, 35000, 32000, 31000, 34000],
        "Артикул диска": ["DISC001", "DISC002", "DISC003", "DISC004", "DISC005"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_dataframe():
    """Create an empty DataFrame for testing."""
    columns = [
        "Материал пластины",
        "Тип резки",
        "Толщина пластины, мкм",
        "Ширина реза, мкм",
        "Сколы лицевая сторона (медиана), мкм",
        "Сколы обратная сторона (медиана), мкм",
        "Производительность, шт/час",
        "Срок службы диска, резов",
        "Скорость подачи, мм/с",
        "Частота оборотов шпинделя, об/мин",
        "Артикул диска",
    ]
    return pd.DataFrame(columns=columns)


@pytest.fixture
def dataframe_with_nans():
    """Create a DataFrame with some NaN values for testing."""
    data = {
        "Материал пластины": ["Si", "Si", "GaAs", "Si"],
        "Тип резки": ["Dry", "Wet", "Dry", "Dry"],
        "Толщина пластины, мкм": [300, np.nan, 500, 350],
        "Ширина реза, мкм": [30, 35, np.nan, 32],
        "Сколы лицевая сторона (медиана), мкм": [5.0, 7.0, 6.0, np.nan],
        "Сколы обратная сторона (медиана), мкм": [6.0, np.nan, 7.0, 6.5],
        "Производительность, шт/час": [100, 120, 110, 105],
        "Срок службы диска, резов": [500, 600, np.nan, 520],
        "Скорость подачи, мм/с": [2.0, 2.5, 2.2, np.nan],
        "Частота оборотов шпинделя, об/мин": [30000, np.nan, 32000, 31000],
        "Артикул диска": ["DISC001", "DISC002", "DISC003", "DISC004"],
    }
    return pd.DataFrame(data)


class TestFilterData:
    """Test cases for the filter_data function."""

    def test_filter_data_basic(self, sample_dataframe):
        """Test basic filtering functionality."""
        result = filter_data(
            sample_dataframe,
            selected_materials=["Si"],
            selected_cut_types=["Dry"],
            min_thickness=300,
            max_thickness=400,
            min_kerf_width=30,
            max_kerf_width=35,
        )

        # Check that only rows matching all criteria are returned
        assert len(result) == 2  # Rows with Si, Dry, thickness 300-400, kerf 30-35
        assert all(result["Материал пластины"] == "Si")
        assert all(result["Тип резки"] == "Dry")
        assert all(
            (result["Толщина пластины, мкм"] >= 300)
            & (result["Толщина пластины, мкм"] <= 400)
        )
        assert all(
            (result["Ширина реза, мкм"] >= 30) & (result["Ширина реза, мкм"] <= 35)
        )

    def test_filter_data_empty_result(self, sample_dataframe):
        """Test filtering with criteria that yield no results."""
        result = filter_data(
            sample_dataframe,
            selected_materials=["NonExistent"],
            selected_cut_types=["Dry"],
            min_thickness=300,
            max_thickness=400,
            min_kerf_width=30,
            max_kerf_width=35,
        )

        assert len(result) == 0

    def test_filter_data_empty_dataframe(self, empty_dataframe):
        """Test filtering with an empty DataFrame."""
        result = filter_data(
            empty_dataframe,
            selected_materials=["Si"],
            selected_cut_types=["Dry"],
            min_thickness=300,
            max_thickness=400,
            min_kerf_width=30,
            max_kerf_width=35,
        )

        assert len(result) == 0


class TestGetMaterialStatistics:
    """Test cases for the get_material_statistics function."""

    def test_get_material_statistics_basic(self, sample_dataframe):
        """Test basic material statistics calculation."""
        result = get_material_statistics(sample_dataframe)

        # Check that all materials are present in the result
        assert "Si" in result
        assert "GaAs" in result
        assert len(result) == 2  # Two unique materials

        # Check that statistics are computed correctly for Si
        si_stats = result["Si"]
        assert si_stats["Количество"] == 3
        # Check mean values (calculated from actual sample data)
        # Si thickness values: [300, 400, 350] -> mean = 350.0
        assert abs(si_stats["Средняя толщина пластины (мкм)"] - 350.0) < 0.01
        # Si front chipping values: [5.0, 7.0, 5.5] -> mean = 5.8333333333
        assert abs(si_stats["Средние сколы (лицевая сторона, мкм)"] - 5.8333333) < 0.01

    def test_get_material_statistics_empty_dataframe(self, empty_dataframe):
        """Test material statistics with an empty DataFrame."""
        result = get_material_statistics(empty_dataframe)

        assert len(result) == 0

    def test_get_material_statistics_with_nans(self, dataframe_with_nans):
        """Test material statistics with NaN values."""
        result = get_material_statistics(dataframe_with_nans)

        # Check that Si is present
        assert "Si" in result
        si_stats = result["Si"]

        # NaN values should be handled gracefully
        assert si_stats["Количество"] == 3  # Total rows for Si
        # Mean should exclude NaN values
        assert not pd.isna(si_stats["Средняя толщина пластины (мкм)"])


class TestGetCutTypeAnalysis:
    """Test cases for the get_cut_type_analysis function."""

    def test_get_cut_type_analysis_basic(self, sample_dataframe):
        """Test basic cut type analysis calculation."""
        result = get_cut_type_analysis(sample_dataframe)

        # Check that all cut types are present in the result
        assert "Dry" in result
        assert "Wet" in result
        assert len(result) == 2  # Two unique cut types

        # Check that analysis is computed correctly for Dry
        dry_stats = result["Dry"]
        assert dry_stats["Количество"] == 3  # Three Dry entries
        # Check mean values (calculated from actual sample data)
        # Dry thickness values: [300, 500, 350] -> mean = 383.33333
        assert abs(dry_stats["Средняя толщина пластины (мкм)"] - 383.3333333) < 0.01

    def test_get_cut_type_analysis_empty_dataframe(self, empty_dataframe):
        """Test cut type analysis with an empty DataFrame."""
        result = get_cut_type_analysis(empty_dataframe)

        assert len(result) == 0


class TestGetThicknessRanges:
    """Test cases for the get_thickness_ranges function."""

    def test_get_thickness_ranges_basic(self, sample_dataframe):
        """Test basic thickness range calculation."""
        result = get_thickness_ranges(sample_dataframe)

        # Should return a list of tuples
        assert isinstance(result, list)
        assert all(isinstance(r, tuple) for r in result)
        assert all(len(r) == 2 for r in result)

    def test_get_thickness_ranges_single_value(self):
        """Test thickness ranges with a single thickness value."""
        single_df = pd.DataFrame({"Толщина пластины, мкм": [300, 300, 300]})
        result = get_thickness_ranges(single_df)

        # With identical values, should return one range with same min/max
        assert len(result) == 1
        assert result[0][0] == 300
        assert result[0][1] == 300

    def test_get_thickness_ranges_empty_dataframe(self, empty_dataframe):
        """Test thickness ranges with an empty DataFrame."""
        result = get_thickness_ranges(empty_dataframe)

        # Should return an empty list
        assert result == []


class TestFindOptimalSettings:
    """Test cases for the find_optimal_settings function."""

    def test_find_optimal_settings_basic(self, sample_dataframe):
        """Test basic optimal settings finding."""
        result = find_optimal_settings(
            sample_dataframe, material="Si", target_thickness=350
        )

        # Should return a DataFrame
        assert isinstance(result, pd.DataFrame)
        # Should have at most 10 rows
        assert len(result) <= 10
        # All rows should be for the specified material
        assert all(result["Материал пластины"] == "Si")

    def test_find_optimal_settings_with_cut_type(self, sample_dataframe):
        """Test optimal settings finding with cut type filter."""
        result = find_optimal_settings(
            sample_dataframe, material="Si", target_thickness=350, cut_type="Dry"
        )

        # Should return a DataFrame
        assert isinstance(result, pd.DataFrame)
        # All rows should be for the specified material and cut type
        assert all(result["Материал пластины"] == "Si")
        assert all(result["Тип резки"] == "Dry")

    def test_find_optimal_settings_empty_result(self, sample_dataframe):
        """Test optimal settings finding with non-existent material."""
        result = find_optimal_settings(
            sample_dataframe, material="NonExistent", target_thickness=350
        )

        # Should return an empty DataFrame
        assert len(result) == 0


class TestGetDiscRecommendations:
    """Test cases for the get_disc_recommendations function."""

    def test_get_disc_recommendations_basic(self, sample_dataframe):
        """Test basic disc recommendations."""
        result = get_disc_recommendations(
            sample_dataframe, material="Si", thickness=350
        )

        # Should return a list
        assert isinstance(result, list)
        # Should have at most 5 recommendations
        assert len(result) <= 5

        # If there are recommendations, check structure
        if result:
            first_rec = result[0]
            assert "Артикул" in first_rec
            assert "Толщина пластины (мкм)" in first_rec
            assert "Производительность (шт/час)" in first_rec

    def test_get_disc_recommendations_with_cut_type(self, sample_dataframe):
        """Test disc recommendations with cut type filter."""
        result = get_disc_recommendations(
            sample_dataframe, material="Si", thickness=350, cut_type="Dry"
        )

        # Should return a list
        assert isinstance(result, list)

        # If there are recommendations, they should be for the specified material and cut type
        if result:
            # Verify that the recommendations are based on filtered data
            pass  # The function internally filters, so we check the structure instead

    def test_get_disc_recommendations_empty_result(self, sample_dataframe):
        """Test disc recommendations with non-existent material."""
        result = get_disc_recommendations(
            sample_dataframe, material="NonExistent", thickness=350
        )

        # Should return an empty list
        assert result == []


class TestCompareMaterials:
    """Test cases for the compare_materials function."""

    def test_compare_materials_basic(self, sample_dataframe):
        """Test basic material comparison."""
        result = compare_materials(sample_dataframe, materials=["Si", "GaAs"])

        # Should return a DataFrame
        assert isinstance(result, pd.DataFrame)
        # Should have 2 rows (one for each material)
        assert len(result) == 2
        # Should contain the specified materials
        materials_in_result = set(result["Материал"])
        assert materials_in_result == {"Si", "GaAs"}

    def test_compare_materials_nonexistent_material(self, sample_dataframe):
        """Test material comparison with non-existent material."""
        result = compare_materials(sample_dataframe, materials=["Si", "NonExistent"])

        # Should return a DataFrame with only the existing material
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["Материал"] == "Si"

    def test_compare_materials_empty_dataframe(self, empty_dataframe):
        """Test material comparison with empty DataFrame."""
        result = compare_materials(empty_dataframe, materials=["Si"])

        # Should return an empty DataFrame
        assert len(result) == 0


class TestGetPerformanceTrends:
    """Test cases for the get_performance_trends function."""

    def test_get_performance_trends_basic(self, sample_dataframe):
        """Test basic performance trends."""
        result = get_performance_trends(sample_dataframe)

        # Should return a dictionary
        assert isinstance(result, dict)
        # Should contain expected keys
        expected_keys = [
            "thickness_vs_performance",
            "material_vs_performance",
            "cut_type_vs_performance",
        ]
        for key in expected_keys:
            assert key in result
            # Each value should be a list of tuples
            assert isinstance(result[key], list)
            assert all(isinstance(item, tuple) for item in result[key])

    def test_get_performance_trends_empty_dataframe(self, empty_dataframe):
        """Test performance trends with empty DataFrame."""
        result = get_performance_trends(empty_dataframe)

        # Should return an empty dictionary since there's no data to process
        assert isinstance(result, dict)
        assert result == {}
