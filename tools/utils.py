from langchain.agents import Tool


def get_today_date(input: str) -> str:
    import datetime

    today = datetime.date.today()
    return f"\n {today} \n"


def get_summarized_text(text: str) -> str:
    from langchain_openai import ChatOpenAI
    from langchain.chains.summarize import load_summarize_chain

    llm = ChatOpenAI(temperature=0, model_name="meta-llama/Meta-Llama-3.1-8B-Instruct")
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.invoke(text)


get_today_date_tool = Tool(
    name="Ottieni data",
    func=get_today_date,
    description="Useful for getting today's date",
)

get_summarized_text_tool = Tool(
    name="Get Summarized Text",
    func=get_summarized_text,
    description="Useful for getting summarized text for any document.",
)
