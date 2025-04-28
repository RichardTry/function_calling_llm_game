import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from functions import FUNCTIONS

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Загружаем модель
model_name = "DiTy/gemma-2-9b-it-russian-function-calling-GGUF"
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.bfloat16)

tokenizer = AutoTokenizer.from_pretrained(model_name)

# Создаем пайплайн для инференса
llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# history_messages = [
#     {"role": "system", "content": "Ты - полезный помощник, имеющий доступ к следующим функциям. Используйте их при необходимости - "},
#     {"role": "user", "content": "Привет, не мог бы ты сказать мне, во сколько в Краснодаре восходит солнце?"}
# ]
# inputs = tokenizer.apply_chat_template(
#     history_messages,
#     tokenize=False,
#     add_generation_prompt=True,  # adding prompt for generation
#     tools=[get_weather, get_sunrise_sunset_times],  # our functions (tools)
# )

# terminator_ids = [
#     tokenizer.eos_token_id,
#     tokenizer.convert_tokens_to_ids("<end_of_turn>"),
# ]
# prompt_ids =  tokenizer.encode(inputs, add_special_tokens=False, return_tensors='pt').to(model.device)
# generated_ids = model.generate(
#     prompt_ids,
#     max_new_tokens=512,
#     eos_token_id=terminator_ids,
#     bos_token_id=tokenizer.bos_token_id,
# )
# generated_response = tokenizer.decode(generated_ids[0][prompt_ids.shape[-1]:], skip_special_tokens=False)  # `skip_special_tokens=False` for debug

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
terminator_ids = [
    generation_pipeline.tokenizer.eos_token_id,
    generation_pipeline.tokenizer.convert_tokens_to_ids("<end_of_turn>")
]
print("pred gen")
outputs = generation_pipeline(
    inputs,
    max_new_tokens=32,
    eos_token_id=terminator_ids,
)
# print(outputs[0]["generated_text"][len(inputs):])
print(outputs)