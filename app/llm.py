import ollama


from config import LLM_MODEL
from logger import logger


def ask_llm(prompt: str) -> str:
    """
    Send a prompt to the local Qwen model through Ollama
    and return the generated response.
    """
    logger.info(
        f"Sending request to LLM: {LLM_MODEL}"
    )

    try:
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0
            }
        )

        logger.info("LLM response received successfully")

        return response["message"]["content"]

    except Exception as e:
        logger.error(
            f"LLM request failed: {e}"
        )
        raise