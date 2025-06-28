# 🔗 Smart URL Answer Bot

Extract insights and get answers from web content using AI-powered retrieval and question answering.

![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-ff4b4b)
![LangChain](https://img.shields.io/badge/LangChain-RAG-blueviolet)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🚀 Demo
🔗 **Live Demo (Streamlit Cloud)**: *Coming soon...*

---

## 📌 Features

- 🔍 Analyze up to 3 web URLs at a time
- 📚 Convert page content into vector embeddings
- 🧠 Ask questions and get accurate answers based on content
- 🧾 See cited sources and references
- 🎈 Stylish Streamlit UI with real-time status updates

---

## 🧠 Tech Stack

| Layer | Tech |
|-------|------|
| UI | Streamlit |
| LLM | Groq (LLaMA 3.3 70B) |
| Embeddings | HuggingFace - `gte-base-en-v1.5` |
| Vector DB | ChromaDB |
| Loader | `UnstructuredURLLoader` |
| Orchestration | LangChain |

---

## ⚙️ Installation

### 🖥️ Local Setup

```bash
git clone https://github.com/YOUR_USERNAME/smart-url-bot.git
cd smart-url-bot

# (Recommended) Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
