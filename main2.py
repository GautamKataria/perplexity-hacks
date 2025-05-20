# Rishi's file to test the code in modules directory
# requirements.txt (Added to gitignore)
import asyncio
from modules.agent_intent_handler import get_subject_and_focus_from_agent
from modules.prompt_generator import generate_prompts
from modules.sonar_client import fetch_sonar_responses
from modules.response_parser import parse_sonar_responses
from modules.summarizer import generate_360_summary
import json
from typing import Dict, List
import sys

def print_section(title: str, content: any):
    """Helper function to print formatted sections"""
    print("\n" + "="*50)
    print(f"📌 {title}")
    print("="*50)
    if isinstance(content, (dict, list)):
        print(json.dumps(content, indent=2))
    else:
        print(content)

async def test_perplexity_analysis(query: str):
    try:
        # Step 1: Test Intent Analysis
        print_section("1. Testing Intent Analysis", f"Query: {query}")
        subject, focus = get_subject_and_focus_from_agent(query)
        print_section("Intent Analysis Results", {
            "subject": subject,
            "focus_areas": focus
        })

        # Step 2: Test Prompt Generation
        print_section("2. Testing Prompt Generation", "")
        prompts = generate_prompts(subject, focus)
        print_section("Generated Prompts", prompts)

        # Step 3: Test Sonar API Calls
        print_section("3. Testing Sonar API Calls", "")
        responses = await fetch_sonar_responses(prompts)
        print_section("Sonar API Responses", responses)

        # Step 4: Test Response Parsing
        print_section("4. Testing Response Parsing", "")
        structured_data = parse_sonar_responses(responses)
        print_section("Structured Data", structured_data)

        # Step 5: Test Summary Generation
        print_section("5. Testing Summary Generation", "")
        summary = generate_360_summary(structured_data)
        print_section("Final Summary", summary)

        return True

    except Exception as e:
        print_section("❌ Error", f"An error occurred: {str(e)}")
        return False

def main():
    # Default test query if none provided
    default_query = "What's happening with NVIDIA in AI?"
    
    # Get query from command line or use default
    query = sys.argv[1] if len(sys.argv) > 1 else default_query
    
    print("\n🚀 Starting Perplexity Analysis Test")
    print(f"Query: {query}")
    
    # Run the test
    success = asyncio.run(test_perplexity_analysis(query))
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")

if __name__ == "__main__":
    main()
