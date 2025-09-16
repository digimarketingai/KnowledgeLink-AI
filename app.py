# -*- coding: utf-8 -*-

# Import necessary libraries
# 導入必要的函式庫
import gradio as gr
import os
from openai import OpenAI
import textract

# --- Bilingual UI Text & Configuration ---
# --- 雙語 UI 文本與設定 ---

# A dictionary to map user-friendly display names to the required technical model identifiers.
# This allows the UI to be clean while the backend uses the correct code.
# 使用字典將使用者易於理解的顯示名稱映射到後端所需的技術模型標識符。
# 這樣可以讓 UI 介面更簡潔，同時確保後端使用正確的 API 代碼。
MODEL_MAP = {
    # Display Name (Key) : Technical ID (Value)
    # 顯示名稱 (鍵) : 技術 ID (值)
    "DeepSeek: DeepSeek R1": "openrouter:deepseek/deepseek-r1:free",
    "Moonshot: Kimi K2": "openrouter:moonshotai/kimi-k2:free",
    "Google: Gemini 2.0 Flash": "openrouter:google/gemini-2.0-flash-exp:free",
    "Google: Gemini 2.5 Flash": "openrouter:google/gemini-2.5-flash-image-preview:free",
    "Google: Gemma 3N 4B": "openrouter:google/gemma-3n-e4b-it:free",
    "Meta: Llama 4 Maverick": "openrouter:meta-llama/llama-4-maverick:free"
}

# --- Function Definitions ---
# --- 功能函式定義 ---

def chat_response(message, history, state):
    """
    Handles the chat interaction with the AI model.
    處理與 AI 模型聊天互動的函式。
    """
    client = state.get("client")
    system_prompt = state.get("system_prompt")
    model = state.get("model")

    if not all([client, system_prompt, model]):
        return "Error: The AI service has not been properly activated. Please refresh and complete the setup. / 錯誤：AI服務未正確啟動。請重新整理頁面並完成設定。"

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        print(f"API call failed: {e}")
        return f"Sorry, an error occurred: {e} / 抱歉，發生錯誤：{e}"

def activate_service(api_key, knowledge_file, model_display_name):
    """
    Activates the chatbot service by processing the knowledge file and setting up the AI client.
    透過處理知識庫文件和設定 AI 客戶端來啟動聊天機器人服務。
    """
    if not api_key or not api_key.strip():
        raise gr.Error(
            "API Key is required! / API 金鑰為必填項目！",
            "Please enter your OpenRouter API key. / 請輸入您的 OpenRouter API 金鑰。"
        )
    
    if knowledge_file is None:
        raise gr.Error(
            "Knowledge base file is missing! / 缺少知識庫文件！",
            "Please upload a .txt, .doc, or .docx file. / 請上傳 .txt, .doc, 或 .docx 格式的檔案。"
        )
    
    if not model_display_name:
        raise gr.Error(
            "AI Model not selected! / 未選擇 AI 模型！",
            "Please choose a model from the dropdown list. / 請從下拉選單中選擇一個模型。"
        )

    try:
        file_path = knowledge_file.name
        
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                knowledge_base = f.read()
        elif file_path.endswith(('.doc', '.docx')):
            knowledge_bytes = textract.process(file_path)
            knowledge_base = knowledge_bytes.decode('utf-8')
        else:
            raise gr.Error(
                "Unsupported file format! / 不支援的檔案格式！",
                "Please upload only .txt, .doc, or .docx files. / 請僅上傳 .txt, .doc, 或 .docx 檔案。"
            )

    except Exception as e:
        raise gr.Error(
            f"Error reading or processing file: {e} / 讀取或處理檔案時出錯：{e}",
            "Please ensure the file is not corrupted and is in the correct format. / 請確保檔案未損壞且格式正確。"
        )

    system_prompt = f"""
    You are a professional customer service assistant. Your primary task is to answer user questions based *only* on the "Knowledge Base" provided below.
    Your instructions are:
    1.  First, detect the language of the user's question (e.g., English or Chinese).
    2.  You MUST answer in the SAME language as the user's question.
    3.  NEVER invent any information that is not in the "Knowledge Base".
    4.  If the user's question cannot be answered using the "Knowledge Base", you MUST politely reply with this exact phrase in the user's language: "This question is beyond the scope of my current knowledge. For more detailed assistance, you can contact customer support at support@digimarketingai.example.com."
    5.  Be concise and helpful.

    --- KNOWLEDGE BASE ---
    {knowledge_base}
    --- END KNOWLEDGE BASE ---
    """

    # Look up the technical model name from the display name selected by the user.
    # 根據使用者選擇的顯示名稱，查找對應的技術模型名稱。
    technical_model_name = MODEL_MAP[model_display_name]

    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=api_key,
    )

    new_state = {
        "client": client,
        "system_prompt": system_prompt,
        "model": technical_model_name  # Store the correct technical name for the API call.
    }
    
    return new_state, gr.update(visible=False), gr.update(visible=True)

# --- Gradio UI Definition ---
# --- Gradio UI 介面定義 ---

with gr.Blocks(theme=gr.themes.Soft(), title="KnowledgeLink AI Chatbot / AI 知識庫客服") as demo:
    state = gr.State({})

    with gr.Column(visible=True) as setup_view:
        gr.Markdown("# KnowledgeLink AI Chatbot Activation\n# AI 聊天機器人啟動介面")
        gr.Markdown("Please provide your API key, choose a model, and upload a knowledge base file to start. / 請提供您的 API 金鑰、選擇模型並上傳知識庫檔案以啟動服務。")
        
        model_dropdown = gr.Dropdown(
            label="Choose an AI Model / 選擇 AI 模型",
            choices=list(MODEL_MAP.keys()),  # Show user-friendly names in the dropdown.
            value=list(MODEL_MAP.keys())[0], # Default to the first model's friendly name.
            info="Select the AI model for the chat. / 選擇用於聊天的 AI 模型。"
        )
        
        api_key_input = gr.Textbox(
            label="OpenRouter API Key / OpenRouter API 金鑰",
            placeholder="Paste your sk-or-xxxxxxxx key here / 在此貼上您的 sk-or-xxxxxxxx 金鑰",
            type="password",
            info="Your key is used only for this session and is not stored. / 您的金鑰僅用於本次會話，不會被儲存。"
        )
        
        knowledge_upload = gr.File(
            label="Upload Knowledge Base File (.txt, .doc, .docx) / 上傳知識庫文件",
            file_types=['.txt', '.doc', '.docx'],
            info="Upload the document that the AI will use as its knowledge source. / 上傳 AI 將用作知識來源的文件。"
        )
        
        activate_button = gr.Button("✅ Activate AI Chatbot / 啟動 AI 聊天機器人", variant="primary")

    with gr.Column(visible=False) as chat_view:
        gr.Markdown("# AI Online Support Center\n# AI 線上支援中心")
        gr.Markdown("Hello! I am your AI assistant. How can I help you today? / 您好！我是您的 AI 助理，今天有什麼可以幫助您的嗎？")
        
        gr.ChatInterface(
            fn=chat_response,
            title="KnowledgeLink AI Chatbot / AI 知識庫客服",
            examples=[["What are the course prices?"], ["課程價格是多少？"], ["Is there a free trial?"]],
            submit_btn="Send / 發送",
            retry_btn="Retry / 重試",
            undo_btn="Undo / 復原",
            clear_btn="Clear / 清除對話",
            additional_inputs=[state]
        )

    activate_button.click(
        fn=activate_service,
        inputs=[api_key_input, knowledge_upload, model_dropdown],
        outputs=[state, setup_view, chat_view]
    )

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
