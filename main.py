import html
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from llm import semantic_search, generate_context, docsearch
import openai
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"Hello": "World"}

chat_history = []
system_dict = {'role': 'system', 'content': 'You are assistant bot who looks through documents and answers questions.'}
chat_history.append(system_dict)
user_input_list = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            user_input = await websocket.receive_text()
            user_input_list.append(user_input)

            #if len(user_input_list) == 1:
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
            ai_dict['content'] = ai_response.choices[0].message.content
            chat_history.append(ai_dict)
            
            await websocket.send_text(f"{ai_response.choices[0].message.content}")
            await websocket.send_text(f"{context}")
    except:
        print("Connection closed due to inactivity.")