import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader, PdfWriter
from tempfile import NamedTemporaryFile
import base64
from htmlTemplates import expander_css, css, bot_template, user_template

# Set Up the API Keys
load_dotenv()

# Create the Web Page Layout
def main():
    st.set_page_config(page_title="Interactive PDF Reader", page_icon="📖", layout="wide")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "page_number" not in st.session_state:
        st.session_state.page_number = None
    if "pdf_file" not in st.session_state:
        st.session_state.pdf_file = None
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.title("Interactive Reader 📖")
        st.write("Ask a question from the PDF:")
        user_question = st.text_input("", placeholder="What is the time complexity of the divide and conquer algorithm?")
        
        # Chat History Section
        with st.expander("Your Chat", expanded=True):
            st.markdown(expander_css, unsafe_allow_html=True)
            st.write(css, unsafe_allow_html=True)
            if user_question:
                handle_userinput(user_question)
        
        # Documents Upload Section
        st.subheader("Your documents")
        st.write("Upload your PDF here and click on 'Process'")
        pdf_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
        
        if st.button("Process"):
            if pdf_file is not None:
                with st.spinner("Processing"):
                    st.session_state.conversation = process_file(pdf_file)
                    st.session_state.pdf_file = pdf_file
                st.success("Processing complete!")
            else:
                st.warning("Please upload a PDF file first.")
    
    with col2:
        # Apply custom CSS
        st.markdown(expander_css, unsafe_allow_html=True)
        
        # Display PDF pages based on user queries
        if st.session_state.pdf_file and st.session_state.page_number is not None:
            pdf_display = extract_and_display_pdf_pages(st.session_state.pdf_file, st.session_state.page_number)
            if pdf_display:
                st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.info("No PDF pages to display.")
        elif st.session_state.pdf_file:
            st.info("Ask a question to see relevant PDF pages.")
        else:
            st.info("Upload and process a PDF to see preview.")


# Function to Process the Input File
def process_file(pdf_file):
    # Create embeddings object using HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Save the uploaded file temporarily and load it
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_file_path = tmp_file.name
    
    # Load PDF document
    loader = PyPDFLoader(tmp_file_path)
    documents = loader.load_and_split()
    
    # vector store using Chroma
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    # return conversation chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0),
        retriever=vectorstore.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True
    )
    
    return conversation_chain

# Set Up the Chatbot
def handle_userinput(user_question):
    if st.session_state.conversation is not None:
        # Get response from the conversation chain
        response = st.session_state.conversation({
            'question': user_question,
            'chat_history': st.session_state.chat_history
        })
        
        # Append question and response to chat history
        st.session_state.chat_history.append((user_question, response['answer']))
        
        # Get page number from source documents if available
        if response.get('source_documents'):
            # Extract page number from the first source document
            source_doc = response['source_documents'][0]
            if hasattr(source_doc, 'metadata') and 'page' in source_doc.metadata:
                st.session_state.page_number = source_doc.metadata['page']
        
        # Update the chat display
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            st.write(user_template.replace("{{MSG}}", question), unsafe_allow_html=True)
            st.write(bot_template.replace("{{MSG}}", answer), unsafe_allow_html=True)
    else:
        st.warning("Please upload and process a PDF file first.")

# Respond to User Queries
def extract_and_display_pdf_pages(pdf_file, page_number):
    if pdf_file is not None and page_number is not None:
        # Read the PDF
        pdf_reader = PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)
        
        # Determine start and end pages (add context pages before and after)
        start_page = max(0, page_number - 2)
        end_page = min(total_pages - 1, page_number + 2)
        
        # Create a new PDF with the selected pages
        pdf_writer = PdfWriter()
        for page_num in range(start_page, end_page + 1):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        
        # Save the extracted pages to a temporary file
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf_writer.write(tmp_file)
            tmp_file_path = tmp_file.name
        
        # Read the temporary file and encode it
        with open(tmp_file_path, "rb") as f:
            pdf_data = f.read()
            
        # Encode to base64 for display
        base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
        
        # Create iframe HTML
        pdf_display = f'''
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}#toolbar=1&navpanes=1&scrollbar=1&page=1&zoom=FitH" 
            width="100%" 
            height="95vh" 
            type="application/pdf" 
            style="border: none; min-height: 800px;">
        </iframe>
        '''
        
        return pdf_display
    return None


if __name__ == "__main__":
    main()