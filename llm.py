import config
from langchain import vectorstores, embeddings, PromptTemplate
import pinecone
import openai

#### this module creates a qa chain. it feeds the existing database on pinecone as context

### Change Embeddings Here!
openai_embeddings = embeddings.openai.OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)

### initialize pinecone
pinecone.init(
    api_key= config.PINECONE_API_KEY,  # find at app.pinecone.io
    environment= config.PINECONE_API_ENV  # next to api key in console
)

### load database from pinecone
docsearch = vectorstores.Pinecone.from_existing_index(index_name= config.PINECONE_INDEX,
                                                      embedding=openai_embeddings, 
                                                      namespace=config.PINECONE_NAMESPACE)


def semantic_search(query, database):

    relevant_data_list = database.similarity_search_with_score(query, k=2)
    relevant_data_string = ""

    for relevant_data in relevant_data_list:
        distance = relevant_data[1]
        
        if distance > 0.25:
            relevant_data_string = relevant_data_string + relevant_data[0].page_content
    
    if len(relevant_data_string) == 0:
        relevant_data_string = "No Information found!"
    return relevant_data_string

def generate_context(search_function, query, database):
    context_template = """
    I am provding you with the context to answer the questions at the end of the prompt! Here is the context: {context} \n\n####\n Stick to the context and answer the questions at the end of the prompt. If no context is provided, let me know! \n\n####\n Question:
    """

    context_prompt_template = PromptTemplate(input_variables=["context"], template=context_template)

    context_prompt = (context_prompt_template.format(context= search_function(query, database)))
    return context_prompt

chat_history = []
system_dict = {'role': 'system', 'content': 'You are an AI search engine'}
chat_history.append(system_dict)

user_input = "What boundary conditions were used in the study? Give answer in detail. The context must be related to velocity and pressure boundary condition, maybe include simulation conditions"

user_input_list = []
user_input_list.append(user_input)

if len(user_input_list) == 1:
    context = generate_context(semantic_search, user_input, database=docsearch)
    user_input = context + user_input

user_dict = {'role': 'user'}
user_dict['content'] = user_input
chat_history.append(user_dict)

    
ai_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=chat_history,
    temperature = .7
)
ai_dict = {'role': 'assistant'}
ai_dict['content'] = ai_response
chat_history.append(ai_dict)

