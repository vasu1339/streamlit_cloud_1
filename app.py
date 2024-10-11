import streamlit as st
import pandas as pd
import joblib

# Load the saved model
model = joblib.load('loan_approval_model.pkl')

# Function to display the home page
def show_home_page():
    st.title("Loan Eligibility Prediction")
    
    # Add an appropriate image for the home page (replace "home_image.jpg" with your image)
    st.image("1.png", caption="Loan Approval Process", use_column_width=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Eligibility Criteria"):
            st.session_state.page = 'criteria'

    with col2:
        if st.button("Quick Eligibility Check"):
            st.session_state.page = 'check'

    with col3:
        if st.button("Instructions"):
            st.session_state.page = 'rules'



    
    
    # Importance of eligibility system description
    st.markdown("""
    ### Importance of Eligibility System:
    The loan eligibility system is crucial to ensure that individuals understand their financial capabilities and responsibilities before applying for a loan. It helps them avoid rejection and make informed decisions.
    """)

# Function for displaying loan eligibility criteria
def show_eligibility_criteria_page():
    st.title("Eligibility Criteria for Different Loans")

    # Home Loan Section
    st.header("🏠 Home Loan Eligibility Criteria")
    st.image("2.jpg", caption="Home Loan", use_column_width=True)
    st.markdown("""
    - **Age**
    - **Credit score**
    - **Financial liabilities**
    - **Current financial position**

    Tips to increase your eligibility:
    - Add an earning family member as a co-applicant
    - Present income flow with regular savings
    - Invest regularly
    - Present details of additional variable income
    """)

    # Car Loan Section
    st.header("🚗 Car Loan Eligibility Criteria")
    st.image("3.jpg", caption="Car Loan", use_column_width=True)
    st.markdown("""
    - **Age**
    - **Work experience**
    - **For self-employed individuals**: Duration of business
    - **Earnings**
    - **Make & model of the car**
    
    Tips to increase eligibility:
    - Pay your debts on time
    - Work on improving your credit score
    """)

    # Personal Loan Section
    st.header("💼 Personal Loan Eligibility Criteria")
    st.image("6.png", caption="Personal Loan", use_column_width=True)
    st.markdown("""
    - **Employment type**
    - **Income tax returns**
    - **Income requirements based on geography**
    - **Work experience**

    Tips to increase eligibility:
    - Clear all your debts
    - Improve your credit score
    """)

    # Education Loan Section
    st.header("🎓 Education Loan Eligibility Criteria")
    st.image("5.jpg", caption="Education Loan", use_column_width=True)
    st.markdown("""
    - **Admission confirmation from a recognized institute**
    - **Age**: 18 to 35
    - **Co-applicant** required for full-time students
    
    Tips to increase eligibility:
    - Good marks in the entrance exam
    - Good academic record
    """)

    if st.button("Go to Home"):
        st.session_state.page = 'home'

# Function for quick eligibility check
def show_quick_check_page():
    st.title("Quick Loan Eligibility Check")

    st.markdown("### Applicant Information")
    gender = st.selectbox('Gender', ['Male', 'Female'], index=0)
    married = st.selectbox('Married?', ['Yes', 'No'], index=0)
    dependents = st.slider('Number of Dependents', 0, 3)

    st.markdown("### Financial Information")
    education = st.selectbox('Education Level', ['Graduate', 'Not Graduate'], index=0)
    self_employed = st.selectbox('Self-Employed?', ['Yes', 'No'], index=0)
    applicant_income = st.number_input('Applicant Income (₹)', min_value=0, max_value=10000000, step=50000, value=500000)
    coapplicant_income = st.number_input('Coapplicant Income (₹)', min_value=0, max_value=10000000, step=50000, value=100000)
    loan_amount = st.number_input('Loan Amount (₹)', min_value=0, max_value=10000000, step=50000, value=500000)
    loan_amount_term = st.slider('Loan Amount Term (in months)', min_value=12, max_value=480, step=12, value=360)

    credit_history = st.selectbox('Credit History', ['No History (0)', 'Good History (1)'], index=1)

    st.markdown("### Property and Assets Information")
    property_area = st.selectbox('Property Area', ['Urban', 'Semiurban', 'Rural'], index=0)
    assets = st.number_input('Total Assets Value (₹)', min_value=0, max_value=100000000, step=100000, value=1000000)

    # Convert categorical variables for prediction
    gender = 1 if gender == 'Male' else 0
    married = 1 if married == 'Yes' else 0
    education = 0 if education == 'Graduate' else 1
    self_employed = 1 if self_employed == 'Yes' else 0
    credit_history = 1 if credit_history == 'Good History (1)' else 0
    property_area = 2 if property_area == 'Urban' else 1 if property_area == 'Semiurban' else 0

    # Prediction
    if st.button("Predict Loan Approval"):
        input_data = pd.DataFrame([[gender, married, dependents, education, self_employed, applicant_income, coapplicant_income,
                                     loan_amount, loan_amount_term, credit_history, property_area, assets]],
                                   columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome',
                                            'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 
                                            'Property_Area', 'Assets'])

        prediction = model.predict(input_data)
        
        # Display result
        if prediction[0] == 1:
            st.markdown(f"<h3 style='color: green;'>Loan is Approved!</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h3 style='color: red;'>Loan is Rejected.</h3>", unsafe_allow_html=True)

    if st.button("Go to Home"):
        st.session_state.page = 'home'

# Function for displaying rules
def show_rules_page():
    st.title("Rules for Using the Quick Eligibility Check")
    st.markdown("""
    ### Please follow these guidelines to ensure accurate results:
    - Ensure all financial details are accurate and up to date.
    - Only enter numeric values for income, loan amount, and assets.
    - The eligibility check is based on common parameters; always consult with a lender for specific cases.
    - Your credit score plays a crucial role in the prediction. Make sure your credit history details are correct.
    """)

    if st.button("Go to Home"):
        st.session_state.page = 'home'

# Main application logic
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Routing to different pages
if st.session_state.page == 'home':
    show_home_page()
elif st.session_state.page == 'criteria':
    show_eligibility_criteria_page()
elif st.session_state.page == 'check':
    show_quick_check_page()
elif st.session_state.page == 'rules':
    show_rules_page()
