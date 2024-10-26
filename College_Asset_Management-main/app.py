import streamlit as st
import pandas as pd

# Load existing login data from Excel file if available
try:
    login_df = pd.read_excel("login.xlsx")
except FileNotFoundError:
    login_df = pd.DataFrame(columns=['Username', 'Password'])

# Load existing asset data from Excel file if available
try:
    asset_df = pd.read_excel("data.xlsx")
except FileNotFoundError:
    asset_df = pd.DataFrame(columns=['Asset Name', 'Quantity', 'Location'])

# Title of the web app
st.title('College Asset Management System')

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Login", "Signup"])

if page == "Signup":
    st.title("Signup")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    signup_button = st.button("Signup")

    if signup_button:
        if new_username in login_df['Username'].values:
            st.error("Username already exists. Please choose a different one.")
        else:
            new_user = {'Username': new_username, 'Password': new_password}
            login_df = login_df._append(new_user, ignore_index=True)
            login_df.to_excel("login.xlsx", index=False)
            st.success("Signup successful! Please proceed to login.")

elif page == "Login":
    st.title("Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if not username_input or not password_input:
            st.error("Please enter username and password.")
        elif username_input in login_df['Username'].values:
            user_row = login_df[login_df['Username'] == username_input]
            if user_row['Password'].iloc[0] == password_input:
                st.success("Login successful!")
                st.session_state.logged_in = True
            else:
                st.error("Incorrect password. Please try again.")
        else:
            st.error("Username not found.")

# Logout page
if st.session_state.get('logged_in'):
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False

    # Asset Management page
    st.write('## Current Asset Inventory')
    st.write(asset_df)

    # Add asset form
    st.write('## Add New Asset')
    asset_name = st.text_input('Asset Name')
    quantity = st.number_input('Quantity', min_value=1)
    location = st.text_input('Location')
    if st.button('Add Asset'):
        new_asset = {'Asset Name': asset_name, 'Quantity': quantity, 'Location': location}
        asset_df = asset_df._append(new_asset, ignore_index=True)
        asset_df.to_excel("data.xlsx", index=False)
        st.success('Asset added successfully!')

    # Display updated DataFrame
    st.write('## Updated Asset Inventory')
    st.write(asset_df)

    # Search asset by name
    st.write('## Search Asset')
    search_term = st.text_input('Enter asset name to search:')
    search_results = asset_df[asset_df['Asset Name'].str.contains(search_term, case=False)]
    st.write(search_results)
else:
    st.warning("Please login to access the asset management page.")
