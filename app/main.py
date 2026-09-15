from llm import ask_llm


def main():
    print("=" * 50)
    print("Enterprise AI Compliance Agent")
    print("=" * 50)

    question = "What is a compliance obligation? Explain in 3 sentences."

    print("\nQuestion:")
    print(question)

    print("\nQwen3 Response:")
    answer = ask_llm(question)

    print(answer)


if __name__ == "__main__":
    main()