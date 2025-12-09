import streamlit as st
import pandas as pd
import pickle as pk


model = pk.load(open('model.pkl','rb'))
scaler = pk.load(open('scaler.pkl','rb'))


st.set_page_config(
    page_title="Loan Approval Prediction App",
    page_icon="🏦",
    layout="centered"
)


st.markdown("""
    <style>
    /* Background Gradient */
    body {
        background: linear-gradient(135deg, #e0f7fa, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Title Styling */
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: 800;
        color: #2c3e50;
        animation: fadeInDown 1.2s ease;
    }

    /* Input Fields Blue Glow */
    .stSlider, .stSelectbox, .stTextInput, .stNumberInput {
        border: 2px solid transparent;
        border-radius: 12px;
        padding: 5px;
        transition: all 0.4s ease;
    }
    .stSlider:hover, .stSelectbox:hover, .stTextInput:hover, .stNumberInput:hover {
        border: 2px solid #3498db;
        box-shadow: 0 0 12px #3498db;
        animation: glowBorder 1.5s infinite alternate;
    }
    .stSlider:focus, .stSelectbox:focus, .stTextInput:focus, .stNumberInput:focus {
        border: 2px solid #2980b9;
        box-shadow: 0 0 15px #2980b9;
    }

    @keyframes glowBorder {
        0% { box-shadow: 0 0 5px #3498db; }
        50% { box-shadow: 0 0 15px #2980b9; }
        100% { box-shadow: 0 0 5px #3498db; }
    }

    /* Predict Button Styling */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #1abc9c, #16a085);
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
        animation: fadeInUp 1s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #16a085, #1abc9c);
        transform: scale(1.05);
    }

    /* Prediction Result */
    .approved {
        color: #27ae60;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        animation: pulse 1.5s infinite;
    }
    .rejected {
        color: #e74c3c;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        animation: shake 0.8s infinite;
    }

    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        50% { transform: translateX(5px); }
        75% { transform: translateX(-5px); }
        100% { transform: translateX(0); }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🏦 Loan Approval Prediction App</h1>", unsafe_allow_html=True)

# ================== Inputs ==================
no_of_dep = st.slider('👨‍👩‍👧 Number of Dependents', 0, 5)
grad = st.selectbox('🎓 Education',['Graduated','Not Graduated'])
self_emp = st.selectbox('💼 Self Employed ?',['Yes','No'])
Annual_Income = st.slider('💰 Annual Income (₹)', 0, 10000000, step=50000)
Loan_Amount = st.slider('🏠 Loan Amount (₹)', 0, 10000000, step=50000)
Loan_Dur = st.slider('📅 Loan Duration (Years)', 0, 20)
Cibil = st.slider('📊 CIBIL Score', 0, 1000)
Total_assets = st.slider('🏦 Total Assets (₹)', 0, 10000000, step=50000)

# ================== Encoding ==================
grad_s = 0 if grad =='Graduated' else 1
emp_s = 0 if self_emp =='No' else 1

# ================== Prediction ==================
if st.button("🔮 Predict Loan Status"):
    pred_data = pd.DataFrame([[no_of_dep,grad_s,emp_s,Annual_Income,Loan_Amount,Loan_Dur,Cibil,Total_assets]],
                         columns=['no_of_dependents','education','self_employed','income_annum','loan_amount','loan_term','cibil_score','Total_assets'])
    pred_data = scaler.transform(pred_data)
    predict = model.predict(pred_data)

    if predict[0] == 1:
        st.markdown("<p class='approved'>✅ Loan is Approved</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='rejected'>❌ Loan is Rejected</p>", unsafe_allow_html=True)
