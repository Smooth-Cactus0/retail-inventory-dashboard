# Retail Inventory Management Dashboard

Advanced multi-store inventory analytics platform with predictive reorder alerts, supplier scorecards, and stockout cost analysis.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

# Retail Inventory Management Dashboard

## 🌐 Live Demo

**[👉 Try the live dashboard here!](https://retail-inventory-dashboard-jvrdashqpqb7bbrwx4bjr3.streamlit.app/
)** ← Click to see it in action

No installation required - explore the full dashboard with sample retail data.

---

Advanced multi-store inventory analytics platform with predictive reorder alerts, supplier scorecards, and stockout cost analysis.



## 🎯 Features

### Inventory Analytics
- **Health Heatmap** - Visual grid showing stock levels across stores and departments
- **ABC Analysis** - Pareto charts identifying products driving 80% of revenue
- **Turnover Metrics** - Calculate inventory efficiency by department
- **Stockout Cost Analysis** - Quantify revenue impact of out-of-stock items

### Smart Alerts
- **Priority Reorder System** - Urgency scoring with Critical/High/Medium classification
- **Low Stock Warnings** - Automated alerts when inventory hits reorder points
- **Days of Supply** - Forward-looking inventory projections

### Supplier Management
- **Performance Scorecard** - Compare suppliers on reliability, defect rate, lead time
- **Spend Analysis** - Track purchasing patterns and vendor relationships
- **Purchase Order Tracking** - Monitor PO status and delivery timelines

### Multi-Dimensional Analysis
- 8 store locations across 6 states
- 4 departments with 50+ SKUs
- 14 supplier relationships
- 180 days of historical data
- 60K+ inventory snapshots
- 30K+ sales transactions

## 🛠️ Tech Stack

- **Streamlit** - Interactive web framework
- **Pandas** - Data manipulation and aggregation
- **Plotly** - Advanced visualizations (heatmaps, dual-axis, subplots)
- **NumPy** - Numerical computations

## 📊 Visualizations

- Inventory health heatmaps
- ABC/Pareto analysis with cumulative curves
- Supplier performance scorecards with dual-axis charts
- Stockout impact analysis
- Multi-panel sales trend analysis
- Geographic performance by store

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/retail-inventory-dashboard.git
cd retail-inventory-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate sample data:
```bash
python generate_retail_data.py
```

4. Run the dashboard:
```bash
streamlit run retail_dashboard.py
```

## 📈 Use Cases

- **Retail Operations** - Track inventory across multiple locations
- **Supply Chain Management** - Optimize reorder points and supplier relationships
- **Financial Planning** - Analyze inventory value and turnover efficiency
- **Loss Prevention** - Identify and quantify stockout costs
- **Strategic Planning** - ABC analysis for product portfolio optimization

## 📁 Data Structure

The dashboard uses 6 interconnected datasets:
- `retail_stores.csv` - Store locations and attributes
- `retail_products.csv` - Product catalog with hierarchy
- `retail_suppliers.csv` - Supplier performance metrics
- `retail_inventory.csv` - Daily inventory snapshots
- `retail_sales.csv` - Transaction-level sales data
- `retail_purchase_orders.csv` - PO tracking

## 💼 Portfolio Project

This dashboard demonstrates:
- Complex data modeling with relational datasets
- Advanced analytics (ABC analysis, turnover ratios, cost impact)
- Multi-dimensional business intelligence
- Supply chain domain expertise
- Professional visualization design
- Scalable architecture for enterprise retail

## 👤 Contact

**[Alexy Louis]**
- Email: alexy.louis.scholar@gmail.com
- LinkedIn: [https://www.linkedin.com/in/alexy-louis-19a5a9262/]
- Portfolio: see https://github.com/Smooth-Cactus0

## License

MIT License - Free to use for your projects!
```

### **.gitignore**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# Streamlit
.streamlit/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db