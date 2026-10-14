# Candidate Screening Agent

An automated, AI-driven technical screening tool built with Python and OpenRouter. It leverages a two-step agentic pipeline:

1. **Deterministic Decision Making:** Uses `typesafe/jev-1.13` to evaluate candidate profiles against job specifications and assign probabilistic match categories (`strong_match`, `potential_match`, `reject`).
2. **Natural Language Generation:** Passes the routed decision state to `meta-llama/llama-3.3-70b-instruct` to generate professional recruitment feedback notes.