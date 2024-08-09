import streamlit as st
import requests


# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Maritalk "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

url = "https://chat.maritaca.ai/api/chat/inference"


my_key = "117854799329334839999_93d20327f9285d30"

auth_header = {
    "authorization": f"Key {my_key}"
}

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):
    messages = [
        {"role": "user", "content": "bom dia, esta é a mensagem do usuario"},
        {"role": "assistant", "content": "bom dia, esta é a resposta do assistente"},
        {"role": "user", "content": "%s" % prompt},
    ]

    request_data = {
        "messages": messages,
        "do_sample": True,
        'max_tokens': 200,
        "temperature": 0.0,
        "top_p": 0.95,
        "model": "sabia-3",
    }

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    def get_maritalk_response(request_data, headers):
        response = requests.post(
            url,
            json=request_data,
            headers=headers
        )

        if not response.ok:
            raise Exception(
                f"Request failed with status code {response.status_code}: {response.text}")
        return response.json()

    response = get_maritalk_response(request_data, auth_header)

    # Stream the response to the chat using `st.write_stream`, then store it in
    # session state.
    with st.chat_message("assistant"):
        response = st.write(response["answer"])
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
