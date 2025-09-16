# import streamlit as st
# import joblib
# import numpy as np
# import pandas as pd
# import datetime
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from reportlab.platypus import Table, TableStyle

# # Set page config for better appearance
# st.set_page_config(page_title="Heart Disease Prediction", page_icon="❤️", layout="centered")

# # Custom CSS for improved styling
# st.markdown("""
#     <style>
#     .main { background-color: #f5f5f5; padding: 20px; border-radius: 10px; }
#     .stButton>button { background-color: #4CAF50; color: white; border-radius: 5px; }
#     .stTextInput>div>input { border-radius: 5px; }
#     .stSelectbox>div>div>select { border-radius: 5px; }
#     .stNumberInput>div>input { border-radius: 5px; }
#     .header { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 10px; }
#     .subheader { font-size: 18px; color: #555; margin-bottom: 15px; }
#     </style>
# """, unsafe_allow_html=True)

# # === Load Model ===
# model = joblib.load("models/final_model.pkl")

# # === Sidebar Instructions ===
# with st.sidebar:
#     st.header("Instructions")
#     st.markdown("""
#     1. Enter the patient's details in the form.
#     2. Click **Predict** to get the heart disease prediction.
#     3. Download the generated PDF report for a detailed summary.
#     **Note**: All fields are required, including the patient's name.
#     """)

# # === Main UI ===
# st.title("Heart Disease Prediction App ❤️")
# st.markdown('<div class="header">Enter Patient Information</div>', unsafe_allow_html=True)
# st.markdown('<div class="subheader">Provide the following details to predict heart disease risk.</div>', unsafe_allow_html=True)

# # Input form with columns for better layout
# col1, col2 = st.columns(2)
# with col1:
#     patient_name = st.text_input("Patient Name", help="Enter the patient's full name.")
#     sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Male" if x == 1 else "Female", help="Select patient’s gender.")
#     cp = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3], format_func=lambda x: ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"][x], help="Type of chest pain.")
#     thalach = st.number_input("Max Heart Rate (thalach)", min_value=50, max_value=250, value=180, help="Max heart rate during stress test.")
# with col2:
#     exang = st.selectbox("Exercise Induced Angina", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes", help="Angina induced by exercise.")
#     oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1, help="ST depression induced by exercise.")
#     slope = st.selectbox("Slope of ST Segment", options=[0, 1, 2], format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x], help="Slope of ST segment during exercise.")
#     ca = st.selectbox("Number of Major Vessels", options=[0, 1, 2, 3, 4], help="Vessels colored by fluoroscopy.")
#     thal = st.selectbox("Thalassemia", options=[0, 1, 2, 3], format_func=lambda x: ["Not described", "Normal", "Reversible defect", "Fixed defect"][x], help="Thalassemia condition.")

# # Convert to array
# input_data = np.array([[sex, cp, thalach, exang, oldpeak, slope, ca, thal]])

# def generate_pdf_report(patient_name, sex, cp, thalach, exang, oldpeak, slope, ca, thal, result, probability):
#     # Generate filename
#     filename = f"heart_report_{patient_name.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     c = canvas.Canvas(filename, pagesize=letter)
    
#     # Title
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(50, 770, "Heart Disease Prediction Report")
#     c.setLineWidth(1)
#     c.line(50, 765, 550, 765)
    
#     # Table data
#     data = [
#         ["Feature", "Value"],
#         ["Patient Name", patient_name],
#         ["Date and Time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
#         ["Sex", "Female" if sex == 0 else "Male"],
#         ["Chest Pain Type", ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"][cp]],
#         ["Max Heart Rate (thalach)", str(thalach)],
#         ["Exercise Induced Angina", "No" if exang == 0 else "Yes"],
#         ["ST Depression", str(oldpeak)],
#         ["Slope of ST Segment", ["Upsloping", "Flat", "Downsloping"][slope]],
#         ["Number of Major Vessels", str(ca)],
#         ["Thalassemia", ["Not described", "Normal", "Reversible defect", "Fixed defect"][thal]],
#         ["Prediction", result],
#         ["Probability", f"{probability:.2f}"]
#     ]
    
#     # Create table
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, -1), 12),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#     ]))
    
#     # Draw table
#     table.wrapOn(c, 500, 600)
#     table.drawOn(c, 50, 450)
    
#     # Disclaimer
#     c.setFont("Helvetica", 10)
#     c.drawString(50, 400, "Disclaimer: This report is generated by an AI model for informational purposes only.")
#     c.drawString(50, 385, "Consult a healthcare professional for medical advice.")
    
#     c.save()
#     return filename

# if st.button("Predict"):
#     if not patient_name.strip():
#         st.error("Please enter the patient's name.")
#     else:
#         with st.spinner("Generating prediction..."):
#             prediction = model.predict(input_data)[0]
#             probability = model.predict_proba(input_data)[0][1]
#             result = "Patient is at risk of Heart Disease 💔" if prediction == 1 else "No Heart Disease detected ✅"
        
#         # Display results in a table
#         st.markdown('<div class="header">Prediction Results</div>', unsafe_allow_html=True)
#         result_data = {
#             "Metric": ["Prediction", "Probability"],
#             "Value": [result, f"{probability:.2f}"]
#         }
#         st.table(result_data)
        
#         # Generate and offer PDF download
#         with st.spinner("Generating PDF report..."):
#             try:
#                 pdf_filename = generate_pdf_report(patient_name, sex, cp, thalach, exang, oldpeak, slope, ca, thal, result, probability)
#                 with open(pdf_filename, "rb") as f:
#                     st.download_button(
#                         "📥 Download Report",
#                         f,
#                         file_name=pdf_filename,
#                         mime="application/pdf",
#                         help="Download the detailed prediction report as a PDF."
#                     )
#             except FileNotFoundError:
#                 st.error("Failed to generate PDF. Please try again or check the server configuration.")

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Set page config for better appearance
st.set_page_config(page_title="Heart Disease Prediction", page_icon="❤️", layout="centered")

# Custom CSS for improved styling
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; padding: 20px; border-radius: 10px; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 5px; }
    .stTextInput>div>input { border-radius: 5px; }
    .stSelectbox>div>div>select { border-radius: 5px; }
    .stNumberInput>div>input { border-radius: 5px; }
    .header { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 10px; }
    .subheader { font-size: 18px; color: #555; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# === Load Model ===
model = joblib.load("models/final_model.pkl")

# === Sidebar Instructions ===
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1. Enter the patient's details in the form.
    2. Click **Predict** to get the heart disease prediction.
    3. Download the generated PDF report for a detailed summary.
    **Note**: All fields are required, including the patient's name.
    """)

# === Main UI ===
st.title("Heart Disease Prediction App ❤️")
st.markdown('<div class="header">Enter Patient Information</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Provide the following details to predict heart disease risk.</div>', unsafe_allow_html=True)

# Input form with columns for better layout
col1, col2 = st.columns(2)
with col1:
    patient_name = st.text_input("Patient Name", help="Enter the patient's full name.")
    sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male", help="Select patient’s gender.")
    cp = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3], format_func=lambda x: ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"][x], help="Type of chest pain.")
    thalach = st.number_input("Max Heart Rate (thalach)", min_value=50, max_value=250, value=180, help="Max heart rate during stress test.")
with col2:
    exang = st.selectbox("Exercise Induced Angina", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes", help="Angina induced by exercise.")
    oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1, help="ST depression induced by exercise.")
    slope = st.selectbox("Slope of ST Segment", options=[0, 1, 2], format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x], help="Slope of ST segment during exercise.")
    ca = st.selectbox("Number of Major Vessels", options=[0, 1, 2, 3, 4], help="Vessels colored by fluoroscopy.")
    thal = st.selectbox("Thalassemia", options=[0, 1, 2, 3], format_func=lambda x: ["Not described", "Normal", "Reversible defect", "Fixed defect"][x], help="Thalassemia condition.")

# Convert to array
input_data = np.array([[sex, cp, thalach, exang, oldpeak, slope, ca, thal]])

def generate_pdf_report(patient_name, sex, cp, thalach, exang, oldpeak, slope, ca, thal, result, probability):
    # Generate filename
    filename = f"heart_report_{patient_name.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Page dimensions (letter: 612x792 points)
    page_width, page_height = letter  # 612, 792
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    title = "Heart Disease Prediction Report"
    title_width = c.stringWidth(title, "Helvetica-Bold", 16)
    c.drawString((page_width - title_width) / 2, 750, title)
    c.setLineWidth(1)
    c.line(50, 745, page_width - 50, 745)
    
    # Table data
    data = [
        ["Feature", "Value"],
        ["Patient Name", patient_name],
        ["Date and Time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["Sex", "Female" if sex == 0 else "Male"],
        ["Chest Pain Type", ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"][cp]],
        ["Max Heart Rate (thalach)", str(thalach)],
        ["Exercise Induced Angina", "No" if exang == 0 else "Yes"],
        ["ST Depression", str(oldpeak)],
        ["Slope of ST Segment", ["Upsloping", "Flat", "Downsloping"][slope]],
        ["Number of Major Vessels", str(ca)],
        ["Thalassemia", ["Not described", "Normal", "Reversible defect", "Fixed defect"][thal]],
        ["Prediction", result],
        ["Probability", f"{probability:.2f}"]
    ]
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    # Calculate table dimensions
    table_width = 500
    table.wrap(table_width, 400)  # Estimate height
    table_height = sum(table._rowHeights)
    
    # Center the table on the page
    x = (page_width - table_width) / 2  # Horizontal centering
    y = (page_height - table_height) / 2  # Vertical centering, adjusted to middle of page
    
    # Draw table
    table.drawOn(c, x, y)
    
    # Disclaimer (below table, centered)
    styles = getSampleStyleSheet()
    disclaimer_text = (
        "Disclaimer: This report is generated by an AI model for informational purposes only. "
        "Consult a healthcare professional for medical advice."
    )
    disclaimer = Paragraph(disclaimer_text, styles['Normal'])
    disclaimer_width = 500
    disclaimer.wrap(disclaimer_width, 50)
    disclaimer.drawOn(c, (page_width - disclaimer_width) / 2, y - 60)
    
    c.save()
    return filename

if st.button("Predict"):
    if not patient_name.strip():
        st.error("Please enter the patient's name.")
    else:
        with st.spinner("Generating prediction..."):
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]
            result = "Patient is at risk of Heart Disease 💔" if prediction == 1 else "No Heart Disease detected ✅"
        
        # Display results in a table
        st.markdown('<div class="header">Prediction Results</div>', unsafe_allow_html=True)
        result_data = {
            "Metric": ["Prediction", "Probability"],
            "Value": [result, f"{probability:.2f}"]
        }
        st.table(result_data)
        
        # Generate and offer PDF download
        with st.spinner("Generating PDF report..."):
            try:
                pdf_filename = generate_pdf_report(patient_name, sex, cp, thalach, exang, oldpeak, slope, ca, thal, result, probability)
                with open(pdf_filename, "rb") as f:
                    st.download_button(
                        "📥 Download Report",
                        f,
                        file_name=pdf_filename,
                        mime="application/pdf",
                        help="Download the detailed prediction report as a PDF."
                    )
            except FileNotFoundError:
                st.error("Failed to generate PDF. Please try again or check the server configuration.")
