import streamlit as st
import datetime
from pages.Image import makeImage, show_image_from_url

# def image_page():
#     st.header("Images")

#     sex = st.session_state["sex"]
#     dob = st.session_state["dob"]
#     address = st.session_state["address"]
#     occupation = st.session_state["occupation"]

#     url = makeImage(sex, dob, occupation, address, [], [], [])
#     show_image_from_url(url)

# TODO: Pre populate fields
def registration_form():
    # Display the registration form
    st.header("Patient Profile")

    with st.form("registration_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        sex = st.selectbox("Sex", ["Male", "Female"])
        address = st.text_area("Address")
        exercise_habits = st.text_input("Exercise Habits")
        family_history = st.text_area("Family History")
        diet = st.text_input("Diet")
        if diet == "Other":
            diet_details = st.text_input("Please specify your diet")
        else:
            diet_details = diet
        occupation = st.text_input("Occupation")

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Save the user's information (or do something with the data)
            st.session_state['registered'] = True
            st.session_state['first_name'] = first_name
            st.session_state['last_name'] = last_name
            st.session_state['dob'] = dob.strftime('%Y-%m-%d')
            st.session_state['sex'] = sex
            st.session_state['address'] = address

            st.session_state['exercise_habits'] = exercise_habits
            st.session_state['family_history'] = family_history
            st.session_state['diet'] = diet_details
            st.session_state['occupation'] = occupation

def physical_feeling_form():
    # Display the physical feeling form
    st.header("How Are You Feeling?")

    symptoms = st.multiselect(
        "Select your current physical symptoms:", 
        ["No symptoms", "Pain", "Discomfort", "Nausea", "Headache", "Fatigue", "Dizziness", "Other"]
    )

    if "Other" in symptoms:
        other_symptoms = st.text_input("Please describe other symptoms:")
    else:
        other_symptoms = ""

    if st.button("Submit"):
        st.session_state['symptoms'] = symptoms + [other_symptoms] if other_symptoms else symptoms
        st.session_state['feeling_submitted'] = True

# Main logic
if 'registered' not in st.session_state:
    st.session_state['registered'] = False
if 'feeling_submitted' not in st.session_state:
    st.session_state['feeling_submitted'] = False

if not st.session_state['registered']:
    registration_form()
elif not st.session_state['feeling_submitted']:
    physical_feeling_form()
# elif st.session_state['registered'] and st.session_state['feeling_submitted']:
#     sex = st.session_state["sex"]
#     dob = st.session_state["dob"]
#     address = st.session_state["address"]
#     occupation = st.session_state["occupation"]
#     image_page()
else:
    st.header("Thank you for providing your information!")
    st.write("Registration Details:")
    st.write(f"**Name:** {st.session_state['first_name']} {st.session_state['last_name']}")
    st.write(f"**Age:** {st.session_state['age']}")
    st.write(f"**Gender:** {st.session_state['gender']}")
    # st.write(f)
    st.write(f"**Address:** {st.session_state['address']}")
    st.write("**Physical Symptoms:**")
    for symptom in st.session_state['symptoms']:
        st.write("-", symptom)
