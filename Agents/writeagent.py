import config
import logging
from communication import A2AMessage
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from groq import APIError

# Get a logger for this module
logger = logging.getLogger(__name__)

class WriterAgent:
    """
    An AI agent that writes a coherent article based on a list of key points.
    """
    def __init__(self, name: str = "WriterAgent"):
        self.name = name
        self.llm = ChatGroq(temperature=0.7, model_name=config.GROQ_MODEL_NAME, groq_api_key=config.GROQ_API_KEY)
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a professional content writer. Your task is to write a well-structured and engaging paragraph based on the provided key points."),
                ("human", "Please write a paragraph about '{topic}' using the following key points:\n\n{key_points}"),
            ]
        )
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def execute(self, message: A2AMessage) -> A2AMessage:
        """
        Writes an article from the given key points.
        """
        key_points = message.content.get("key_points", [])
        topic = message.content.get("topic", "the provided topic")
        logger.info(f"[{self.name}] Received key points to write about '{topic}'.")

        if not key_points:
            logger.error(f"[{self.name}] No key points provided.")
            return A2AMessage(sender=self.name, content={"status": "FAILURE", "error": "No key points provided."})

        # Format points for the prompt
        formatted_points = "\n".join(f"- {point}" for point in key_points)

        try:
            logger.info(f"[{self.name}] Calling Groq API to write article...")
            article = self.chain.invoke({
                "topic": topic,
                "key_points": formatted_points
            })
            logger.info(f"[{self.name}] Successfully received article from Groq.")

            logger.info(f"[{self.name}] Content writing complete.")
            return A2AMessage(sender=self.name, content={"status": "SUCCESS", "article": article})
            
        except APIError as e:
            logger.error(f"[{self.name}] Groq API Error: {e}")
            return A2AMessage(sender=self.name, content={"status": "FAILURE", "error": f"API Error: {e}"})
        except Exception as e:
            logger.error(f"[{self.name}] An unexpected error occurred: {e}")
            return A2AMessage(sender=self.name, content={"status": "FAILURE", "error": f"An unexpected error occurred: {e}"})
