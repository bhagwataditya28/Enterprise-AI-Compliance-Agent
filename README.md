# Enterprise AI Compliance & Contract Risk Agent

An AI-powered contract analysis application that uses **Retrieval-Augmented Generation (RAG), semantic search, and a local Large Language Model (LLM)** to identify potential contractual compliance and operational risks.

The application analyzes contract documents and produces **structured risk findings, supporting evidence, contract page references, severity levels, recommendations, compliance checks, and an overall risk score.**

> **Note:** The contract included in this repository is fully synthetic and contains intentionally introduced risk scenarios for testing and evaluation. No confidential company or client information is used.

---

## 🎯 Why I Built This

This project was built to gain practical hands-on experience with **Generative AI, RAG pipelines, semantic search, LLM integration, and AI-based risk analysis**, while connecting these technologies with my previous experience in **Risk & Compliance, Python, SQL, and automation**.

The goal was to build a practical AI application rather than a simple chatbot.

The system focuses on a realistic enterprise use case:

**Can an AI system analyze a contract, retrieve the relevant evidence, identify potential contractual risks, and generate an explainable risk report?**

---

## 💡 What the Application Does

A user provides a contract PDF.

The system then:

1. Extracts text while preserving page numbers.
2. Splits the document into overlapping chunks.
3. Converts each chunk into an embedding vector.
4. Stores the processed content in a local knowledge base.
5. Converts the user's analysis request into an embedding.
6. Retrieves the most relevant contract sections using semantic similarity.
7. Sends only the retrieved evidence to the local Qwen3 LLM.
8. Extracts structured contractual risk findings.
9. Normalizes risk categories.
10. Assigns severity and numerical risk scores.
11. Runs deterministic compliance checks.
12. Generates a professional contract risk report.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │     Contract PDF    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Document Extraction │
                         │      + Pages        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Text Chunking     │
                         │   + Overlap         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Sentence Transformer│
                         │    Embeddings       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Local Knowledge Base│
                         └──────────┬──────────┘
                                    │
                           User Analysis Query
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Semantic Search   │
                         │ Cosine Similarity   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     RAG Context     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Qwen3 4B       │
                         │   Local LLM/Ollama  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Structured Risk JSON│
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                ┌──────────────────┐  ┌──────────────────┐
                │ Category         │  │ Compliance       │
                │ Normalization    │  │ Checks           │
                └────────┬─────────┘  └────────┬─────────┘
                         │                     │
                         └──────────┬──────────┘
                                    ▼
                         ┌─────────────────────┐
                         │    Risk Scoring     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Contract Risk Report│
                         └─────────────────────┘
```

---

# 🔎 RAG Pipeline

The core of the project is a simple Retrieval-Augmented Generation pipeline.

### 1. Document Ingestion

The PDF is processed using `pypdf`.

Instead of treating the document as one large text block, the application preserves the **page number and extracted text**.

Example:

```text
Page: 1
Text: Vendor must notify the Company of a security incident...
```

### 2. Chunking

The extracted content is divided into overlapping chunks.

Current configuration:

```text
Chunk size:     500 characters
Overlap:        100 characters
```

The overlap helps preserve context between neighboring chunks.

### 3. Embeddings

Each chunk is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The model generates **384-dimensional embeddings** for the document chunks.

### 4. Semantic Search

When an analysis request is submitted, the query is also converted into an embedding.

The system calculates **cosine similarity** between the query vector and document chunk vectors.

The highest-scoring chunks are retrieved as evidence.

### 5. Retrieval-Augmented Generation

The retrieved contract evidence is provided to Qwen3 through a controlled prompt.

The LLM is instructed to:

* Use only the supplied contract evidence
* Avoid inventing information
* Return structured JSON
* Include supporting evidence
* Include the contract page
* Identify contractual gaps rather than making unsupported legal claims

This allows the LLM to reason over relevant contract content without requiring the entire document to be placed into the prompt.

---

# 🤖 Risk Analysis

The LLM returns structured risk information in JSON format.

Example:

```json
{
  "category": "Information Security",
  "severity": "HIGH",
  "finding": "Contractual security requirement is not sufficiently defined.",
  "evidence": "Supporting contract evidence...",
  "page": 1,
  "recommendation": "Define specific security obligations in the agreement."
}
```

The application then processes the result through additional deterministic components.

### Risk Categories

Examples include:

* Information Security
* Data Retention
* Business Continuity
* Other contractual risk categories

### Severity

Each identified risk receives:

```text
HIGH   → 3 points
MEDIUM → 2 points
LOW    → 1 point
```

The individual scores are combined into an overall risk score.

---

# ✅ Deterministic Compliance Checks

The project does not rely entirely on the LLM.

It also contains deterministic checks for selected contractual requirements, including:

* Security requirements
* Security incident notification
* Data deletion
* Audit rights
* Business continuity

Example:

```text
Security Requirements
Status: PASS

Security Incident Notification
Status: PASS

Data Deletion
Status: GAP

Audit Rights
Status: PASS

Business Continuity
Status: GAP
```

This creates a simple **hybrid approach**:

```text
LLM-based analysis
        +
Deterministic checks
        ↓
More structured risk assessment
```

---

# 🛡️ Hallucination Control

A key design goal of the project is to reduce unsupported LLM-generated findings.

The risk-analysis prompt explicitly instructs the model to:

* Use only retrieved contract evidence
* Not introduce outside information
* Not invent contractual requirements
* Not claim legal non-compliance without evidence
* Return no risks when the evidence does not support a finding

### Unsupported Question Test

The application was tested with:

> Does the contract specify that the vendor has GDPR compliance certification?

The synthetic contract does not contain such a requirement.

The agent therefore returned:

```text
Risks extracted by LLM: 0

Overall Risk Score: 0
Overall Risk Level: LOW

No supported risks identified.
```

This test is intended to verify that the application does not automatically generate a risk simply because a compliance-related term appears in the user's question.

---

# 🧪 Evaluation

The project includes a focused evaluation test set covering three contractual risk categories:

| Test Case            | Expected Category    | Result |
| -------------------- | -------------------- | ------ |
| Information Security | Information Security | ✅ PASS |
| Data Retention       | Data Retention       | ✅ PASS |
| Business Continuity  | Business Continuity  | ✅ PASS |

### Evaluation Result

```text
Tests Passed: 3 / 3
Evaluation Accuracy: 100%
```

**Important:** This represents performance on the three included evaluation cases only. It should **not** be interpreted as general model accuracy or production-level accuracy.

The project also includes a separate unsupported-question/hallucination test.

---

# 🖥️ Application Interface

The project includes a Streamlit interface that allows a user to:

* Upload a contract PDF
* Run contract analysis
* View identified risks
* View severity and risk scores
* View supporting evidence
* View contract page references
* View compliance checks
* Download the generated report

The same analysis pipeline can also be executed from the command line.

---

# 📊 Example Output

```text
ENTERPRISE CONTRACT RISK REPORT

Overall Risk Score : 7
Overall Risk Level : HIGH

------------------------------------------------------------

Risk #1
Category       : Information Security
Severity       : HIGH
Score          : 3
Finding        : Contractual security gap
Evidence       : Supporting contract evidence...
Contract Page  : 1
Recommendation : Define stronger contractual security requirements.

Risk #2
Category       : Data Retention
Severity       : MEDIUM
Score          : 2
Finding        : Data deletion period is not specifically defined.
Evidence       : Supporting contract evidence...
Contract Page  : 2
Recommendation : Establish a specific data deletion timeline.

------------------------------------------------------------

COMPLIANCE CHECKS

Security Requirements
Status  : PASS

Security Incident Notification
Status  : PASS

Data Deletion
Status  : GAP

Audit Rights
Status  : PASS

Business Continuity
Status  : GAP
```

---

# 🛠️ Technology Stack

| Technology                | Purpose                              |
| ------------------------- | ------------------------------------ |
| **Python**                | Application development              |
| **PyPDF**                 | PDF text extraction                  |
| **Sentence Transformers** | Text embeddings                      |
| **all-MiniLM-L6-v2**      | Local embedding model                |
| **NumPy**                 | Vector similarity calculations       |
| **Ollama**                | Local LLM runtime                    |
| **Qwen3 4B**              | Local language model                 |
| **Streamlit**             | Web interface                        |
| **JSON**                  | Knowledge base and structured output |
| **Git/GitHub**            | Version control                      |

---

# 📁 Project Structure

```text
Enterprise-AI-Compliance-Agent/
│
├── app/
│   ├── build_knowledge_base.py
│   ├── category_normalizer.py
│   ├── chunker.py
│   ├── compliance_checker.py
│   ├── config.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── evaluation.py
│   ├── hallucination_test.py
│   ├── llm.py
│   ├── logger.py
│   ├── main.py
│   ├── rag.py
│   ├── report_generator.py
│   ├── risk_agent.py
│   ├── risk_scoring.py
│   ├── search.py
│   └── streamlit_app.py
│
├── data/
│   └── documents/
│       └── Synthetic_Vendor_Services_Agreement.pdf
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 🚀 Getting Started

## Prerequisites

Install:

* Python 3.12+
* Git
* Ollama

The project uses a local Qwen3 model through Ollama, so an external OpenAI API key is not required.

---

## 1. Clone the Repository

```bash
git clone https://github.com/bhagwataditya28/Enterprise-AI-Compliance-Agent.git
cd Enterprise-AI-Compliance-Agent
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install the Local LLM

Install Ollama and pull the Qwen3 model:

```bash
ollama pull qwen3:4b
```

Verify:

```bash
ollama list
```

You should see:

```text
qwen3:4b
```

---

# ▶️ Build the Knowledge Base

From the project root:

```bash
python app/build_knowledge_base.py
```

This will:

```text
Load PDF
   ↓
Extract pages
   ↓
Create chunks
   ↓
Generate embeddings
   ↓
Save knowledge_base.json
```

The generated knowledge base is stored under:

```text
data/processed/
```

Generated processing files are excluded from Git through `.gitignore`.

---

# ▶️ Run the Risk Agent

```bash
python app/risk_agent.py
```

The application will:

1. Load the knowledge base.
2. Load the embedding model.
3. Run semantic retrieval.
4. Send retrieved evidence to Qwen3.
5. Extract structured risks.
6. Normalize categories.
7. Calculate risk scores.
8. Run compliance checks.
9. Generate a contract risk report.

The report is generated under:

```text
data/processed/contract_risk_report.txt
```

---

# 🌐 Run the Streamlit Application

```bash
streamlit run app/streamlit_app.py
```

Then open the local Streamlit URL displayed in the terminal.

Upload a contract PDF and run the analysis through the interface.

---

# 🧪 Run Evaluation Tests

```bash
python app/evaluation.py
```

The evaluation currently tests:

```text
Information Security
Data Retention
Business Continuity
```

---

# 🛡️ Run the Hallucination Test

```bash
python app/hallucination_test.py
```

This tests how the system handles a question that is not supported by the contract evidence.

---

# ⚙️ Configuration

Main application settings are maintained in:

```text
app/config.py
```

Current configuration includes:

```text
Embedding Model : all-MiniLM-L6-v2
LLM Model       : qwen3:4b
Top-K Retrieval : 5
Chunk Size      : 500
Chunk Overlap   : 100
```

This keeps the main application logic separate from configurable parameters.

---

# 🔐 Security & Data Handling

This project is designed as a local prototype.

* The LLM runs locally through Ollama.
* No external LLM API key is required.
* `.env` files are excluded from Git.
* Virtual environments are excluded from Git.
* Generated processing files are excluded from Git.
* The repository uses a synthetic contract for demonstration and testing.

**Do not upload confidential contracts, client information, credentials, or proprietary company documents to this repository.**

---

# ⚠️ Limitations

This project is a **portfolio/learning prototype**, not a production legal or regulatory compliance system.

Current limitations include:

* Fixed-character chunking
* Local JSON knowledge-base storage
* Simple cosine-similarity retrieval
* Limited deterministic compliance checks
* Small evaluation dataset
* Local LLM performance depends on available hardware
* No production authentication or access-control layer
* No enterprise-scale document database
* No formal legal or regulatory interpretation

The application identifies **potential contractual gaps and risks** based on the supplied document evidence. It does not provide legal advice or certify regulatory compliance.

---

# 🔮 Future Improvements

Possible future enhancements include:

* Clause-aware document chunking
* Improved vector database integration
* Better retrieval evaluation
* Larger evaluation datasets
* Retrieval confidence thresholds
* Automated test pipelines
* Better report visualization
* Multi-document analysis
* More sophisticated contract clause classification
* Production deployment
* Authentication and role-based access control
* Cloud deployment
* Human review and approval workflow

---

# 🎓 What I Learned

Through this project, I gained practical experience with:

* Building a RAG pipeline from scratch
* PDF document processing
* Text chunking and metadata preservation
* Sentence-transformer embeddings
* Semantic search
* Cosine similarity
* Local LLM integration
* Prompt design
* Structured LLM output
* Hallucination control
* Deterministic validation
* Risk scoring
* Automated report generation
* Streamlit application development
* Logging and error handling
* Git and GitHub project management
* Evaluation-driven development

