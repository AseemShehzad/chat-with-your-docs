# Overview
This is a simple implementation of a chatbot using FastAPI and OpenAI's GPT-3 model. It uses Pinecone, a vector database for machine learning applications, and Langchain, a Python package for working with word embeddings, to provide semantic search functionality. The chatbot uses this semantic search capability to answer queries based on the data present in the Pinecone database.

## Files
The project contains these main files:

* main.py : The main script that uses FastAPI to start a web server and handle WebSocket communication with the client.
* llm.py : This script handles the semantic search and context generation for the chatbot.
* requirements.txt : Contains the Python packages required to run the chatbot.
* static/index.html : The main page of the chatbot application, written in HTML and JavaScript.
* static/styles.css : The stylesheet for the chatbot application, written in CSS.
## How to Run the Application
First, you need to install all the necessary Python packages. You can do this by running the following command in your terminal:
pip install -r requirements.txt

Next, you need to set up your Pinecone database and OpenAI key:

For Pinecone, you need to obtain an API key and the name of an existing index. Add these details to your config.py file.
For OpenAI, you need to obtain an API key. This key should also be added to your config.py file.
The config.py file should look something like this:

OPENAI_API_KEY = "your-openai-api-key"  
PINECONE_API_KEY = "your-pinecone-api-key"  
PINECONE_API_ENV = "your-pinecone-api-environment"  
PINECONE_INDEX = "your-pinecone-index-name"  
PINECONE_NAMESPACE = "your-pinecone-namespace"  

### Upsert your own Docs
Upload pdf documents in the folder "upsert/docs". Now, run ingest.py. You should your pinecone vector databases updated.

### Run your chatbot!

Now, you're ready to start the application. You can do this by running the following command in your terminal:

uvicorn main:app --reload --port 9090

This command will start a FastAPI server at http://localhost:9090.

Your chatbot should look like this:

https://drive.google.com/file/d/1c5daYjRh18vo0fH7IZCCcVdgx61hsk_I/view?usp=sharing)  

Now go to this URL to run the chatbot:

localhost:8080/static  

You should see the chat interface for your bot.

You can now interact with the chatbot. The chatbot will perform a semantic search based on your query, generate a context based on the search results, and use this context to generate a response using GPT-3.

Please note that the chatbot will not be able to answer your queries accurately if there is no relevant data in your Pinecone database. You may need to populate your Pinecone database with relevant data before you start the application.
