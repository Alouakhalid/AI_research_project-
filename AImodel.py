from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

class AIResearchGenerator:
    def __init__(self):
        """Initialize the AI Research Generator with Gemini 2.5 Flash"""
        self.llm = None
        self.chain = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Gemini 2.5 Flash model"""
        try:
            self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
            print("✅ Successfully connected to Gemini 2.5 Flash")
            
            # Create the prompt template
            self.prompt = ChatPromptTemplate.from_template(
                "You are a professional researcher. Write a comprehensive research paper for students on the topic: {topic}. "
                "Language: {language}. Write with perfect style and no grammar errors. "
                "Include: Abstract, Introduction, Literature Review, Methodology, Results, Discussion, and Conclusion. "
                "Number of pages: {number_of_pages}. "
                "Please format the paper with clear headings and sections. Do not include any asterisks or special formatting characters."
            )
            
            # Create the chain using modern LangChain syntax
            self.chain = self.prompt | self.llm | StrOutputParser()
            
        except Exception as e:
            print(f"❌ Error initializing Gemini 2.5 Flash: {e}")
            self.llm = None
            self.chain = None
    
    def generate_research_paper(self, topic, language="English", pages="3"):
        """
        Generate a research paper using AI
        
        Args:
            topic (str): The research topic
            language (str): The language for the paper
            pages (str): Number of pages
            
        Returns:
            dict: Result with success status and content
        """
        if not self.chain:
            return {
                'success': False,
                'error': 'AI model not initialized. Please check your API key.'
            }
        
        try:
            result = self.chain.invoke({
                "topic": topic,
                "language": language,
                "number_of_pages": pages
            })
            
            return {
                'success': True,
                'research_paper': result,
                'topic': topic,
                'language': language,
                'pages': pages
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error generating research paper: {str(e)}'
            }
    
    def is_ready(self):
        """Check if the AI model is ready to use"""
        return self.chain is not None

# Create a global instance
ai_generator = AIResearchGenerator()

# For direct script execution
if __name__ == "__main__":
    if ai_generator.is_ready():
        user_language = input("Enter the language of the research paper: ")
        topic = input("Enter the topic of the research paper: ")
        number_of_pages = input("Enter the number of pages you want the research paper to be: ")
        
        result = ai_generator.generate_research_paper(topic, user_language, number_of_pages)
        
        if result['success']:
            print("Research Paper:")
            print("=" * 50)
            print(result['research_paper'])
        else:
            print(f"Error: {result['error']}")
    else:
        print("❌ AI model not ready. Please check your API key in the .env file.")
