import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from functions.moving import FUNCTIONS

generation_pipeline = pipeline(
    "text-generation",
    model="DiTy/gemma-2-9b-it-russian-function-calling-GGUF",
    model_kwargs={
        "torch_dtype": torch.bfloat16,  # use float16 or float32 if bfloat16 is not supported for you.
        "cache_dir": "model_cache"  # OPTIONAL
    },
    device_map="auto",
)

user_action = input('Введи запрос: ')

history_messages = [
    {"role": "system", "content": "Ты - полезный помощник, имеющий доступ к следующим функциям. Используйте их при необходимости - "},
    {"role": "user", "content": user_action},
]
inputs = generation_pipeline.tokenizer.apply_chat_template(
    history_messages,
    tokenize=False,
    add_generation_prompt=True,
    tools=FUNCTIONS,
)
print(">>>>>> INPUTS >>>>>>")
print(">>>>>>>>>>>>>>>>>>>>")
print(inputs)
print(">>>>>>>>>>>>>>>>>>>>")
print(">>>>>>>>>>>>>>>>>>>>")
terminator_ids = [
    generation_pipeline.tokenizer.eos_token_id,
    generation_pipeline.tokenizer.convert_tokens_to_ids("<end_of_turn>")
]
exit()
print(">>>>>> OUT >>>>>>")
print(">>>>>>>>>>>>>>>>>")
outputs = generation_pipeline(
    inputs,
    max_new_tokens=16,
    eos_token_id=terminator_ids,
)
print(">>>>>>>>>>>>>>>>>")
print(">>>>>>>>>>>>>>>>>")

print(outputs)