import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Retail Inventory Dashboard",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .professional-header {
        background: linear-gradient(135deg, #a8c0ff 0%, #c5a3ff 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .header-subtitle {
        font-size: 1.2em;
        opacity: 0.9;
        margin-bottom: 15px;
    }
    .header-footer {
        font-size: 0.9em;
        opacity: 0.8;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid rgba(255, 255, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="professional-header">
        <div class="header-title">Retail Inventory Management Dashboard</div>
        <div class="header-subtitle">Advanced analytics for multi-store retail operations</div>
        <div style="display: flex; gap: 20px; margin-top: 10px;">
            <span>✦ Real-time Inventory Tracking</span>
            <span>✦ Predictive Analytics</span>
            <span>✦ Supplier Management</span>
        </div>
        <div class="header-footer">
            Built by [Your Name] | Retail Analytics Specialist | Available for Consulting
        </div>
    </div>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    stores = pd.read_csv('retail_stores.csv')
    products = pd.read_csv('retail_products.csv')
    suppliers = pd.read_csv('retail_suppliers.csv')
    inventory = pd.read_csv('retail_inventory.csv')
    sales = pd.read_csv('retail_sales.csv')
    purchase_orders = pd.read_csv('retail_purchase_orders.csv')
    
    # Convert dates
    inventory['date'] = pd.to_datetime(inventory['date'])
    sales['date'] = pd.to_datetime(sales['date'])
    purchase_orders['order_date'] = pd.to_datetime(purchase_orders['order_date'])
    purchase_orders['expected_delivery'] = pd.to_datetime(purchase_orders['expected_delivery'])
    
    return stores, products, suppliers, inventory, sales, purchase_orders

try:
    stores_df, products_df, suppliers_df, inventory_df, sales_df, po_df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure all CSV files are in the same directory as this dashboard.")
    st.stop()

# Sidebar
st.sidebar.title("Filters")

# Date range filter
min_date = inventory_df['date'].min().date()
max_date = inventory_df['date'].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(max_date - timedelta(days=30), max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    inventory_filtered = inventory_df[
        (inventory_df['date'].dt.date >= date_range[0]) & 
        (inventory_df['date'].dt.date <= date_range[1])
    ]
    sales_filtered = sales_df[
        (sales_df['date'].dt.date >= date_range[0]) & 
        (sales_df['date'].dt.date <= date_range[1])
    ]
else:
    inventory_filtered = inventory_df
    sales_filtered = sales_df

# Store filter
store_options = ['All Stores'] + sorted(stores_df['store_name'].tolist())
selected_store = st.sidebar.selectbox("Store", store_options)

if selected_store != 'All Stores':
    store_id = stores_df[stores_df['store_name'] == selected_store]['store_id'].iloc[0]
    inventory_filtered = inventory_filtered[inventory_filtered['store_id'] == store_id]
    sales_filtered = sales_filtered[sales_filtered['store_id'] == store_id]

# Department filter
dept_options = ['All Departments'] + sorted(products_df['department'].unique().tolist())
selected_dept = st.sidebar.selectbox("Department", dept_options)

if selected_dept != 'All Departments':
    dept_skus = products_df[products_df['department'] == selected_dept]['sku'].tolist()
    inventory_filtered = inventory_filtered[inventory_filtered['sku'].isin(dept_skus)]
    sales_filtered = sales_filtered[sales_filtered['sku'].isin(dept_skus)]

# Merge data for analysis
inventory_enhanced = inventory_filtered.merge(products_df, on='sku', how='left')
inventory_enhanced = inventory_enhanced.merge(stores_df[['store_id', 'store_name', 'region']], on='store_id', how='left')

sales_enhanced = sales_filtered.merge(products_df, on='sku', how='left')
sales_enhanced = sales_enhanced.merge(stores_df[['store_id', 'store_name', 'region']], on='store_id', how='left')

# Get latest inventory snapshot
latest_date = inventory_filtered['date'].max()
current_inventory = inventory_filtered[inventory_filtered['date'] == latest_date]
current_inventory_enhanced = current_inventory.merge(products_df, on='sku', how='left')
current_inventory_enhanced = current_inventory_enhanced.merge(
    stores_df[['store_id', 'store_name', 'region']], 
    on='store_id', 
    how='left'
)

# ========== KPIs ==========
st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

total_inventory_value = current_inventory_enhanced['value_on_hand'].sum()
total_revenue = sales_enhanced['revenue'].sum()
total_profit = sales_enhanced['profit'].sum()
avg_margin = sales_enhanced['profit_margin'].mean()

stockout_count = len(current_inventory[current_inventory['status'] == 'Out of Stock'])
low_stock_count = len(current_inventory[current_inventory['status'] == 'Low Stock'])

with col1:
    st.metric("Inventory Value", f"${total_inventory_value:,.0f}", 
              delta=f"{len(current_inventory):,} items")

with col2:
    st.metric("Total Revenue", f"${total_revenue:,.0f}",
              delta=f"{len(sales_enhanced):,} transactions")

with col3:
    st.metric("Total Profit", f"${total_profit:,.0f}",
              delta=f"{avg_margin:.1f}% margin")

with col4:
    st.metric("Stockouts", stockout_count, 
              delta="Critical" if stockout_count > 10 else "Good",
              delta_color="inverse")

with col5:
    st.metric("Low Stock Items", low_stock_count,
              delta="Warning" if low_stock_count > 50 else "OK",
              delta_color="inverse")

st.markdown("---")

# ========== INVENTORY HEALTH HEATMAP ==========
st.subheader("Inventory Health Heatmap")
st.markdown("Visual overview of stock levels across stores and departments")

# Aggregate by store and department
heatmap_data = current_inventory_enhanced.groupby(['store_name', 'department']).agg({
    'quantity_on_hand': 'sum',
    'status': lambda x: (x == 'Out of Stock').sum()
}).reset_index()

heatmap_pivot = heatmap_data.pivot(index='department', columns='store_name', values='quantity_on_hand')

fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_pivot.values,
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    colorscale='RdYlGn',
    text=heatmap_pivot.values,
    texttemplate='%{text:.0f}',
    textfont={"size": 10},
    colorbar=dict(title="Stock Level")
))

fig_heatmap.update_layout(
    title="Stock Levels by Store and Department",
    xaxis_title="Store",
    yaxis_title="Department",
    height=400
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")

# ========== ABC ANALYSIS ==========
col1, col2 = st.columns(2)

with col1:
    st.subheader("ABC Analysis - Revenue Concentration")
    
    # Calculate cumulative revenue by product
    product_revenue = sales_enhanced.groupby('sku')['revenue'].sum().sort_values(ascending=False).reset_index()
    product_revenue['cumulative_revenue'] = product_revenue['revenue'].cumsum()
    product_revenue['cumulative_pct'] = (product_revenue['cumulative_revenue'] / product_revenue['revenue'].sum()) * 100
    product_revenue['rank'] = range(1, len(product_revenue) + 1)
    
    # Classify ABC
    product_revenue['class'] = 'C'
    product_revenue.loc[product_revenue['cumulative_pct'] <= 80, 'class'] = 'A'
    product_revenue.loc[(product_revenue['cumulative_pct'] > 80) & (product_revenue['cumulative_pct'] <= 95), 'class'] = 'B'
    
    fig_abc = go.Figure()
    
    fig_abc.add_trace(go.Bar(
        x=product_revenue['rank'],
        y=product_revenue['revenue'],
        name='Revenue',
        marker_color='#a8c0ff'
    ))
    
    fig_abc.add_trace(go.Scatter(
        x=product_revenue['rank'],
        y=product_revenue['cumulative_pct'],
        name='Cumulative %',
        yaxis='y2',
        line=dict(color='#e59866', width=3)
    ))
    
    fig_abc.update_layout(
        title='Products Ranked by Revenue (Pareto)',
        xaxis_title='Product Rank',
        yaxis_title='Revenue ($)',
        yaxis2=dict(
            title='Cumulative %',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_abc, use_container_width=True)
    
    # ABC Summary
    abc_summary = product_revenue.groupby('class').agg({
        'sku': 'count',
        'revenue': 'sum'
    }).reset_index()
    abc_summary.columns = ['Class', 'Product Count', 'Revenue']
    abc_summary['Revenue %'] = (abc_summary['Revenue'] / abc_summary['Revenue'].sum() * 100).round(1)
    
    st.dataframe(abc_summary, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Inventory Turnover Analysis")
    
    # Calculate turnover by department - use COGS from sales data
    sales_by_dept = sales_enhanced.groupby('department').agg({
        'revenue': 'sum',
        'profit': 'sum'
    }).reset_index()
    
    # Calculate COGS (Cost of Goods Sold) = Revenue - Profit
    sales_by_dept['cogs'] = sales_by_dept['revenue'] - sales_by_dept['profit']
    
    avg_inventory_by_dept = current_inventory_enhanced.groupby('department')['value_on_hand'].sum().reset_index()
    
    turnover_data = sales_by_dept.merge(avg_inventory_by_dept, on='department')
    turnover_data['turnover_ratio'] = turnover_data['cogs'] / turnover_data['value_on_hand']
    turnover_data['turnover_ratio'] = turnover_data['turnover_ratio'].fillna(0)
    
    fig_turnover = px.bar(
        turnover_data.sort_values('turnover_ratio', ascending=True),
        y='department',
        x='turnover_ratio',
        orientation='h',
        title='Inventory Turnover by Department',
        labels={'turnover_ratio': 'Turnover Ratio', 'department': 'Department'},
        color='turnover_ratio',
        color_continuous_scale='Mint'
    )
    
    fig_turnover.update_layout(
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_turnover, use_container_width=True)
    
    st.info("Higher turnover = faster inventory movement = better efficiency")

st.markdown("---")

# ========== STOCKOUT COST ANALYSIS ==========
st.subheader("Stockout Impact Analysis")

stockout_records = inventory_enhanced[inventory_enhanced['status'] == 'Out of Stock']
stockout_analysis = stockout_records.groupby(['store_name', 'department']).size().reset_index(name='stockout_days')

# Estimate lost revenue (assume avg daily sales * retail price)
estimated_daily_loss = sales_enhanced.groupby('sku')['revenue'].mean().mean()
stockout_analysis['estimated_lost_revenue'] = stockout_analysis['stockout_days'] * estimated_daily_loss

col1, col2 = st.columns(2)

with col1:
    fig_stockout_store = px.bar(
        stockout_analysis.groupby('store_name')['stockout_days'].sum().sort_values(ascending=False).reset_index(),
        x='stockout_days',
        y='store_name',
        orientation='h',
        title='Stockout Days by Store',
        labels={'stockout_days': 'Total Stockout Days', 'store_name': 'Store'},
        color='stockout_days',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_stockout_store, use_container_width=True)

with col2:
    total_lost_revenue = stockout_analysis['estimated_lost_revenue'].sum()
    
    fig_stockout_dept = px.pie(
        stockout_analysis.groupby('department')['estimated_lost_revenue'].sum().reset_index(),
        values='estimated_lost_revenue',
        names='department',
        title=f'Estimated Lost Revenue: ${total_lost_revenue:,.0f}',
        color_discrete_sequence=['#FFB6C1', '#B0E0E6', '#98D8C8', '#F7DC6F']
    )
    st.plotly_chart(fig_stockout_dept, use_container_width=True)

st.markdown("---")

# ========== SUPPLIER SCORECARD ==========
st.subheader("Supplier Performance Scorecard")

# Merge PO data with supplier info
po_analysis = po_df.merge(suppliers_df, on='supplier_id', how='left')
po_analysis = po_analysis.merge(products_df[['sku', 'department']], on='sku', how='left')

supplier_metrics = po_analysis.groupby('supplier_name').agg({
    'po_number': 'count',
    'total_cost': 'sum',
    'reliability_score': 'first',
    'defect_rate': 'first',
    'avg_lead_time': 'first'
}).reset_index()

supplier_metrics.columns = ['Supplier', 'PO Count', 'Total Spend', 'Reliability %', 'Defect %', 'Avg Lead Time (days)']
supplier_metrics = supplier_metrics.sort_values('Total Spend', ascending=False).head(10)

fig_supplier = go.Figure()

fig_supplier.add_trace(go.Bar(
    name='Total Spend',
    x=supplier_metrics['Supplier'],
    y=supplier_metrics['Total Spend'],
    marker_color='#a8c0ff'
))

fig_supplier.add_trace(go.Scatter(
    name='Reliability Score',
    x=supplier_metrics['Supplier'],
    y=supplier_metrics['Reliability %'],
    yaxis='y2',
    mode='markers+lines',
    marker=dict(size=12, color='#5dae8b', line=dict(width=2, color='white'))
))

fig_supplier.update_layout(
    title='Top 10 Suppliers by Spend vs Reliability',
    xaxis_title='Supplier',
    yaxis_title='Total Spend ($)',
    yaxis2=dict(
        title='Reliability Score (%)',
        overlaying='y',
        side='right',
        range=[70, 100]
    ),
    hovermode='x unified',
    height=400
)

st.plotly_chart(fig_supplier, use_container_width=True)

# Supplier table - format values manually
supplier_metrics['Total Spend'] = supplier_metrics['Total Spend'].apply(lambda x: f'${x:,.0f}')
supplier_metrics['Reliability %'] = supplier_metrics['Reliability %'].apply(lambda x: f'{x:.1f}%')
supplier_metrics['Defect %'] = supplier_metrics['Defect %'].apply(lambda x: f'{x:.2f}%')
supplier_metrics['Avg Lead Time (days)'] = supplier_metrics['Avg Lead Time (days)'].apply(lambda x: f'{x:.0f}')

st.dataframe(supplier_metrics, use_container_width=True, hide_index=True)

st.markdown("---")

# ========== REORDER ALERTS ==========
st.subheader("Reorder Priority Dashboard")

reorder_needed = current_inventory_enhanced[
    current_inventory_enhanced['quantity_on_hand'] <= current_inventory_enhanced['reorder_point']
].copy()

if len(reorder_needed) > 0:
    reorder_needed['urgency_score'] = (
        (reorder_needed['reorder_point'] - reorder_needed['quantity_on_hand']) / 
        reorder_needed['reorder_point'] * 100
    )
    reorder_needed['priority'] = pd.cut(
        reorder_needed['urgency_score'],
        bins=[-np.inf, 50, 80, np.inf],
        labels=['Medium', 'High', 'Critical']
    )
    
    priority_counts = reorder_needed['priority'].value_counts()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        critical_count = priority_counts.get('Critical', 0)
        st.metric("Critical Priority", critical_count, 
                  delta="Immediate Action Required" if critical_count > 0 else "None",
                  delta_color="inverse")
    
    with col2:
        high_count = priority_counts.get('High', 0)
        st.metric("High Priority", high_count,
                  delta="Order Within 48hrs" if high_count > 0 else "None")
    
    with col3:
        medium_count = priority_counts.get('Medium', 0)
        st.metric("Medium Priority", medium_count,
                  delta="Order This Week" if medium_count > 0 else "None")
    
    # Show top reorder items - format manually
    top_reorders = reorder_needed.nlargest(10, 'urgency_score')[
        ['store_name', 'product_name', 'department', 'quantity_on_hand', 
         'reorder_point', 'urgency_score', 'priority']
    ].copy()
    
    # Format numeric columns
    top_reorders['quantity_on_hand'] = top_reorders['quantity_on_hand'].apply(lambda x: f'{x:.0f}')
    top_reorders['reorder_point'] = top_reorders['reorder_point'].apply(lambda x: f'{x:.0f}')
    top_reorders['urgency_score'] = top_reorders['urgency_score'].apply(lambda x: f'{x:.1f}%')
    
    st.dataframe(top_reorders, use_container_width=True, hide_index=True)
else:
    st.success("All items adequately stocked! No reorders needed.")

st.markdown("---")

# ========== SALES TRENDS ==========
st.subheader("Sales Performance Trends")

daily_sales = sales_enhanced.groupby('date').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'transaction_id': 'count'
}).reset_index()

daily_sales.columns = ['Date', 'Revenue', 'Profit', 'Transactions']

fig_trends = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Daily Revenue & Profit', 'Transaction Volume'),
    vertical_spacing=0.15
)

fig_trends.add_trace(
    go.Scatter(x=daily_sales['Date'], y=daily_sales['Revenue'], 
               name='Revenue', line=dict(color='#a8c0ff', width=2)),
    row=1, col=1
)

fig_trends.add_trace(
    go.Scatter(x=daily_sales['Date'], y=daily_sales['Profit'], 
               name='Profit', line=dict(color='#5dae8b', width=2)),
    row=1, col=1
)

fig_trends.add_trace(
    go.Bar(x=daily_sales['Date'], y=daily_sales['Transactions'], 
           name='Transactions', marker_color='#e59866'),
    row=2, col=1
)

fig_trends.update_xaxes(title_text="Date", row=2, col=1)
fig_trends.update_yaxes(title_text="Amount ($)", row=1, col=1)
fig_trends.update_yaxes(title_text="Count", row=2, col=1)

fig_trends.update_layout(height=600, showlegend=True, hovermode='x unified')

st.plotly_chart(fig_trends, use_container_width=True)

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Advanced Retail Analytics Dashboard | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)