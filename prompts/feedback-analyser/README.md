# AI Feedback Analyser — Prompt Engineering Artifact

A production-grade system prompt that classifies raw customer feedback into structured product insights. Built for B2B SaaS product teams who receive high volumes of unstructured feedback and need to triage it into actionable data without manual review.

## What it does

Takes raw, messy customer feedback as input and returns a structured JSON object containing:
- The underlying core problem (not just the surface complaint)
- User impact level (low / medium / high)
- Product area mapping
- Confidence score with decision rule
- One specific, actionable next step

## The prompt

```
SYSTEM:
You are an AI Product Requirements Analyst at a B2B SaaS company.
Your job is to convert raw, messy customer feedback into clear
product insights and actionable next steps. You think like a
senior product manager: structured, evidence-driven, and pragmatic.

When given raw user feedback, you will:
1. Identify the underlying core problem (not just the surface complaint)
2. Infer user impact (low/medium/high) based on severity and frequency signals
3. Map the issue to the most relevant product area
4. Evaluate confidence using this rule:
   - high: feedback names a specific feature, action, or workflow
   - medium: feedback describes a symptom but not a specific cause
   - low: feedback is vague, emotional, or missing context
5. Recommend one specific next step starting with an action verb

Always respond in this exact JSON format only:
{
  "core_problem": "string",
  "user_impact": "low|medium|high",
  "product_area": "string",
  "confidence": "low|medium|high",
  "next_step": "string — one sentence, starts with an action verb"
}

If input is too vague to analyse, return:
{
  "core_problem": "insufficient information",
  "user_impact": "unknown",
  "product_area": "unknown",
  "confidence": "low",
  "next_step": "Request more specific feedback from the user"
}

Example input: "I can't figure out how to export my data to CSV"
Example output:
{
  "core_problem": "Export functionality is not discoverable",
  "user_impact": "high",
  "product_area": "data management",
  "confidence": "high",
  "next_step": "Audit export button placement and add a contextual tooltip on the data table"
}

Example input: "The app is super slow when loading dashboards"
Example output:
{
  "core_problem": "Dashboard load performance is degraded",
  "user_impact": "high",
  "product_area": "performance",
  "confidence": "medium",
  "next_step": "Instrument dashboard load times and identify the top 3 slowest queries"
}

You MUST NOT:
- Invent features or assumptions not supported by the feedback
- Overgeneralise from a single vague input
- Assign high confidence if the feedback lacks specifics
- Provide more than one next step
- Output anything outside the specified JSON format
```

## Design decisions

**Why structured JSON output?**
The model's response needs to be machine-readable so it can feed downstream systems — a Jira ticket creator, a Slack alert, a product analytics dashboard. Plain text responses can't be processed programmatically at scale.

**Why a confidence decision rule?**
Without a defined rule, confidence scores drift across calls. "High confidence" means different things in different contexts. The three-tier rule (specific feature = high, symptom = medium, vague = low) makes scores consistent and auditable.

**Why one next step only?**
Multiple next steps create ambiguity about ownership. One action verb-led step forces prioritisation and makes the output immediately assignable to a team or individual.

**Why a fallback for vague input?**
Without a failure mode clause, the model forces vague input into the schema and produces low-quality output confidently. The fallback returns an honest signal that the input needs more context before analysis is meaningful.

**Why two examples instead of one?**
One example teaches the format. Two examples teach the pattern. The second example (performance symptom) is meaningfully different from the first (discoverability) — showing the model how to vary core_problem based on what's actually described, not just how to fill in the fields.

## How to use

Drop the system prompt into any LLM API call (Anthropic Claude, OpenAI GPT-4o) and pass raw feedback as the user message.

```python
import anthropic

client = anthropic.Anthropic()

def analyse_feedback(raw_feedback: str) -> dict:
    response = client.messages.create(
        model="claude-haiku-3-5",
        max_tokens=300,
        system=SYSTEM_PROMPT,  # paste prompt above
        messages=[
            {"role": "user", "content": raw_feedback}
        ]
    )
    import json
    return json.loads(response.content[0].text)

# Example
result = analyse_feedback("I can never find where to add a new user")
print(result)
# {
#   "core_problem": "User management entry point is not discoverable",
#   "user_impact": "high",
#   "product_area": "user management",
#   "confidence": "high",
#   "next_step": "Add a prominent 'Invite user' button to the main navigation"
# }
```

## Scaling this in production

This prompt is designed to run at volume. Practical integration points:

- **Typeform / survey tools** — trigger on new submission, classify automatically, write to Airtable or Notion
- **Intercom / Zendesk** — classify support tickets on creation, route by product_area, flag high-impact issues
- **Slack** — post feedback → bot classifies → structured output posted to #product-insights channel
- **NPS follow-ups** — run detractor responses through this before your PM team reviews them

At Claude Haiku pricing ($0.80 input / $4.00 output per 1M tokens), classifying 10,000 pieces of feedback costs approximately $2–3. No human triage team required.

## Repo structure

```
feedback-analyser/
├── README.md           ← this file
├── prompt.txt          ← system prompt only, clean copy
├── example.py          ← Python integration example
└── .env.example        ← ANTHROPIC_API_KEY=your_key_here
```
