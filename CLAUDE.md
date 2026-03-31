# CLAUDE.md - Lead Gen Engine

## What This Repo Is
A CLI pipeline that audits how AI agents misrepresent Montreal brands in French, generates "Scary Reports" proving the gap, and drafts personalized outreach emails. This is the SALES ENGINE, not the product.

## The Product (separate repo)
The actual remediation platform lives at github.com/NaimGQKC/AIMarketing -- a React + FastAPI app that fixes the inference gaps we find here. This repo generates the leads; that repo is what we sell them.

## The Three "Scary Metrics" We Audit
1. Competitor Hijacking: French AI search for Brand X surfaces Brand Y instead
2. Spec Dilution: Technical specs (Gore-Tex, 800-fill) get flattened to generic French terms
3. Ghosting: Brand appears in English AI results, completely absent in French

## Outreach Rules (Anti-AI Smell)
- Subject: "{brand} scores {score}/100 on French AI discovery"
- No "Partnership Opportunity", no "I hope you're having a great week"
- No em dashes. Max 4 sentences.
- Tone: bug report from a local peer, not a vendor pitch
- Sign off: Alex, AI PM -- Montreal (JMSB/Ampliwork)

## Tech
- Python 3.11+
- Tavily API (search), OpenAI API (GPT-4o probes), Google GenAI (Gemini probes)
- Claude Code as direct engine + third LLM
- requests + BeautifulSoup for page scraping
- WebSearch + WebFetch built-in tools

## Real Audit Methodology -- Multi-Source, Multi-LLM

### Data Sources
1. **WebSearch + WebFetch** (built-in): Find brand pages, contact people, company news
2. **Tavily API** (backup search): Higher quality search when built-in isn't enough
3. **Real page scraping**: Fetch actual EN and FR product pages, extract real specs
4. **Multi-LLM probing**: Test Claude (you), GPT-4o (OpenAI API), Gemini (Google API)

### Probe Types -- 3 probes x 3 LLMs x 2 languages = 18 data points per brand

**Probe A -- Generic Discovery (Ghosting + Competitor Hijacking)**
Consumer searches for category WITHOUT naming the brand.
- EN: "What is the best {product_category} in Montreal? Compare top options with technical specs and pricing."
- FR: "Quel est le meilleur {product_category} a Montreal? Comparer les meilleures options avec specifications techniques et prix."
Extract: Does brand appear? Rank? Which competitors instead? Same brands in both languages?

**Probe B -- Brand Accuracy (Spec Dilution)**
- EN: "What are the full technical specs of {brand} {product_category}? Materials, technology, pricing."
- FR: "Quelles sont les specifications techniques completes de {brand} {product_category}? Materiaux, technologie, prix."
Extract: Specs dropped/genericized/hallucinated in FR? Prices accurate? Vague terms replacing technical ones?

**Probe C -- Competitive Displacement**
- EN: "How does {brand} compare to {top_competitor} for {product_category}?"
- FR: "Comment {brand} se compare a {top_competitor} pour {product_category}?"
Extract: Does AI favor different brand in FR vs EN?

### Scoring: Inference Alignment Score (IAS) 0-100
Averaged across all available LLMs:
- Brand appears in generic FR search: +30
- Brand rank same in FR as EN: +20
- All technical specs preserved in FR: +20
- No competitor hijacking in FR: +15
- Pricing accurate in FR: +15
< 40 = RED ALERT | 40-70 = YELLOW | 70+ = GREEN

### Pipeline Triggers
- "run audit" = full pipeline, all brands in targets.csv, parallel sub-agents
- "audit [brand]" = single brand
- "find leads [sector]" = search for new brands to add to targets.csv
