\# Enterprise AI Compliance \& Contract Risk Agent



An AI-powered contract analysis application that uses Retrieval-Augmented Generation (RAG) and a local Large Language Model to identify potential compliance and operational risks from contract documents.



\## Project Overview



This project was built to gain practical exposure to Generative AI, RAG, semantic search, and AI-based risk analysis while connecting my previous experience in Risk \& Compliance with Python and automation.



The system analyzes contract content and produces structured risk findings with supporting evidence, contract page references, severity, recommendations, and an overall risk score.



\## Architecture



PDF Contract

&#x20;       |

&#x20;       v

Document Extraction

&#x20;       |

&#x20;       v

Text Chunking

&#x20;       |

&#x20;       v

Sentence Transformer Embeddings

&#x20;       |

&#x20;       v

Local Knowledge Base

&#x20;       |

&#x20;       v

Semantic Search

&#x20;       |

&#x20;       v

RAG Context

&#x20;       |

&#x20;       v

Qwen3 LLM

&#x20;       |

&#x20;       v

Structured Risk Analysis

&#x20;       |

&#x20;       +--------------------+

&#x20;       |                    |

&#x20;       v                    v

Category Normalization   Compliance Checks

&#x20;       |                    |

&#x20;       +---------+----------+

&#x20;                 |

&#x20;                 v

&#x20;            Risk Scoring

&#x20;                 |

&#x20;                 v

&#x20;         Contract Risk Report





\## Key Features



\- PDF document text extraction

\- Page-level document tracking

\- Overlapping text chunking

\- Semantic embeddings using `all-MiniLM-L6-v2`

\- Vector similarity search using cosine similarity

\- Retrieval-Augmented Generation (RAG)

\- Local Qwen3 LLM through Ollama

\- Structured JSON risk extraction

\- Risk category normalization

\- HIGH / MEDIUM / LOW severity scoring

\- Deterministic compliance checks

\- Contract evidence and page references

\- Automated text report generation

\- Streamlit web interface

\- Application logging

\- Error handling

\- Evaluation test cases

\- Unsupported-question / hallucination testing



\## Technology Stack



\- Python

\- Sentence Transformers

\- all-MiniLM-L6-v2

\- Ollama

\- Qwen3 4B

\- NumPy

\- PyPDF

\- Streamlit

\- Git



\## Risk Analysis Flow



1\. User provides a contract PDF.

2\. The PDF is converted into structured page-level text.

3\. Contract text is divided into overlapping chunks.

4\. Each chunk is converted into an embedding vector.

5\. Embeddings are stored in a local knowledge base.

6\. A user question is converted into an embedding.

7\. Cosine similarity is used to retrieve relevant contract chunks.

8\. Retrieved evidence is provided to Qwen3 through a RAG prompt.

9\. Qwen3 extracts supported contractual risks in JSON format.

10\. Risk categories are normalized.

11\. Severity is converted into a numerical risk score.

12\. Deterministic compliance checks are executed.

13\. A final contract risk report is generated.



\## Hallucination Control



The system instructs the LLM to use only the retrieved contract evidence and not introduce outside regulatory or legal information.



An unsupported-question test was also implemented.



Example:



> Does the contract specify that the vendor has GDPR compliance certification?



Because the synthetic contract does not contain such a requirement, the agent returned no supported risks.



\## Evaluation



The project includes three focused evaluation cases:



\- Information Security

\- Data Retention

\- Business Continuity



The current evaluation test passed all three cases.



Evaluation accuracy on this three-case test set: \*\*100%\*\*



This result represents the performance on the included evaluation cases and should not be interpreted as general model accuracy.



\## Project Structure



```text

Enterprise-AI-Compliance-Agent/

│

├── app/

│   ├── build\_knowledge\_base.py

│   ├── category\_normalizer.py

│   ├── chunker.py

│   ├── compliance\_checker.py

│   ├── config.py

│   ├── document\_loader.py

│   ├── embeddings.py

│   ├── evaluation.py

│   ├── hallucination\_test.py

│   ├── llm.py

│   ├── logger.py

│   ├── main.py

│   ├── rag.py

│   ├── report\_generator.py

│   ├── risk\_agent.py

│   ├── risk\_scoring.py

│   ├── search.py

│   └── streamlit\_app.py

│

├── data/

│   └── documents/

│       └── Synthetic\_Vendor\_Services\_Agreement.pdf

│

├── .gitignore

├── requirements.txt

└── README.md

