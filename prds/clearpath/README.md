# Product Brief: ClearPath — AI-Powered Enterprise Onboarding Intelligence

**Problem:** Enterprise customer onboarding at B2B payments companies loses weeks to manual document review, fragmented compliance checks, and broken internal handoffs — delaying time-to-revenue and burning ops capacity on work AI can do.

**User:** Four internal personas with compounding pain:
- **Ops team** — manually processing applications, chasing missing documents, re-keying data across systems
- **Compliance team** — reviewing KYC/KYB documents manually, flagging exceptions by hand, no intelligent prioritisation
- **Sales team** — losing deals and credibility when activation takes weeks instead of days
- **Enterprise customer** — waiting in silence, receiving generic "we need more documents" emails with no clarity on what's missing or why

**Solution:** An internal AI agent — ClearPath — that automates document extraction and validation, surfaces compliance exceptions with reasoning, orchestrates handoffs between teams, and gives every stakeholder real-time visibility into onboarding status.

**AI Component:** Three AI layers working together:
1. **Document intelligence (RAG + OCR + LLM extraction)** — ingest uploaded documents, extract structured data, validate completeness against jurisdiction-specific requirements
2. **Compliance reasoning agent** — compare extracted data against KYC/KYB rules, flag anomalies with plain-language explanations, score risk level, suggest resolution path
3. **Handoff orchestration agent** — monitor workflow state, trigger next-step notifications, chase missing items automatically, escalate stale cases to human reviewers

AI is the right tool here because the bottlenecks are high-volume, rules-based, document-heavy tasks with predictable structure — exactly where LLMs with tool use outperform manual human review.

---

## User Stories

**Ops team**
- As an ops analyst, I want ClearPath to automatically extract customer data from uploaded documents so that I stop re-keying information that's already in a PDF
- As an ops team lead, I want to see all in-flight applications ranked by risk and age so that I can prioritise my team's attention without building manual trackers

**Compliance team**
- As a compliance reviewer, I want ClearPath to pre-screen documents and flag specific anomalies with reasoning so that I focus my time on exceptions, not routine checks
- As a compliance officer, I want every AI flag to include a confidence score and the specific rule it maps to so that I can make defensible decisions quickly

**Sales team**
- As an account executive, I want real-time visibility into my customer's onboarding status so that I can set accurate expectations and intervene before deals go cold
- As a sales leader, I want to see average activation time by customer segment so that I can identify where deals are stalling and push for process fixes

**Enterprise customer**
- As a new enterprise customer, I want to receive specific, actionable document requests (not generic chase emails) so that I can complete onboarding without back-and-forth
- As a customer, I want a clear view of what's been approved, what's pending, and what's blocking my activation so that I'm never in the dark

---

## Success Metrics

**Primary**
- Onboarding cycle time reduced by additional 35% from current baseline (target: from current state to under 5 business days for standard cases)
- Manual document review hours per application reduced by 60%

**Secondary**
- Compliance exception false positive rate under 8% (AI flags that turn out to be non-issues)
- Ops team capacity freed — measure as applications processed per analyst per week (target: 2x current)
- Sales activation visibility — % of AEs checking ClearPath weekly (adoption proxy)
- Customer satisfaction with onboarding process — CSAT score improvement vs baseline

**Guardrail**
- Compliance accuracy: AI must never approve a KYC/KYB case autonomously — all compliance decisions require human sign-off. AI recommends; human decides.
- Zero tolerance for PII mishandling — all document data encrypted at rest and in transit, access logged per user
- Audit trail completeness — every AI action must be logged with timestamp, model version, input, and output for regulatory review

---

## AI Evaluation Criteria

**Document extraction accuracy**
- Target: 95%+ field extraction accuracy on standard document types (passports, company registration, bank statements)
- Measurement: weekly human spot-check on 5% random sample of processed documents
- Failure mode: extraction confidence below threshold → route to human review queue automatically, never silently pass

**Compliance reasoning quality**
- Target: compliance team agrees with AI flag reasoning 85%+ of the time
- Measurement: reviewer feedback loop — thumbs up/down on every AI flag with optional free text
- Failure mode: if weekly agreement rate drops below 75%, freeze new flag types and retrain on accumulated feedback

**Handoff orchestration reliability**
- Target: zero missed escalations — every case that breaches SLA threshold must trigger a notification
- Measurement: SLA breach rate before and after ClearPath
- Failure mode: if orchestration misses an escalation, case auto-routes to team lead with incident flag

**Latency budget**
- Document extraction: under 30 seconds per document
- Compliance pre-screen: under 2 minutes per application
- Handoff notification: real-time (under 60 seconds of trigger event)

**Cost per application processed**
- Target: under $0.50 AI cost per onboarding application (input + output tokens across all three AI layers)
- Review threshold: if cost exceeds $0.80 per application, review prompt design and chunking strategy

---

## Scope

**In:**
- Document ingestion, OCR, and structured data extraction
- KYC/KYB pre-screening with AI-generated flag reasoning and confidence scores
- Internal workflow orchestration — status tracking, handoff triggers, SLA alerts
- Sales and ops dashboard — real-time pipeline visibility
- Customer-facing status page — what's approved, pending, blocking
- Audit log — every AI action recorded for regulatory compliance
- Human review queue — all AI recommendations that require sign-off

**Out:**
- Autonomous compliance approvals — humans always make the final call
- External customer document upload portal (Phase 2)
- Integration with third-party KYC vendors (Phase 2)
- Support for unstructured document types (handwritten forms, legacy formats) — Phase 2
- Multi-language document support beyond English — Phase 2

---

## Open Questions

1. **Model selection:** Do we use a general LLM (Claude, GPT-4o) or a document-specialist model (AWS Textract, Azure Form Recogniser) for extraction? Likely hybrid — specialist for extraction, general LLM for reasoning. Needs spike.

2. **Regulatory defensibility:** In regulated jurisdictions (EU, UK, US), what level of AI involvement in KYC/KYB is permissible? Need legal review before compliance reasoning agent goes live.

3. **Feedback loop ownership:** Who owns the weekly model evaluation and flag accuracy review? Compliance team or a dedicated AI ops function? Needs team design decision.

4. **Rollout sequence:** Do we launch document extraction first (lower risk, high value) and add compliance reasoning in Phase 2? Or ship all three layers together? Recommend phased — extraction first, reasoning after 60 days of extraction data.

5. **Build vs buy:** Evaluate off-the-shelf onboarding intelligence vendors (Alloy, Persona, Sardine) against internal build. Internal build justified if customisation requirements are high; buy justified if speed to compliance coverage matters more.

---

## GTM Strategy (Internal Rollout)

**Phase 1 — Pilot (weeks 1–6)**
- Deploy document extraction only to one ops team (10–15 analysts)
- Measure extraction accuracy, time savings, analyst trust
- Weekly feedback sessions — treat ops team as design partners

**Phase 2 — Compliance reasoning (weeks 7–12)**
- Add compliance pre-screening for standard KYC/KYB document types
- Compliance team reviews every flag with feedback loop active
- Do not reduce headcount — use freed capacity for complex cases

**Phase 3 — Full rollout (weeks 13–20)**
- Expand to all ops and compliance teams
- Launch sales visibility dashboard
- Launch customer status page
- Establish AI ops review cadence (weekly accuracy reviews)

**Enablement requirements:**
- Training session for ops team on how AI flags work and when to override
- Compliance team briefed on regulatory boundaries of AI-assisted review
- Executive communication: what ClearPath does, what it doesn't do, and what the guardrails are
