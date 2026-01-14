import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Checkout", layout="wide")

# -------------------------------
# Theme State (sync with shopping.py)
# -------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

with st.sidebar:
    st.markdown("## 🎨 Theme")
    theme_choice = st.radio("Mode", ["Light", "Dark"],
        index=0 if st.session_state.theme == "Light" else 1)

if theme_choice != st.session_state.theme:
    st.session_state.theme = theme_choice
    st.rerun()

# -------------------------------
# Apply Theme & Button Style (including hover)
# -------------------------------
if st.session_state.theme == "Light":
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8fafc, #eef2ff); color: #0f172a; }
    h1,h2,h3,p,div,label { color:#0f172a !important; }

    /* Buttons style */
    .stButton>button, .stButton button { 
        background: linear-gradient(135deg,#4f46e5,#7c3aed) !important; 
        color:white !important; 
        border-radius:12px !important; 
        font-weight:600 !important; 
        padding: 8px 18px !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important; /* smooth hover transition */
    }

    /* Hover effect */
    .stButton>button:hover, .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.35) !important;
        filter: brightness(1.1);
        cursor: pointer;
    }

    .receipt-card { background:white; padding:20px; border-radius:16px; box-shadow:0 10px 25px rgba(0,0,0,0.1); margin-bottom:20px;}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020617, #0f172a); color: #e5e7eb; }
    h1,h2,h3,p,div,label { color:#e5e7eb !important; }

    /* Buttons style */
    .stButton>button, .stButton button { 
        background: linear-gradient(135deg,#7c3aed,#a78bfa) !important; 
        color:white !important; 
        border-radius:12px !important; 
        font-weight:600 !important; 
        padding: 8px 18px !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4) !important;
        transition: all 0.3s ease !important;
    }

    /* Hover effect */
    .stButton>button:hover, .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.6) !important;
        filter: brightness(1.1);
        cursor: pointer;
    }

    .receipt-card { background:#0f172a; padding:20px; border-radius:16px; box-shadow:0 10px 25px rgba(0,0,0,0.6); margin-bottom:20px;}
    </style>
    """, unsafe_allow_html=True)


# -------------------------------
# Page Title
# -------------------------------
st.title("🧾 Checkout")

# -------------------------------
# Check Cart
# -------------------------------
if "cart" not in st.session_state or not st.session_state.cart:
    st.warning("Your cart is empty. Go back to shop first.")
    st.stop()

# -------------------------------
# Customer Form
# -------------------------------
st.subheader("📋 Customer Information")
with st.form("checkout_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
    with col2:
        address = st.text_area("Delivery Address")
        payment = st.selectbox("Payment Method", ["Cash on Delivery", "GCash", "Credit/Debit Card"])
    
    # ✅ Styled submit button inside form
    submitted = st.form_submit_button("✅ Place Order")

# -------------------------------
# Order Summary
# -------------------------------
st.subheader("🛒 Order Summary")
total = 0
for item, info in st.session_state.cart.items():
    st.write(f"**{item}** x {info['quantity']} = ₱{info['price']*info['quantity']}")
    total += info['price']*info['quantity']
st.markdown(f"### 💰 Total: ₱{total}")

# -------------------------------
# Place Order
# -------------------------------
if submitted:
    if not name or not address or not phone:
        st.error("Please complete all required fields.")
    else:
        if "orders" not in st.session_state:
            st.session_state.orders = []

        order = {
            "order_id": len(st.session_state.orders)+1,
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "payment": payment,
            "items": st.session_state.cart,
            "total": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        st.session_state.orders.append(order)
        st.session_state.cart = {}
        st.success("🎉 Order placed successfully!")
        st.balloons()

        # -------------------------------
        # Beautiful Receipt Card (styled)
        # -------------------------------
        st.markdown("<div class='receipt-card'>", unsafe_allow_html=True)
        st.markdown(f"### 🧾 Order Receipt #{order['order_id']}")
        st.write(f"**Name:** {order['name']}")
        st.write(f"**Email:** {order['email']}")
        st.write(f"**Phone:** {order['phone']}")
        st.write(f"**Address:** {order['address']}")
        st.write(f"**Payment:** {order['payment']}")
        st.write(f"**Date:** {order['date']}")
        st.markdown("#### Items Purchased:")
        for item, info in order['items'].items():
            st.write(f"- {item} x {info['quantity']} = ₱{info['price']*info['quantity']}")
        st.markdown(f"### 💰 Total Paid: ₱{order['total']}")
        st.markdown("</div>", unsafe_allow_html=True)
