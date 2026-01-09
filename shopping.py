from datetime import datetime
import os
from PIL import Image
import streamlit as st

# --- Configuration ---
st.set_page_config(layout="wide", page_title="SwiftBuy Shop")

# --- CSS Styling ---
st.markdown("""
<style>
.block-container { padding-top: 5rem; padding-bottom: 2rem; padding-left: 2rem; padding-right: 2rem; }
.header-container { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; margin-bottom: 20px; }
.nav-links { flex-grow: 1; text-align: center; }
.nav-links a { margin: 0 30px; text-decoration: none; color: #333; font-size: 16px; font-family: serif; }
.logo { font-size: 24px; font-weight: bold; font-family: serif; width: 200px; white-space: nowrap; }
.cart-icon { font-size: 16px; font-family: serif; width: 200px; text-align: right; }
h1 { margin-top: 10px; margin-bottom: 5px; font-family: serif; }
p { margin-bottom: 15px; font-family: serif; }
hr { margin: 15px 0; }
div[data-testid="stSelectbox"] { margin-bottom: 0px !important; }
.cols-box { border: 1px solid #ddd; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- Initialize Cart & Tickets ---
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# --- Cart count ---
def cart_count():
    return sum(item['quantity'] for item in st.session_state.cart.values())

# --- Page Navigation ---
def go_to_tickets():
    st.switch_page("pages/tickets.py")  # Update path if needed

# --- Product Card ---
def product_card(name, price, category="Bags", color="Black", feature="Durable", description="High-quality product", image=None):
    with st.container():
        # Display local image
        if image and os.path.exists(image):
            img = Image.open(image)
            st.image(img, width="stretch", caption=description)  # ✅ corrected
        else:
            st.markdown(
                "<div style='background-color: #e0e0e0; height: 180px; width: 100%; border-radius: 5px; margin-bottom:10px;'></div>",
                unsafe_allow_html=True
            )
            st.write(description)

        st.markdown(f"**{name}**")
        st.write(f"Category: {category}")
        st.write(f"Color: {color}")
        st.write(f"Feature: {feature}")
        st.write(f"Price: ₱{price}")

        # Add to Cart button
        add_to_cart_key = f"add-{name}-{price}"
        if st.button("Add to Cart", key=add_to_cart_key):
            if name in st.session_state.cart:
                st.session_state.cart[name]["quantity"] += 1
            else:
                st.session_state.cart[name] = {"price": price, "quantity": 1}

            ticket_id = len(st.session_state.tickets) + 1
            severity = 1 if price < 50 else 3 if price < 150 else 5
            st.session_state.tickets.append({
                "id": ticket_id,
                "product_name": name,
                "severity": severity,
                "created_at": datetime.now()
            })

            st.success(f"{name} added to cart and Ticket #{ticket_id} created!")

# --- Header ---
def render_header():
    col1, col2, col3 = st.columns([2,6,2])
    with col1:
        st.markdown("<div class='logo'>δ SwiftBuy</div>", unsafe_allow_html=True)
    with col2:
        nav1, nav2, nav3, nav4 = st.columns(4)
        with nav1:
            if st.button("Shop", key="nav_shop"):
                st.info("Shop clicked!")
        with nav2:
            if st.button("Trends", key="nav_trends"):
                st.info("Trends clicked!")
        with nav3:
            if st.button("Tickets", key="nav_tickets"):
                go_to_tickets()
        with nav4:
            if st.button("...", key="nav_more"):
                st.info("More clicked!")
    with col3:
        st.markdown(f"<div class='cart-icon'>🛒 Cart ({cart_count()})</div>", unsafe_allow_html=True)

render_header()

# --- Hero Section ---
st.markdown("<h1>Get Inspired</h1>", unsafe_allow_html=True)
st.markdown(
    "Browsing for your next long-haul trip, everyday journey, or just fancy a look at "
    "what's new from community favourites to almost sold out items."
)

# --- Filters ---
categories = ["All Categories", "Bags", "Pencils", "Notebooks", "Accessories", "Electronics"]
colors = ["All Color", "Black", "Red", "Blue", "Grey", "White", "Yellow", "Green", "Brown"]
features = ["All Features", "Durable", "Ergonomic", "Waterproof"]

filter_cols = st.columns([1,1,1,1,3,1])
with filter_cols[0]:
    selected_category = st.selectbox("Category", categories, label_visibility="collapsed")
with filter_cols[1]:
    selected_color = st.selectbox("Color", colors, label_visibility="collapsed")
with filter_cols[2]:
    selected_feature = st.selectbox("Features", features, label_visibility="collapsed")
with filter_cols[3]:
    selected_price = st.selectbox("Price", ["All Prices", "Under 50", "50 - 100", "Over 100"], label_visibility="collapsed")
with filter_cols[5]:
    selected_sort = st.selectbox("Sort", ["New In", "Price: Low to High", "Price: High to Low"], label_visibility="collapsed")

st.markdown("---")

# --- Product List ---
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
    {"name":"Classic Notebook","price":15,"category":"Notebooks","color":"Yellow","feature":"Durable",
     "description":"Perfect for everyday notes.","image":"images/classic_notebook.jpg"},
    {"name":"Planner Notebook","price":30,"category":"Notebooks","color":"Black","feature":"Ergonomic",
     "description":"Organize your daily tasks easily.","image":"images/planner_notebook.jpg"},
    {"name":"Grid Notebook","price":20,"category":"Notebooks","color":"White","feature":"Durable",
     "description":"Ideal for math and technical notes.","image":"images/grid_notebook.jpg"},
    {"name":"Journal Notebook","price":35,"category":"Notebooks","color":"Brown","feature":"Durable",
     "description":"Personal journal with premium paper.","image":"images/journal_notebook.jpg"},
    {"name":"Study Notes Pad","price":18,"category":"Notebooks","color":"Blue","feature":"Ergonomic",
     "description":"Designed for long study sessions.","image":"images/study_notes_pad.jpg"},
    {"name":"Sketch Pencil Set","price":20,"category":"Pencils","color":"Black","feature":"Ergonomic",
     "description":"Smooth and high-quality pencils.","image":"images/sketch_pencil_set.jpg"},
    {"name":"Color Pencil Pack","price":25,"category":"Pencils","color":"Multi","feature":"Durable",
     "description":"Bright colors for art and design.","image":"images/color_pencil_pack.jpg"},
    {"name":"Mechanical Pencil","price":10,"category":"Pencils","color":"Grey","feature":"Ergonomic",
     "description":"Refillable and easy to use.","image":"images/mechanical_pencil.jpg"},
    {"name":"Kids Pencil Set","price":12,"category":"Pencils","color":"Yellow","feature":"Durable",
     "description":"Safe and fun pencils for kids.","image":"images/kids_pencil_set.jpg"},
    {"name":"Eco Bottle","price":25,"category":"Accessories","color":"Green","feature":"Durable",
     "description":"Reusable bottle for everyday use.","image":"images/eco_bottle.jpg"},
    {"name":"Laptop Sleeve","price":50,"category":"Accessories","color":"Grey","feature":"Durable",
     "description":"Protective sleeve for laptops.","image":"images/laptop_sleeve.jpg"},
    {"name":"Desk Organizer","price":35,"category":"Accessories","color":"Brown","feature":"Durable",
     "description":"Keep your desk tidy and organized.","image":"images/desk_organizer.jpg"},
    {"name":"Phone Stand","price":15,"category":"Accessories","color":"Black","feature":"Ergonomic",
     "description":"Hands-free phone holder.","image":"images/phone_stand.jpg"},
    {"name":"USB Cable Organizer","price":12,"category":"Accessories","color":"White","feature":"Durable",
     "description":"Neatly organize your cables.","image":"images/usb_cable_organizer.jpg"},
    {"name":"Wireless Earbuds","price":80,"category":"Electronics","color":"White","feature":"Ergonomic",
     "description":"Comfortable earbuds with clear sound.","image":"images/wireless_earbuds.jpg"},
    {"name":"Bluetooth Speaker","price":120,"category":"Electronics","color":"Black","feature":"Waterproof",
     "description":"Portable speaker with powerful bass.","image":"images/bluetooth_speaker.jpg"},
    {"name":"Wireless Mouse","price":40,"category":"Electronics","color":"Grey","feature":"Ergonomic",
     "description":"Smooth and precise mouse.","image":"images/wireless_mouse.jpg"},
    {"name":"Keyboard Combo","price":90,"category":"Electronics","color":"Black","feature":"Durable",
     "description":"Keyboard and mouse combo.","image":"images/keyboard_combo.jpg"},
    {"name":"Power Bank","price":60,"category":"Electronics","color":"Blue","feature":"Durable",
     "description":"Fast charging power bank.","image":"images/power_bank.jpg"},
    {"name":"Smart Watch","price":150,"category":"Electronics","color":"Black","feature":"Waterproof",
     "description":"Track fitness and notifications.","image":"images/smart_watch.jpg"},
]

# --- Filter & Sort ---
def filter_products(product):
    if selected_category != "All Categories" and product["category"] != selected_category:
        return False
    if selected_color != "All Color" and product["color"] != selected_color:
        return False
    if selected_feature != "All Features" and product["feature"] != selected_feature:
        return False
    if selected_price == "Under 50" and product["price"] >= 50:
        return False
    if selected_price == "50 - 100" and (product["price"] < 50 or product["price"] > 100):
        return False
    if selected_price == "Over 100" and product["price"] <= 100:
        return False
    return True

filtered_products = list(filter(filter_products, product_list))
if selected_sort == "Price: Low to High":
    filtered_products.sort(key=lambda x: x["price"])
elif selected_sort == "Price: High to Low":
    filtered_products.sort(key=lambda x: x["price"], reverse=True)

# --- Render Products ---
for i in range(0, len(filtered_products), 4):
    cols = st.columns(4)
    for j, product in enumerate(filtered_products[i:i+4]):
        with cols[j]:
            product_card(**product)

# --- Cart Sidebar ---
with st.sidebar:
    st.header("🛒 Shopping Cart")
    
    if st.session_state.cart:
        total = 0
        to_remove = []

        for name, info in st.session_state.cart.items():
            st.markdown("---")  # separate items

            # Product name and total
            st.write(f"**{name}** x {info['quantity']} - ₱{info['price']*info['quantity']}")

            # Bigger buttons using HTML and columns
            col_inc, col_dec, col_rm = st.columns([1,1,1])
            
            with col_inc:
                if st.button("➕", key=f"inc-{name}", help="Increase quantity"):
                    st.session_state.cart[name]["quantity"] += 1
            with col_dec:
                if st.button("➖", key=f"dec-{name}", help="Decrease quantity"):
                    st.session_state.cart[name]["quantity"] -= 1
                    if st.session_state.cart[name]["quantity"] <= 0:
                        to_remove.append(name)
            with col_rm:
                if st.button("🗑️", key=f"rm-{name}", help="Remove item"):
                    to_remove.append(name)

            total += info['price'] * info['quantity']

        # Remove items after looping to avoid modifying dict during iteration
        for item in to_remove:
            if item in st.session_state.cart:
                del st.session_state.cart[item]

        st.markdown(f"**Total: ₱{total}**")

    else:
        st.write("Your cart is empty.")
