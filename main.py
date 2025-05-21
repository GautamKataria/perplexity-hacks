from modules.prompt_generator import generate_prompts
from modules.sonar_client import fetch_sonar_responses
from modules.response_parser import parse_sonar_responses
from modules.summarizer import generate_360_summary
from modules.agent_intent_handler import get_subject_and_focus_from_agent
import asyncio

def main(query: str):
    # Step 1: Intent recognition with optional direct answer
    intent = get_subject_and_focus_from_agent(query)
    print("intent:", intent)

    if intent.get("type") == "direct_answer" and "answer" in intent:
        print("\n🔹 Direct Answer:\n", intent["answer"])
        return

    subject = intent["subject"]
    focuses = intent["focus"]

    # Step 2: Generate analysis prompts
    prompts = generate_prompts(subject, focuses)
    print("prompts:", prompts)

    # Step 3: Fetch Sonar responses
    responses = asyncio.run(fetch_sonar_responses(prompts))
    print("responses:", responses)

    # Step 4: Parse structured data
    structured_data = parse_sonar_responses(responses)
    print("structured_data:", structured_data)

    # Step 5: Summarize key insights
    summary = generate_360_summary(structured_data)
    print("summary:", summary)

if __name__ == "__main__":
    import sys
    user_input = sys.argv[1] if len(sys.argv) > 1 else input("Enter your query: ")
    main(user_input)



### fastapi version commented out for now

# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from typing import List, Dict, Any

# from modules.prompt_generator import generate_prompts
# from modules.sonar_client import fetch_sonar_responses
# from modules.response_parser import parse_sonar_responses
# from modules.summarizer import generate_360_summary
# from modules.agent_intent_handler import get_subject_and_focus_from_agent

# import asyncio
# app = FastAPI()


# class QueryRequest(BaseModel):
#     input: str


# class ChartResponse(BaseModel):
#     subject: str
#     focus: List[str]
#     prompts: List[Dict[str, Any]]
#     structured_data: Dict[str, str]
#     summary: str


# @app.post("/analyze", response_model=ChartResponse)
# async def analyze_query(request: QueryRequest):
#     query = request.input

#     # Step 1: AI Agent detects subject + focus areas
#     subject, focus = get_subject_and_focus_from_agent(query)

#     # Step 2: Prompt generation
#     prompts = generate_prompts(subject, focus)

#     # Step 3: Fetch Sonar responses
#     responses = await fetch_sonar_responses(prompts)

#     # Step 4: Parse structured data
#     structured_data = parse_sonar_responses(responses)

#     # Step 5: Generate summary
#     summary = generate_360_summary(structured_data)

#     return {
#         "subject": subject,
#         "focus": focus,
#         "prompts": prompts,
#         "structured_data": structured_data,
#         "summary": summary,
#     }
