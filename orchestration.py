import logging
from Agents.researchagent import ResearcherAgent
from Agents.writeagent import WriterAgent
from communication import A2AMessage
from pdf_generator import PDFGenerator
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class ContentOrchestrator:
    """
    Orchestrates the workflow between the Researcher and Writer agents.
    """
    def __init__(self):
        self.researcher_agent = ResearcherAgent()
        self.writer_agent = WriterAgent()
        self.pdf_generator = PDFGenerator()
        logger.info("[Orchestrator] System initialized. Ready for content creation.")

    def generate_content(self, topic: str):
        """
        Generate content for the given topic and return result in API format.
        """
        try:
            # Run the workflow
            self.run_workflow(topic)
            
            # Look for the generated PDF file
            output_dir = Path("output")
            if output_dir.exists():
                # Find the most recent PDF file for this topic
                pdf_files = list(output_dir.glob(f"*{topic.replace(' ', '_')}*.pdf"))
                if pdf_files:
                    # Get the most recent file
                    latest_file = max(pdf_files, key=lambda x: x.stat().st_mtime)
                    return {
                        "success": True,
                        "file_path": str(latest_file),
                        "message": "Content generated successfully"
                    }
            
            # If no PDF found, check for text file
            if os.path.exists("output.txt"):
                return {
                    "success": True,
                    "file_path": "output.txt",
                    "message": "Content generated successfully (text file)"
                }
            
            return {
                "success": False,
                "error": "No output file generated"
            }
            
        except Exception as e:
            logger.error(f"Error in generate_content: {str(e)}")
            return {
                "success": False,
                "error": f"Content generation failed: {str(e)}"
            }

    def run_workflow(self, topic: str):
        """
        Manages the step-by-step process of creating content.
        """
        logger.info("="*50)
        logger.info(f"[Orchestrator] Starting new content workflow for topic: '{topic}'")
        logger.info("="*50)

        # Step 1: Send topic to the Researcher Agent
        research_request = A2AMessage(sender="Orchestrator", content={"topic": topic})
        research_response = self.researcher_agent.execute(research_request)

        logger.info("--- Research Result ---")
        logger.info(research_response)

        # Context-driven decision: If research is successful, proceed to writing.
        if research_response.content.get("status") == "SUCCESS":
            logger.info("[Orchestrator] Research successful. Engaging Writer Agent.")

            # Step 2: Send research points to the Writer Agent
            key_points = research_response.content["key_points"]
            write_request = A2AMessage(sender="Orchestrator", content={"topic": topic, "key_points": key_points})
            write_response = self.writer_agent.execute(write_request)

            logger.info("--- Final Article ---")
            if write_response.content.get("status") == "SUCCESS":
                final_article = write_response.content.get('article', 'No article was generated.')
                print("\n" + final_article + "\n")
                
                # Generate PDF instead of text file
                try:
                    pdf_path = self.pdf_generator.create_pdf(topic, final_article)
                    logger.info(f"[Orchestrator] Article saved as PDF: {pdf_path}")
                    print(f"[Orchestrator] Article saved as PDF: {pdf_path}")
                except Exception as e:
                    logger.error(f"[Orchestrator] PDF generation failed: {e}")
                    print(f"[Orchestrator] PDF generation failed: {e}")
                    # Fallback to text file
                    with open("output.txt", "a", encoding="utf-8") as f:
                        f.write(f"=== Article on: {topic} ===\n{final_article}\n\n")
                    logger.info("[Orchestrator] Article saved to output.txt as fallback.")
                    print("[Orchestrator] Article saved to output.txt as fallback.")
            else:
                error_msg = write_response.content.get('error', 'Unknown error during writing phase.')
                logger.error(f"[Orchestrator] Workflow failed during writing phase: {error_msg}")
                print(f"[Orchestrator] Workflow failed during writing phase: {error_msg}")
        else:
            error_msg = research_response.content.get('error', 'Unknown error during research phase.')
            logger.error(f"[Orchestrator] Workflow failed during research phase: {error_msg}")
            print(f"[Orchestrator] Workflow failed during research phase: {error_msg}")

        logger.info("="*50)
        logger.info("[Orchestrator] Workflow finished.")
        logger.info("="*50 + "\n")
