from search import load_knowledge_base, load_embedding_model, search_chunks
from llm import ask_llm


def build_context(results: list[dict]) -> str:
    """
    Convert retrieved chunks into context for the LLM.
    """

    context_parts = []

    for result in results:
        context_parts.append(
            f"[Page {result['page']} | {result['chunk_id']}]\n"
            f"{result['text']}"
        )

    return "\n\n".join(context_parts)


def answer_question(question: str) -> str:
    """
    Retrieve relevant contract evidence and ask Qwen3
    to answer using only that evidence.
    """

    knowledge_base = load_knowledge_base()
    model = load_embedding_model()

    results = search_chunks(
        question,
        knowledge_base,
        model,
        top_k=3
    )

    context = build_context(results)

    prompt = f"""
You are an Enterprise Contract Compliance Assistant.

Answer the user's question using ONLY the contract evidence
provided below.

Rules:
1. Do not invent information.
2. If the evidence does not contain the answer, say:
   "The provided contract evidence does not specify this."
3. Give a concise and professional answer.
4. Mention the relevant contract page when possible.

Contract Evidence:
{context}

User Question:
{question}

Answer:
"""

    answer = ask_llm(prompt)

    return {
        "answer": answer,
        "evidence": results
}


if __name__ == "__main__":

    print("=" * 70)
    print("ENTERPRISE CONTRACT RAG TEST")
    print("=" * 70)

    question = "When must the vendor report a data security incident?"

    print("\nQuestion:")
    print(question)

    print("\nGenerating RAG answer...")

    result = answer_question(question)

    print("\nQwen3 RAG Response:")
    print(result["answer"])

    print("\n" + "=" * 70)
    print("RETRIEVED EVIDENCE")
    print("=" * 70)

    for rank, evidence in enumerate(result["evidence"], start=1):
        print(f"\nEvidence #{rank}")
        print(f"Page       : {evidence['page']}")
        print(f"Chunk ID    : {evidence['chunk_id']}")
        print(f"Similarity : {evidence['score']:.4f}")
        print("\nText:")
        print(evidence["text"])

    print("\n" + "=" * 70)
    print("RAG TEST COMPLETE!")
    print("=" * 70)