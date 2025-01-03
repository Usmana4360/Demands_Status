import pandas as pd
import streamlit as st

# Title of the App
st.title("Procurement Operations Dashboard")

# Sidebar for uploading data
st.sidebar.header("Upload Procurement Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the CSV file
    df = pd.read_csv(uploaded_file)
    
    st.sidebar.success("File uploaded successfully!")

    # Display raw data
    st.subheader("Procurement Data")
    st.dataframe(df)

    # Key Performance Indicators (KPIs)
    st.subheader("Key Metrics")
    total_cost = df['Cost'].sum() if 'Cost' in df.columns else 0
    pending_requests = df[df['Status'] == 'pending'].shape[0]
    top_supplier = df['Supplier'].value_counts().idxmax() if 'Supplier' in df.columns else "N/A"
    st.metric("Total Cost", f"${total_cost:,.2f}")
    st.metric("Pending Requests", pending_requests)
    st.metric("Top Supplier", top_supplier)

    # Filter Section
    st.subheader("Filter Data")
    status_options = df['Status'].dropna().unique().tolist() if 'Status' in df.columns else []
    supplier_options = df['Supplier'].dropna().unique().tolist() if 'Supplier' in df.columns else []
    department_options = df['Department'].dropna().unique().tolist() if 'Department' in df.columns else []

    selected_status = st.selectbox("Filter by Status", ["All"] + status_options)
    selected_supplier = st.selectbox("Filter by Supplier", ["All"] + supplier_options)
    selected_department = st.selectbox("Filter by Department", ["All"] + department_options)

    # Filter logic
    filtered_df = df.copy()
    if selected_status != "All":
        filtered_df = filtered_df[filtered_df['Status'] == selected_status]
    if selected_supplier != "All":
        filtered_df = filtered_df[filtered_df['Supplier'] == selected_supplier]
    if selected_department != "All":
        filtered_df = filtered_df[filtered_df['Department'] == selected_department]

    # Sorting Section
    st.subheader("Sort Data")
    sort_column = st.selectbox("Select Column to Sort", df.columns)
    sort_order = st.radio("Sort Order", ["Ascending", "Descending"])
    if sort_column:
        ascending = sort_order == "Ascending"
        filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

    # Display filtered and sorted data
    st.subheader("Filtered and Sorted Data")
    st.dataframe(filtered_df)

    # Download filtered data
    st.subheader("Download Data")
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_procurement_data.csv",
        mime="text/csv",
    )
else:
    st.warning("Please upload a CSV file to get started.")

