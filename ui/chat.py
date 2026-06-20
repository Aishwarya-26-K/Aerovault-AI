import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/api/ask"


st.set_page_config(
    page_title="Aviation RAG Assistant",
    page_icon="✈️",
    layout="wide"
)


# -----------------------------
# Dark Aviation Theme + Text Fix
# -----------------------------

st.markdown(
    """
    <style>

    .stApp {

        background: linear-gradient(
            135deg,
            #001f3f,
            #003366,
            #001a33
        );

    }


    h1 {

        color: #ffffff !important;

    }


    .stCaption {

        color: #cce6ff !important;

    }



    /* Chat cards */

    div[data-testid="stChatMessage"] {

        background: rgba(255,255,255,0.12);

        border-radius: 18px;

        padding: 18px;

        margin-bottom: 15px;

        border:
        1px solid rgba(255,255,255,0.25);

        backdrop-filter: blur(10px);

    }



    /* All text visible */

    p, li, span, div {

        color: #ffffff;

    }



    div[data-testid="stChatMessage"] p {

        color: #ffffff !important;

    }



    /* Sources box */

    div[data-testid="stExpander"] * {

        color: #ffffff !important;

    }



    /* Confidence card */

    div[data-testid="stMetric"] {

        background:
        rgba(255,255,255,0.15);

        padding: 15px;

        border-radius: 15px;

    }


    div[data-testid="stMetricLabel"] {

        color: #cce6ff !important;

    }



    /* Input */

    div[data-testid="stChatInput"] {

        background-color: white;

        border-radius: 18px;

    }



    /* Sidebar */

    section[data-testid="stSidebar"] {

        background: #001426;

    }


    section[data-testid="stSidebar"] * {

        color: white !important;

    }


    </style>
    """,
    unsafe_allow_html=True
)



# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.title("✈️ Aviation RAG")

    st.write(
        "Document Intelligence Assistant"
    )

    st.divider()


    st.write("Features")


    st.success("✓ PDF Knowledge Base")

    st.success("✓ FAISS Retrieval")

    st.success("✓ RAG Generation")

    st.success("✓ Confidence Guardrail")

    st.success("✓ Source Tracking")



# -----------------------------
# Main
# -----------------------------

st.title("✈️ Aviation RAG Assistant")


st.caption(
    "Ask questions from aviation documents"
)



# Store messages

if "messages" not in st.session_state:

    st.session_state.messages = []



# Display chat history

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

        if "extra" in message:

            st.markdown(
                message["extra"]
            )



question = st.chat_input(
    "Ask an aviation question..."
)



if question:


    with st.chat_message("user"):

        st.write(question)


    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )



    with st.chat_message("assistant"):


        with st.spinner(
            "Searching aviation documents..."
        ):


            try:


                response = requests.post(

                    API_URL,

                    json={
                        "question": question
                    }

                )


                data = response.json()



                answer = data["answer"]

                confidence = data["confidence"]

                label = data["confidence_label"]



                st.write(answer)



                if label == "High":

                    icon = "🟢"

                elif label == "Medium":

                    icon = "🟡"

                else:

                    icon = "🔴"



                st.metric(
                    "Confidence",
                    f"{icon} {confidence*100:.0f}%"
                )


                st.write(
                    f"Confidence Level: **{label}**"
                )



                with st.expander(
                    "📄 View sources"
                ):


                    for src in data["sources"]:

                        st.write(
                            f"📄 {src['file']} | Page {src['page']}"
                        )



                st.session_state.messages.append(

                    {
                        "role": "assistant",

                        "content": answer,

                        "extra":
                        f"""
Confidence: **{label}**

Sources: {len(data['sources'])} documents
"""
                    }

                )



            except Exception as e:

                st.error(
                    f"Backend connection failed: {e}"
                )