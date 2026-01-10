import streamlit as st
from queue import PriorityQueue
from datetime import datetime

# --- Initialize tickets ---
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# --- Priority function ---
def compute_priority(ticket):
    severity_weight = 0.7
    time_weight = 0.3
    waiting_minutes = (datetime.now() - ticket["created_at"]).total_seconds() / 60
    return -(severity_weight * ticket["severity"] + time_weight * waiting_minutes / 60)

st.title("🛎️ Support Ticket Queue")

if not st.session_state.tickets:
    st.info("No tickets yet! Add products from the shop to generate tickets.")

# --- Prepare ticket list ---
pq = PriorityQueue()
for t in st.session_state.tickets:
    pq.put((compute_priority(t), t))

ticket_list = []
while not pq.empty():
    _, t = pq.get()
    waiting_time = int((datetime.now() - t["created_at"]).total_seconds() / 60)
    ticket_list.append({
        "Ticket ID": t["id"],
        "Product": t["product_name"],
        "Severity": t["severity"],
        "Waiting Time (min)": waiting_time
    })

# --- Display tickets with buttons ---
for ticket in ticket_list:
    st.markdown(f"**Ticket #{ticket['Ticket ID']} — {ticket['Product']}**")
    st.write(f"Severity: {ticket['Severity']} | Waiting Time: {ticket['Waiting Time (min)']} min")
    col1, col2 = st.columns(2)
    with col1:
        resolve_key = f"resolve-{ticket['Ticket ID']}"
        if st.button("Resolve", key=resolve_key):
            # Remove ticket
            st.session_state.tickets = [t for t in st.session_state.tickets if t["id"] != ticket["Ticket ID"]]
            st.success(f"Ticket #{ticket['Ticket ID']} resolved!")
            break  # Stop iteration to avoid duplicate button triggers
    with col2:
        assign_key = f"assign-{ticket['Ticket ID']}"
        if st.button("Assign to Agent", key=assign_key):
            st.success(f"Ticket #{ticket['Ticket ID']} assigned to an agent!")
