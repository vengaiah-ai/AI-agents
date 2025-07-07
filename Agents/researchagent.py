import config
import logging
from communication import A2AMessage
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from groq import APIError

# Get a logger for this module
logger = logging.getLogger(__name__)

class ResearcherAgent:
    """
    An AI agent that takes a topic and generates key research points.
    """
    def __init__(self, name: str = "ResearcherAgent"):
        self.name = name
        self.llm = ChatGroq(temperature=0.2, model_name=config.GROQ_MODEL_NAME, groq_api_key=config.GROQ_API_KEY)
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a world-class researcher. Your job is to find the most important key points about a given topic. Provide the output as a clean, numbered list."),
                ("human", "Please research the following topic: {topic}"),
            ]
        )
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def execute(self, message: A2AMessage) -> A2AMessage:
        """
        Generates research points for the given topic.
        """
        topic = message.content.get("topic")
        logger.info(f"[{self.name}] Received topic for research: '{topic}'")

        if not topic:
            logger.error(f"[{self.name}] No topic provided.")
            return A2AMessage(sender=self.name, content={"status": "FAILURE", "error": "No topic provided."})

        try:
            # --- This is where the API call happens ---
            logger.info(f"[{self.name}] Calling Groq API to research topic...")
            research_points_text = self.chain.invoke({"topic": topic})
            logger.info(f"[{self.name}] Successfully received response from Groq.")
            
            research_points = [p.strip() for p in research_points_text.split('\n') if p.strip()]

            if not research_points:
                logger.warning(f"[{self.name}] API call succeeded but returned no research points.")
                return A2AMessage(sender=self.name, content={"status": "FAILURE", "error": "Content generation failed."})

            logger.info(f"[{self.name}] Research complete.")
            return A2AMessage(sender=self.name, content={"status": "SUCCESS", "key_points": research_points})

        except APIError as e:
            logger.error(f"[{self.name}] Groq API Error: {e}")
            return A2AMessage(sender=self.name, content={"status": "FAILURE", "error": f"API Error: {e}"})
        except Exception as e:
            logger.error(f"[{self.name}] An unexpected error occurred: {e}")
            return A2AMessage(sender=self.name, content={"status": "FAILURE", "error": f"An unexpected error occurred: {e}"})
