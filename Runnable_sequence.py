from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv

load_dotenv()

model= ChatGoogleGenerativeAI(model='gemini-2.5-flash')

prompt1 = PromptTemplate(
    template='Generate joke on the {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Explain the {text} in a few words',
    input_variables=['text']
)

output_parser = StrOutputParser()

chains = RunnableSequence(prompt1,model,output_parser,prompt2,model,output_parser)

result= chains.invoke({'topic':'Relationship'})
print(result)