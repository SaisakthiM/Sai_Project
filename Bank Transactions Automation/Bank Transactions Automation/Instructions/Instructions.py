"""

Dependencies : numpy, pandas, os, datetime, streamlit,plotly
# 1. Import the required libraries

import streamlit as st
import pandas as pd
import datetime as dt
import os


Note : To open the GUI interface, run the command 'streamlit run Main.py' in the terminal.

To write the code in the GUI interface, use the command 'st.write()'.
st.set_page_config(page_title="Bank Transactions Automation", page_icon="💰", layout="wide")
st.write("# Bank Transactions Automation")

edited_df1 = st.data_editor(
                    st.session_state.main_df[["Date", "Description", "Withdrawal", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Withdrawal": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )
                st.write(edited_df1)
                save_button = st.button("Apply Changes", type="primary")
                if save_button:
                    for idx, row in edited_df1.iterrows():
                        new_category = row["Category"]
                        if new_category == st.session_state.debits_df.at[idx, "Category"]:
                            continue
                        
                        details = row["Details"]
                        st.session_state.debits_df.at[idx, "Category"] = new_category
                        add_keyword(new_category, details)
                        
st.session_state.main_df[["Date", "Description", "Balance", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Withdrawal": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )
                st.write(edited_df2)
                if save_button:
                    for idx, row in edited_df2.iterrows():
                        new_category = row["Category"]
                        if new_category == st.session_state.debits_df.at[idx, "Category"]:
                            continue
                        
                        details = row["Details"]
                        st.session_state.debits_df.at[idx, "Category"] = new_category
                        add_keyword(new_category, details)


"Total Withdrawls": st.column_config.NumberColumn(withdraw_df.sum(), format="%.2f AED")

total = df["Withdrawls"].sum()
                st.dataframe(
                    total,
                    column_config={
                        "Withdrawls": st.column_config.NumberColumn("Withdrawls", format="%.2f AED"),
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="total_withdrawl"
                )
        






"""