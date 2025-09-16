#@title 🚀 All-in-One Chatbot Launcher
#@markdown 1.  **Enter your API Key** in the input box below.
#@markdown 2.  **Run this cell**. An upload button will appear after the initial setup.
#@markdown 3.  **Click "Choose Files"** and upload your `.txt` knowledge base file.
#@markdown 4.  The app will launch, and a clickable URL + embed code will be generated.
#@markdown ---
#@markdown 1. **在下方的輸入框中輸入您的 API 金鑰**。
#@markdown 2. **執行此儲存格**，初始設定後會出現上傳按鈕。
#@markdown 3. **點擊 "Choose Files"** 並上傳您的 `.txt` 知識庫檔案。
#@markdown 4. 應用程式將會啟動，並生成可點擊的網址與嵌入碼。

OPENROUTER_API_KEY = "" #@param {type:"string"}

import os
import subprocess
import re
import textwrap
from google.colab import files
from IPython.display import display, HTML, clear_output

# --- Python Code for app.py ---
APP_PY_CODE = textwrap.dedent("""
    # -*- coding: utf-8 -*-
    import gradio as gr
    from openai import OpenAI
    import os
    import sys
    import warnings
    import argparse # <-- NEW: Import argparse

    # Suppress known warnings to keep the log clean
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # --- Model Configuration ---
    MODEL_NAME = "openrouter:meta-llama/llama-4-maverick:free"

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
            
            completion = client.chat.completions.create(
                model=model,
                messages=messages_to_send
            )
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
        # NEW: Set up and parse command-line arguments
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

# --- HTML Template for the embed code ---
HTML_TEMPLATE = """
<div style="border: 2px solid #4CAF50; padding: 16px; border-radius: 10px; background-color: #f0fff0;">
<h3 style="font-family: sans-serif; color: #2E7D32;">✅ Your Chatbot is Live!</h3>
<p style="font-family: sans-serif; font-size: 1rem; color: #555;">
    <a href="{url}" target="_blank" style="font-size: 1.1rem; font-weight: bold; color: #1a73e8;">Click here to open your chatbot in a new tab.</a>
    <br><br>
    Or, copy the complete HTML code below to embed it on your website (e.g., Google Sites).<br>
    (或者，複製下方的完整 HTML 程式碼以嵌入您的網站。)
</p>
<pre style="background-color: #e0e0e0; border: 1px solid #ccc; border-radius: 8px; padding: 16px; white-space: pre-wrap; word-wrap: break-word; font-size: 0.9rem;"><code>&lt;iframe
    src="{url}"
    style="width: 100%; height: 700px; border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"
    allow="microphone"
    frameborder="0"
&gt;&lt;/iframe&gt;</code></pre>
</div>
"""

def run_app_and_generate_embed(api_key, knowledge_file_path):
    # NEW: Build the command with command-line arguments
    command = [
        "python", "-u", "app.py",
        "--api-key", api_key,
        "--knowledge-file", knowledge_file_path
    ]
    
    # The `env` argument is no longer needed
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8'
    )
    
    url_pattern = re.compile(r'(https?://[a-zA-Z0-9-]+\.gradio\.live)')
    
    print("🚀 Launching Gradio App... Please wait for the public URL.")
    print("🚀 正在啟動 Gradio 應用程式... 請等待公開網址生成。")
    print("-" * 60)

    for line in iter(process.stdout.readline, ''):
        print(line, end='')
        match = url_pattern.search(line)
        if match:
            url = match.group(1)
            clear_output(wait=True)
            display(HTML(HTML_TEMPLATE.format(url=url)))
            print("-" * 60)
            print("👇 Server logs will continue to appear below. 👇")
            print("👇 伺服器日誌將繼續顯示在下方。 👇")
            print("-" * 60)
    
    process.stdout.close()
    process.wait()

# --- Main Logic ---
if not OPENROUTER_API_KEY.strip():
    print("⚠️ Please enter your API key in the input box above and run the cell again.")
else:
    clear_output()
    print("⚙️ Starting setup...")
    print("   - Writing app.py and requirements.txt...")
    with open("app.py", "w", encoding="utf-8") as f: f.write(APP_PY_CODE)
    with open("requirements.txt", "w", encoding="utf-8") as f: f.write(REQUIREMENTS_TXT_CODE)
    print("   - Installing required packages...")
    subprocess.run(["pip", "install", "-q", "-r", "requirements.txt"], check=True)
    print("✅ Setup complete.")
    print("\n⬆️ Please upload your knowledge base .txt file:")
    uploaded = files.upload()
    
    if not uploaded:
        print("\n❌ No file uploaded. Please run the cell again and select a file.")
    else:
        file_name = next(iter(uploaded))
        if not file_name.endswith('.txt'):
            print(f"\n❌ Invalid file type: '{file_name}'. Please upload a .txt file.")
        else:
            clear_output()
            # NEW: Call the launcher with arguments instead of environment variables
            run_app_and_generate_embed(api_key=OPENROUTER_API_KEY, knowledge_file_path=file_name)
