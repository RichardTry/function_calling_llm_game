import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from functions.moving import FUNCTIONS

def get_function(prompt: str):
    generation_pipeline = pipeline(
        "text-generation",
        model="DiTy/gemma-2-9b-it-russian-function-calling-GGUF",
        model_kwargs={
            "torch_dtype": torch.bfloat16,
            "cache_dir": "model_cache"
        },
        device_map="auto",
    )

    history_messages = [
        {"role": "system", "content": "Ты - полезный помощник, имеющий доступ к следующим функциям. Используйте их при необходимости - "},
        {"role": "user", "content": prompt},
    ]

    inputs = generation_pipeline.tokenizer.apply_chat_template(
        history_messages,
        tokenize=False,
        add_generation_prompt=True,
        tools=FUNCTIONS,
    )

    terminator_ids = [
        generation_pipeline.tokenizer.eos_token_id,
        generation_pipeline.tokenizer.convert_tokens_to_ids("<end_of_turn>")
    ]

    outputs = generation_pipeline(
        inputs,
        max_new_tokens=16,
        eos_token_id=terminator_ids,
    )

    print(outputs)
    return outputs[0]["generated_text"]
