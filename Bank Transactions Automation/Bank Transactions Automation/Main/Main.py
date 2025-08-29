import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import random

st.set_page_config(page_title="Bank Transactions Automation", page_icon="💰", layout="wide")

category_file = "Pycharm\Python Project\Beginner Project\Bank Transactions Automation\Main\categories.json"

if "categories" not in st.session_state:
    st.session_state.categories = {
        'Uncategorized' : []
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
        df["Deposits"] = df["Deposits"].str.replace(",","").astype(float)
        df["Withdrawls"] = df["Withdrawls"].str.replace(",","").astype(float)
        df["Balance"] = df["Balance"].str.replace(",","").astype(float)
        return categorize_transaction(df)
    except Exception as e:
        st.error(f"Error Processing the File 😔 : {str(e)}")

def categorize_transaction(df):
    df["Category"] = "Uncategorized"
    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue
        lower_keywords = [keyword.lower() for keyword in keywords]
        for idx, row in df.iterrows():
            details = row["Description"].lower()
            if details in lower_keywords:
                df.at[idx, "Category"] = category
    return df
        

def main():
    st.title("🔥 Transaction Analyzer / " +
            "Simple Dashboard📊")
    uploaded_file = st.file_uploader("Upload your bank transactions CSV file", type=["csv"])
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        st.title("💹 Transaction History 💵")
        st.write(df)
        if df is not None:
            st.session_state.main_df = df.copy()
            withdraw_df = df["Withdrawls"].copy()
            balance_df = df["Balance"].copy()
            
            st.session_state.withdraw_df = withdraw_df.copy()
            st.session_state.balance_df = balance_df.copy()
            
            tab1,tab2,tab3 = st.tabs(["Amount Taken (Withdraw)","Amount Remaining (Balance)","Add Categories"])
            with tab1: 
                edited_df1 = st.data_editor(
                    st.session_state.main_df[["Date", "Description", "Withdrawls", "Category"]],
                    column_config={
                        "Withdrawls": st.column_config.NumberColumn("Withdrawls", format="%.2f AED"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )
                
                save_button1 = st.button("Apply Changes", type="primary", key="apply_changes_button_1")
                if save_button1:
                    for idx, row in edited_df1.iterrows():
                        new_category = row["Category"]
                        if new_category == st.session_state.main_df.at[idx, "Category"]:
                            continue
                        
                        details = row["Description"]
                        st.session_state.main_df.at[idx, "Category"] = new_category
                        add_keyword(new_category, details)
                        
                        
                st.subheader("")
                st.subheader("Withdrawl Summary")
                category_total = df.groupby("Category")["Withdrawls"].sum().reset_index()
                category_total = category_total.sort_values(by="Withdrawls", ascending=False)
                st.dataframe(
                    category_total,
                    column_config={
                        "Withdrawls": st.column_config.NumberColumn("Withdrawls", format="%.2f AED"),
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_summary3")
                
                
                st.subheader("")
                st.subheader("💸 Withdrawals Chart (In Terms of Date) 💸")
                fig = px.bar(
                    withdraw_df,
                    x=df["Withdrawls"],
                    y=df["Date"],
                    orientation="h",
                    title="",
                    text_auto=True,
                    color=df["Withdrawls"],  # Color bars based on amount
                    color_continuous_scale="Blues"  # Nice color theme
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("")
                st.subheader("💸 Withdrawals Chart (In Terms of Expenses) 💸")
                fig = px.pie(
                    category_total,
                    values="Withdrawls",
                    names="Category",
                    title=""
                )
                st.plotly_chart(fig, use_container_width=True)
                
                
                st.subheader("")
                total = df["Withdrawls"].sum()
                col1, col2, col3 = st.columns([3,2,1])
                with col3:
                    st.metric(label="💲Total Withdrawal💲", value=f"${total:,.2f}")

                
                
                
            with tab2:
                
                edited_df2 = st.data_editor(
                    st.session_state.main_df[["Date", "Description", "Balance", "Category"]],
                    
                    column_config={
                        "Balance": st.column_config.NumberColumn("Balance", format="%.2f AED"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor2"
                )
                
                save_button2 = st.button("Apply Changes", type="primary", key="apply_changes_button_2")
                if save_button2:
                    for idx, row in edited_df1.iterrows():
                        new_category = row["Category"]
                        if new_category == st.session_state.main_df.at[idx, "Category"]:
                            continue
                        
                        details = row["Description"]
                        st.session_state.main_df.at[idx, "Category"] = new_category
                        add_keyword(new_category, details)
                        
                        
                st.subheader("")
                st.subheader("Balance Summary")
                category_total = df.groupby("Category")["Balance"].sum().reset_index()
                category_total = category_total.sort_values(by="Balance", ascending=False)
                st.dataframe(
                    category_total,
                    column_config={
                        "Balance": st.column_config.NumberColumn("Balance", format="%.2f AED")
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_summary4")
                
                st.subheader("")
                st.subheader("💸 Balance Chart (In Terms of Date) 💸")
                fig = px.bar(
                    withdraw_df,
                    x=df["Balance"],
                    y=df["Date"],
                    orientation="h",
                    title="",
                    text_auto=True,
                    color=df["Balance"],  # Color bars based on amount
                    color_continuous_scale="Blues"  # Nice color theme
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("")
                st.subheader("💸 Balance Chart (In Terms of Expenses) 💸")
                fig = px.pie(
                    category_total,
                    values="Balance",
                    names="Category",
                    title=""
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("")
                total = df["Balance"].sum()
                col1, col2, col3 = st.columns([3,2,1])
                with col3:
                    st.metric(label="💲Total Balance💲", value=f"${total:,.2f}")
            with tab3:
                
                st.markdown("<h1 style='text-align: center;'>💰 Categorize Your Transactions 💰</h1>", unsafe_allow_html=True)
                new_category = st.text_input("New Category Name")
                add_button = st.button("Add Category")
                
                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        
                        st.rerun()
            
                
                            
main()




