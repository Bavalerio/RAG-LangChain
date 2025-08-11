# Interactive PDF Reader 📖

An intelligent PDF reader application built with **Streamlit**, **LangChain**, and **OpenAI** that allows users to upload PDF documents and ask questions about their content using natural language processing.

![Interactive PDF Reader](https://github.com/user-attachments/assets/7480efdf-285f-4483-9fe1-666993cbf5e1)

## ✨ Features

- **📄 PDF Upload & Processing**: Upload any PDF document for analysis
- **🤖 AI-Powered Chat**: Ask questions about your PDF content using OpenAI's GPT models
- **🔍 Smart Search**: Vector-based search using HuggingFace embeddings for accurate context retrieval
- **📚 Interactive PDF Viewer**: Full-featured PDF viewer with zoom, navigation, and page controls
- **💬 Chat History**: Persistent conversation history during your session
- **🎯 Context-Aware Responses**: Displays relevant PDF pages alongside AI answers

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: LangChain, OpenAI GPT-3.5, HuggingFace Transformers
- **Vector Database**: ChromaDB
- **PDF Processing**: PyPDF2, LangChain PDF Loaders
- **Embeddings**: HuggingFace Sentence Transformers

## 📋 Prerequisites

- Python 3.8+
- OpenAI API Key
- HuggingFace API Token (optional, for better embedding models)

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/interactive-pdf-reader.git
   cd interactive-pdf-reader
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   
   Create a `.env` file in the root directory:
   ```bash
   # Required
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Optional (for enhanced embeddings)
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
   ```

   ### Getting API Keys:
   
   **OpenAI API Key**:
   1. Go to [OpenAI API Platform](https://platform.openai.com/)
   2. Create an account or sign in
   3. Navigate to API Keys section
   4. Create a new secret key
   5. Copy the key to your `.env` file
   
   **HuggingFace Token** (Optional):
   1. Go to [HuggingFace](https://huggingface.co/)
   2. Create an account and sign in
   3. Go to Settings > Access Tokens
   4. Create a new token
   5. Copy the token to your `.env` file

## 🏃‍♂️ Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```
   Or if `streamlit` command is not found:
   ```bash
   python3 -m streamlit run app.py
   ```

2. **Open your browser** and navigate to the displayed URL (typically `http://localhost:8501`)

3. **Upload a PDF**:
   - Click "Browse files" in the "Your documents" section
   - Select a PDF file from your computer
   - Click the "Process" button to analyze the document

4. **Ask questions**:
   - Type your question in the input field
   - Press Enter to get AI-powered answers
   - View the chat history in the expandable "Your Chat" section

5. **Browse relevant content**:
   - The right panel shows relevant PDF pages based on your questions
   - Use the PDF viewer controls to zoom, navigate, and explore

## 📁 Project Structure

```
interactive-pdf-reader/
├── app.py                 # Main Streamlit application
├── htmlTemplates.py       # CSS and HTML templates for chat UI
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## 💡 How It Works

1. **Document Processing**: 
   - PDF is uploaded and processed using PyPDF2 and LangChain's PyPDFLoader
   - Text is split into chunks for efficient processing

2. **Vector Embedding**: 
   - Document chunks are converted to vector embeddings using HuggingFace models
   - Embeddings are stored in ChromaDB for fast similarity search

3. **Question Answering**:
   - User questions are converted to embeddings
   - Similar document chunks are retrieved using vector search
   - OpenAI's GPT model generates answers using retrieved context

4. **PDF Display**:
   - Relevant page numbers are extracted from source documents
   - PDF pages are dynamically displayed with context (±2 pages)

## 🚨 Important Notes

- **API Costs**: This application uses OpenAI's API, which may incur costs based on usage
- **File Size**: Large PDF files may take longer to process and use more tokens
- **Internet Required**: The application requires an internet connection for API calls
- **Privacy**: PDFs are processed locally but questions/content are sent to OpenAI's API
