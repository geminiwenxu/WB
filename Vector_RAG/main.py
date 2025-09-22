import streamlit as st
import pandas as pd
from io import StringIO
import streamlit as st
st.markdown("<h1 style='text-align: center; color: blue;'>AI Policy Assistant</h1>", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center; color: orange;'>AI Policy Assisstant is a smart document reader</h1>", unsafe_allow_html=True)

st.set_page_config(
page_title="",
page_icon="🧊",
layout="wide",
initial_sidebar_state="expanded",
menu_items={
'Get Help': 'https://www.extremelycoolapp.com/help',
'Report a bug': "https://www.extremelycoolapp.com/bug",
'About': "# This is a header. This is an *extremely* cool app!"
}
)


# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.header("Please answer these questions below:")
    name_company = st.text_input("Name of the firm")
    legal_form = st.text_input("Legal form of the company")
    ownership_structure = st.text_input("Ownership structure")
    product = st.text_input("Product")
    HRI_involvement = st.text_input("HRI involvement")
    FATCA_CRS = st.text_input("FATCA/CRS relevance")
    MDS = st.text_input("Details to MDs")
    UBO = st.text_input("Details to UBOs")
    additional_notes = st.text_input("Additional notes")
with col2:
    st.header("Country Checklist")
    
    with st.form("my_form"):
        st.write("Choose the country")
        country = st.selectbox("Which country to select",("Germany", "Austria"))
        option = st.selectbox(
        "Which option?",
        ("Booking office", "writing office", "None"),)
        st.write("You selected:", option)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("The office option selected is: ", option, " for country: ", country)
    
    


  