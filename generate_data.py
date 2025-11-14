# generate_data.py
"""
Robust synthetic e-commerce data generator producing:
customers.csv (5000), products.csv (2000), orders.csv (20000),
order_items.csv (50000), reviews.csv (8000)
"""

import random, os
from datetime import datetime, timedelta
import pandas as pd, numpy as np

# ---------- Config ----------
OUT_DIR = "."
random.seed(42)
np.random.seed(42)

N_CUSTOMERS = 5000
N_PRODUCTS = 2000
N_ORDERS = 20000
N_ORDER_ITEMS = 50000
N_REVIEWS = 8000

TODAY = datetime(2025, 11, 14)

# ---------- Helpers ----------
def zero_pad(num, width): return str(num).zfill(width)
def rand_date_between(start: datetime, end: datetime) -> str:
    if start > end:
        start, end = end, start
    return (start + timedelta(days=random.randint(0, max(0,(end-start).days)))).strftime("%Y-%m-%d")

# ---------- 1) Customers ----------
first_names = ["Aarav","Vivaan","Aditya","Arjun","Sai","Ananya","Saanvi","Diya","Isha","Riya",
               "Rahul","Karthik","Priya","Neha","Aditi","Kabir","Rohan","Maya","Sophia","Aria",
               "Liam","Noah","Olivia","Emma","Mia","Lucas","Ethan","Isabella","Chloe","Amelia"]
last_names = ["Sharma","Kumar","Reddy","Patel","Singh","Gupta","Nair","Iyer","Das","Dasgupta",
              "Mehta","Verma","Joshi","Chopra","Bose","Khan","Kapoor","Trivedi","Nath","Saxena"]
cities_states = [
    ("Bengaluru","Karnataka"),("Mumbai","Maharashtra"),("Delhi","Delhi"),("Chennai","Tamil Nadu"),
    ("Kolkata","West Bengal"),("Hyderabad","Telangana"),("Pune","Maharashtra"),("Jaipur","Rajasthan"),
    ("Lucknow","Uttar Pradesh"),("Ahmedabad","Gujarat"),("Surat","Gujarat"),("Visakhapatnam","Andhra Pradesh"),
    ("Coimbatore","Tamil Nadu"),("Nagpur","Maharashtra"),("Indore","Madhya Pradesh"),("Thiruvananthapuram","Kerala"),
    ("Bhopal","Madhya Pradesh"),("Patna","Bihar"),("Vijayawada","Andhra Pradesh"),("Vadodara","Gujarat")
]
genders = ["Male","Female","Other"]
loyalty_levels = ["Bronze","Silver","Gold","Platinum"]
signup_start = datetime(2018,1,1)
signup_end = datetime(2025,10,31)

customers = []
seen_emails = set()
for i in range(1, N_CUSTOMERS+1):
    cid = "CUST" + zero_pad(i,4)
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    name = f"{fn} {ln}"
    email = f"{fn.lower()}.{ln.lower()}{random.randint(1,999)}@example.com"
    while email in seen_emails:
        email = f"{fn.lower()}.{ln.lower()}{random.randint(1000,9999)}@example.com"
    seen_emails.add(email)
    gender = random.choices(genders, weights=[0.48,0.48,0.04])[0]
    age = random.randint(18,70)
    signup_date = rand_date_between(signup_start, signup_end)
    city, state = random.choice(cities_states)
    country = "India"
    loyalty = random.choices(loyalty_levels, weights=[0.6,0.25,0.1,0.05])[0]
    customers.append([cid,name,email,gender,age,signup_date,city,state,country,loyalty])

customers_df = pd.DataFrame(customers, columns=[
    "customer_id","name","email","gender","age","signup_date","city","state","country","loyalty_level"
])
customers_df.to_csv(os.path.join(OUT_DIR,"customers.csv"), index=False)
print("customers.csv ->", len(customers_df))

# ---------- 2) Products ----------
categories = ["Electronics","Fashion","Home","Beauty","Sports"]
brands_by_cat = {
    "Electronics":["SoundWave","Voltix","NovaTech","PixelPro","ElectroMax"],
    "Fashion":["UrbanWear","SilkRoute","Trendify","StyleHub","VogueLane"],
    "Home":["CasaPro","HomeEssence","ComfortLiving","Nestoria","Hearthstone"],
    "Beauty":["GlowMist","LuxeCare","PureBloom","VelvetTouch","AuraSkin"],
    "Sports":["FitFlex","ProActive","Sportify","Endura","PeakGear"]
}
prod_nouns = {
    "Electronics":["Headphones","Speaker","Charger","PowerBank","Smartwatch","Tablet"],
    "Fashion":["T-Shirt","Jeans","Sneakers","Jacket","Dress","Handbag"],
    "Home":["Blender","Vacuum","Cooker","Lamp","SofaCover","Table"],
    "Beauty":["Moisturizer","Serum","Lipstick","Perfume","FaceWash","Mask"],
    "Sports":["YogaMat","Dumbbell","RunningShoes","CyclingHelmet","WaterBottle","TennisRacket"]
}
added_start = datetime(2019,1,1)
added_end = datetime(2025,10,31)

products = []
for i in range(1, N_PRODUCTS+1):
    pid = "P" + zero_pad(i,4)
    cat = random.choice(categories)
    brand = random.choice(brands_by_cat[cat])
    pname = f"{random.choice(['Smart','Pro','Ultra','Mini','Classic','Prime'])} {random.choice(prod_nouns[cat])} {random.randint(100,999)}"
    price_mid = {
        "Electronics": random.uniform(799,19999),
        "Fashion": random.uniform(299,5499),
        "Home": random.uniform(499,12999),
        "Beauty": random.uniform(99,2499),
        "Sports": random.uniform(299,8999)
    }[cat]
    price = round(price_mid * random.uniform(0.8,1.25), 2)
    stock = random.randint(0,2000)
    rating = round(random.uniform(3.2,4.8),2)
    added_date = rand_date_between(added_start, added_end)
    products.append([pid,pname,cat,brand,price,stock,rating,added_date])

products_df = pd.DataFrame(products, columns=[
    "product_id","product_name","category","brand","price","stock_quantity","rating","added_date"
])
products_df.to_csv(os.path.join(OUT_DIR,"products.csv"), index=False)
print("products.csv ->", len(products_df))

price_lookup = dict(zip(products_df.product_id, products_df.price))

# ---------- 3) Orders skeleton ----------
order_start = datetime(2020,1,1)
order_end = TODAY
payment_methods = ["UPI","Card","Wallet","COD","NetBanking"]
order_statuses = ["Delivered","Shipped","Pending","Cancelled"]

month_weights = {m:1.0 for m in range(1,13)}
for m in [11,12]: month_weights[m] = 1.8
for m in [3,4,10]: month_weights[m] = 1.2

orders = []
cust_ids = customers_df.customer_id.tolist()
for i in range(1, N_ORDERS+1):
    oid = "ORD" + zero_pad(i,5)
    cid = random.choice(cust_ids)
    while True:
        d = order_start + timedelta(days=random.randint(0, (order_end-order_start).days))
        if random.random() < (month_weights[d.month] / max(month_weights.values())):
            order_date = d.strftime("%Y-%m-%d")
            break
    payment = random.choices(payment_methods, weights=[0.35,0.35,0.15,0.08,0.07])[0]
    status = random.choices(order_statuses, weights=[0.78,0.12,0.07,0.03])[0]
    # mostly ship to customer's city
    if random.random() < 0.9:
        c = customers_df.loc[customers_df.customer_id==cid].iloc[0]
        ship_city, ship_state = c.city, c.state
    else:
        ship_city, ship_state = random.choice(cities_states)
    orders.append([oid,cid,order_date,payment,status,ship_city,ship_state])

orders_df = pd.DataFrame(orders, columns=[
    "order_id","customer_id","order_date","payment_method","order_status","shipping_city","shipping_state"
])
# create numeric columns safely
orders_df["total_amount"] = 0.0
orders_df["discount"] = 0.0
orders_df["final_amount"] = 0.0

print("orders skeleton ->", len(orders_df))

# ---------- 4) Order items ----------
product_ids = products_df.product_id.tolist()
order_items = []
oi_counter = 1
order_index = 0
num_orders = len(orders_df)

while len(order_items) < N_ORDER_ITEMS:
    oid = orders_df.iloc[order_index % num_orders]["order_id"]
    n_items = random.randint(1,5)
    n_items = min(n_items, N_ORDER_ITEMS - len(order_items))
    chosen = random.sample(product_ids, k=n_items)
    for pid in chosen:
        qty = random.choices([1,2,3], weights=[0.85,0.12,0.03])[0]
        unit_price = round(price_lookup[pid] * random.uniform(0.85,1.05),2)
        total_price = round(unit_price * qty,2)
        order_items.append([ "OI" + zero_pad(oi_counter,6), oid, pid, qty, unit_price, total_price ])
        oi_counter += 1
    order_index += 1

order_items_df = pd.DataFrame(order_items, columns=[
    "order_item_id","order_id","product_id","quantity","unit_price","total_price"
])
order_items_df.to_csv(os.path.join(OUT_DIR,"order_items.csv"), index=False)
print("order_items.csv ->", len(order_items_df))

# ---------- 5) Compute totals robustly (no fragile merge) ----------
# aggregate total_price per order into a dict, then map to orders_df
order_totals_series = order_items_df.groupby("order_id", as_index=False)["total_price"].sum().rename(columns={"total_price":"total_amount"})
# create mapping dict
order_totals_map = dict(zip(order_totals_series["order_id"], order_totals_series["total_amount"]))

# Map totals into orders_df safely
orders_df["total_amount"] = orders_df["order_id"].map(order_totals_map).fillna(0.0).astype(float)

# compute discounts vectorized
loyalty_map = customers_df.set_index("customer_id")["loyalty_level"].to_dict()
loyalty_pct = {"Bronze":0.0,"Silver":0.03,"Gold":0.07,"Platinum":0.12}
orders_df["loyalty_pct"] = orders_df["customer_id"].map(lambda c: loyalty_pct.get(loyalty_map.get(c, "Bronze"), 0.0))

n = len(orders_df)
rand_vals = np.random.rand(n)
coupon_vals = np.random.uniform(0.05,0.15,size=n)
orders_df["coupon_pct"] = np.where(rand_vals < 0.10, coupon_vals, 0.0)
orders_df["order_month"] = pd.to_datetime(orders_df["order_date"]).dt.month
orders_df["seasonal_pct"] = np.where(orders_df["order_month"].isin([11,12]), 0.03, 0.0)

combined_pct = (orders_df["loyalty_pct"] + orders_df["coupon_pct"] + orders_df["seasonal_pct"]).clip(upper=0.25)
orders_df["discount_pct"] = np.where(orders_df["order_status"]=="Cancelled", 0.0, combined_pct)

orders_df["discount"] = (orders_df["total_amount"] * orders_df["discount_pct"]).round(2)
orders_df["final_amount"] = (orders_df["total_amount"] - orders_df["discount"]).round(2)

# drop helper cols
orders_df = orders_df.drop(columns=["loyalty_pct","coupon_pct","order_month","seasonal_pct","discount_pct"])

orders_df.to_csv(os.path.join(OUT_DIR,"orders.csv"), index=False)
print("orders.csv ->", len(orders_df))

# ---------- 6) Reviews ----------
product_added = dict(zip(products_df.product_id, products_df.added_date))
customer_signup = dict(zip(customers_df.customer_id, customers_df.signup_date))

pos = ["Excellent product, highly recommended!","Very satisfied with the purchase.","Good value for money.","Works as expected.","Quality is great for the price."]
neu = ["Product is okay, nothing special.","Average quality, meets expectations.","It's fine but could be better.","Decent product for the price."]
neg = ["Disappointed with the build quality.","Stopped working after a week.","Not worth the money.","Poor customer service experience."]

reviews = []
for i in range(1, N_REVIEWS+1):
    rid = "R" + zero_pad(i,5)
    pid = random.choice(product_ids)
    cid = random.choice(cust_ids)
    p_added = datetime.strptime(product_added[pid], "%Y-%m-%d")
    c_signup = datetime.strptime(customer_signup[cid], "%Y-%m-%d")
    start_dt = max(p_added, c_signup, datetime(2020,1,1))
    if start_dt > TODAY: start_dt = datetime(2021,1,1)
    rdate = rand_date_between(start_dt, TODAY)
    rating = random.choices([5,4,3,2,1], weights=[0.45,0.30,0.15,0.07,0.03])[0]
    if rating >= 4:
        text = random.choice(pos); sent = "Positive"
    elif rating == 3:
        text = random.choice(neu); sent = "Neutral"
    else:
        text = random.choice(neg); sent = "Negative"
    reviews.append([rid,cid,pid,rating,text,rdate,sent])

reviews_df = pd.DataFrame(reviews, columns=["review_id","customer_id","product_id","rating","review_text","review_date","sentiment"])
reviews_df.to_csv(os.path.join(OUT_DIR,"reviews.csv"), index=False)
print("reviews.csv ->", len(reviews_df))

print("All files generated in:", os.path.abspath(OUT_DIR))
