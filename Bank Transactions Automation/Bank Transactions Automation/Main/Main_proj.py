import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Set page configuration for modern look
st.set_page_config(page_title="Bank Transactions Automation", page_icon="💰", layout="wide")

category_file = "Pycharm\Python Project\Beginner Project\Bank Transactions Automation\Main\categories.json"

if "categories" not in st.session_state:
    st.session_state.categories = {
        'Uncategorized': []
    }

if os.path.exists(category_file):
    with open(category_file, 'r') as f:
        st.session_state.categories = json.load(f)

def save_categories():
    with open(category_file, 'w') as f:
        json.dump(st.session_state.categories, f)

def add_keyword(category, keyword):
    if keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    return False

def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        df["Deposits"] = df["Deposits"].str.replace(",", "").astype(float)
        df["Withdrawls"] = df["Withdrawls"].str.replace(",", "").astype(float)
        df["Balance"] = df["Balance"].str.replace(",", "").astype(float)
        return categorize_transaction(df)
    except Exception as e:
        st.error(f"Error Processing the File 😔 : {str(e)}")

def categorize_transaction(df):
    category_mapping = {
        "Income": ["NEFT", "RTGS", "ATM", "Interest", "Reversal"],
        "Expenses": ["Purchase", "Bill", "Tax", "Debit Card", "Commission"],
        "Transfers": ["IMPS", "Transfer", "Cheque"],
        "Miscellaneous": ["Miscellaneous", "Cash"],
        "Service Fees & Deductions": ["Charges", "Commission", "Reversal", "Debit Card", "Tax"]
    }

    df["Category"] = "Uncategorized"
    for category, keywords in category_mapping.items():
        for idx, row in df.iterrows():
            description = str(row["Description"]).lower()  # Ensure case-insensitivity
            if any(keyword.lower() in description for keyword in keywords):
                df.at[idx, "Category"] = category
    return df

# Convert AED to USD
def convert_to_usd(amount_aed):
    conversion_rate = 0.27  # Example conversion rate from AED to USD
    return amount_aed * conversion_rate

# Main function with modern UI and updated graphs
def main():
    st.title("🔥 Transaction Analyzer / Simple Dashboard 📊")
    uploaded_file = st.file_uploader("Upload your bank transactions CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        st.title("💹 Transaction History 💵")
        st.write(df)

        if df is not None:
            # Convert columns to USD
            df["Withdrawls (USD)"] = df["Withdrawls"].apply(convert_to_usd)
            df["Balance (USD)"] = df["Balance"].apply(convert_to_usd)
            
            st.session_state.main_df = df.copy()
            withdraw_df = df["Withdrawls (USD)"].copy()
            balance_df = df["Balance (USD)"].copy()
            st.session_state.withdraw_df = withdraw_df.copy()
            st.session_state.balance_df = balance_df.copy()

            # Using tabs to organize different views
            tab1, tab2, tab3 = st.tabs(["Withdrawals", "Balance", "Add Categories"])

            # Withdrawals Tab
            with tab1:
                st.subheader("💸 Withdrawals Overview")
                category_total = df.groupby("Category")["Withdrawls (USD)"].sum().reset_index()
                category_total = category_total.sort_values(by="Withdrawls (USD)", ascending=False)
                st.dataframe(category_total, use_container_width=True)

                # Line graph for Withdrawals Trend over Time with categories
                st.subheader("📈 Withdrawals Trend Over Time")
                fig1 = px.line(df, x="Date", y="Withdrawls (USD)", color="Category", title="Withdrawals Trend",
                               labels={"Withdrawls (USD)": "Amount Withdrawn (USD)", "Date": "Date"},
                               hover_data=["Date", "Withdrawls (USD)", "Category"])  # Hover effect showing date, amount, and category
                fig1.update_traces(mode='lines+markers', line=dict(width=2), marker=dict(size=5))  # Add markers and lines
                st.plotly_chart(fig1, use_container_width=True)

                # Withdrawals Breakdown by Category (Pie Chart)
                st.subheader("📊 Withdrawals by Category")
                fig2 = px.pie(category_total, values="Withdrawls (USD)", names="Category", title="Withdrawals Breakdown")
                st.plotly_chart(fig2, use_container_width=True)

                # Total Withdrawals Summary (in columns for better layout)
                total_withdrawals = df["Withdrawls (USD)"].sum()
                col1, col2, col3 = st.columns([3, 2, 1])
                with col3:
                    st.metric(label="💲Total Withdrawn💲", value=f"${total_withdrawals:,.2f}")

            # Balance Tab
            with tab2:
                st.subheader("💸 Balance Overview")
                category_total = df.groupby("Category")["Balance (USD)"].sum().reset_index()
                category_total = category_total.sort_values(by="Balance (USD)", ascending=False)
                st.dataframe(category_total, use_container_width=True)

                # Line graph for Balance Trend over Time with categories
                st.subheader("📈 Balance Trend Over Time")
                fig3 = px.line(df, x="Date", y="Balance (USD)", color="Category", title="Balance Trend",
                               labels={"Balance (USD)": "Account Balance (USD)", "Date": "Date"},
                               hover_data=["Date", "Balance (USD)", "Category"])  # Hover effect showing date, balance, and category
                fig3.update_traces(mode='lines+markers', line=dict(width=2), marker=dict(size=5))  # Add markers and lines
                st.plotly_chart(fig3, use_container_width=True)

                # Balance Breakdown by Category (Donut Chart)
                st.subheader("📊 Balance by Category")
                fig4 = px.pie(category_total, values="Balance (USD)", names="Category", title="Balance Breakdown", hole=0.4)
                st.plotly_chart(fig4, use_container_width=True)

                # Total Balance Summary
                total_balance = df["Balance (USD)"].sum()
                col1, col2, col3 = st.columns([3, 2, 1])
                with col3:
                    st.metric(label="💲Total Balance💲", value=f"${total_balance:,.2f}")

            # Add Categories Tab
            with tab3:
                st.markdown("<h1 style='text-align: center;'>💰 Categorize Your Transactions 💰</h1>", unsafe_allow_html=True)
                new_category = st.text_input("New Category Name")
                add_button = st.button("Add Category")

                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.success(f"Category '{new_category}' added successfully!")
                        st.rerun()

if __name__ == '__main__':
    main()