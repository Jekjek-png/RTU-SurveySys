import streamlit as st 

def show_dashboard():
    st.markdown("<h1 style='color:#003366;'>Hello,</h1>", unsafe_allow_html=True)


    if st.session_state.get("role") == "Student":
        st.markdown("<h2 style='color:#003366;'>MGA BATA</h2>", unsafe_allow_html=True)
        if st.button("📝 Start New Survey", use_container_width=True):
            switch_page('survey')
    else:
        dept = st.session_state.get("department", "General")
        st.markdown(f"<h2 style='color:#003366;'>Department: {dept}</h2>", unsafe_allow_html=True)
        st.write("### Top Concerns in Your Department")
        concerns = {
            "Clinic": ["Long waiting times", "Medicine stock shortages", "Need for more doctors"],
            "Accounting": ["Delayed payment processing", "System errors in verification"],
            "MISU": ["Password reset delays", "System downtime issues"]
        }
        for issue in concerns.get(dept, ["No concerns reported"]):
            st.markdown(f"- {issue}")


    st.divider()
    st.write("### Overall Satisfaction Rating")
    st.title("246 Evaluated")
    st.metric(label="Positive Feedback", value="85%", delta="3% vs last month")
    st.progress(0.85)


    st.write("---")
    st.write("### Recent Transactions")
    logs = [
        ("Clinic", "Medical Consultation", "⭐⭐⭐⭐⭐"),
        ("Accounting", "Payment Verification", "⭐⭐⭐⭐"),
        ("MISU", "Password Reset", "⭐⭐⭐⭐⭐")
    ]
    for office, task, stars in logs:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{office}**\n\n*{task}*")
        c2.write(stars)
        st.divider()


    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.page = "login"
        st.session_state.role = None
        st.session_state.department = None

