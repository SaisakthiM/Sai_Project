import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import tempfile

def generate_report_card(name, roll_no, marks_dict, total_marks, percentage, grade):
    img = Image.new('RGB', (800, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
        title_font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
        title_font = font

    draw.text((260, 20), "REPORT CARD", font=title_font, fill="black")
    draw.text((50, 80), f"Name: {name}", font=font, fill="black")
    draw.text((50, 110), f"Roll No: {roll_no}", font=font, fill="black")

    draw.text((50, 160), "Subject", font=font, fill="black")
    draw.text((300, 160), "Marks", font=font, fill="black")
    y = 190
    for subject, marks in marks_dict.items():
        draw.text((50, y), subject, font=font, fill="black")
        draw.text((300, y), str(marks), font=font, fill="black")
        y += 30

    draw.text((50, y + 20), f"Total Marks: {total_marks}", font=font, fill="black")
    draw.text((50, y + 50), f"Percentage: {percentage:.2f}%", font=font, fill="black")
    draw.text((50, y + 80), f"Grade: {grade}", font=font, fill="black")

    return img

st.set_page_config(page_title="Report Card Generator", page_icon="📄", layout="centered")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #2E86C1;'>📄 Report Card Generator</h1>
        <p style='font-size: 18px;'>Upload a CSV file with student scores and generate report cards as images</p>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV uploaded successfully!")

    if 'Name' not in df.columns:
        st.error("CSV must contain a 'Name' column.")
    else:
        for idx, row in df.iterrows():
            name = row['Name']
            marks = row.drop('Name').to_dict()
            percentage = row.drop('Percentage').to_dict()
            card_img = generate_report_card(name, marks)
            is_success, buffer = cv2.imencode(".png", card_img)
            st.image(buffer.tobytes(), caption=f"{name}'s Report Card", use_container_width=True)
