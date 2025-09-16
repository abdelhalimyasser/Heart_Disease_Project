import streamlit as st
import joblib
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

# === Load Model ===
model = joblib.load("models/final_model.pkl")

st.title("Heart Disease Prediction App ❤️")

# === Input Form ===
st.header("Patient Information")
sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male", help="Select patient’s gender.")
cp = st.selectbox("Chest Pain Type (cp)", options=[0, 1, 2, 3], format_func=lambda x: ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"][x], help="Type of chest pain. Typical angina (0) is less risky; Atypical (1) and Non-anginal (2) are high risk.")
thalach = st.number_input("Maximum Heart Rate (thalach)", min_value=50, max_value=250, value=180, help="Max heart rate during stress test.")
exang = st.selectbox("Exercise Induced Angina (exang)", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes", help="Angina induced by exercise.")
oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
slope = st.selectbox("Slope of ST Segment (slope)", options=[0, 1, 2], format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x], help="Slope of ST segment during exercise.")
ca = st.selectbox("Number of Major Vessels (ca)", options=[0, 1, 2, 3, 4], help="Vessels colored by fluoroscopy.")
thal = st.selectbox("Thalassemia (thal)", options=[0, 1, 2, 3], format_func=lambda x: ["Not described", "Normal", "Reversible defect", "Fixed defect"][x], help="Thalassemia condition. Normal (1) or Fixed defect (3) are less risky; Reversible defect (2) is high risk.")

# Convert to array
input_data = np.array([[sex, cp, thalach, exang, oldpeak, slope, ca, thal]])

if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    result = "Patient is at risk of Heart Disease 💔" if prediction == 1 else "No Heart Disease detected ✅"

    st.subheader("Result:")
    st.write(result)
    st.write(f"Prediction Probability: {probability:.2f}")

    # === Generate PDF Report ===
    filename = f"heart_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Heart Disease Prediction Report")
    c.line(50, 747, 550, 747)
    c.drawString(50, 720, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 700, f"Sex: {sex}")
    c.drawString(50, 680, f"Chest Pain Type: {cp}")
    c.drawString(50, 660, f"Max Heart Rate (thalach): {thalach}")
    c.drawString(50, 640, f"Exercise Angina (exang): {exang}")
    c.drawString(50, 620, f"Oldpeak: {oldpeak}")
    c.drawString(50, 600, f"Slope: {slope}")
    c.drawString(50, 580, f"CA: {ca}")
    c.drawString(50, 560, f"Thal: {thal}")
    c.drawString(50, 530, f"Prediction: {result}")
    c.drawString(50, 510, f"Probability: {probability:.2f}")
    c.save()

    with open(filename, "rb") as f:
        st.download_button("📥 Download Report", f, file_name=filename, mime="application/pdf")
