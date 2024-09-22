import streamlit as st
import datetime
import streamlit as st
from models.text_model import MedicalChatbot, TASK_SPECIFIC_INSTRUCTIONS


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
        first_name = st.text_input("First Name", value="Jane")
        last_name = st.text_input("Last Name", value="Doe")
        dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        sex = st.selectbox("Sex", ["Male", "Female"], index=1)
        address = st.text_area("Address", value="San Francisco")
        phone = st.text_input("Phone Number", value="123456789")
        exercise_habits = st.text_input("Exercise Habits", value="Once a week")
        family_history = st.text_area("Family History")
        diet = st.text_input("Diet", value="Heavy carbs, less protein and veggies")
        occupation = st.text_input("Occupation", value="Farmer")

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Save the user's information (or do something with the data)
            st.session_state['registered'] = True
            st.session_state['first_name'] = first_name
            st.session_state['last_name'] = last_name
            st.session_state['dob'] = dob.strftime('%Y-%m-%d')
            st.session_state['sex'] = sex
            st.session_state['address'] = address
            st.session_state['phone'] = phone

            st.session_state['exercise_habits'] = exercise_habits
            st.session_state['family_history'] = family_history
            st.session_state['diet'] = diet
            st.session_state['occupation'] = occupation

def physical_feeling_form():
    # Display the physical feeling form
    st.header("How Are You Feeling?")

    with st.form("intake"):
        condition = st.text_area("How are you feeling today?")
        conditionSince = st.text_input("How long have you been feeling this way?")
        stepsTaken = st.text_area("What steps have you taken to try to feel better?")

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Save the user's information (or do something with the data)
            st.session_state['condition'] = condition
            st.session_state['conditionSince'] = conditionSince
            st.session_state['stepsTaken'] = stepsTaken
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
#   if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {'role': "user", "content": TASK_SPECIFIC_INSTRUCTIONS},
#             {'role': "assistant", "content": "Understood"},
#         ]

#   chatbot = MedicalChatbot(st.session_state)
#   response_placeholder = st.empty()
#   initial_welcome = chatbot.process_user_input("introduce yourself")
#   response_placeholder.markdown(initial_welcome)

#   if len(st.session_state.messages) >= 5: 
#       for message in st.session_state.messages[7:]:
#           # ignore tool use blocks
#           if isinstance(message["content"], str):
#               with st.chat_message(message["role"]):
#                   st.markdown(message["content"])

#   if user_message := st.chat_input("Ask questions here"):
#       st.chat_message("user").markdown(user_message)

#       with st.chat_message("assistant"):
#           with st.spinner("Thinking..."):
#               response_placeholder = st.empty()
#               full_response = chatbot.process_user_input(user_message)
#               response_placeholder.markdown(full_response)
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
