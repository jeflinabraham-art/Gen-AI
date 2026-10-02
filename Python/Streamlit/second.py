import streamlit as st
import pandas as pd

st.title("My Streamlit Application")

# display data 
data = {
    "Name": ["Jeff", "Aryan", "Yatharth"],
    "City": ["Delhi", "Rajasthan", "Bihar"]
}
# DataFrame is a Pandas object representing tabular data. Pandas takes your dictionary and creates a DataFrame object.
df = pd.DataFrame(data)

# You're telling Streamlit: Take this DataFrame object and display it as a table in my web app. you can also use st.write(df)
st.dataframe(df)



# charts
df = pd.DataFrame({
        "num": [1,2,3,4,5,6,7,8,9,10],
        "num_sq": [1,4,9,16,25,36,49,64,81,100]
    }
)
st.line_chart(df, x="num", y="num_sq")

# upload file
uploaded_file = st.file_uploader("Upload a csv file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.text("Preview of uploaded data:")
    st.dataframe(df)
 

# session state

# When you click a button, Streamlit essentially re-runs your Python script from the top. Streamlit receives the interaction from your browser and says: The UI changed. I need to execute the script again to figure out what the UI should look like now.

# Without session_state, a normal variable would reset. Your PYTHON VARIABLES disappear when the script reruns, but values stored in st.session_state survive the rerun.
counter = 0
if st.button("Increase count "):
    counter += 1
st.write(counter)


if "counter" not in st.session_state:
    st.session_state.counter = 0  
if st.button("Increase counter"):
    st.session_state.counter += 1  
st.write(st.session_state.counter)  
