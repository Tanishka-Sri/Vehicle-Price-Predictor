import streamlit as st
import pandas as pd
import joblib
import base64

# Function to encode background image to base64
def get_base64_bg(file_path):
    with open(file_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"

# Inject background image using base64
def set_bg_image(image_path):
    bg_url = get_base64_bg(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .main {{
            background-color: rgba(0, 0, 0, 0.65);
            padding: 2rem;
            border-radius: 1rem;
        }}
        h1 {{
            color: yellow;
            text-align: center;
        }}
        label {{
            color: yellow !important;
        }}
        .stButton > button {{
            background-color: #1E90FF;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Load model
model = joblib.load("LinearRegressionModel.pkl")

# Set page config
st.set_page_config(page_title="AutoWorth", layout="centered")

# Set background
set_bg_image("background.jpg")

# App UI
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<h1>🚗 AutoWorth 🚗 </h1>', unsafe_allow_html=True)
st.markdown("<p style='color:white;'>Enter the car details below to predict the estimated price:</p>", unsafe_allow_html=True)

# Inputs
name = st.text_input("Car Name", value="Hyundai Santro")
company = st.text_input("Company", value="Hyundai")
year = st.number_input("Year of Manufacture", 1980, 2025, 2015)
kms_driven = st.number_input("Kilometers Driven", 0, 1000000, 50000)
fuel_type = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'CNG'])

# Prediction
if st.button("Predict Price"):
    try:
        input_df = pd.DataFrame({
            'name': [name],
            'company': [company],
            'year': [year],
            'kms_driven': [kms_driven],
            'fuel_type': [fuel_type]
        })
        prediction = model.predict(input_df)[0]
        st.success(f"Predicted Price: ₹ {prediction:,.2f}")
    except Exception as e:
        st.error(f"Prediction error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
