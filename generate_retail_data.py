# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 11:25:12 2025

@author: alexy
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# ========== STORE LOCATIONS ==========
stores_data = {
    'store_id': ['ST001', 'ST002', 'ST003', 'ST004', 'ST005', 'ST006', 'ST007', 'ST008'],
    'store_name': ['Downtown Flagship', 'West Side Mall', 'Airport Plaza', 'Suburban Center',
                   'Harbor View', 'Tech District', 'University Square', 'Riverside Outlet'],
    'city': ['Seattle', 'Portland', 'San Francisco', 'Los Angeles', 
             'San Diego', 'Austin', 'Denver', 'Phoenix'],
    'state': ['WA', 'OR', 'CA', 'CA', 'CA', 'TX', 'CO', 'AZ'],
    'region': ['Northwest', 'Northwest', 'West', 'West', 'West', 'South', 'Mountain', 'Southwest'],
    'store_type': ['Flagship', 'Standard', 'Airport', 'Standard', 'Standard', 'Standard', 'Standard', 'Outlet'],
    'size_sqft': [15000, 8000, 5000, 10000, 9000, 8500, 7000, 12000],
    'opening_date': ['2018-03-15', '2019-06-01', '2020-01-10', '2017-09-20', 
                     '2019-11-15', '2020-05-01', '2018-08-10', '2021-02-01']
}
stores_df = pd.DataFrame(stores_data)

# ========== PRODUCT HIERARCHY ==========
departments = {
    'Electronics': ['Computers', 'Mobile Devices', 'Audio', 'Smart Home'],
    'Appliances': ['Kitchen', 'Laundry', 'Climate Control'],
    'Home & Living': ['Furniture', 'Bedding', 'Decor'],
    'Outdoor': ['Garden', 'Patio', 'BBQ & Grills']
}

products_list = []
sku_counter = 1000

for dept, categories in departments.items():
    for category in categories:
        # Create 3-5 products per category
        num_products = np.random.randint(3, 6)
        for i in range(num_products):
            sku = f'SKU{sku_counter:05d}'
            sku_counter += 1
            
            # Generate realistic product attributes
            base_cost = np.random.uniform(20, 800)
            markup = np.random.uniform(1.3, 2.5)
            retail_price = round(base_cost * markup, 2)
            
            products_list.append({
                'sku': sku,
                'department': dept,
                'category': category,
                'product_name': f'{category} Item {i+1}',
                'supplier_id': f'SUP{np.random.randint(1, 15):03d}',
                'cost': round(base_cost, 2),
                'retail_price': retail_price,
                'reorder_point': np.random.randint(10, 50),
                'reorder_quantity': np.random.randint(20, 100),
                'lead_time_days': np.random.randint(7, 45),
                'shelf_life_days': np.random.choice([None, 180, 365, 730]),
                'weight_kg': round(np.random.uniform(0.5, 25), 2),
                'is_seasonal': np.random.choice([True, False], p=[0.3, 0.7])
            })

products_df = pd.DataFrame(products_list)

# ========== SUPPLIERS ==========
suppliers_data = []
for i in range(1, 15):
    suppliers_data.append({
        'supplier_id': f'SUP{i:03d}',
        'supplier_name': f'Supplier {i} Inc.',
        'country': np.random.choice(['USA', 'China', 'Germany', 'Japan', 'South Korea'], p=[0.4, 0.3, 0.1, 0.1, 0.1]),
        'reliability_score': round(np.random.uniform(75, 99), 1),
        'avg_lead_time': np.random.randint(14, 60),
        'defect_rate': round(np.random.uniform(0.1, 5.0), 2)
    })
suppliers_df = pd.DataFrame(suppliers_data)

# ========== DAILY INVENTORY SNAPSHOTS ==========
# Generate 180 days of inventory data
start_date = datetime(2024, 6, 1)
end_date = datetime(2024, 11, 27)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

inventory_records = []

for date in date_range:
    for _, store in stores_df.iterrows():
        for _, product in products_df.iterrows():
            # Not all products in all stores
            if np.random.random() < 0.85:  # 85% chance product is stocked
                
                # Initialize or carry forward inventory
                base_stock = np.random.randint(5, 150)
                
                # Add seasonality
                month = date.month
                seasonal_factor = 1.0
                if product['is_seasonal']:
                    if month in [11, 12]:  # Holiday season
                        seasonal_factor = 1.5
                    elif month in [6, 7, 8]:  # Summer
                        seasonal_factor = 1.3
                
                # Daily sales with variation
                avg_daily_sales = np.random.uniform(2, 15) * seasonal_factor
                daily_sales = max(0, int(np.random.poisson(avg_daily_sales)))
                
                current_stock = max(0, base_stock - daily_sales)
                
                # Determine status
                if current_stock == 0:
                    status = 'Out of Stock'
                elif current_stock <= product['reorder_point']:
                    status = 'Low Stock'
                elif current_stock > product['reorder_quantity'] * 1.5:
                    status = 'Overstock'
                else:
                    status = 'In Stock'
                
                # Calculate days of supply
                days_supply = int(current_stock / avg_daily_sales) if avg_daily_sales > 0 else 999
                
                inventory_records.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'store_id': store['store_id'],
                    'sku': product['sku'],
                    'quantity_on_hand': current_stock,
                    'quantity_sold': daily_sales,
                    'status': status,
                    'days_of_supply': min(days_supply, 999),
                    'value_on_hand': round(current_stock * product['cost'], 2)
                })

inventory_df = pd.DataFrame(inventory_records)

# ========== SALES TRANSACTIONS ==========
sales_records = []
transaction_id = 10000

for date in date_range:
    daily_transactions = np.random.randint(50, 200)  # 50-200 transactions per day
    
    for _ in range(daily_transactions):
        store = stores_df.sample(1).iloc[0]
        
        # 1-3 items per transaction
        num_items = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
        
        for _ in range(num_items):
            product = products_df.sample(1).iloc[0]
            quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.5, 0.2, 0.15, 0.08, 0.05, 0.02])
            
            # Apply occasional discounts
            discount = 0
            if np.random.random() < 0.15:  # 15% chance of discount
                discount = round(product['retail_price'] * np.random.uniform(0.1, 0.3), 2)
            
            final_price = product['retail_price'] - discount
            revenue = round(quantity * final_price, 2)
            profit = round(revenue - (quantity * product['cost']), 2)
            
            sales_records.append({
                'transaction_id': f'TXN{transaction_id:08d}',
                'date': date.strftime('%Y-%m-%d'),
                'store_id': store['store_id'],
                'sku': product['sku'],
                'quantity': quantity,
                'unit_price': product['retail_price'],
                'discount': discount,
                'revenue': revenue,
                'cost': round(quantity * product['cost'], 2),
                'profit': profit,
                'profit_margin': round((profit / revenue * 100), 2) if revenue > 0 else 0
            })
            transaction_id += 1

sales_df = pd.DataFrame(sales_records)

# ========== PURCHASE ORDERS ==========
po_records = []
po_id = 5000

# Generate purchase orders for restocking
for date in date_range[::7]:  # Weekly POs
    num_pos = np.random.randint(5, 15)
    
    for _ in range(num_pos):
        product = products_df.sample(1).iloc[0]
        store = stores_df.sample(1).iloc[0]
        
        order_quantity = product['reorder_quantity']
        unit_cost = product['cost']
        total_cost = round(order_quantity * unit_cost, 2)
        
        delivery_date = date + timedelta(days=int(product['lead_time_days']))
        
        # PO status
        if delivery_date < datetime.now():
            po_status = np.random.choice(['Delivered', 'Delivered', 'Delivered', 'Partially Delivered'], 
                                        p=[0.85, 0.1, 0.03, 0.02])
        else:
            po_status = 'In Transit'
        
        po_records.append({
            'po_number': f'PO{po_id:06d}',
            'order_date': date.strftime('%Y-%m-%d'),
            'expected_delivery': delivery_date.strftime('%Y-%m-%d'),
            'store_id': store['store_id'],
            'sku': product['sku'],
            'supplier_id': product['supplier_id'],
            'order_quantity': order_quantity,
            'unit_cost': unit_cost,
            'total_cost': total_cost,
            'status': po_status
        })
        po_id += 1

po_df = pd.DataFrame(po_records)

# ========== SAVE ALL FILES ==========
stores_df.to_csv('C:/Users/alexy/Documents/Claude_projects/Portfolio creation/Dashboard_inventory/retail_stores.csv', index=False)
products_df.to_csv('C:/Users/alexy/Documents/Claude_projects/Portfolio creation/Dashboard_inventory/retail_products.csv', index=False)
suppliers_df.to_csv('C:/Users/alexy/Documents/Claude_projects/Portfolio creation/Dashboard_inventory/retail_suppliers.csv', index=False)
inventory_df.to_csv('C:/Users/alexy/Documents/Claude_projects/Portfolio creation/Dashboard_inventory/retail_inventory.csv', index=False)
sales_df.to_csv('C:/Users/alexy/Documents/Claude_projects/Portfolio creation/Dashboard_inventory/retail_sales.csv', index=False)
po_df.to_csv('C:/Users/alexy/Documents/Claude_projects/Portfolio creation/Dashboard_inventory/retail_purchase_orders.csv', index=False)


# ========== SUMMARY ==========
print("=" * 60)
print("RETAIL INVENTORY DATA GENERATED SUCCESSFULLY")
print("=" * 60)
print(f"\n📍 Stores: {len(stores_df)} locations across {stores_df['state'].nunique()} states")
print(f"📦 Products: {len(products_df)} SKUs across {products_df['department'].nunique()} departments")
print(f"🏭 Suppliers: {len(suppliers_df)} suppliers")
print(f"📊 Inventory Records: {len(inventory_df):,} daily snapshots")
print(f"💰 Sales Transactions: {len(sales_df):,} transactions")
print(f"📋 Purchase Orders: {len(po_df):,} POs")
print(f"\n💵 Total Revenue: ${sales_df['revenue'].sum():,.2f}")
print(f"💸 Total Profit: ${sales_df['profit'].sum():,.2f}")
print(f"📈 Avg Profit Margin: {sales_df['profit_margin'].mean():.1f}%")
print(f"\n📅 Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"📁 Files saved:")
print("   - retail_stores.csv")
print("   - retail_products.csv")
print("   - retail_suppliers.csv")
print("   - retail_inventory.csv")
print("   - retail_sales.csv")
print("   - retail_purchase_orders.csv")
print("\n✅ Ready to build the dashboard!")
print("=" * 60)