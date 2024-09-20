import os
import time
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from typing import Optional

st.set_page_config(layout="wide")

# Load environment variables
load_dotenv()

APP_ST_TITLE = "Semantic NLQuery Interface"
APP_ST_SUBHEADER = "Advanced Natural Language Querying for Databases and Documents"
APP_REFRESH_DOCUMENT_LOADER_INTERVAL = 60 * 60 * 3

DOCUMENT_LOADER_BASE_DIR_MAIN = "/bdax/artifact/"
DOCUMENT_LOADER_BASE_DIR_BACKUP = "data/"
DOCUMENT_LOADER_BASE_DIR = DOCUMENT_LOADER_BASE_DIR_MAIN if os.path.exists(DOCUMENT_LOADER_BASE_DIR_MAIN) else DOCUMENT_LOADER_BASE_DIR_BACKUP 
print(f"DOCUMENT_LOADER_BASE_DIR: {DOCUMENT_LOADER_BASE_DIR}")

def main():       
    st.title(APP_ST_TITLE)
    st.subheader(APP_ST_SUBHEADER)    

    if "vectorstore" not in st.session_state:
        pass 

    conversation_context = st.session_state.get("conversation_context", [])

    if "conversation_context" not in st.session_state: 
        st.session_state["conversation_context"] = []
    
    conversation_context = st.session_state.conversation_context
    db_name = 'aquarium.db'
    
    col1, col2 = st.columns([1, 1])    
    
    st.markdown("""
    <style>
    .main > div {
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stColumn {
        gap: 1rem;
    }
    .scrollable-history {
        height: 900px;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 10px;
        background-color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)    

    with col1:
        st.subheader("Conversation Interface")
        enable_llm_mode = st.checkbox("Enable LLM-enhanced mode", False)
        mode = st.radio(
            "Select mode:",
            ("Natural Language to SQL Query", "Document Search"),
            index=0,
            disabled=enable_llm_mode
        )        
        
        if mode == "Document Search":
            upload_files = st.checkbox("Upload your files", key="upload_files_checkbox")
            if upload_files:                    
                uploaded_files = st.file_uploader(
                    "Choose files to upload", 
                    accept_multiple_files=True,
                    type=["pdf", "txt", "csv", "md", "json", "xml", "sql", "python", "r"],  
                    key="file_uploader"
                )
                
                if uploaded_files:
                    for file in uploaded_files:
                        st.write(f"Filename: {file.name}")
                        
        query = st.text_area("Enter your natural language query here...:", placeholder="Select few data from stocks table (refer to [Vector DB Tips] section below)")
            
        if st.button("Execute Query"):
                if enable_llm_mode:
                    prompt = f"{query}: {conversation_context[-1:] if conversation_context else []}"                    
                    print(f"prompt [query:conversation_context_last] : {prompt}")
                    
                    llm_result = None  # Simulate an LLM result here
                    st.write("LLM Result:")
                    st.write(llm_result)
                    
                    conversation_context.append(f"<b>LLM Query:</b> {query}")
                    conversation_context.append(f"<b>LLM Result:</b> {llm_result}")                    
                    print(f"conversation_context [LLM]: {conversation_context}")
                else:
                    if mode == "Natural Language to SQL Query":
                        sql_query = None
                        vector_db_result = None  # Simulate a result

                        st.write("Vector DB to SQLite Result:")
                        if isinstance(vector_db_result, pd.DataFrame):
                            st.dataframe(vector_db_result)
                        else:
                            st.write(vector_db_result)

                        st.write("Generated SQL Query:")
                        st.code(sql_query, language='sql')                    
                
                        conversation_context.append(f"<b>Vector DB Query:</b> {query}")
                        conversation_context.append(f"<b>Generated SQL Query:</b> {sql_query}")
                        if isinstance(vector_db_result, pd.DataFrame):
                            conversation_context.append(f"<b>Vector DB Result:</b> <pre>{vector_db_result.to_string()}</pre>")
                        else:
                            conversation_context.append(f"<b>Vector DB Result:</b> {vector_db_result}")
                        print(f"conversation_context [Vector]: {conversation_context}")
                    else:
                        if upload_files:
                            question_answered = None  # Simulate an answer
                            conversation_context.append(f"<b>RAG2 Query:</b> {query}")
                            conversation_context.append(f"<b>RAG2 Result:</b> {question_answered}")
                            print(f"conversation_context [RAG2]: {conversation_context}")                                
                        else:
                            rag_result = st.session_state.chain.invoke(query)  # Simulate a result
                            print(rag_result)
                            st.write("Vector DB Result:")
                            st.write(rag_result)
                            
                            conversation_context.append(f"<b>RAG Query:</b> {query}")
                            conversation_context.append(f"<b>RAG Result:</b> {rag_result}")
                            print(f"conversation_context [RAG]: {conversation_context}")            

                if len(conversation_context) > 10:
                    st.session_state.conversation_context = conversation_context[-10:]
                else:
                    st.session_state.conversation_context = conversation_context        
                              
    with col2:        
        st.subheader("Conversation History") 
        history_html = "<div class='scrollable-history'>"
        for message in reversed(st.session_state.conversation_context):
            history_html += f"<p>{message}</p>"
        history_html += "</div>"
        st.markdown(history_html, unsafe_allow_html=True)       
    
    new_content = """
        <div>        
        <blockquote>
        The GPT Workbook [aLLMatters] has a range of useful features, including tools for masking/redacting personally identifiable information (PII), reality checking, adaptive processing, generative multi-modal image processing, and support for UDF (using Python) for pre-processed prompt data. It also includes a Workbook & topic feature, pre-defined prompts, and artifacts available in both plain text and HTML formats.
            <cite> - BMK</cite>
        </blockquote>
        <blockquote>
            <b>Tables in Vector DB</b>: stock_prices, GMINER_PORTFOLIO, GOLF_CC_ADDRESS<br>
            <b>Query Examples</b>:<br>
            "Select sample data in gminer_portfolio"<br>
            "Show few data for the Citigroup (SYMBOL = C) in gminer_portfolio"<br>            
            "Find the sample date for Citigroup (SYMBOL = C) having highest close price in gminer_portfolio" -> (LLM) "find 1) the list of executives and 2) company news on that day for this stock and 3) stock prices for the competitors (JPM, Goldman Sachs, Morgan Stanley)"<br>
            "Find the trading_date for Citigroup (SYMBOL = C) having highest close in gminer_portfolio and show the trading date and close price" -> (LLM) "list all CEOs for these stocks"<br>
            "Find the trading date for Citigroup (SYMBOL = C) having highest close in GMINER_PORTFOLIO table and show all unique stocks (SYMBOL) with trading date and close and volume of which close is bigger than Citigroup (SYMBOL = C) on the trading date"<br>
            "Show few sample data in golf_cc_address"<br>
            "Retrieve all the information from the golf_cc_address, but only show the first 10 entries"<br>
            "Show few sample data and correct_address contains NSW in golf_cc_address" -> (LLM) "find contact details and website for these Golf CC"<br>
        </blockquote>
        <br>
        <b>GPT Workbook:</b> <a href="http://www.[***].com.au/[***]" target="_blank">[***]</a> | Diagram: <a href="[***]-diagram.jpg" target="_blank">diagram</a> | UI: <a href="[***]-ui.jpg" target="_blank">UI</a> | Marking-How-To: <a href="docs/masking-how-to.html" target="_blank">Masking</a>
        <br>
        <b>LLM use-case:</b> <a href="http://www.[***].com.au/[***]/use-case/interactive-db-llm-rag.html" target="_blank">interactive-db-llm-rag</a> | Prompts Engineering: <a href="https://learnprompting.org/docs/intro" target="_blank">Guide</a> | AI Regulations: <a href="docs/ai-regulations.html" target="_blank">AI Acts</a> | <a href="[***].com.au/docs/eu-ai-act-translated.pdf" target="_blank">EU AI Act 2024 Translated</a>
        <hr>        
        Disclaimer: The content generated by GPT Workbook [aLLMatters] is for entertainment and informational purposes only. It is not intended to be used for any other purpose, including but not limited to, commercial or professional use. The content is not guaranteed to be accurate or complete, and it should not be relied upon for any decision-making.<br>
        aLLMatters AI-NLP Query Interface: [***]-RAG for Text to SQL, LLM Integration, RAG, Vector-Based Databases and Specialized Domain Databases.
        </div>
        """

    complete_message = f"""
        <div class='vector-db-tips'>
            <hr>
            <b>Vector DB Tips:</b>
            {new_content}
        </div>
        """

    st.markdown(complete_message, unsafe_allow_html=True)

if __name__ == '__main__':
    main()