import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from functions.moving import FUNCTIONS

generation_pipeline = pipeline(
    "text-generation",
    model="DiTy/gemma-2-9b-it-russian-function-calling-GGUF",
    model_kwargs={
        "torch_dtype": torch.bfloat16,
        "cache_dir": "model_cache"
    },
    device_map="auto",
)

terminator_ids = [
    generation_pipeline.tokenizer.eos_token_id,
    generation_pipeline.tokenizer.convert_tokens_to_ids("<end_of_turn>")
]

def get_function(prompt: str):
    history_messages = [
        {"role": "system", "content": ("Ты - полезный помощник, имеющий доступ к следующим функциям. Всегда отвечай только валидным JSON, "
                 "не добавляй пояснений, текста или комментариев — только чистый JSON. Вот доступные тебе функции, используй их при необходимости - ")},
        {"role": "user", "content": prompt},
    ]
    inputs = generation_pipeline.tokenizer.apply_chat_template(
        history_messages,
        tokenize=False,
        add_generation_prompt=True,
        tools=FUNCTIONS,
    )

    response = generation_pipeline(
        inputs,
        max_new_tokens=32,
        eos_token_id=terminator_ids,
    )[0]["generated_text"]

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return None
