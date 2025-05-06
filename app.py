import streamlit as st
import pandas as pd
import time
from distance_utils import get_distance_km

BATCH_SIZE = 500  # limit based on your ORS quota

st.set_page_config(page_title="Distance Calculator", layout="centered")
st.title("📍 Distance Calculator (Max 500 rows/day)")

uploaded_file = st.file_uploader("📤 Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if not {"Location A", "Location B"}.issubset(df.columns):
        st.error("❌ Excel must contain 'Location A' and 'Location B' columns.")
    else:
        df["Distance (km)"] = ""
        rows_to_process = min(BATCH_SIZE, len(df))

        with st.spinner(f"⏳ Processing first {rows_to_process} rows..."):
            for i in range(rows_to_process):
                loc_a = f"{df.at[i, 'Location A']} School, Pune"
                loc_b = f"{df.at[i, 'Location B']} College, Pune"
                df.at[i, "Distance (km)"] = get_distance_km(loc_a, loc_b)
                time.sleep(1.2)  # control rate limit

        st.success("✅ Distance calculation complete!")
        st.download_button(
            "📥 Download Results",
            data=df.to_excel(index=False),
            file_name="distance_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
