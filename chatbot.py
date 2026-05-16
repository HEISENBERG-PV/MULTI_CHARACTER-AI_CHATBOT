from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model(
    "google_genai:gemini-2.5-flash-lite"
)

print("----------AI CHATBOT----------")
print("----------PRESS 'e' TO EXIT----------")

while True:
    promt = input("You : ")
    if(promt == 'e'):
        break
    res = model.invoke(promt)
    
    print("AI : "+ res.content)