import google.generativeai as genai
from fastapi import HTTPException
from app.config import settings

SYSTEM_INSTRUCTION = """
You are an AI financial education tutor integrated into a stock market dashboard.
Your primary role is to help beginner investors understand stock market concepts, terminology, and how predictive models work conceptually.
You must STRICTLY adhere to the following rules:
1. ONLY answer questions related to finance, stock markets, economics, investing, or the features of this dashboard.
2. If the user asks about ANY other topic (e.g., cooking, coding unrelated to the app, general trivia, politics), politely decline and remind them you are an educational finance tutor.
3. Keep your answers clear, beginner-friendly, and concise.
4. DO NOT provide personalized financial advice (e.g., "should I buy AAPL?"). State clearly that any information is for educational purposes only.
"""

def get_chat_model():
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY is not configured on the server."
        )
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
    return model

async def generate_chat_response(messages: list) -> str:
    """
    Format expected from ui: [{'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'hi'}]
    Google GenAI SDK expects contents as `[{role: 'user', parts: [...]}, {role: 'model', parts: [...]}]`.
    """
    try:
        model = get_chat_model()
        
        formatted_history = []
        for msg in messages[:-1]:
            role = "model" if msg.get("role") == "assistant" else "user"
            formatted_history.append(
                {"role": role, "parts": [msg.get("content", "")]}
            )
            
        last_message = messages[-1].get("content", "")
        
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(last_message)
        
        return response.text
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat generation failed: {str(e)}")
