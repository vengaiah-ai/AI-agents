import logging_config # Import and run the setup
from orchestration import ContentOrchestrator

# Setup logging as the first step
logging_config.setup_logging()

def main():
    """
    Main function to initialize and run the content creation workflow.
    """
    # Initialize the orchestrator
    orchestrator = ContentOrchestrator()

    while True:
        topic = input("Enter a topic (or 'exit' to quit): ").strip()
        if topic.lower() == 'exit':
            print("Exiting. Goodbye!")
            break
        if not topic:
            print("Please enter a non-empty topic.")
            continue
        orchestrator.run_workflow(topic)

if __name__ == "__main__":
    main()
