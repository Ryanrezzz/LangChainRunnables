from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnablePassthrough,RunnableParallel,RunnableLambda
from dotenv import load_dotenv

load_dotenv()

model= ChatGoogleGenerativeAI(model='gemini-2.5-flash')
parser = StrOutputParser()

prompt1 = PromptTemplate(
    template='Generate 1 joke on the {topic}',
    input_variables=['topic']
)


joke_chain = RunnableSequence(prompt1,model,parser)

chains = RunnableParallel(
    {
        'joke':RunnablePassthrough(),
        'WordCount':RunnableLambda(lambda x: len(x.split()))

    }
   
)


final_chain= RunnableSequence(joke_chain,chains)


result= final_chain.invoke({'topic':'Relationship'})
print(result)