import streamlit as st
import pandas as pd
import pymssql
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns

# Функція для підключення до бази даних
def connect_to_db():
    server = 'demo-mssql-database.c7y8qoeky66p.eu-north-1.rds.amazonaws.com'
    database = 'BikeStores'
    username = 'admin'
    password = 'mssql-22-01-2025'
    
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
    return conn

# Функція для отримання даних з бази
def fetch_data(query):
    conn = connect_to_db()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Налаштування сторінки
st.set_page_config(page_title="Bike Store Dashboard", layout="wide", initial_sidebar_state="expanded")

# Стилізація
st.markdown("""
<style>
.main-header {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    background-color: #1E2761;
    color: white;
    padding: 20px;
    border-radius: 5px;
}
.metric-container {
    background-color: #D6E4F0;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
}
.metric-value {
    font-size: 40px;
    font-weight: bold;
}
.metric-label {
    font-size: 18px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# Заголовок
st.markdown('<div class="main-header">Bike Store Dashboard</div>', unsafe_allow_html=True)

# Фільтри у верхній частині
col_filter1, col_filter2 = st.columns([3, 1])

with col_filter1:
    # Фільтр для року
    year_query = "SELECT DISTINCT YEAR(order_date) as year FROM sales.orders ORDER BY year"
    years = fetch_data(year_query)['year'].tolist()
    year = st.selectbox('Year', years, index=len(years)-1)

with col_filter2:
    # Фільтр для штату
    state_query = "SELECT DISTINCT state FROM sales.customers ORDER BY state"
    states = fetch_data(state_query)['state'].tolist()
    all_states_option = "All states"
    states = [all_states_option] + states
    state = st.selectbox('State', states)

# Формування умов фільтрації для SQL-запитів
year_condition = f"YEAR(o.order_date) = {year}"
state_condition = f"AND c.state = '{state}'" if state != all_states_option else ""

# Основні метрики
# Запит для отримання загальних даних
metrics_query = f"""
SELECT 
    SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS revenue,
    SUM(oi.quantity) AS total_units,
    COUNT(DISTINCT oi.product_id) AS unique_products,
    COUNT(DISTINCT o.customer_id) AS unique_customers
FROM 
    sales.orders o
    JOIN sales.order_items oi ON o.order_id = oi.order_id
    JOIN sales.customers c ON o.customer_id = c.customer_id
WHERE 
    {year_condition}
    {state_condition}
"""
metrics_data = fetch_data(metrics_query)

# Відображення метрик в рядок
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Revenue</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">${metrics_data["revenue"].values[0]:,.0f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total Units</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{metrics_data["total_units"].values[0]:,.0f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label"># Units</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{metrics_data["unique_products"].values[0]:,.0f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label"># Customers</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{metrics_data["unique_customers"].values[0]:,.0f}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### Profitability at glance for all states and all years")

# Графіки
col_graph1, col_graph2 = st.columns(2)

# Графік 1: Revenue by year
with col_graph1:
    st.subheader("Revenue by year")
    
    revenue_by_year_query = """
    SELECT 
        YEAR(o.order_date) AS year,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS revenue
    FROM 
        sales.orders o
        JOIN sales.order_items oi ON o.order_id = oi.order_id
    GROUP BY 
        YEAR(o.order_date)
    ORDER BY 
        year
    """
    revenue_by_year = fetch_data(revenue_by_year_query)
    
    fig = px.bar(revenue_by_year, x='year', y='revenue', 
                text=revenue_by_year['revenue'].apply(lambda x: f"${x/1000000:.2f} млн"),
                color_discrete_sequence=['#1E2761'])
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            tickprefix="$",
            ticksuffix=" млн",
            gridcolor='lightgray',
            gridwidth=0.5,
        )
    )
    fig.update_traces(textposition='inside')
    st.plotly_chart(fig, use_container_width=True)

# Графік 2: Revenue by month
with col_graph2:
    st.subheader("Revenue by month")
    
    revenue_by_month_query = f"""
    SELECT 
        MONTH(o.order_date) AS month_num,
        DATENAME(month, o.order_date) AS month_name,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS revenue
    FROM 
        sales.orders o
        JOIN sales.order_items oi ON o.order_id = oi.order_id
        JOIN sales.customers c ON o.customer_id = c.customer_id
    WHERE 
        {year_condition}
        {state_condition}
    GROUP BY 
        MONTH(o.order_date),
        DATENAME(month, o.order_date)
    ORDER BY 
        month_num
    """
    revenue_by_month = fetch_data(revenue_by_month_query)
    
    fig = px.line(revenue_by_month, x='month_name', y='revenue', 
                 markers=True, line_shape='spline',
                 color_discrete_sequence=['#1E2761'])
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            tickprefix="$",
            ticksuffix=" тис.",
            gridcolor='lightgray',
            gridwidth=0.5,
        )
    )
    
    # Додавання значень над точками
    for i, row in revenue_by_month.iterrows():
        fig.add_annotation(
            x=row['month_name'],
            y=row['revenue'],
            text=f"${row['revenue']/1000:.0f} тис.",
            showarrow=False,
            yshift=10,
            font=dict(size=10)
        )
    
    st.plotly_chart(fig, use_container_width=True)

col_graph3, col_graph4 = st.columns(2)

# Графік 3: Revenue by Categories
with col_graph3:
    st.subheader("Revenue by Categories")
    
    category_query = f"""
    SELECT 
        c.category_name,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS revenue
    FROM 
        sales.orders o
        JOIN sales.order_items oi ON o.order_id = oi.order_id
        JOIN production.products p ON oi.product_id = p.product_id
        JOIN production.categories c ON p.category_id = c.category_id
        JOIN sales.customers cust ON o.customer_id = cust.customer_id
    WHERE 
        {year_condition}
        {state_condition}
    GROUP BY 
        c.category_name
    ORDER BY 
        revenue DESC
    """
    category_data = fetch_data(category_query)
    
    # Створення treemap
    fig = px.treemap(category_data, path=['category_name'], values='revenue',
                   color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_traces(textinfo="label+value", texttemplate="%{label}<br>$%{value:,.0f}")
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    
    st.plotly_chart(fig, use_container_width=True)

# Графік 4: Revenue by Stores
with col_graph4:
    st.subheader("Revenue by Stores")
    
    store_query = f"""
    SELECT 
        s.store_name,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS revenue
    FROM 
        sales.orders o
        JOIN sales.order_items oi ON o.order_id = oi.order_id
        JOIN sales.stores s ON o.store_id = s.store_id
        JOIN sales.customers c ON o.customer_id = c.customer_id
    WHERE 
        {year_condition}
        {state_condition}
    GROUP BY 
        s.store_name
    ORDER BY 
        revenue DESC
    """
    store_data = fetch_data(store_query)
    
    # Створення кругової діаграми
    fig = px.pie(store_data, values='revenue', names='store_name',
               color_discrete_sequence=['#1E2761', '#4F7CAC', '#8EAEBD'],
               hole=0.3)
    
    # Додавання підписів з процентами та значеннями
    total_revenue = store_data['revenue'].sum()
    fig.update_traces(
        textposition='inside',
        textinfo='label+percent+value',
        texttemplate='%{label}<br>$%{value:,.2f} (%{percent})',
        insidetextorientation='radial'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Графік 5: Revenue by Brands
col_graph5, col_dummy = st.columns([2, 0.1])

with col_graph5:
    st.subheader("Revenue by Brands")
    
    brand_query = f"""
    SELECT 
        b.brand_name,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS revenue
    FROM 
        sales.orders o
        JOIN sales.order_items oi ON o.order_id = oi.order_id
        JOIN production.products p ON oi.product_id = p.product_id
        JOIN production.brands b ON p.brand_id = b.brand_id
        JOIN sales.customers c ON o.customer_id = c.customer_id
    WHERE 
        {year_condition}
        {state_condition}
    GROUP BY 
        b.brand_name
    ORDER BY 
        revenue DESC
    """
    brand_data = fetch_data(brand_query)
    
    # Створення кругової діаграми
    fig = px.pie(brand_data, values='revenue', names='brand_name',
               color_discrete_sequence=px.colors.qualitative.Dark24,
               hole=0.3)
    
    # Додавання підписів з процентами та значеннями
    total_revenue = brand_data['revenue'].sum()
    fig.update_traces(
        textposition='inside',
        textinfo='label+percent+value',
        texttemplate='%{label}<br>$%{value:,.2f} (%{percent})',
        insidetextorientation='radial'
    )
    
    # Додавання легенди
    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Футер з додатковою інформацією
st.markdown("---")
st.markdown("Dashboard created using Streamlit and SQL Server")
