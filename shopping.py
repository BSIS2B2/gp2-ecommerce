from datetime import datetime
import os
from PIL import Image
import streamlit as st

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(layout="wide", page_title="SwiftBuy Shop")

# --------------------------------------------------
# Theme State
# --------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# --------------------------------------------------
# Theme Switcher (Sidebar)
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🎨 Theme")
    theme_choice = st.radio("Mode", ["Light", "Dark"],
        index=0 if st.session_state.theme == "Light" else 1)

if theme_choice != st.session_state.theme:
    st.session_state.theme = theme_choice
    st.rerun()

# --------------------------------------------------
# Apply Theme
# --------------------------------------------------
if st.session_state.theme == "Light":
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8fafc, #eef2ff); color: #0f172a; }
    .cols-box { background: white; border-radius: 16px; padding: 18px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: 0.3s; }
    .cols-box:hover { transform: translateY(-6px); box-shadow: 0 15px 35px rgba(0,0,0,0.12); }
    .logo { color: #4f46e5; font-size: 28px; font-weight: 800; }
    .cart-icon { color: #0f172a; font-weight: 600; text-align:right; }
    h1 { color: #0f172a; }
    .stButton > button { background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; border-radius: 12px; font-weight: 600; }
    section[data-testid="stSidebar"] { background: #0f172a; }
    section[data-testid="stSidebar"] * { color: white; }
    .price { color: #4f46e5; font-weight: 800; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020617, #0f172a); color: #e5e7eb; }
    .cols-box { background: #020617; border-radius: 16px; padding: 18px; box-shadow: 0 10px 25px rgba(0,0,0,0.6); transition: 0.3s; border: 1px solid #1e293b; }
    .cols-box:hover { transform: translateY(-6px); box-shadow: 0 15px 35px rgba(0,0,0,0.8); }
    .logo { color: #a78bfa; font-size: 28px; font-weight: 800; }
    .cart-icon { color: #e5e7eb; font-weight: 600; text-align:right; }
    h1 { color: #f9fafb; }
    .stButton > button { background: linear-gradient(135deg, #7c3aed, #a78bfa); color: white; border-radius: 12px; font-weight: 600; }
    section[data-testid="stSidebar"] { background: #020617; border-right: 1px solid #1e293b; }
    section[data-testid="stSidebar"] * { color: #e5e7eb; }
    .price { color: #a78bfa; font-weight: 800; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# Init Cart & Tickets
# --------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "tickets" not in st.session_state:
    st.session_state.tickets = []

def cart_count():
    return sum(item["quantity"] for item in st.session_state.cart.values())

# --------------------------------------------------
# Header (Logo left, Cart right)
# --------------------------------------------------
h1, h2 = st.columns([8,2])
with h1:
    st.markdown("<div class='logo'>δ SwiftBuy</div>", unsafe_allow_html=True)
with h2:
    st.markdown(f"<div class='cart-icon'>🛒 Cart ({cart_count()})</div>", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# Hero Section
# --------------------------------------------------
st.markdown("<h1>Get Inspired</h1>", unsafe_allow_html=True)
st.markdown(
    "<p>Browsing for your next long-haul trip, everyday journey, or just fancy a look at "
    "what's new from community favourites to almost sold out items.</p>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# Filters
# --------------------------------------------------
categories = ["All Categories", "Bags", "Pencils", "Notebooks", "Accessories", "Electronics"]
colors = ["All Color", "Black", "Red", "Blue", "Grey", "White", "Yellow", "Green", "Brown"]
features = ["All Features", "Durable", "Ergonomic", "Waterproof"]

f1,f2,f3,f4,f5 = st.columns([1,1,1,1,1])
with f1: selected_category = st.selectbox("Category", categories)
with f2: selected_color = st.selectbox("Color", colors)
with f3: selected_feature = st.selectbox("Features", features)
with f4: selected_price = st.selectbox("Price", ["All Prices", "Under 50", "50 - 100", "Over 100"])
with f5: selected_sort = st.selectbox("Sort", ["New In", "Price: Low to High", "Price: High to Low"])

st.markdown("---")

# --------------------------------------------------
# Products (Sample)
# --------------------------------------------------
product_list = [
    {"name":"Urban Bag","price":300,"category":"Bags","color":"Black","feature":"Durable",
     "description":"Spacious and sturdy, perfect for everyday use.","image":"images/urban_bag.jpg"},

    {"name":"Sports Pack","price":250,"category":"Bags","color":"Grey","feature":"Waterproof",
     "description":"Perfect for gym and outdoor activities.","image":"images/sports_pack.jpg"},

    {"name":"Camo Space Bag","price":350,"category":"Bags","color":"Blue","feature":"Ergonomic",
     "description":"Stylish design with comfortable straps.","image":"images/camo_space_bag.jpg"},

    {"name":"Cat Fun Bag","price":280,"category":"Bags","color":"Red","feature":"Durable",
     "description":"Cute pattern, ideal for kids and teens.","image":"images/cat_fun_bag.jpg"},
     
    {"name":"Travel Backpack","price":400,"category":"Bags","color":"Blue","feature":"Waterproof",
    "description":"Large capacity, ideal for trips.","image":"images/travel_backpack.jpg"},

    {"name":"Leather Office Bag","price":450,"category":"Bags","color":"Brown","feature":"Durable",
     "description":"Professional look for office use.","image":"images/leather_office_bag.jpg"},

    {"name":"Mini Sling Bag","price":180,"category":"Bags","color":"Black","feature":"Ergonomic",
     "description":"Lightweight sling bag for daily essentials.","image":"images/mini_sling_bag.jpg"},

    {"name":"School Backpack","price":220,"category":"Bags","color":"Red","feature":"Durable",
     "description":"Perfect for students and school needs.","image":"images/school_backpack.jpg"},

    {"name":"Classic Notebook","price":30,"category":"Notebooks","color":"Yellow","feature":"Durable",
     "description":"Perfect for everyday notes.","image":"images/classic_notebook.jpg"},

    {"name":"Planner Notebook","price":50,"category":"Notebooks","color":"Black","feature":"Ergonomic",
     "description":"Organize your daily tasks easily.","image":"images/planner_notebook.jpg"},

    {"name":"Grid Notebook","price":80,"category":"Notebooks","color":"White","feature":"Durable",
     "description":"Ideal for math and technical notes.","image":"images/grid_notebook.jpg"},

    {"name":"Journal Notebook","price":70,"category":"Notebooks","color":"Brown","feature":"Durable",
     "description":"Personal journal with premium paper.","image":"images/journal_notebook.jpg"},

    {"name":"Study Notes Pad","price":45,"category":"Notebooks","color":"Blue","feature":"Ergonomic",
     "description":"Designed for long study sessions.","image":"images/study_notes_pad.jpg"},

    {"name":"Sketch Pencil Set","price":305,"category":"Pencils","color":"Black","feature":"Ergonomic",
     "description":"Smooth and high-quality pencils.","image":"images/sketch_pencil_set.jpg"},

    {"name":"Color Pencil Pack","price":205,"category":"Pencils","color":"Multi","feature":"Durable",
     "description":"Bright colors for art and design.","image":"images/color_pencil_pack.jpg"},

    {"name":"Mechanical Pencil","price":450,"category":"Pencils","color":"Grey","feature":"Ergonomic",
     "description":"Refillable and easy to use.","image":"images/mechanical_pencil.jpg"},

    {"name":"Kids Pencil Set","price":150,"category":"Pencils","color":"Yellow","feature":"Durable",
     "description":"Safe and fun pencils for kids.","image":"images/kids_pencil_set.jpg"},

    {"name":"Eco Bottle","price":150,"category":"Accessories","color":"Green","feature":"Durable",
     "description":"Reusable bottle for everyday use.","image":"images/eco_bottle.jpg"},

    {"name":"Laptop Sleeve","price":199,"category":"Accessories","color":"Grey","feature":"Durable",
     "description":"Protective sleeve for laptops.","image":"images/laptop_sleeve.jpg"},

    {"name":"Desk Organizer","price":1500,"category":"Accessories","color":"Brown","feature":"Durable",
     "description":"Keep your desk tidy and organized.","image":"images/desk_organizer.jpg"},

    {"name":"Phone Stand","price":165,"category":"Accessories","color":"Black","feature":"Ergonomic",
     "description":"Hands-free phone holder.","image":"images/phone_stand.jpg"},

    {"name":"USB Cable Organizer","price":55,"category":"Accessories","color":"White","feature":"Durable",
     "description":"Neatly organize your cables.","image":"images/usb_cable_organizer.jpg"},

    {"name":"Wireless Earbuds","price":199,"category":"Electronics","color":"White","feature":"Ergonomic",
     "description":"Comfortable earbuds with clear sound.","image":"images/wireless_earbuds.jpg"},

    {"name":"Bluetooth Speaker","price":545,"category":"Electronics","color":"Black","feature":"Waterproof",
     "description":"Portable speaker with powerful bass.","image":"images/bluetooth_speaker.jpg"},

    {"name":"Wireless Mouse","price":565,"category":"Electronics","color":"Grey","feature":"Ergonomic",
     "description":"Smooth and precise mouse.","image":"images/wireless_mouse.jpg"},

    {"name":"Keyboard Combo","price":689,"category":"Electronics","color":"Black","feature":"Durable",
     "description":"Keyboard and mouse combo.","image":"images/keyboard_combo.jpg"},

    {"name":"Power Bank","price":699,"category":"Electronics","color":"Blue","feature":"Durable",
     "description":"Fast charging power bank.","image":"images/power_bank.jpg"},

    {"name":"Smart Watch","price":899,"category":"Electronics","color":"Black","feature":"Waterproof",
     "description":"Track fitness and notifications.","image":"images/smart_watch.jpg"},
     
]

def filter_products(p):
    if selected_category != "All Categories" and p["category"] != selected_category: return False
    if selected_color != "All Color" and p["color"] != selected_color: return False
    if selected_feature != "All Features" and p["feature"] != selected_feature: return False
    if selected_price == "Under 50" and p["price"] >= 50: return False
    if selected_price == "50 - 100" and not (50 <= p["price"] <= 100): return False
    if selected_price == "Over 100" and p["price"] <= 100: return False
    return True

products = list(filter(filter_products, product_list))
if selected_sort == "Price: Low to High":
    products.sort(key=lambda x: x["price"])
elif selected_sort == "Price: High to Low":
    products.sort(key=lambda x: x["price"], reverse=True)

# --------------------------------------------------
# Product Card
# --------------------------------------------------
def product_card(p):
    st.markdown("<div class='cols-box'>", unsafe_allow_html=True)

    if os.path.exists(p["image"]):
        st.image(Image.open(p["image"]), use_container_width=True)

    st.markdown(f"### {p['name']}")
    st.write(p["description"])
    st.markdown(f"<div class='price'>₱{p['price']}</div>", unsafe_allow_html=True)

    if st.button("Add to Cart", key=p["name"]):
        if p["name"] in st.session_state.cart:
            st.session_state.cart[p["name"]]["quantity"] += 1
        else:
            st.session_state.cart[p["name"]] = {"price": p["price"], "quantity": 1}

        ticket_id = len(st.session_state.tickets) + 1
        severity = 1 if p["price"] < 50 else 3 if p["price"] < 150 else 5

        st.session_state.tickets.append({
            "id": ticket_id,
            "product_name": p["name"],
            "severity": severity,
            "created_at": datetime.now(),
            "status": "Pending",
            "agent": None
        })

        st.success("Added to cart!")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# Render Products
# --------------------------------------------------
for i in range(0, len(products), 4):
    cols = st.columns(4)
    for j, p in enumerate(products[i:i+4]):
        with cols[j]:
            product_card(p)

# --------------------------------------------------
# Sidebar Cart
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🛒 Shopping Cart")

    if st.session_state.cart:
        total = 0
        for name, info in st.session_state.cart.items():
            st.write(f"**{name}** x {info['quantity']} = ₱{info['price']*info['quantity']}")
            total += info['price'] * info['quantity']
        st.markdown("---")
        st.markdown(f"### Total: ₱{total}")

        # ✅ Checkout Button
        if st.button("Proceed to Checkout 🧾"):
            st.switch_page("pages/checkout.py")

    else:
        st.info("Cart is empty")
