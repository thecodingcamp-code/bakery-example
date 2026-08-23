import streamlit as st
import csv
import io
from datetime import datetime

st.title("Bakery Daily Report")
st.write("Upload today's sales file to generate a report.")

uploaded_file = st.file_uploader("Choose a sales CSV file", type="csv")

if uploaded_file is not None:
    text_file = io.TextIOWrapper(uploaded_file, encoding="utf-8")
    reader = csv.DictReader(text_file)
    sales = []
    for row in reader:
        row["quantity"] = int(row["quantity"])
        row["price"] = float(row["price"])
        sales.append(row)

    if st.button("Generate Report"):
        total_items = sum(item["quantity"] for item in sales)
        total_revenue = sum(item["quantity"] * item["price"] for item in sales)
        best_seller = max(sales, key=lambda item: item["quantity"])

        st.subheader(f"Report for {datetime.now():%Y-%m-%d}")
        st.metric("Total items sold", total_items)
        st.metric("Total revenue", f"${total_revenue:.2f}")
        st.write(f"Best seller: **{best_seller['item']}** ({best_seller['quantity']} sold)")

        report_text = (
            f"Daily Bakery Report - {datetime.now():%Y-%m-%d}\n"
            f"Total items sold: {total_items}\n"
            f"Total revenue: ${total_revenue:.2f}\n"
            f"Best seller: {best_seller['item']} ({best_seller['quantity']} sold)"
        )
        st.download_button("Download report as text file", report_text, file_name="report.txt")