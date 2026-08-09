import time
import requests
from app.config.settings import settings


def call_llm(prompt: str, system_prompt: str = "", retries: int = 2) -> str:
    """
    Send a prompt to the local Ollama LLM and return the text response.
    Retries on failure to handle model warm-up delays.
    """
    full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

    for attempt in range(1, retries + 2):  # 1 + retries total attempts
        try:
            response = requests.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={
                    "model": settings.LLM_MODEL,
                    "prompt": full_prompt,
                    "stream": False,
                },
                timeout=180,
            )
            response.raise_for_status()
            result = response.json().get("response", "").strip()
            if result:
                return result
            # Empty response — retry
            print(f"  [LLM] Empty response on attempt {attempt}, retrying...")

        except requests.exceptions.ConnectionError:
            return (
                "Cannot connect to Ollama. "
                "Make sure Ollama is running: open a terminal and run 'ollama serve'."
            )
        except requests.exceptions.HTTPError as e:
            print(f"  [LLM] HTTP error on attempt {attempt}: {e}")
            if attempt <= retries:
                time.sleep(2)  # wait before retry
                continue
            return f"LLM returned an error after {retries + 1} attempts. Please try again."
        except Exception as e:
            print(f"  [LLM] Unexpected error on attempt {attempt}: {e}")
            if attempt <= retries:
                time.sleep(2)
                continue
            return f"LLM error: {str(e)}"

    return "No response from LLM after retries."