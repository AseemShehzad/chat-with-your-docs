from langchain import document_loaders, embeddings, vectorstores
import pinecone
from langchain.text_splitter import TokenTextSplitter
import sys
sys.path.append('./')
import config


docs = document_loaders.DirectoryLoader('upsert\docs').load()

text_splitter = TokenTextSplitter(chunk_size=1200, chunk_overlap=100)
print(f"{len(docs)} documents loaded. Splitting into chunks...")

doc_string = ""
for doc in docs:
    doc_string = doc.page_content + doc_string + " I love you"
    
chunks = text_splitter.split_text(doc_string)
print(f"{len(chunks)} chunks created.")

### Change Embeddings Here!
openai_embeddings = embeddings.openai.OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
print("Embeddings loaded.")
### initialize pinecone
pinecone.init(
    api_key= config.PINECONE_API_KEY,  # find at app.pinecone.io
    environment= config.PINECONE_API_ENV  # next to api key in console
)
print("Pinecone initialized.")
db = vectorstores.Pinecone.from_texts(chunks, embedding=openai_embeddings, index_name=config.PINECONE_INDEX, namespace=config.PINECONE_NAMESPACE)
print("Database created.")