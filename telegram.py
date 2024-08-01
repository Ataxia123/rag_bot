# from prompts.react import prompt_react
from tools.utils import get_today_date_tool, get_summarized_text_tool
from tools.tavily import web_search_tool
from tools.retrieval_eventi import get_relevant_document_tool
import os
import telepot
import time
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import re
from dotenv import load_dotenv

load_dotenv(override=True)

# Tools

TELEGRAM_BOT_ID = os.getenv("TELEGRAM_BOT_ID")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")

tools = [
    get_relevant_document_tool,
    get_today_date_tool,
    web_search_tool,
    get_summarized_text_tool,
]
retrieved_text = ""

# Load ReAct prompt
prompt_react = hub.pull("hwchase17/react")

# Initialize ChatGroq model for language understanding
model = ChatOpenAI(
    model_name="meta-llama/Meta-Llama-3.1-8B-Instruct",
    base_url="http://vllm:8000/v1",
    temperature=0,
)

# Create ReAct agent
react_agent = create_react_agent(model, tools=tools, prompt=prompt_react)
react_agent_executor = AgentExecutor(
    agent=react_agent, tools=tools, verbose=True, handle_parsing_errors=True
)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        try:
            # name = msg["first_name"]
            response = react_agent_executor.invoke({"input": msg["text"].split(" ")})

            # #traduci
            # prompt_template = ChatPromptTemplate.from_template("Traduci {text} in italiano. Restituisci solo la traduzione fedele senza commenti aggiuntivi. Non restituire dizionari, solo stringhe, senza virgolette. La traduzione: ")
            # chain = ( {"text": RunnablePassthrough() } | prompt_template | model  )
            # res=chain.invoke({"text": response['output']}).content
            # res=re.sub(r'\n', '', res)
            # res=re.sub(r'\\', '', res)
            bot.sendMessage(TELEGRAM_GROUP_ID, response["output"])

        except Exception as e:
            bot.sendMessage(TELEGRAM_GROUP_ID, "Ho avuto un problema!")
            bot.sendMessage(TELEGRAM_GROUP_ID, e)

    # elif content_type == 'photo':
    # bot.sendPhoto(TELEGRAM_GROUP_ID, )
    else:
        response = bot.sendMessage(TELEGRAM_GROUP_ID, "Non ho capito!")


bot = telepot.Bot(TELEGRAM_BOT_ID)
bot.message_loop(on_chat_message)
print("In attesa di nuovi messaggi...")

while 1:
    time.sleep(10)
