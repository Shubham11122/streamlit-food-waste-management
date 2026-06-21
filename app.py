import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# =============================================
# DATABASE
# =============================================

DB_PATH = "food_wastage.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def run_query(query, params=()):
    conn = get_conn()
    df   = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def run_write(query, params=()):
    conn = get_conn()
    conn.execute(query, params)
    conn.commit()
    conn.close()

# =============================================
# PAGE CONFIG
# =============================================

st.set_page_config(
    page_title="Food Waste Management",
    page_icon="🍱",
    layout="wide"
)

# =============================================
# GLOBAL STYLES
# =============================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027 0%, #1a3a2a 60%, #0f2027 100%);
    border-right: 1px solid #1e4d30;
}
[data-testid="stSidebar"] * { color: #e0f2e9 !important; }

.sidebar-logo {
    text-align: center;
    padding: 18px 0 10px 0;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 1px;
    color: #52e09c !important;
    border-bottom: 1px solid #1e4d30;
    margin-bottom: 18px;
}
.sidebar-logo span {
    display: block;
    font-size: 11px;
    font-weight: 400;
    letter-spacing: 2px;
    color: #6bbf8e !important;
    text-transform: uppercase;
    margin-top: 2px;
}
.nav-section-label {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4a8c66 !important;
    padding: 10px 16px 4px 16px;
    font-weight: 600;
}
[data-testid="stAppViewContainer"] { background: #0d1117; }
.block-container { padding-top: 28px !important; padding-bottom: 40px !important; }

.page-header {
    background: linear-gradient(90deg, #0f2d1f, #163d28);
    border: 1px solid #1e4d30;
    border-radius: 14px;
    padding: 24px 30px;
    margin-bottom: 24px;
}
.page-header h1 { color: #52e09c !important; font-size: 26px !important; font-weight: 700 !important; margin: 0 0 4px 0 !important; }
.page-header p  { color: #6bbf8e !important; font-size: 14px !important; margin: 0 !important; }

[data-testid="metric-container"] {
    background: #111b14;
    border: 1px solid #1e4d30;
    border-radius: 12px;
    padding: 16px 20px !important;
}
[data-testid="stMetricValue"] { color: #52e09c !important; font-size: 28px !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #6bbf8e !important; font-size: 13px !important; }

.hero-box {
    background: linear-gradient(120deg, #0a2a18 0%, #0f3d22 50%, #0a2a18 100%);
    border: 1px solid #1e4d30;
    border-radius: 18px;
    padding: 48px 40px;
    text-align: center;
    margin-bottom: 28px;
}
.hero-box h1 { color: #52e09c !important; font-size: 34px !important; font-weight: 700 !important; margin-bottom: 8px !important; }
.hero-box p  { color: #a8d5b5 !important; font-size: 16px !important; max-width: 600px; margin: 0 auto !important; line-height: 1.7; }

.feat-card {
    background: #111b14;
    border: 1px solid #1e4d30;
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    min-height: 160px;
}
.feat-card .icon { font-size: 32px; margin-bottom: 10px; }
.feat-card h4 { color: #52e09c !important; font-size: 15px !important; font-weight: 600 !important; margin-bottom: 8px !important; }
.feat-card p  { color: #7aba96 !important; font-size: 13px !important; line-height: 1.6 !important; }

.footer-box {
    background: #0d1a11;
    border: 1px solid #1e4d30;
    border-radius: 12px;
    padding: 20px 26px;
    margin-top: 28px;
    color: #6bbf8e !important;
    font-size: 13px;
}
.footer-box b { color: #52e09c !important; }

[data-testid="stForm"] {
    background: #111b14;
    border: 1px solid #1e4d30;
    border-radius: 14px;
    padding: 20px !important;
}
hr { border-color: #1e4d30 !important; }
</style>
""", unsafe_allow_html=True)

# =============================================
# SIDEBAR
# =============================================

NAV_ITEMS = [
    ("🏠", "Home",          "OVERVIEW"),
    ("📊", "Dashboard",     "OVERVIEW"),
    ("🔍", "Browse Food",   "FOOD"),
    ("🍱", "Food Listings", "FOOD"),
    ("📋", "Claims",        "OPERATIONS"),
    ("🏢", "Providers",     "OPERATIONS"),
    ("👥", "Receivers",     "OPERATIONS"),
    ("📈", "Analytics",     "INSIGHTS"),
    ("🧠", "SQL Insights",  "INSIGHTS"),
]

if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        🍱 FoodShare
        <span>Waste Management System</span>
    </div>
    """, unsafe_allow_html=True)

    current_section = None
    for icon, label, section in NAV_ITEMS:
        if section != current_section:
            st.markdown(f'<div class="nav-section-label">{section}</div>', unsafe_allow_html=True)
            current_section = section
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.page = label
            st.rerun()

    st.markdown("""
    <div style="padding:12px 16px;border-top:1px solid #1e4d30;margin-top:16px;">
        <div style="color:#4a8c66;font-size:11px;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">Database</div>
        <div style="color:#52e09c;font-size:12px;font-weight:600;">🗄️ SQLite</div>
        <div style="color:#4a8c66;font-size:11px;margin-top:2px;">food_wastage.db</div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page

# =============================================
# HELPERS
# =============================================

def page_header(title, subtitle=""):
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {"<p>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def chart_layout(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#a8d5b5",
        showlegend=True
    )
    return fig

# =============================================
# PAGE: HOME
# =============================================

def show_home():
    st.markdown("""
    <div class="hero-box">
        <h1>🍽️ Local Food Wastage Management</h1>
        <p>Connecting food providers — restaurants, supermarkets, grocery stores —
        with NGOs, shelters and communities in need.
        Smart redistribution to reduce waste and hunger.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📌 Project Overview")
    st.info("""
    Millions of meals are wasted every day while many people struggle to access food.
    This platform enables food listing, food claiming, claim tracking,
    and analytical reporting to reduce food wastage and connect communities.
    """)

    st.subheader("⚙️ How It Works")
    st.markdown("""
    **Provider → Food Listing → Receiver → Claim → Distribution**

    1. Food Providers list surplus food available for pickup.
    2. Receivers browse available food listings.
    3. Receivers claim food items they need.
    4. Claims are processed and tracked through the platform.
    5. Food gets redistributed instead of wasted.
    """)

    st.subheader("🚀 Core Modules")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feat-card"><div class="icon">♻️</div><h4>Reduce Food Waste</h4><p>Prevent surplus food from being discarded by connecting providers with receivers.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feat-card"><div class="icon">🍲</div><h4>Reduce Hunger</h4><p>Help NGOs, shelters and individuals access available food resources in their city.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feat-card"><div class="icon">🚚</div><h4>Improve Distribution</h4><p>Create an efficient food redistribution network through digital tracking.</p></div>', unsafe_allow_html=True)

    st.write("")
    st.subheader("🎯 Business Objectives")
    c1, c2 = st.columns(2)
    with c1:
        st.success("**Reduce Food Waste** — Identify and redistribute surplus food before it expires.")
    with c2:
        st.success("**Reduce Hunger** — Connect available food resources with communities in need.")

    st.markdown("""
    <div class="footer-box">
        <b>Tech Stack:</b> Python · SQLite · Streamlit · Pandas · Plotly
        &nbsp;|&nbsp;
        <b>Domain:</b> Food Management · Waste Reduction · Social Good
    </div>
    """, unsafe_allow_html=True)

# =============================================
# PAGE: DASHBOARD
# =============================================

def show_dashboard():
    page_header("📊 Dashboard", "Monitor food availability, provider contributions and claim activity.")

    providers = run_query("SELECT * FROM providers")
    receivers = run_query("SELECT * FROM receivers")
    food      = run_query("SELECT * FROM food_listings")
    claims    = run_query("SELECT * FROM claims")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🏢 Providers",     f"{len(providers):,}")
    c2.metric("🤝 Receivers",     f"{len(receivers):,}")
    c3.metric("🍱 Food Listings", f"{len(food):,}")
    c4.metric("📝 Claims",        f"{len(claims):,}")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        df  = claims.groupby("status").size().reset_index(name="count")
        fig = px.pie(df, names="status", values="count", hole=0.5,
                     title="Claims by Status",
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(chart_layout(fig), use_container_width=True)
    with col2:
        df  = food.groupby("food_type")["quantity"].sum().reset_index()
        fig = px.bar(df, x="food_type", y="quantity",
                     title="Food Quantity by Type", color="food_type",
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if "provider_type" in food.columns:
            df  = food.groupby("provider_type")["quantity"].sum().reset_index()
            fig = px.bar(df, x="provider_type", y="quantity", color="provider_type",
                         title="Food by Provider Type",
                         color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(chart_layout(fig), use_container_width=True)
    with col2:
        df  = food.groupby("meal_type").size().reset_index(name="count")
        fig = px.bar(df, x="meal_type", y="count", color="meal_type",
                     title="Meal Type Distribution",
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.subheader("📍 Top Locations by Food Quantity")
    df = food.groupby("location")["quantity"].sum().reset_index()\
             .sort_values("quantity", ascending=False).head(10)
    fig = px.bar(df, x="location", y="quantity", color="quantity",
                 title="Top 10 Locations", color_continuous_scale="Greens")
    st.plotly_chart(chart_layout(fig), use_container_width=True)

    top_food     = food.groupby("food_type")["quantity"].sum().idxmax()
    top_provider = food.groupby("provider_type")["quantity"].sum().idxmax() if "provider_type" in food.columns else "N/A"
    st.info(f"""
    • Highest food category: **{top_food}**
    • Largest provider type: **{top_provider}**
    • Total listings: **{len(food):,}**
    • Total claims: **{len(claims):,}**
    """)

# =============================================
# PAGE: BROWSE FOOD
# =============================================

def show_browse_food():
    page_header("🔍 Browse Available Food", "Search and explore available food listings.")

    food_df = run_query("""
        SELECT f.food_id, f.food_name, f.quantity, f.expiry_date,
               f.location, f.food_type, f.meal_type,
               p.provider_id, p.name AS provider_name,
               p.type AS provider_type, p.address, p.city, p.contact
        FROM food_listings f
        INNER JOIN providers p ON f.provider_id = p.provider_id
    """)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        loc = st.selectbox("Location", ["All"] + sorted(food_df["location"].dropna().unique().tolist()))
    with col2:
        ft  = st.selectbox("Food Type", ["All"] + sorted(food_df["food_type"].dropna().unique().tolist()))
    with col3:
        mt  = st.selectbox("Meal Type", ["All"] + sorted(food_df["meal_type"].dropna().unique().tolist()))
    with col4:
        pv  = st.selectbox("Provider", ["All"] + sorted(food_df["provider_name"].dropna().unique().tolist()))

    df = food_df.copy()
    if loc != "All": df = df[df["location"]      == loc]
    if ft  != "All": df = df[df["food_type"]     == ft]
    if mt  != "All": df = df[df["meal_type"]     == mt]
    if pv  != "All": df = df[df["provider_name"] == pv]

    st.success(f"Found **{len(df)}** listings — Total Quantity: **{df['quantity'].sum()}**")
    st.dataframe(df[["food_id","food_name","quantity","food_type","meal_type",
                      "location","provider_name","contact"]],
                 use_container_width=True, hide_index=True)

    if len(df) > 0:
        st.divider()
        st.subheader("📦 Food & Provider Details")
        opts = {f"{r.food_id} - {r.food_name}": r.food_id for _, r in df.iterrows()}
        sel  = st.selectbox("Select Food Item", list(opts.keys()))
        d    = df[df["food_id"] == opts[sel]].iloc[0]
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"""
**🍽️ Food Information**

**Name:** {d['food_name']}
**Quantity:** {d['quantity']}
**Food Type:** {d['food_type']}
**Meal Type:** {d['meal_type']}
**Expiry Date:** {d['expiry_date']}
""")
        with c2:
            st.success(f"""
**🏢 Provider Information**

**Provider:** {d['provider_name']}
**Type:** {d['provider_type']}
**City:** {d['city']}
**Contact:** {d['contact']}
**Address:** {d['address']}
""")

# =============================================
# PAGE: FOOD LISTINGS
# =============================================

def show_food_listings():
    page_header("🍱 Food Listings Management", "Add, edit or remove food listings.")

    tab1,tab2,tab3,tab4 = st.tabs(["📖 All Listings","➕ Add","✏️ Edit","🗑 Delete"])

    with tab1:
        df = run_query("SELECT * FROM food_listings ORDER BY food_id")
        st.metric("Total Listings", len(df))
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        providers_df     = run_query("SELECT provider_id, name FROM providers ORDER BY name")
        provider_options = {f"#{r.provider_id} — {r.name}": r.provider_id
                            for _, r in providers_df.iterrows()}
        with st.form("add_food_form"):
            food_name   = st.text_input("Food Name")
            quantity    = st.number_input("Quantity", min_value=1, value=10)
            expiry_date = st.date_input("Expiry Date")
            provider    = st.selectbox("Provider", list(provider_options.keys()))
            location    = st.text_input("Location (City)")
            food_type   = st.selectbox("Food Type", ["Vegetarian","Non-Vegetarian","Vegan"])
            meal_type   = st.selectbox("Meal Type", ["Breakfast","Lunch","Dinner","Snacks"])
            submit      = st.form_submit_button("➕ Add Listing")
        if submit:
            run_write("""INSERT INTO food_listings
                (food_name,quantity,expiry_date,provider_id,location,food_type,meal_type)
                VALUES (?,?,?,?,?,?,?)""",
                (food_name, quantity, str(expiry_date),
                 provider_options[provider], location, food_type, meal_type))
            st.success("Food Listing Added!")
            st.rerun()

    with tab3:
        listings_df      = run_query("SELECT * FROM food_listings ORDER BY food_id")
        providers_df     = run_query("SELECT provider_id, name FROM providers ORDER BY name")
        listing_options  = {f"#{r.food_id} — {r.food_name}": r.food_id for _, r in listings_df.iterrows()}
        provider_options = {f"#{r.provider_id} — {r.name}": r.provider_id for _, r in providers_df.iterrows()}

        sel = st.selectbox("Select listing to edit", list(listing_options.keys()))
        sid = listing_options[sel]
        row = listings_df[listings_df["food_id"] == sid].iloc[0]

        p_keys  = list(provider_options.keys())
        p_idx   = next((i for i,k in enumerate(p_keys) if provider_options[k]==row["provider_id"]), 0)
        ft_list = ["Vegetarian","Non-Vegetarian","Vegan"]
        mt_list = ["Breakfast","Lunch","Dinner","Snacks"]

        with st.form("edit_food_form"):
            food_name   = st.text_input("Food Name", value=row["food_name"])
            quantity    = st.number_input("Quantity", min_value=1, value=int(row["quantity"]))
            expiry_date = st.date_input("Expiry Date", value=pd.to_datetime(row["expiry_date"]))
            provider    = st.selectbox("Provider", p_keys, index=p_idx)
            location    = st.text_input("Location", value=row["location"])
            food_type   = st.selectbox("Food Type", ft_list,
                                       index=ft_list.index(row["food_type"]) if row["food_type"] in ft_list else 0)
            meal_type   = st.selectbox("Meal Type", mt_list,
                                       index=mt_list.index(row["meal_type"]) if row["meal_type"] in mt_list else 0)
            update      = st.form_submit_button("💾 Save Changes")
        if update:
            run_write("""UPDATE food_listings
                SET food_name=?,quantity=?,expiry_date=?,provider_id=?,
                    location=?,food_type=?,meal_type=?
                WHERE food_id=?""",
                (food_name, quantity, str(expiry_date), provider_options[provider],
                 location, food_type, meal_type, sid))
            st.success("Food Listing Updated!")
            st.rerun()

    with tab4:
        listings_df     = run_query("SELECT * FROM food_listings ORDER BY food_id")
        listing_options = {f"#{r.food_id} — {r.food_name}": r.food_id for _, r in listings_df.iterrows()}
        sel       = st.selectbox("Select listing to delete", list(listing_options.keys()))
        delete_id = listing_options[sel]
        st.warning("This action cannot be undone.")
        if st.button("🗑 Delete Listing", use_container_width=True):
            run_write("DELETE FROM food_listings WHERE food_id=?", (delete_id,))
            st.success("Deleted!")
            st.rerun()

# =============================================
# PAGE: CLAIMS
# =============================================

def show_claims():
    page_header("📋 Claims Center", "Manage food claims, update statuses and track distribution.")

    tab1,tab2,tab3,tab4 = st.tabs(["📖 All Claims","➕ Add Claim","✏️ Update Status","🗑 Delete"])

    with tab1:
        claims_df = run_query("""
            SELECT c.claim_id, f.food_name, r.name AS receiver_name, c.status, c.timestamp
            FROM claims c
            JOIN food_listings f ON c.food_id=f.food_id
            JOIN receivers r ON c.receiver_id=r.receiver_id
            ORDER BY c.claim_id DESC
        """)
        sf = st.selectbox("Filter by Status", ["All","Pending","Completed","Cancelled"])
        df = claims_df if sf=="All" else claims_df[claims_df["status"]==sf]
        st.metric("Total Claims", len(df))
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        food_df     = run_query("SELECT food_id, food_name FROM food_listings ORDER BY food_name")
        receiver_df = run_query("SELECT receiver_id, name FROM receivers ORDER BY name")
        food_opts   = {f"#{r.food_id} — {r.food_name}": r.food_id for _, r in food_df.iterrows()}
        recv_opts   = {f"#{r.receiver_id} — {r.name}": r.receiver_id for _, r in receiver_df.iterrows()}

        with st.form("add_claim_form"):
            sel_food = st.selectbox("Food Item", list(food_opts.keys()))
            sel_recv = st.selectbox("Receiver",  list(recv_opts.keys()))
            status   = st.selectbox("Status", ["Pending","Completed","Cancelled"])
            add      = st.form_submit_button("➕ Add Claim")
        if add:
            run_write("INSERT INTO claims (food_id,receiver_id,status,timestamp) VALUES (?,?,?,?)",
                      (food_opts[sel_food], recv_opts[sel_recv], status,
                       datetime.now().strftime("%Y-%m-%d %H:%M")))
            st.success("Claim Added!")
            st.rerun()

    with tab3:
        claims_df  = run_query("""
            SELECT c.claim_id, f.food_name, r.name AS receiver_name, c.status
            FROM claims c
            JOIN food_listings f ON c.food_id=f.food_id
            JOIN receivers r ON c.receiver_id=r.receiver_id
            ORDER BY c.claim_id DESC
        """)
        claim_opts  = {f"#{r.claim_id} — {r.food_name} → {r.receiver_name}": r.claim_id
                       for _, r in claims_df.iterrows()}
        sel         = st.selectbox("Select Claim", list(claim_opts.keys()))
        cid         = claim_opts[sel]
        row         = claims_df[claims_df["claim_id"]==cid].iloc[0]
        status_list = ["Pending","Completed","Cancelled"]
        cur_idx     = status_list.index(row["status"]) if row["status"] in status_list else 0

        with st.form("update_claim_form"):
            st.text_input("Food Item", value=row["food_name"],     disabled=True)
            st.text_input("Receiver",  value=row["receiver_name"], disabled=True)
            status = st.selectbox("Status", status_list, index=cur_idx)
            upd    = st.form_submit_button("💾 Save Changes")
        if upd:
            run_write("UPDATE claims SET status=? WHERE claim_id=?", (status, cid))
            st.success("Claim Updated!")
            st.rerun()

    with tab4:
        claims_df  = run_query("""
            SELECT c.claim_id, f.food_name, r.name AS receiver_name
            FROM claims c
            JOIN food_listings f ON c.food_id=f.food_id
            JOIN receivers r ON c.receiver_id=r.receiver_id
            ORDER BY c.claim_id DESC
        """)
        claim_opts = {f"#{r.claim_id} — {r.food_name} → {r.receiver_name}": r.claim_id
                      for _, r in claims_df.iterrows()}
        sel       = st.selectbox("Select Claim To Delete", list(claim_opts.keys()))
        delete_id = claim_opts[sel]
        st.warning("This action cannot be undone.")
        if st.button("🗑 Delete Claim", use_container_width=True):
            run_write("DELETE FROM claims WHERE claim_id=?", (delete_id,))
            st.success("Deleted!")
            st.rerun()

# =============================================
# PAGE: PROVIDERS
# =============================================

def show_providers():
    page_header("🏢 Providers Directory", "Manage food providers and donation partners.")

    providers_df = run_query("SELECT * FROM providers ORDER BY name")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Providers", len(providers_df))
    c2.metric("Restaurants",    len(providers_df[providers_df["type"]=="Restaurant"]))
    c3.metric("Grocery Stores", len(providers_df[providers_df["type"]=="Grocery Store"]))
    c4.metric("Supermarkets",   len(providers_df[providers_df["type"]=="Supermarket"]))

    st.divider()
    tab1,tab2,tab3,tab4 = st.tabs(["📖 Directory","➕ Add","✏️ Edit","🗑 Delete"])

    with tab1:
        col1,col2,col3 = st.columns(3)
        city_f = col1.selectbox("City", ["All"]+sorted(providers_df["city"].dropna().unique().tolist()))
        type_f = col2.selectbox("Type", ["All"]+sorted(providers_df["type"].dropna().unique().tolist()))
        search = col3.text_input("Search Provider")
        df = providers_df.copy()
        if city_f != "All": df = df[df["city"]==city_f]
        if type_f != "All": df = df[df["type"]==type_f]
        if search:          df = df[df["name"].str.contains(search, case=False, na=False)]
        st.metric("Providers Found", len(df))
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("add_provider"):
            name   = st.text_input("Provider Name")
            ptype  = st.selectbox("Type", ["Restaurant","Grocery Store","Supermarket","Catering Service"])
            addr   = st.text_area("Address")
            city   = st.text_input("City")
            cont   = st.text_input("Contact")
            submit = st.form_submit_button("Add Provider")
        if submit:
            run_write("INSERT INTO providers (name,type,address,city,contact) VALUES (?,?,?,?,?)",
                      (name, ptype, addr, city, cont))
            st.success("Provider Added!")
            st.rerun()

    with tab3:
        providers_df = run_query("SELECT * FROM providers ORDER BY name")
        prov_opts    = {f"#{r.provider_id} — {r.name}": r.provider_id for _, r in providers_df.iterrows()}
        sel          = st.selectbox("Select Provider", list(prov_opts.keys()))
        pid          = prov_opts[sel]
        row          = providers_df[providers_df["provider_id"]==pid].iloc[0]
        p_types      = ["Restaurant","Grocery Store","Supermarket","Catering Service"]

        with st.form("edit_provider"):
            name   = st.text_input("Name",    value=row["name"])
            ptype  = st.selectbox("Type", p_types,
                                  index=p_types.index(row["type"]) if row["type"] in p_types else 0)
            addr   = st.text_area("Address",  value=row["address"])
            city   = st.text_input("City",    value=row["city"])
            cont   = st.text_input("Contact", value=row["contact"])
            upd    = st.form_submit_button("Save Changes")
        if upd:
            run_write("UPDATE providers SET name=?,type=?,address=?,city=?,contact=? WHERE provider_id=?",
                      (name, ptype, addr, city, cont, pid))
            st.success("Provider Updated!")
            st.rerun()

    with tab4:
        providers_df = run_query("SELECT * FROM providers ORDER BY name")
        prov_opts    = {f"#{r.provider_id} — {r.name}": r.provider_id for _, r in providers_df.iterrows()}
        sel          = st.selectbox("Select Provider To Delete", list(prov_opts.keys()))
        delete_id    = prov_opts[sel]
        st.warning("This action cannot be undone.")
        if st.button("🗑 Delete Provider", use_container_width=True):
            try:
                run_write("DELETE FROM providers WHERE provider_id=?", (delete_id,))
                st.success("Deleted!")
                st.rerun()
            except Exception:
                st.error("Provider has linked food listings. Delete those first.")

# =============================================
# PAGE: RECEIVERS
# =============================================

def show_receivers():
    page_header("👥 Receivers Directory", "Manage NGOs, Shelters and Individuals receiving food.")

    receivers_df = run_query("SELECT * FROM receivers ORDER BY name")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Receivers", len(receivers_df))
    c2.metric("NGOs",        len(receivers_df[receivers_df["type"]=="NGO"]))
    c3.metric("Shelters",    len(receivers_df[receivers_df["type"]=="Shelter"]))
    c4.metric("Individuals", len(receivers_df[receivers_df["type"]=="Individual"]))

    st.divider()
    tab1,tab2,tab3,tab4 = st.tabs(["📖 Directory","➕ Add","✏️ Edit","🗑 Delete"])

    with tab1:
        col1,col2,col3 = st.columns(3)
        city_f = col1.selectbox("City", ["All"]+sorted(receivers_df["city"].dropna().unique().tolist()))
        type_f = col2.selectbox("Type", ["All"]+sorted(receivers_df["type"].dropna().unique().tolist()))
        search = col3.text_input("Search Receiver")
        df = receivers_df.copy()
        if city_f != "All": df = df[df["city"]==city_f]
        if type_f != "All": df = df[df["type"]==type_f]
        if search:          df = df[df["name"].str.contains(search, case=False, na=False)]
        st.metric("Receivers Found", len(df))
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("add_receiver"):
            name   = st.text_input("Receiver Name")
            rtype  = st.selectbox("Type", ["NGO","Shelter","Individual"])
            city   = st.text_input("City")
            cont   = st.text_input("Contact")
            submit = st.form_submit_button("Add Receiver")
        if submit:
            run_write("INSERT INTO receivers (name,type,city,contact) VALUES (?,?,?,?)",
                      (name, rtype, city, cont))
            st.success("Receiver Added!")
            st.rerun()

    with tab3:
        receivers_df = run_query("SELECT * FROM receivers ORDER BY name")
        recv_opts    = {f"#{r.receiver_id} — {r.name}": r.receiver_id for _, r in receivers_df.iterrows()}
        sel          = st.selectbox("Select Receiver", list(recv_opts.keys()))
        rid          = recv_opts[sel]
        row          = receivers_df[receivers_df["receiver_id"]==rid].iloc[0]
        r_types      = ["NGO","Shelter","Individual"]

        with st.form("edit_receiver"):
            name   = st.text_input("Name",    value=row["name"])
            rtype  = st.selectbox("Type", r_types,
                                  index=r_types.index(row["type"]) if row["type"] in r_types else 0)
            city   = st.text_input("City",    value=row["city"])
            cont   = st.text_input("Contact", value=row["contact"])
            upd    = st.form_submit_button("Save Changes")
        if upd:
            run_write("UPDATE receivers SET name=?,type=?,city=?,contact=? WHERE receiver_id=?",
                      (name, rtype, city, cont, rid))
            st.success("Receiver Updated!")
            st.rerun()

    with tab4:
        receivers_df = run_query("SELECT * FROM receivers ORDER BY name")
        recv_opts    = {f"#{r.receiver_id} — {r.name}": r.receiver_id for _, r in receivers_df.iterrows()}
        sel          = st.selectbox("Select Receiver To Delete", list(recv_opts.keys()))
        delete_id    = recv_opts[sel]
        st.warning("This action cannot be undone.")
        if st.button("🗑 Delete Receiver", use_container_width=True):
            try:
                run_write("DELETE FROM receivers WHERE receiver_id=?", (delete_id,))
                st.success("Deleted!")
                st.rerun()
            except Exception:
                st.error("Receiver has linked claims. Delete claims first.")

# =============================================
# PAGE: ANALYTICS
# =============================================

def show_analytics():
    page_header("📈 Analytics & Insights", "Business insights for food distribution, providers, claims and receivers.")

    food_df      = run_query("SELECT * FROM food_listings")
    claims_df    = run_query("SELECT * FROM claims")
    providers_df = run_query("SELECT * FROM providers")
    receivers_df = run_query("SELECT * FROM receivers")

    total_claims = len(claims_df)
    completed    = len(claims_df[claims_df["status"]=="Completed"])
    success_rate = round(completed/total_claims*100, 2) if total_claims > 0 else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🍱 Food Listings",  f"{len(food_df):,}")
    c2.metric("📦 Total Quantity", f"{int(food_df['quantity'].sum()):,}")
    c3.metric("📋 Total Claims",   f"{total_claims:,}")
    c4.metric("✅ Success %",      f"{success_rate}%")

    st.divider()

    st.subheader("🍱 Food Insights")
    col1,col2 = st.columns(2)
    with col1:
        df  = food_df.groupby("food_type").size().reset_index(name="count")
        fig = px.pie(df, names="food_type", values="count", title="Food Type Distribution",
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(chart_layout(fig), use_container_width=True)
    with col2:
        df  = food_df.groupby("meal_type").size().reset_index(name="count")
        fig = px.bar(df, x="meal_type", y="count", title="Meal Type Distribution",
                     color_discrete_sequence=["#52e09c"])
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.subheader("🏢 Provider Insights")
    prov_qty  = run_query("""
        SELECT p.name, SUM(f.quantity) AS TotalQuantity
        FROM food_listings f JOIN providers p ON f.provider_id=p.provider_id
        GROUP BY p.name ORDER BY TotalQuantity DESC LIMIT 10
    """)
    prov_type = run_query("""
        SELECT p.type, SUM(f.quantity) AS TotalQuantity
        FROM food_listings f JOIN providers p ON f.provider_id=p.provider_id
        GROUP BY p.type
    """)
    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(prov_qty, x="name", y="TotalQuantity", title="Top Providers by Quantity",
                     color_discrete_sequence=["#52e09c"])
        st.plotly_chart(chart_layout(fig), use_container_width=True)
    with col2:
        fig = px.pie(prov_type, names="type", values="TotalQuantity", title="Provider Type Contribution",
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.subheader("🤝 Claims Insights")
    claim_status = run_query("SELECT status, COUNT(*) AS TotalClaims FROM claims GROUP BY status")
    claim_date   = run_query("""
        SELECT DATE(timestamp) AS ClaimDate, COUNT(*) AS TotalClaims
        FROM claims GROUP BY DATE(timestamp) ORDER BY ClaimDate
    """)
    col1,col2 = st.columns(2)
    with col1:
        fig = px.pie(claim_status, names="status", values="TotalClaims", hole=0.5,
                     title="Claim Status Breakdown",
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(chart_layout(fig), use_container_width=True)
    with col2:
        fig = px.line(claim_date, x="ClaimDate", y="TotalClaims", markers=True,
                      title="Claims Over Time", color_discrete_sequence=["#52e09c"])
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.subheader("👥 Receiver Insights")
    recv_top  = run_query("""
        SELECT r.name, COUNT(*) AS ClaimsReceived
        FROM claims c JOIN receivers r ON c.receiver_id=r.receiver_id
        GROUP BY r.name ORDER BY ClaimsReceived DESC LIMIT 10
    """)
    recv_type = run_query("SELECT type, COUNT(*) AS TotalReceivers FROM receivers GROUP BY type")
    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(recv_top, x="name", y="ClaimsReceived", title="Top Receivers",
                     color_discrete_sequence=["#52e09c"])
        st.plotly_chart(chart_layout(fig), use_container_width=True)
    with col2:
        fig = px.pie(recv_type, names="type", values="TotalReceivers",
                     title="Receiver Type Distribution",
                     color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.divider()
    st.subheader("📊 Database Summary")
    st.dataframe(pd.DataFrame({
        "Table":   ["Food Listings","Providers","Receivers","Claims"],
        "Records": [len(food_df), len(providers_df), len(receivers_df), len(claims_df)]
    }), use_container_width=True, hide_index=True)

# =============================================
# PAGE: SQL INSIGHTS
# =============================================

def show_sql_insights():
    page_header("🧠 SQL Insights & Trends", "Run SQL business queries directly against the database.")

    queries = {
        "Food Providers & Receivers": {
            "Q1. How many food providers and receivers are there in each city?": """
                SELECT p.city, COUNT(DISTINCT p.provider_id) AS Providers,
                       COUNT(DISTINCT r.receiver_id) AS Receivers
                FROM providers p LEFT JOIN receivers r ON p.city=r.city
                GROUP BY p.city ORDER BY p.city""",
            "Q2. Provider Type Contributing Most Food": """
                SELECT provider_type, SUM(quantity) AS total_food
                FROM food_listings GROUP BY provider_type ORDER BY total_food DESC""",
            "Q3. Most Claimed Food Items": """
                SELECT f.food_name, COUNT(c.claim_id) AS total_claims
                FROM food_listings f JOIN claims c ON f.food_id=c.food_id
                GROUP BY f.food_name ORDER BY total_claims DESC LIMIT 10""",
        },
        "Food Listings": {
            "Q4. Which City Has The Highest Food Demand": """
                SELECT r.city, COUNT(c.claim_id) AS total_claims
                FROM receivers r JOIN claims c ON r.receiver_id=c.receiver_id
                GROUP BY r.city ORDER BY total_claims DESC LIMIT 10""",
            "Q5. Food Type Most In Demand": """
                SELECT f.food_type, COUNT(c.claim_id) AS total_claims
                FROM food_listings f JOIN claims c ON f.food_id=c.food_id
                GROUP BY f.food_type ORDER BY total_claims DESC""",
            "Q6. Meal Type Most In Demand": """
                SELECT f.meal_type, COUNT(c.claim_id) AS total_claims
                FROM food_listings f JOIN claims c ON f.food_id=c.food_id
                GROUP BY f.meal_type ORDER BY total_claims DESC""",
        },
        "Claims Analysis": {
            "Q7. Claim Status Percentage": """
                SELECT status,
                       ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM claims),2) AS percentage
                FROM claims GROUP BY status""",
            "Q8. Claim Status Distribution": """
                SELECT status, COUNT(*) AS total_claims FROM claims GROUP BY status""",
        },
        "Business Intelligence": {
            "Q9. Top 10 Providers By Quantity": """
                SELECT p.name, SUM(f.quantity) AS total_quantity
                FROM food_listings f JOIN providers p ON f.provider_id=p.provider_id
                GROUP BY p.name ORDER BY total_quantity DESC LIMIT 10""",
            "Q10. Top 10 Receivers By Claims": """
                SELECT r.name, COUNT(c.claim_id) AS total_claims
                FROM receivers r JOIN claims c ON r.receiver_id=c.receiver_id
                GROUP BY r.name ORDER BY total_claims DESC LIMIT 10""",
        }
    }

    section = st.selectbox("Select Section", list(queries.keys()))
    for i, (question, sql) in enumerate(queries[section].items()):
        with st.expander(question):
            st.code(sql.strip(), language="sql")
            if st.button("▶ Run Query", key=f"q_{i}"):
                try:
                    df = run_query(sql)
                    st.success(f"{len(df)} rows returned")
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(str(e))

    st.divider()
    st.subheader("🎯 Project Conclusion")
    st.success("""
    The Food Waste Management System demonstrates how data analytics and operational management
    can work together to reduce food waste and improve food redistribution efficiency.

    By combining SQLite, Python, Streamlit, and business intelligence techniques,
    the platform enables providers, receivers, and administrators to make informed decisions
    and maximize social impact.
    """)

# =============================================
# ROUTER
# =============================================

if   page == "Home":          show_home()
elif page == "Dashboard":     show_dashboard()
elif page == "Browse Food":   show_browse_food()
elif page == "Food Listings": show_food_listings()
elif page == "Claims":        show_claims()
elif page == "Providers":     show_providers()
elif page == "Receivers":     show_receivers()
elif page == "Analytics":     show_analytics()
elif page == "SQL Insights":  show_sql_insights()
