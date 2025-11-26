# Patch-Note Clustering  
Context-Based Clustering of Game Patch Notes Using Gemini

---

## Overview

Patch-Note Clustering is an AI engineering application that uses **Google Gemini 2.5 Flash** to cluster game patch notes into meaningful, reusable categories. Patch notes from multiple games are processed in batches, clustered by an LLM, and merged into an evolving global taxonomy stored in JSON.

The system supports:

- Incremental clustering across multiple games  
- Prompt-cached mini-finetuning (clusters improve over time)  
- Safety guardrails and injection detection  
- Telemetry logging  
- Offline evaluation without API calls  
- Reproducible end-to-end execution  

This project extends a thesis on game patch note collection and contributes to research on text classification, patch-notes analysis, and context-based clustering.

---

## Features

### LLM-Based Patch Note Clustering
- Batches patch notes (max 30 per batch)
- Sends them to Gemini for clustering
- Produces structured JSON clusters

### Mini-Finetune Enhancement (Prompt-Cached Patterns)
- Past LLM outputs (clusters) stored in `taxonomy.json`
- These are injected into future prompts  
- The model **reuses and improves clusters over time**

### Safety & Robustness
- Strict JSON-only system prompt
- Injection detection (`ignore all previous instructions`, etc.)
- Input length control via batching
- API key isolation via `.env`

### Telemetry
Logs every LLM call:
- timestamp  
- input length  
- latency  
- batch number  
- pathway `"PROMPT_CACHED"`  

Stored in:  
`data/telemetry/run_stats.json`

### Offline Evaluation
`test.py` verifies:
- all notes appear in taxonomy
- taxonomy schema validity
- notes contain required fields  
**No Gemini calls.**

---

## Project Structure

```
patch-note-clustering/
│
├── main.py                   # Pipeline entry point (batching + LLM + merging)
├── src/
│   ├── llm_call.py           # Gemini API call (uses API_KEY)
│   ├── prepare_prompts.py    # Builds system/user prompts w/ cached patterns
│   ├── telemetry.py          # Logs latency + metadata
│   └──.env.example
│
├── util/
│   ├── file_handler.py       # Loads notes + taxonomy, writes updated clusters
│   ├── cluster.py            # Cluster + SingleNote data classes
│   ├── helper_funtions.py    # Batching, JSON extraction, injection detection
│   └── game_data.py          # Schema for game patch note payloads
│
├── data/
│   ├── notes/                # Notes to process (user-provided)
│   ├── clusters/
│   │   └── taxonomy.json     # Output taxonomy (grows incrementally)
│   ├── examples/             # Example inputs for testing
│
├── test.py                   # Offline evaluation suite
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Create a virtual environment (recommended)

```
python -m venv venv
```

```
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

Dependencies:
```
google-genai
python-dotenv
```

---

## Configuration

### 1. Copy `.env.example` → `.env` (Optional)

```
cp .env.example .env
```

### 2. Insert your Gemini API key

```
API_KEY=your_api_key_here
```

**Note: API_KEY can also be defined in the run command**  

---

## Preparing Data

### Input notes
Notes are present in, these notes are used to make the taxonomy shipped with this application:

```
data/notes/
```

### Seed data (already included):

- `data/examples/`

---

## Running the Clustering Pipeline

Use environment variables + CLI arguments:

### PowerShell (Windows)
```
$env:API_KEY="YOUR_KEY"; python main.py --notes_dir "data/examples" --clusters_dir "data/clusters/taxonomy.json"
```
if you have already followed step 2, you can use the following;
```
python main.py --notes_dir "data/examples" --clusters_dir "data/clusters/taxonomy.json"
```

### macOS/Linux
```
API_KEY="YOUR_KEY" python3 main.py --notes_dir data/examples --clusters_dir data/clusters/taxonomy.json
```

**Note: Diretory with the notes can be defined here (--notes_dir path/to/notes), you can use data/examples here to use seed data. Same can be done for (--clusters_dir path/to/taxonomy). Right now taxonomy.json contains data from data/notes, you can enrich it with data/example or delete it and recreate it using data/notes. Creating a same taxonomy with same data wont be meaningfull and will just give you doubled down data.**

---

## Output

A global taxonomy is written to:

```
data/clusters/taxonomy.json
```

Format example:

```json
{
  "cluster_id": "C003",
  "name": "Engine Bug Fixes",
  "description": "Fixes related to rendering, file handling, and engine crashes.",
  "single_notes": [
    {
      "app_id": "40",
      "title": "Update released",
      "content": "Fixed demo playback bug..."
    }
  ]
}
```

---

## Offline Evaluation (No LLM Required)

Run:

```
python test/test.py
```

Checks include:

- all notes present  
- cluster schema correctness  
- note schema correctness  

Ensures reproducible, verifiable results.

---

## Telemetry

Telemetry is logged automatically per batch:

```
data/telemetry/run_stats.json
```

Example:

```json
{
  "timestamp": "2025-01-10T13:22:11",
  "batch": 2,
  "input_len": 5240,
  "latency": 1.82,
  "pathway": "PROMPT_CACHED"
}
```

---

## Author  
**Saksham Tejpal (100874871)**  
saksham.tejpal@ontariotechu.net

