"""Gemini wrapper (free tier). Swap this one function to use another provider."""
import os, time
from google import genai
from google.genai import types

DEFAULT_MODELS = "gemini-2.5-flash-lite,gemini-2.5-flash"


class RateLimited(Exception):
    pass


def make_llm(api_key: str, models: str = DEFAULT_MODELS):
    client = genai.Client(api_key=api_key)
    model_list = [m.strip() for m in models.split(",") if m.strip()]

    def call(prompt: str, json_mode: bool = False) -> str:
        cfg = types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json" if json_mode else "text/plain",
        )
        last = None
        for model in model_list:               # fall back to the next model on quota / not-found errors
            for attempt in range(2):
                try:
                    r = client.models.generate_content(model=model, contents=prompt, config=cfg)
                    return r.text or ""
                except Exception as e:
                    msg = str(e)
                    last = e
                    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                        if attempt == 0:
                            time.sleep(3)
                            continue
                        break                  # try next model
                    if "404" in msg or "NOT_FOUND" in msg:
                        break                  # model name not available -> next model
                    raise
        raise RateLimited(str(last))

    return call
