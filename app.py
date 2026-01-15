import streamlit as st
import pandas as pd
import numpy as np
from disc_cutting_analyzer.data_loader import get_all_data, get_available_materials, get_available_cut_types
from disc_cutting_analyzer.plotting import (
    create_chipping_plot, create_performance_plot, 
    create_process_parameters_plot, create_disc_parameters_plot, 
    create_summary_metrics
)
from disc_cutting_analyzer.analysis import (
    filter_data, get_material_statistics, 
    get_cut_type_analysis, find_optimal_settings,
    get_disc_recommendations, compare_materials
)
from disc_cutting_analyzer.decrypting import get_article_info, validate_article_format


def main():
    # Set page config
    st.set_page_config(
        page_title="Интерактивная база данных дисковой резки полупроводниковых пластин",
        page_icon="🔍",
        layout="wide"
    )
    
    # Main title
    st.title("Интерактивная база данных дисковой резки полупроводниковых пластин")
    
    # File uploader for custom database
    uploaded_file = st.file_uploader(
        "Загрузите свою базу данных (XLSX)",
        type=['xlsx'],
        help="Загрузите файл в формате XLSX с данными, аналогичными исходной базе данных"
    )
    
    with st.spinner("Loading data..."):
        if uploaded_file is not None:
            # If user uploads a file, use it
            from disc_cutting_analyzer.data_loader import load_uploaded_data
            data = load_uploaded_data(uploaded_file)
        else:
            # Otherwise use the default data
            data = get_all_data()
    
    if data.empty:
        st.error("Не удалось загрузить данные. Пожалуйста, проверьте наличие файла данных.")
        return
    
    # Sidebar controls
    st.sidebar.header("Фильтры данных")
    
    # Get available materials and cut types
    available_materials = get_available_materials(data)
    available_cut_types = get_available_cut_types(data)
    
    # Material selection
    selected_materials = st.sidebar.multiselect(
        "Материалы пластин",
        options=available_materials,
        default=available_materials[:3] if available_materials else []
    )
    
    # Cut type selection
    selected_cut_types = st.sidebar.multiselect(
        "Типы резки",
        options=available_cut_types,
        default=available_cut_types if available_cut_types else []
    )
    
    # Thickness range slider
    min_thickness = float(data['Толщина пластины, мкм'].min()) if not data.empty else 50.0
    max_thickness = float(data['Толщина пластины, мкм'].max()) if not data.empty else 500.0
    thickness_range = st.sidebar.slider(
        "Диапазон толщин пластин (мкм)",
        min_value=int(min_thickness),
        max_value=int(max_thickness),
        value=(int(min_thickness), int(max_thickness)),
        step=25
    )
    
    # Kerf width range slider
    min_kerf_width = float(data['Ширина реза, мкм'].min()) if not data.empty else 25.0
    max_kerf_width = float(data['Ширина реза, мкм'].max()) if not data.empty else 120.0
    kerf_width_range = st.sidebar.slider(
        "Диапазон ширины реза (мкм)",
        min_value=int(min_kerf_width),
        max_value=int(max_kerf_width),
        value=(int(min_kerf_width), int(max_kerf_width)),
        step=5
    )
    
    # Filter data based on selections
    filtered_data = filter_data(
        data,
        selected_materials,
        selected_cut_types,
        thickness_range[0],
        thickness_range[1],
        kerf_width_range[0],
        kerf_width_range[1]
    )
    
    # Calculate summary metrics
    metrics = create_summary_metrics(
        data,
        selected_materials,
        selected_cut_types,
        thickness_range[0],
        thickness_range[1],
        kerf_width_range[0],
        kerf_width_range[1]
    )
    
    # Display metrics
    st.subheader("Ключевые показатели")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Средние сколы (лицевая сторона)",
            value=f"{metrics['avg_front_chipping']:.2f} мкм"
        )
    
    with col2:
        st.metric(
            label="Средние сколы (обратная сторона)",
            value=f"{metrics['avg_back_chipping']:.2f} мкм" if metrics['avg_back_chipping'] > 0 else "Нет данных"
        )
    
    with col3:
        st.metric(
            label="Средняя производительность",
            value=f"{metrics['avg_performance']:.2f} шт/час"
        )
    
    with col4:
        st.metric(
            label="Средний срок службы диска",
            value=f"{metrics['avg_blade_life']:.2f} резов"
        )
    
    with col5:
        st.metric(
            label="Всего записей",
            value=metrics['total_records']
        )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Графики сколов", 
        "Графики производительности", 
        "Графики параметров процесса",
        "Таблица данных",
        "Декодер артикула"
    ])
    
    with tab1:
        st.subheader("Графики сколов в зависимости от толщины пластины по материалам")
        chipping_fig = create_chipping_plot(
            data,
            selected_materials,
            selected_cut_types,
            thickness_range[0],
            thickness_range[1],
            kerf_width_range[0],
            kerf_width_range[1]
        )
        st.plotly_chart(chipping_fig, use_container_width=True)
    
    with tab2:
        st.subheader("Графики производительности и срока службы дисков в зависимости от толщины пластины по материалам")
        performance_fig = create_performance_plot(
            data,
            selected_materials,
            selected_cut_types,
            thickness_range[0],
            thickness_range[1],
            kerf_width_range[0],
            kerf_width_range[1]
        )
        st.plotly_chart(performance_fig, use_container_width=True)
    
    with tab3:
        st.subheader("Графики параметров процесса в зависимости от толщины пластины по материалам")
        process_fig = create_process_parameters_plot(
            data,
            selected_materials,
            selected_cut_types,
            thickness_range[0],
            thickness_range[1],
            kerf_width_range[0],
            kerf_width_range[1]
        )
        st.plotly_chart(process_fig, use_container_width=True)
    
    with tab4:
        st.subheader("Таблица данных за выбранный период")
        if not filtered_data.empty:
            # Show the filtered data
            st.dataframe(filtered_data, use_container_width=True)
            
            # Download button for filtered data
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Скачать данные как CSV",
                data=csv,
                file_name="filtered_disc_data.csv",
                mime="text/csv"
            )
        else:
            st.info("Нет данных для отображения по выбранным фильтрам")
    
    with tab5:
        st.subheader("Виджет расшифровки артикула")
        
        # Article decoder widget
        col1, col2 = st.columns([3, 1])
        
        with col1:
            article_input = st.text_input(
                "Введите артикул диска",
                placeholder="Например: 00757-1130-250-100",
                help="Формат артикула: 00757-XXXX-XXX-XXX"
            )
        
        with col2:
            st.write("")  # Spacer
            decode_clicked = st.button("Расшифровать")
        
        if decode_clicked and article_input:
            if validate_article_format(article_input):
                article_info = get_article_info(article_input)
                
                if article_info:
                    st.success(f"Артикул: {article_info['article']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Параметры диска:**")
                        st.write(f"- Тип диска: {article_info['product_family']}")
                        st.write(f"- Размер алмазного зерна: {article_info['grit_size']}")
                        st.write(f"- Концентрация алмаза: {article_info['diamond_percent']}")
                    
                    with col2:
                        st.write("**Прочие параметры:**")
                        st.write(f"- Толщина лезвия: {article_info['blade_thickness']}")
                        st.write(f"- Вылет лезвия: {article_info['blade_exposure']}")
                        st.write(f"- Твердость связки: {article_info['bond_hardness']}")
                    
                    # Order button
                    if st.button("Заказать", type="primary"):
                        st.balloons()
                        st.success(f"Запрос на заказ диска с артикулом {article_input} отправлен!")
                else:
                    st.error("Не удалось расшифровать артикул. Проверьте правильность ввода.")
            else:
                st.error("Неправильный формат артикула. Формат должен быть: 00757-XXXX-XXX-XXX")
        
        elif decode_clicked:
            st.warning("Пожалуйста, введите артикул диска для расшифровки.")
    
    # Additional analysis section
    st.subheader("Дополнительный анализ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Статистика по материалам**")
        if selected_materials:
            mat_stats = get_material_statistics(filtered_data)
            stats_df = pd.DataFrame.from_dict(mat_stats, orient='index')
            st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        st.write("**Анализ по типам резки**")
        if selected_cut_types:
            cut_analysis = get_cut_type_analysis(filtered_data)
            analysis_df = pd.DataFrame.from_dict(cut_analysis, orient='index')
            st.dataframe(analysis_df, use_container_width=True)


if __name__ == "__main__":
    main()