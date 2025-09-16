#@title 🚀 All-in-One Interactive Chatbot Launcher (v6.0)
#@markdown 1.  **Enter your API Key** in the input box below.
#@markdown 2.  **Run this cell**. It will set up the environment, then prompt you to upload a file.
#@markdown 3.  **Click "Choose Files"** when it appears and upload your `.txt` knowledge base file.
#@markdown 4.  The app will launch automatically, and a clickable URL will appear in the output.
#@markdown ---
#@markdown 1. **在下方的輸入框中輸入您的 API 金鑰**。
#@markdown 2. **執行此儲存格**。它會先設定環境，然後提示您上傳檔案。
#@markdown 3. **當按鈕出現時，點擊 "Choose Files"** 並上傳您的 `.txt` 知識庫檔案。
#@markdown 4. 應用程式將自動啟動，可點擊的網址將會顯示在輸出中。

OPENROUTER_API_KEY = "" #@param {type:"string"}

import textwrap
import subprocess
import sys
from google.colab import files
from IPython.display import clear_output

# --- Python Code for app.py (with command-line argument support) ---
# This script is written to a file and is designed to be called from the command line.
APP_PY_CODE = textwrap.dedent("""
    # -*- coding: utf-8 -*-
    import gradio as gr
    from openai import OpenAI
    import os
    import sys
    import warnings
    import argparse # Use argparse to read command-line inputs

    # Suppress known warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # --- Model Configuration ---
    MODEL_NAME = "meta-llama/llama-4-maverick:free"

    # --- Core Functions ---
    def chat_response(message, history, state):
        api_key = state.get("api_key")
        system_prompt = state.get("system_prompt")
        model = state.get("model")

        if not all([api_key, system_prompt, model]):
            return "FATAL ERROR: Session state is incomplete. Please restart the application."

        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
            messages_to_send = [{"role": "system", "content": system_prompt}]
            messages_to_send.extend(history)
            messages_to_send.append({"role": "user", "content": message})
            completion = client.chat.completions.create(model=model, messages=messages_to_send)
            return completion.choices[0].message.content
        except Exception as e:
            print(f"API call failed: {e}", file=sys.stderr)
            return f"Sorry, an error occurred during the API call: {e}"

    def read_knowledge_file(file_path):
        knowledge_base = None
        encodings_to_try = ['utf-8', 'big5', 'gbk', 'utf-16', 'latin-1']
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    knowledge_base = f.read()
                print(f"Successfully read file with encoding: {encoding}")
                return knowledge_base
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        return None

    # --- Main Execution Block ---
    if __name__ == "__main__":
        # Set up and parse command-line arguments
        parser = argparse.ArgumentParser(description="Launch a Gradio chatbot with a knowledge base.")
        parser.add_argument("--api-key", required=True, help="Your OpenRouter API key.")
        parser.add_argument("--knowledge-file", required=True, help="Path to the .txt knowledge base file.")
        args = parser.parse_args()

        API_KEY = args.api_key
        KNOWLEDGE_FILE_PATH = args.knowledge_file
        
        knowledge_base = read_knowledge_file(KNOWLEDGE_FILE_PATH)
        if knowledge_base is None:
            print(f"FATAL ERROR: Could not read or decode the file at {KNOWLEDGE_FILE_PATH}", file=sys.stderr)
            sys.exit(1)

        system_prompt = f'''
        You are a professional customer service assistant. Your task is to answer user questions based only on the "Knowledge Base" below.
        Rules:
        1) Detect the user's language and reply in the same language.
        2) Do not invent information not present in the Knowledge Base.
        3) If the answer is not in the Knowledge Base, reply exactly: "This question is beyond the scope of my current knowledge. For more detailed assistance, you can contact customer support at support@digimarketingai.example.com."
        4) Be concise and helpful.

        --- KNOWLEDGE BASE ---
        {knowledge_base}
        --- END KNOWLEDGE BASE ---
        '''

        initial_state = {"api_key": API_KEY, "system_prompt": system_prompt, "model": MODEL_NAME}

        with gr.Blocks(theme=gr.themes.Soft(), title="AI 知識庫客服 / KnowledgeLink AI Chatbot") as demo:
            state = gr.State(value=initial_state)
            gr.Markdown("# AI 線上支援中心\\n# AI Online Support Center")
            gr.Markdown("您好！我是您的 AI 助理。/ Hello! I am your AI assistant.")
            gr.ChatInterface(
                fn=chat_response,
                type="messages",
                title="AI 知識庫客服 / KnowledgeLink AI Chatbot",
                examples=[["課程價格是多少？"], ["What are the course prices?"], ["Is there a free trial?"]],
                additional_inputs=[state]
            )

        demo.launch(share=True, debug=False)
""")

# --- Content for requirements.txt ---
REQUIREMENTS_TXT_CODE = """
gradio
openai
"""

# --- Main Logic for the Colab Cell ---
if not OPENROUTER_API_KEY.strip():
    print("⚠️ Please enter your API key in the input box above and run the cell again.")
else:
    # 1. SETUP PHASE
    clear_output()
    print("⚙️ Starting setup...")
    print("   - Writing app.py and requirements.txt...")
    with open("app.py", "w", encoding="utf-8") as f: f.write(APP_PY_CODE)
    with open("requirements.txt", "w", encoding="utf-8") as f: f.write(REQUIREMENTS_TXT_CODE)
    
    print("   - Installing required packages...")
    subprocess.run(["pip", "install", "-q", "-r", "requirements.txt"], check=True)
    print("✅ Setup complete.")
    
    # 2. INTERACTIVE INPUT PHASE
    print("\n⬆️ Please upload your knowledge base .txt file:")
    uploaded = files.upload()
    
    if not uploaded:
        print("\n❌ No file uploaded. Please run the cell again and select a file.")
    else:
        file_name = next(iter(uploaded))
        
        if not file_name.endswith('.txt'):
            print(f"\n❌ Invalid file type: '{file_name}'. Please upload a .txt file.")
        else:
            # 3. LAUNCH PHASE
            clear_output()
            print(f"✅ API Key received and '{file_name}' uploaded.")
            print("🚀 Launching chatbot... The Gradio UI link will appear below.")
            print("👇 Server logs will appear below the Gradio link. 👇")
            print("-" * 60)
            
            # Construct and run the command using the inputs.
            # get_ipython().system() is used to stream the live output from the command to the cell.
            command = f'python -u app.py --api-key "{OPENROUTER_API_KEY}" --knowledge-file "{file_name}"'
            get_ipython().system(command)
