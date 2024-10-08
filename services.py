product_catalog={}



def init_catalog(product_info):
    for product in product_info:
        product['quantity']=0
        product_id=product.get('product_id',None)
        if product_id is None:
            print('Error: product_id not found')
            continue
        product_catalog[product_id]=product
    
def process_restock(restock):
    for stock in restock:
        product_id=stock.get('product_id',None)
        if product_id is None:
            print('Error: product_id not found')
            continue
        product=product_catalog.get(product_id,None)
        if product is None:
            print('Error: product is not part of inventory')
            continue
        product['quantity']=product['quantity']+stock.get('quantity', 0)

def process_order(order):
    print("processing order",order.get('order_id',0))
    shipped=[]
    left_over=[]
    for item in order.get('requested',[]):
        product_id=item.get('product_id', None)
        if product_id is None:
            print('Error: product_id is not found')
            continue
        product=product_catalog.get(product_id, None)
        if product is None:
            print('Error: product is not part of inventory')
            continue
        if product.get('quantity',0)==0:
            print('Error: product is out of stock')
            continue
        legit_quantity=0
        if item.get('quantity',0)*product.get('mass_g',0)>1800:
            legit_quantity=1800//product.get('mass_g', 0)
        else:
            legit_quantity=item.get('quantity', 0)
        shipped.append({'product_id':product_id,'quantity':legit_quantity})
        left_over.append({'product_id':product_id,'quantity':item.get('quantity',0)-legit_quantity})
        product_catalog[product_id]['quantity']=product_catalog[product_id]['quantity']-legit_quantity
    ship_package({'order_id':order.get('order_id',0),'shipped':shipped})
    return left_over
            

def ship_package(shipment):
    print(shipment)