import pandas as pd

def list_products(products: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # Filter for orders in February 2020
    feb_orders = orders[(orders['order_date'] >= '2020-02-01') & 
                        (orders['order_date'] <= '2020-02-29')]
    
    # Group by product_id and sum the units
    grouped = feb_orders.groupby('product_id')['unit'].sum().reset_index()
    
    # Filter for products with at least 100 units
    filtered = grouped[grouped['unit'] >= 100]
    
    # Merge with Products table to get names
    result = pd.merge(filtered, products, on='product_id')
    
    # Return the required columns
    return result[['product_name', 'unit']]