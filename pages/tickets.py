import streamlit as st
from queue import PriorityQueue
from datetime import datetime

st.set_page_config(page_title="Support Tickets", layout="wide")

# --- Initialize tickets ---
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# --- Priority function ---
def compute_priority(ticket):
    severity_weight = 0.7
    time_weight = 0.3
    waiting_minutes = (datetime.now() - ticket["created_at"]).total_seconds() / 60
    return -(severity_weight * ticket["severity"] + time_weight * (waiting_minutes / 60))

st.title("🛎️ Support Ticket Queue System")

if not st.session_state.tickets:
    st.info("No tickets yet! Add products from the shop to generate tickets.")
    st.stop()

# --- Prepare ticket queue ---
pq = PriorityQueue()
for t in st.session_state.tickets:
    if t.get("status") != "Resolved":  # optional: hide resolved from queue
        pq.put((compute_priority(t), t))

ticket_list = []
while not pq.empty():
    _, t = pq.get()
    waiting_time = int((datetime.now() - t["created_at"]).total_seconds() / 60)
    ticket_list.append({
        "id": t["id"],
        "product": t["product_name"],
        "severity": t["severity"],
        "waiting": waiting_time,
        "status": t.get("status", "Pending"),
        "agent": t.get("agent")
    })

# --- Filters ---
filter_status = st.selectbox("Filter tickets", ["All", "Pending", "Assigned", "Resolved"])

if filter_status != "All":
    ticket_list = [t for t in ticket_list if t["status"] == filter_status]

agents = ["Arce", "Kath", "Dennis", "Clark"]

# --- Display tickets ---
for ticket in ticket_list:

    st.markdown(f"## 🎫 Ticket #{ticket['id']} — {ticket['product']}")
    st.write(f"**Severity:** {ticket['severity']} | **Waiting:** {ticket['waiting']} min")
    st.write(f"**Status:** {ticket['status']} | **Agent:** {ticket['agent'] or 'Unassigned'}")

    # Priority indicator
    if ticket["severity"] >= 4:
        st.error("🔴 High Priority")
    elif ticket["severity"] >= 2:
        st.warning("🟡 Medium Priority")
    else:
        st.success("🟢 Low Priority")

    col1, col2, col3 = st.columns(3)

    # --- Assign ---
    with col1:
        selected_agent = st.selectbox(
            "Assign agent", agents, key=f"agent-{ticket['id']}"
        )
        if st.button("Assign", key=f"assign-{ticket['id']}"):
            for t in st.session_state.tickets:
                if t["id"] == ticket["id"]:
                    t["agent"] = selected_agent
                    t["status"] = "Assigned"
            st.rerun()

    # --- Resolve ---
    with col2:
        if st.button("Resolve", key=f"resolve-{ticket['id']}"):
            for t in st.session_state.tickets:
                if t["id"] == ticket["id"]:
                    t["status"] = "Resolved"
            st.success("✅ Ticket resolved!")
            st.rerun()

    # --- Delete ---
    with col3:
        if st.button("Delete", key=f"delete-{ticket['id']}"):
            st.session_state.tickets = [
                t for t in st.session_state.tickets if t["id"] != ticket["id"]
            ]
            st.warning("🗑️ Ticket deleted")
            st.rerun()

    st.markdown("---")
