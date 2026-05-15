import streamlit as st 

# --- SURVEY PAGE ---
def show_survey():
    st.button("⬅️ Back to Dashboard", on_click=switch_page, args=('dashboard',))
    st.header("Service Satisfaction Survey")
    st.info("Your feedback helps us improve our services.")


    with st.form("survey_form"):
        st.subheader("I. Profile")
        col1, col2 = st.columns(2)
        with col1:
            service = st.selectbox("Service Availed", ["Clinic","Accounting","MISU","Library","Registrar"])
            name = st.text_input("Respondent Name")
            date_visit = st.date_input("Date Visited")
        with col2:
            gender = st.selectbox("Gender Upon Birth", ["Male","Female","Prefer not to say"])
            age = st.selectbox("Age Bracket", ["Below 18","18-30","31-45","46-60","60+"])
            category = st.selectbox("Category", ["Student","Faculty","Staff","Visitor"])


        st.divider()
        st.subheader("II. Citizen's Charter (CC)")
        cc1 = st.radio("CC1 Awareness", [
            "I know what a CC is and I saw this office's CC",
            "I know what a CC is but I did not see this office's CC",
            "I learned of the CC only when I saw this office's CC",
            "I do not know what a CC is and did not see one in this office"
        ])
        if "I do not know" in cc1:
            st.warning("Note: Answer N/A for CC2 and CC3.")
        cc2 = st.radio("CC2 Visibility", ["Easy to see","Somewhat easy","Difficult","Not visible","N/A"])
        cc3 = st.radio("CC3 Helpfulness", ["Helped very much","Somewhat helped","Did not help","N/A"])


        st.divider()
        st.subheader("III. Service Quality")
        questions = [
            "I am satisfied with the service that I availed",
            "I spent a reasonable amount of time for my transaction",
            "The office followed the requirements/steps provided",
            "The steps and payment were easy and simple",
            "I easily found information from the office/website",
            "I feel the office was fair to everyone",
            "I was treated courteously by the staff",
            "I got what I needed from the office"
        ]
        ratings = {}
        for q in questions:
            st.write(f"**{q}**")
            cols = st.columns(5)
            selected = None
            for i, col in enumerate(cols, start=1):
                if col.checkbox(str(i), key=f"{q}_{i}"):
                    selected = i
            ratings[q] = selected if selected else "No response"
            st.divider()


        st.write("**I paid a reasonable amount of fees**")
        cols_fee = st.columns(6)
        fee_options = [1,2,3,4,5,"N/A"]
        fee_selected = None
        for opt, col in zip(fee_options, cols_fee):
            if col.checkbox(str(opt), key=f"fee_{opt}"):
                fee_selected = opt
        fee_rating = fee_selected if fee_selected else "No response"


        st.divider()
        st.subheader("IV. Comments & Staff")
        comments = st.text_area("General Comments/Suggestions")
        employee = st.text_input("Attending Employee")
        emp_feedback = st.text_area("Comments for the employee")


        submitted = st.form_submit_button("Submit Survey")
        if submitted:
            st.success("Thank you! Your feedback has been recorded.")


# --- 4. NAVIGATION LOGIC ---
if st.session_state.page == 'login':
    show_login()
elif st.session_state.page == 'signup':
    show_signup()
elif st.session_state.page == 'dashboard':
    show_dashboard()
elif st.session_state.page == 'survey':
    show_survey()
