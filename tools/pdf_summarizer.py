# tools/pdf_summarizer.py
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import PyPDF2

class PDFSummarizerTool:
    def __init__(self, llm):
        self.llm = llm
        self.tool = Tool(
            name="PDF Summarizer",
            func=self.summarize_pdf,
            description="Useful for summarizing PDF files. Input should be the path to a PDF file."
        )
    
    def summarize_pdf(self, pdf_file_path="agent-builder/uploads"):
        try:
            with open(pdf_file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                # Summarize with LLM
                summary_prompt = PromptTemplate(
                    input_variables=["text"],
                    template="Please summarize the following text in 3-5 bullet points:\n\n{text}"
                )
                chain = LLMChain(llm=self.llm, prompt=summary_prompt)
                summary = chain.run(text=text[:3000])
                
                return summary
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    
    def __call__(self):
        return self.tool