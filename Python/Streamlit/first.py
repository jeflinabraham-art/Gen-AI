# to run streamlit app: streamlit run <filename>.py
# make sure you use the correct python interpreter:
#   1. press ctrl+shift+p
#   2. search Python: Select Interpreter
#   3. select the interpreter inside of your project env -> C:\Users\ASUS\UpSkill\GEN AI\Python\Streamlit\myEnv\Scripts\python.exe

import streamlit as st
import pandas as pd
import numpy as np

st.title("Streamlit Application")
st.header("This is a header")
st.subheader("This is a subheader")

# Use st.text() when you specifically want plain text.
st.text("This is plain text")

# st.write() looks at the type of the object and chooses an appropriate Streamlit representation. Use st.write() when you want a convenient general-purpose way to display Python objects and content.
st.write("General purpose display")
st.write(["apple", "Mango", "Orange", "kiwi"])
st.write({"Jef": 23, "Nikhil": 25, "Rit": 22})
st.write(10)

# text input
name = st.text_input("Enter your name: ")
if (name):
    st.write(f"Hello {name}, Welcome to my streamlit application.")

# sliders and number inputs
age = st.slider("Select your age: ", 0,100,25)
st.write("Your age is: ", age)

number = st.number_input("Enter a number: ", min_value=0, max_value=100)
st.write(f"You entered: {number}")

# button and actions
if st.button("Click me"):
    st.success("You clicked the button!!")

# select box/ dropdowns
lang = st.selectbox("choose your favourite programming language", 
             ["Python", "Java", "C++", "GoLang"])
st.write(f"You selected {lang}")

# sidebar 
st.sidebar.title("Sidebar Menu")
page = st.sidebar.selectbox("Choose a page", ["Home", "About", "Contact"])
st.write(f"You selected: {page}")


# columns
col1, col2, col3 = st.columns(3)

with col1:
    # **Bold**
    st.write("👤 **Name**")
    st.write("Jeflin")

with col2:
    st.write("🎂 **Age**")
    st.write("23")

with col3:
    st.write("💼 **Job**")
    st.write("Software Engineer")

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









