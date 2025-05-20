from typing import List, Dict


def parse_sonar_responses(responses: List[Dict]) -> Dict[str, str]:
    """
    Organize raw Perplexity responses by pillar name.
    Input: List of {pillar: str, content: str}
    Output: Dict mapping each pillar to its content
    """
    structured_output = {}

    for item in responses:
        pillar = item.get("pillar", "unknown")
        content = item.get("content", "")

        if pillar not in structured_output:
            structured_output[pillar] = content
        else:
            # Append if duplicate pillars appear (e.g., history + current news)
            structured_output[pillar] += f"\n\n{content}"

    return structured_output
