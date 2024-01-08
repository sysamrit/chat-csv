import streamlit as st
import pandas as pd
from pandasai.llm import OpenAI
from pandasai import Agent
from pandasai.responses.streamlit_response import StreamlitResponse

openai_api_key = "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"

st.set_page_config(layout="wide")
data=pd.read_csv("final_refubrished_data.csv")
# openai_api_key=st.secrets["OPENAI_API_KEY"]

initial=True
# if "open_ai_model" not in st.session_state:
#     st.session_state["open_ai_model"]="gpt-3.5-turbo-0613"

initial_prompt='I am giving you a name \'Amrit Buddy\'. Please act like a assistant of Amrit Cement Ltd. We are a cement manufacturing company from east-india. We provide you a csv file which is basically a sales report of our company with 7 columns. I am expalining you the columns. Inv typ is the invoice type which is auto genarated by system. Plant is the name of our plants were we produce our cements. Inv Dt is basically the date of billing or a invoice date. Area is the sales area or a district of state and zone is the state name. Mat. Code is a material code of our product which is nothing but cement. The last one Inv Qt.(MT) is the invoice quantity or simply a quantity of cement which is sold.'

llm=OpenAI(api_token=openai_api_key,model='gpt-4')
agent=Agent(data, config={"llm": llm,"response_parser":StreamlitResponse,"verbose": True})
agent.add_message(initial_prompt)

def getQueryResult(prompt):
    result=agent.chat(prompt)
    result_type = type(result)
    print(result_type)
    if result_type == pd.DataFrame:
        st.dataframe(result)
        return (1,result)
    else:
        st.markdown(result)
        return (0,result)

# @skill
# def printInDataframeFormate(dataframe):
#     st.dataframe(data=dataframe)
# agent.add_skills(printInDataframeFormate)

st.title(body="Amrit Buddy")
st.markdown("""
<style>
    .e1nzilvr1 {
        text-align: center;
        color:#E74C3C;
    }
</style>
""", unsafe_allow_html=True)
st.dataframe(data)
st.markdown("""
<style>
    .e1vs0wn30 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)
# if initial == True:
#     getQueryResult(initial_prompt)
#     initial=False

if "messages" not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    if message['role']=="User":
        with st.chat_message(message['role'],avatar="user.webp"):
            st.markdown(message['content'])
    else:
        with st.chat_message(message['role'],avatar="bot.png"):
            if message['content-type']==1:
                st.dataframe(message['content'])
            else:
                st.markdown(message['content'])




prompt = st.chat_input("Ask me anything.....")
if prompt is not None:
    with st.chat_message("User",avatar="user.webp"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"User","content":prompt})
    response=""
    with st.chat_message("Assistant",avatar="bot.png"): 
        resultT=getQueryResult(prompt)
        st.session_state.messages.append({"role":"assistant","content":resultT[1],"content-type":resultT[0]})

