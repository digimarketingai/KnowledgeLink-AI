# -*- coding: utf-8 -*-
import gradio as gr
from openai import OpenAI
import os
import sys
import warnings
import argparse
import time

# Suppress known warnings to keep the console output clean
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- Model Configuration ---
MODEL_NAME = "meta-llama/llama-4-maverick:free"

# --- Core Functions ---
def chat_response(message, history, state):
    """
    Handles the chat logic by sending user messages to the OpenRouter API
    and returning the model's response.
    """
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
    """
    Reads a text file using multiple common encodings to ensure compatibility.
    Returns the file content as a string or None if reading fails.
    """
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
        gr.Markdown("# AI 線上支援中心\n# AI Online Support Center")
        gr.Markdown("您好！我是您的 AI 助理。/ Hello! I am your AI assistant.")
        gr.ChatInterface(
            fn=chat_response,
            type="messages",
            title="AI 知識庫客服 / KnowledgeLink AI Chatbot",
            examples=[["課程價格是多少？"], ["What are the course prices?"], ["Is there a free trial?"]],
            additional_inputs=[state]
        )

    try:
        # --- THIS IS THE CORRECTED LINE ---
        # Unpack the tuple correctly: the public URL is the THIRD item.
        _, _, public_url = demo.launch(share=True, prevent_thread_lock=True)
    except Exception as e:
        print(f"Could not launch Gradio app: {e}", file=sys.stderr)
        sys.exit(1)

    if public_url:
        print("\n" + "="*80)
        print("✅ Gradio App is running on a public URL!")
        print(f"🔗 Public URL: {public_url}")
        print("\n👇 To embed this Gradio bot on your website, copy the following HTML code: 👇")
        
        embed_html = f'<iframe src="{public_url}" width="100%" height="600" style="border:none; min-height: 450px;" title="Gradio Chatbot"></iframe>'
        
        print("\n" + embed_html + "\n")
        print("="*80 + "\n")
    else:
        print("\n" + "="*80)
        print("⚠️  Could not create a public URL. The app is likely running locally only.")
        print("Please ensure your network connection is active and try again.")
        print("="*80 + "\n")


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down Gradio app...")
        demo.close()
        print("Gradio app shut down successfully.")
