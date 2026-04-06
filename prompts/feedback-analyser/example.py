import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

with open("prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()


def analyse_feedback(raw_feedback: str) -> dict:
    """
    Classifies raw customer feedback into structured product insights.

    Args:
        raw_feedback: Raw, unstructured feedback string from a customer

    Returns:
        dict with keys: core_problem, user_impact, product_area,
                        confidence, next_step
    """
    response = client.messages.create(
        model="claude-haiku-3-5-20251001",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": raw_feedback}
        ]
    )

    return json.loads(response.content[0].text)


def analyse_batch(feedback_list: list[str]) -> list[dict]:
    """
    Classifies a list of feedback items.

    Args:
        feedback_list: List of raw feedback strings

    Returns:
        List of structured insight dicts
    """
    results = []
    for feedback in feedback_list:
        try:
            result = analyse_feedback(feedback)
            result["original_feedback"] = feedback
            results.append(result)
        except json.JSONDecodeError:
            results.append({
                "core_problem": "parse error",
                "user_impact": "unknown",
                "product_area": "unknown",
                "confidence": "low",
                "next_step": "Review raw model output manually",
                "original_feedback": feedback
            })
    return results


if __name__ == "__main__":
    test_feedback = [
        "I can never find where to add a new user",
        "The app is super slow when loading dashboards",
        "Why is the export button so hard to find?",
        "This is terrible",  # vague — should return low confidence
    ]

    print("Running feedback analyser...\n")
    results = analyse_batch(test_feedback)

    for r in results:
        print(f"Feedback : {r['original_feedback']}")
        print(f"Problem  : {r['core_problem']}")
        print(f"Impact   : {r['user_impact']} | Confidence: {r['confidence']}")
        print(f"Area     : {r['product_area']}")
        print(f"Action   : {r['next_step']}")
        print("-" * 60)
