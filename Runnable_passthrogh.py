from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnablePassthrough,RunnableParallel
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
passthrogh= RunnablePassthrough()

joke_chain= RunnableSequence(prompt1,model,output_parser)

parallel_chain = RunnableParallel(
    {
        'joke': RunnablePassthrough(),
        'explanation': RunnableSequence(prompt2,model,output_parser)
    }
)
final_chain = RunnableSequence(joke_chain,parallel_chain)

result= final_chain.invoke({'topic':'Relationship'})
print(result)