import streamlit as st

# --- Helper for navigation ---
def switch_page(page_name):
    st.session_state.page = page_name

# --- Login Page ---
def show_login():
    st.header("Login Page")
    st.text_input("Username")
    st.text_input("Password", type="password")
    if st.button("Login"):
        switch_page("dashboard")
    st.button("Go to Signup", on_click=switch_page, args=("signup",))

# --- Signup Page ---
def show_signup():
    st.header("Signup Page")
    st.text_input("New Username")
    st.text_input("New Password", type="password")
    if st.button("Create Account"):
        switch_page("login")

# --- Dashboard Page ---
def show_dashboard():
    st.header("Dashboard")
    st.button("Take Survey", on_click=switch_page, args=("survey",))

# --- Survey Page (your existing code) ---
def show_survey():
    st.button("⬅️ Back to Dashboard", on_click=switch_page, args=('dashboard',))
    st.header("Service Satisfaction Survey")
    st.info("Your feedback helps us improve our services.")
    # keep your survey form code here ...


# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "login"   # default start page

# --- Navigation Logic ---
if st.session_state.page == 'login':
    show_login()
elif st.session_state.page == 'signup':
    show_signup()
elif st.session_state.page == 'dashboard':
    show_dashboard()
elif st.session_state.page == 'survey':
    show_survey()
