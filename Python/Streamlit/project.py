
# Capstone Project — Personal Finance Dashboard
# What the App Does: Users upload an expense CSV file and the app provides:

# • Expense summary metrics
# • Category-wise spending analysis
# • Monthly spending trends
# • Interactive filters
# • Clean dashboard layout



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Dashboard")

st.title("💰 Personal Finance Dashboard")
st.write("Upload your expense CSV file to analyze your spending habits.")

# Sidebar
st.sidebar.header("Upload Your Data")

uploaded_file = st.sidebar.file_uploader("Upload Expense CSV", type=["csv"])

if uploaded_file is not None:

    # Read the uploaded CSV file and convert its data into a Pandas DataFrame.
    df = pd.read_csv(uploaded_file)

    # Convert the "Date" column from string format into Pandas datetime format so that we can perform date-based operations like extracting month/year.
    # format="%d-%m-%Y" tells Pandas how the date is written in your CSV.
    df["Date"] = pd.to_datetime(df["Date"], format="%m-%d-%Y")

    # Sidebar Filters
    st.sidebar.header("Filters")

    # multiselect() creates a dropdown where the user can select multiple options.
    category_filter = st.sidebar.multiselect(
        "Select Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    payment_filter = st.sidebar.multiselect(
        "Payment Mode",
        options=df["Payment_Mode"].unique(),
        default=df["Payment_Mode"].unique()
    )

    filtered_df = df[
        (df["Category"].isin(category_filter)) &
        (df["Payment_Mode"].isin(payment_filter))
    ]

    # Top Metrics
    total_spent = filtered_df["Amount"].sum()
    avg_spent = filtered_df["Amount"].mean()
    max_spent = filtered_df["Amount"].max()

    col1, col2, col3 = st.columns(3)

    # :, → adds commas.
    # .2f → two decimal places.
    # example, 25430.5 gets converted to ₹25,430.50
    # metric() is a Streamlit function used to display an important number/KPI in a nice dashboard-style format.
    col1.metric("Total Spending", f"₹{total_spent:,.2f}")
    col2.metric("Average Transaction", f"₹{avg_spent:,.2f}")
    col3.metric("Highest Expense", f"₹{max_spent:,.2f}")

    # Adds a horizontal line.
    st.divider()

    # Raw Data
    st.subheader("📄 Transaction Data")
    st.dataframe(filtered_df)

    # Category Analysis
    st.subheader("📊 Spending by Category")

    # groupBy() is basically saying "I've created the groups based on category. Now tell me what calculation you want to perform on them."
    # the result is a pandas grouped dataframe.
    grouped = filtered_df.groupby("Category")

    # take the 'Amount' column from the grouped dataframe and do sum.
    # Pandas adds the amounts inside each group.
    # the result is a pandas series with category as INDEX and amount as VALUE.
    category_data = grouped["Amount"].sum()


    # This creates the plotting area, gives two Matplotlib objects:
    # fig1: is the entire chart (Think of fig1 as the whole piece of paper).
    # ax1: is the actual plotting area where your graph is drawn (Think of ax1 as the area on that paper where you're actually drawing the graph).
    fig1, axes = plt.subplots()

    # You're telling Pandas: "Take my Series and make a bar chart from it, and draw that chart inside ax1."
    # category_data is a Series, and Pandas has a built-in rule for plotting a Series:
    # Series index → X-axis
    # Series values → Y-axis
    category_data.plot(kind="bar", ax=axes)

    axes.set_ylabel("Amount Spent")
    axes.set_xlabel("Category")

    # means: Streamlit, take this Matplotlib Figure and display it in my web app.
    st.pyplot(fig1)

    st.divider()

    # Monthly Trend
    st.subheader("📈 Monthly Spending Trend")

    # .dt allows Pandas to perform date/time operations on a datetime column.
    filtered_df["Month"] = filtered_df["Date"].dt.to_period("M")

    # Put all rows having the same month into the same group.
    grouped = filtered_df.groupby("Month")

    # From those groups, I'm interested in the Amount column. Add the amounts within each month.
    monthly_data = grouped["Amount"].sum()

    fig2, ax2 = plt.subplots()
    monthly_data.plot(kind="line", marker="o", ax=ax2)
    ax2.set_ylabel("Amount")
    ax2.set_xlabel("Month")

    st.pyplot(fig2)

    st.divider()

else:
    st.info("Please upload a CSV file to begin analysis.")