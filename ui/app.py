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

sex = st.selectbox("Sex", [0, 1])  # 0 = Female, 1 = Male
cp = st.selectbox("Chest Pain Type (cp)", [0, 1, 2, 3])
thalach = st.number_input("Maximum Heart Rate Achieved (thalach)", min_value=50, max_value=250, value=150)
exang = st.selectbox("Exercise Induced Angina (exang)", [0, 1])
oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
slope = st.selectbox("Slope of Peak Exercise ST Segment (slope)", [0, 1, 2])
ca = st.selectbox("Number of Major Vessels (ca)", [0, 1, 2, 3])
thal = st.selectbox("Thalassemia (thal)", [0, 1, 2, 3])

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
