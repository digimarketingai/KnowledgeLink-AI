# -*- coding: utf-8 -*-

# 導入必要的函式庫
# Import necessary libraries
import gradio as gr
from openai import OpenAI

# --- 雙語 UI 文本與設定 ---
# --- Bilingual UI Text & Configuration ---

# 使用字典將使用者易於理解的顯示名稱映射到後端所需的技術模型標識符。
# A dictionary to map user-friendly display names to the required technical model identifiers.
MODEL_MAP = {
    # 顯示名稱 (鍵) : 技術 ID (值)
    # Display Name (Key) : Technical ID (Value)
    "Google: Gemini 2.0 Flash (Free)": "openrouter:google/gemini-2.0-flash-exp:free",
    "DeepSeek: DeepSeek R1 (Free)": "openrouter:deepseek/deepseek-r1:free",
    "Google: Gemma 3N 4B (Free)": "openrouter:google/gemma-3n-e4b-it:free",
    "Meta: Llama 4 Maverick (Free)": "openrouter:meta-llama/llama-4-maverick:free",
    "Moonshot: Kimi K2 (Free)": "openrouter:moonshotai/kimi-k2:free"
}

# --- 功能函式定義 ---
# --- Function Definitions ---

def chat_response(message, history, state):
    """
    處理與 AI 模型聊天互動的函式。
    Handles the chat interaction with the AI model.
    """
    client = state.get("client")
    system_prompt = state.get("system_prompt")
    model = state.get("model")

    if not all([client, system_prompt, model]):
        return "錯誤：AI服務未正確啟動。請重新整理頁面並完成設定。 / Error: The AI service has not been properly activated. Please refresh and complete the setup."

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
        return f"抱歉，發生錯誤：{e} / Sorry, an error occurred: {e}"

def activate_service(api_key, knowledge_file, model_display_name):
    """
    透過處理知識庫文件和設定 AI 客戶端來啟動聊天機器人服務。
    Activates the chatbot service by processing the knowledge file and setting up the AI client.
    """
    if not api_key or not api_key.strip():
        raise gr.Error(
            "API 金鑰為必填項目！ / API Key is required!",
            "請輸入您的 OpenRouter API 金鑰。 / Please enter your OpenRouter API key."
        )
    
    if knowledge_file is None:
        raise gr.Error(
            "缺少知識庫文件！ / Knowledge base file is missing!",
            "請上傳 .txt 格式的檔案。 / Please upload a .txt file."
        )
    
    if not model_display_name:
        raise gr.Error(
            "未選擇 AI 模型！ / AI Model not selected!",
            "請從下拉選單中選擇一個模型。 / Please choose a model from the dropdown list."
        )

    try:
        file_path = knowledge_file.name
        if not file_path.endswith('.txt'):
             raise gr.Error(
                "不支援的檔案格式！ / Unsupported file format!",
                "請僅上傳 .txt 檔案。 / Please upload only .txt files."
            )
        with open(file_path, 'r', encoding='utf-8') as f:
            knowledge_base = f.read()

    except Exception as e:
        raise gr.Error(
            f"讀取檔案時出錯：{e} / Error reading file: {e}",
            "請確保檔案是有效且未損壞的 .txt 檔案。 / Please ensure the file is a valid, uncorrupted .txt file."
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

    technical_model_name = MODEL_MAP[model_display_name]

    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=api_key,
    )

    new_state = {
        "client": client,
        "system_prompt": system_prompt,
        "model": technical_model_name
    }
    
    return new_state, gr.update(visible=False), gr.update(visible=True)

# --- Gradio UI 介面定義 ---
# --- Gradio UI Definition ---

with gr.Blocks(theme=gr.themes.Soft(), title="AI 知識庫客服 / KnowledgeLink AI Chatbot") as demo:
    state = gr.State({})

    with gr.Column(visible=True) as setup_view:
        gr.Markdown("# AI 聊天機器人啟動介面\n# KnowledgeLink AI Chatbot Activation")
        gr.Markdown("請提供您的 API 金鑰、選擇模型並上傳知識庫檔案以啟動服務。 / Please provide your API key, choose a model, and upload a knowledge base file to start.")
        
        model_dropdown = gr.Dropdown(
            label="選擇 AI 模型 / Choose an AI Model",
            choices=list(MODEL_MAP.keys()),
            value=list(MODEL_MAP.keys())[0],
            info="選擇用於聊天的 AI 模型。 / Select the AI model for the chat."
        )
        
        api_key_input = gr.Textbox(
            label="OpenRouter API 金鑰 / OpenRouter API Key",
            placeholder="在此貼上您的 sk-or-xxxxxxxx 金鑰 / Paste your sk-or-xxxxxxxx key here",
            type="password",
            info="您的金鑰僅用於本次會話，不會被儲存。 / Your key is used only for this session and is not stored."
        )
        
        knowledge_upload = gr.File(
            label="上傳知識庫文件（僅限 .txt） / Upload Knowledge Base File (.txt only)",
            file_types=['.txt']
        )
        
        activate_button = gr.Button("✅ 啟動 AI 聊天機器人 / Activate AI Chatbot", variant="primary")

    with gr.Column(visible=False) as chat_view:
        gr.Markdown("# AI 線上支援中心\n# AI Online Support Center")
        gr.Markdown("您好！我是您的 AI 助理，今天有什麼可以幫助您的嗎？ / Hello! I am your AI assistant. How can I help you today?")
        
        # --- FIX ---
        # Removed 'retry_btn', 'undo_btn', and 'clear_btn' parameters.
        # These are not supported in older versions of Gradio and were causing a TypeError.
        # The interface will now use the default buttons for your Gradio version.
        # --- 修正 ---
        # 移除了 'retry_btn', 'undo_btn', 和 'clear_btn' 參數。
        # 較舊的 Gradio 版本不支援這些參數，它們會導致 TypeError 錯誤。
        # 介面現在將使用您 Gradio 版本的預設按鈕。
        gr.ChatInterface(
            fn=chat_response,
            title="AI 知識庫客服 / KnowledgeLink AI Chatbot",
            examples=[["課程價格是多少？"], ["What are the course prices?"], ["Is there a free trial?"]],
            submit_btn="發送 / Send",
            additional_inputs=[state]
        )

    activate_button.click(
        fn=activate_service,
        inputs=[api_key_input, knowledge_upload, model_dropdown],
        outputs=[state, setup_view, chat_view]
    )

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
