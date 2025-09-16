
### 繁體中文說明 (Traditional Chinese)

**KnowledgeLink AI** 是一個強大的、可快速部署的 AI 客服聊天機器人。它能讀取您提供的知識庫文件（.txt, .doc, .docx），並透過一個公開的 Web 介面，為您的用戶提供即時、準確的雙語問答服務。

無論您是想為您的線上課程、產品或服務建立一個初步的客服管道，KnowledgeLink AI 都能在幾分鐘內完成部署，無需複雜的伺服器設定。

#### ✨ 主要功能

- **動態知識庫**：支援上傳 `.txt`, `.doc`, 和 `.docx` 檔案作為 AI 的知識來源。
- **雙語支援**：能自動偵測用戶的語言（英文/中文），並以相同語言回應。
- **友善的模型選擇介面**：可從下拉選單中選擇 AI 模型，名稱清晰易懂。
- **安全金鑰管理**：API 金鑰在 Web UI 中臨時輸入，不會硬編碼在程式碼中，提升安全性。
- **快速部署**：專為簡單設定而設計，只需幾個指令即可啟動。
- **公開存取**：使用 Gradio 自動產生公開的 Web UI 連結，方便分享給任何人使用。
- **高度客製化**：您可以輕鬆修改 `app.py` 中的系統提示和模型列表，來改變 AI 的角色、規則及可用模型。

#### 🚀 如何部署

請依照以下步驟啟動您的 AI 客服。

1.  **複製此 GitHub 專案**

    在您的終端機中執行此指令，將專案複製到您的環境中。
    ```bash
    git clone https://github.com/digimarketingai/KnowledgeLink-AI.git
    ```

2.  **進入專案目錄**
    ```bash
    cd KnowledgeLink-AI
    ```

3.  **安裝系統依賴套件**

    解析 `.doc` 檔案需要 `antiword` 工具。在 Debian/Ubuntu 系統上，可使用此指令安裝：
    ```bash
    sudo apt-get update && sudo apt-get install -y antiword
    ```

4.  **安裝 Python 套件**

    此指令會讀取 `requirements.txt` 檔案並安裝所有必要的 Python 函式庫。
    ```bash
    pip install -r requirements.txt
    ```

5.  **執行應用程式**

    執行此指令後，應用程式將啟動並在終端機輸出中提供一個公開的 Gradio 連結。
    ```bash
    python app.py
    ```

#### 🛠️ 如何使用 Web UI

1.  點擊終端機輸出中以 `.gradio.live` 結尾的公開網址。
2.  在開啟的網頁中，您會看到完全雙語的**設定介面**：
    -   從顯示易懂名稱的下拉式選單中**「Choose an AI Model / 選擇 AI 模型」**。
    -   **「Enter your OpenRouter API Key / 輸入您的 OpenRouter API 金鑰」**。
    -   **「Upload your knowledge base file / 上傳您的知識庫文件」**（例如 `.docx` 或 `.txt` 檔案）。
3.  點擊 **「✅ Activate AI Chatbot / 啟動 AI 聊天機器人」** 按鈕。
4.  介面將切換至**聊天模式**，您現在可以用英文或中文開始提問了！

---

# 🤖 KnowledgeLink AI Chatbot

This document is available in English and Traditional Chinese. | 本文提供英文與繁體中文版本。

---

### English

**KnowledgeLink AI** is a powerful, rapidly deployable AI customer service chatbot. It reads knowledge base documents you provide (.txt, .doc, .docx) and offers real-time, accurate, bilingual Q&A services to your users through a public web interface.

Whether you want to create an initial customer support channel for your online course, product, or service, KnowledgeLink AI can be deployed in minutes without complex server configurations.

#### ✨ Key Features

- **Dynamic Knowledge Base**: Supports uploading `.txt`, `.doc`, and `.docx` files as the AI's source of knowledge.
- **Bilingual Support**: Automatically detects the user's language (English/Chinese) and responds in the same language.
- **User-Friendly Model Selection**: Choose from a dropdown list of AI models with clear, easy-to-understand names.
- **Secure API Key Handling**: The API key is entered temporarily in the web UI and is not hard-coded, enhancing security.
- **Rapid Deployment**: Designed for an easy setup with just a few simple commands.
- **Public Access**: Automatically generates a public web UI link using Gradio, making it easy to share with anyone.
- **Highly Customizable**: Easily modify the system prompt and model list in `app.py` to change the AI's role, rules, and available models.

#### 🚀 How to Deploy

Follow the steps below to launch your AI chatbot.

1.  **Clone This Repository**

    Run this command in your terminal to clone the project to your environment.
    ```bash
    git clone https://github.com/digimarketingai/KnowledgeLink-AI.git
    ```

2.  **Navigate to the Project Directory**
    ```bash
    cd KnowledgeLink-AI
    ```

3.  **Install System Dependencies**

    The `antiword` tool is required to parse `.doc` files. On Debian-based systems (like Ubuntu), you can install it with:
    ```bash
    sudo apt-get update && sudo apt-get install -y antiword
    ```

4.  **Install Python Packages**

    This command reads the `requirements.txt` file and installs all necessary Python libraries.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Application**

    After running this command, the application will start and provide a public Gradio link in the output.
    ```bash
    python app.py
    ```

#### 🛠️ How to Use the Web UI

1.  Click the public URL ending in `.gradio.live` from the terminal output.
2.  In the web page that opens, you will see the **Setup Interface**, which is fully bilingual:
    -   **Choose an AI Model / 選擇 AI 模型** from the dropdown menu of friendly names.
    -   **Enter your OpenRouter API Key / 輸入您的 OpenRouter API 金鑰**.
    -   **Upload your knowledge base file / 上傳您的知識庫文件** (e.g., a `.docx` or `.txt` file).
3.  Click the **"✅ Activate AI Chatbot / 啟動 AI 聊天機器人"** button.
4.  The interface will switch to the **Chat Mode**, and you can now start asking questions in either English or Chinese!
