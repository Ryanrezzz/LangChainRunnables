from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnablePassthrough,RunnableBranch
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
parser = StrOutputParser()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']

)

prompt2= PromptTemplate(
    template ='Summarize the given {text}',
    input_variables =['text']
)

report_chain = RunnableSequence(prompt1,model,parser)

chain = RunnableBranch(
    (lambda x: len(x.split())>200, RunnableSequence(prompt2,model,parser)),
    RunnablePassthrough()
)

final_chain = RunnableSequence(report_chain,chain)

result = final_chain.invoke({'topic':'AI'})
print(result)

final_chain.get_graph().print_ascii()