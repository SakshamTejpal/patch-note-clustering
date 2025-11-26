# Patch-Note Clustering – Technical Note
### Author: Saksham Tejpal (100874871)

---

## 1. System Overview

This application clusters video game patch notes using an LLM-based workflow. Patch notes are read from JSON files, prepared into batches, sent to Google Gemini 2.5 Flash for semantic clustering, and merged into a global taxonomy.  
The system includes: safety guardrails, telemetry instrumentation, offline evaluation, environmental isolation, and a command-line pipeline.

---

## 2. Architecture

```
+---------------------------------------+
|         Patch Note JSON Files         |
+----------------------+----------------+
                       |
                       v
+---------------------------------------+
|        FileHandler Loader             |
| - loads notes                         |
| - loads existing taxonomy             |
+----------------------+----------------+
                       |
                       v
+---------------------------------------+
|        Prompt Preparation             |
| - builds system & user prompts        |
| - enforces safety constraints         |
+----------------------+----------------+
                       |
                       v
+---------------------------------------+
|     Google Gemini External API        |
|    (Tool Use Enhancement)             |
| - clusters notes                      |
| - generates JSON output               |
+----------------------+----------------+
                       |
                       v
+---------------------------------------+
|       Result Cleaning & Merge         |
| - JSON extraction                     |
| - cluster merging into taxonomy       |
+----------------------+----------------+
                       |
                       v
+---------------------------------------+
|            Telemetry Logger           |
| - latency, batch, size, timestamp     |
+---------------------------------------+
```

---

## 3. Core Feature: LLM-Based Semantic Clustering

The core functionality revolves around:

1. Loading game patch notes from local JSON files.  
2. Splitting notes into fixed-size batches (to control context length).  
3. Preparing strict-format prompts describing clustering rules.  
4. Calling the Gemini external API to:
   - create cluster labels  
   - assign each note to one cluster  
   - return structured JSON output  
5. Cleaning and merging results into a global taxonomy file.

---

## 4. Enhancement Implemented: **Mini-Finetune via Prompt-Cached Patterns**

The application implements the “mini-finetune” enhancement by using **prompt-cached patterns that measurably change LLM behavior over time**.  
Instead of training a model (e.g., LoRA), the system stores all previously generated clusters inside `taxonomy.json` and re-injects these patterns into future prompts.

This creates a persistent, evolving memory layer:

- The LLM **reuses cluster IDs** created in earlier batches/games.  
- Cluster descriptions become more **refined and generalized** over time.  
- Redundant clusters are avoided because the model sees its **own prior outputs**.  
- Semantic behavior **changes measurably** as more games are processed.  
- The taxonomy grows cumulatively, shaping LLM decisions in later iterations.

---

## 5. Safety & Robustness

### **System Prompt Guardrails**
The system prompt clearly defines:
- required JSON structure  
- prohibition of explanations or free text  
- requirement to reuse cluster IDs when appropriate  
- rule-based generation of names and descriptions  

### **Input Length Guard**
- Batches are capped at 30 notes  
- Prevents overflowing the LLM context window  

### **Prompt Injection Detection**
Before sending prompts to the LLM:

```python
if HelperFunctions.contains_injection(user_prompt):
    raise ValueError("Prompt injection detected.")
```

This blocks manipulative content such as:
- “ignore previous instructions”

### **API Key Safety**
- No hardcoded secrets  
- Environment variables loaded via `dotenv`  
- `.env.example` included for reproducibility  
- `.env` excluded from Git tracking  

---

## 6. Telemetry

Each Gemini request is logged in:

```
data/telemetry/run_stats.json
```

Fields logged per request:
- `timestamp`
- `batch`
- `input_len` (prompt length)
- `latency`

Note: All the stats are saved till now, while creating the system.

---

## 7. Offline Evaluation

The evaluator (`test.py`) verifies the pipeline **without calling Gemini**:

### Checks:
1. **Completeness**  
   All patch note titles in `data/test_notes/` must appear in the taxonomy.

2. **Cluster Structure**  
   Each cluster must contain:
   - `cluster_id`
   - `name`
   - `description`
   - `single_notes` (non-empty)

3. **Note Schema Validation**  
   Each note must include:
   - `app_id`
   - `title`
   - `content`

Note: The way system, notes and batches are structured, `test.json` was merged into `text.py`

---

## 8. Reproducibility

The project includes all required reproducibility components:

- `README.md`  
- `requirements.txt`  
- `.env.example` (API key placeholder)  
- Seed data in:
  - `data/examples/`
- Command-line configuration  
- Deterministic pipeline behavior

Note: Please refer to README for running the application

---

## 9. Limitations

- Cluster consistency relies on LLM internal reasoning.  
- No embedding-based similarity; clustering depends strictly on prompt clarity.  
- Free-tier Gemini limits amount of data processed.  
- Merging logic depends on stable cluster_id generation from the LLM.  

---

## 10. Conclusion

This application implements a complete LLM engineering workflow featuring:

- Semantic clustering via Gemini  
- External API tool-use enhancement  
- Full safety and guardrails  
- Telemetry logging  
- Reproducible architecture  
- Offline validation  

It fulfills all core requirements of the Applied AI Engineering assignment.

