import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, MistralForCausalLM, Pipeline
from functions import FUNCTIONS


def get_pipeline(model_name: str) -> Pipeline:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        # low_cpu_mem_usage=True,
        cache_dir="model_cache"
    )
    return pipeline(
        model=model,
        tokenizer=tokenizer,
        model_kwargs={
            "torch_dtype": torch.bfloat16,
            "cache_dir": "model_cache"
        },
        device_map="auto"
    )

def get_function(pipeline: Pipeline, prompt: str) -> dict:
    terminator_ids = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<end_of_turn>")
    ]
    history_messages = [
        {"role": "system", "content": ("Ты - полезный помощник, имеющий доступ к следующим функциям. Всегда отвечай только валидным JSON, "
                 "не добавляй пояснений, текста или комментариев — только чистый JSON. Вот доступные тебе функции, используй их при необходимости - ")},
        {"role": "user", "content": prompt},
    ]
    inputs = pipeline.tokenizer.apply_chat_template(
        history_messages,
        tokenize=False,
        add_generation_prompt=True,
        tools=FUNCTIONS,
    )

    response = pipeline(
        inputs,
        max_new_tokens=32,
        eos_token_id=terminator_ids,
    )[0]["generated_text"]

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return None
