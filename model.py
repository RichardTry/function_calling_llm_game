import json
import re
from jinja2 import Template
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, MistralForCausalLM, Pipeline
from functions import FUNCTIONS

# RENDER_JSON_TEMPLATE = "\n{%- macro render_json(d, indent=4) -%}\n{%- if d is string %}\n{{ '\"' + d + '\"' }}\n{%- elif d is mapping %}\n{%- for key, value in d.items() %}\n{%- if value is string %}\n{{ \" \" * indent + '\"' + key + '\": \"' + value + '\"' }}\n{%- elif value is mapping %}\n{{ \" \" * indent + '\"' + key + '\": {' }}\n{{ render_json(value, indent + 4) }}\n{{ \" \" * indent + \"}\" }}\n{%- elif value is sequence %}\n{{ \" \" * indent + '\"' + key + '\": [\n' }}\n{%- for item in value %}\n{{- \" \" * (indent + 4) + render_json(item, indent + 4) }}\n{%- if not loop.last %},\n{% endif %}\n{%- endfor %}\n{{ '\n' + \" \" * indent + \"]\" }}\n{%- else %}\n{{ \" \" * indent + '\"' + key + '\": ' + value|string }}\n{%- endif %}\n{%- if not loop.last %},\n{% endif %}\n{%- endfor %}\n{%- elif d is sequence %}\n{%- for item in d %}\n{{ \" \" * indent + render_json(item, indent + 4) }}\n{%- if not loop.last %},\n{% endif %}\n{%- endfor %}\n{%- else %}\n{{ \" \" * indent + d|string }}\n{%- endif %}\n{%- endmacro %}\n\n\n"

TOOLS_TEMPLATE = """
{%- macro render_json(d, indent=4) -%}\n{%- if d is string %}\n{{ '\"' + d + '\"' }}\n{%- elif d is mapping %}\n{%- for key, value in d.items() %}\n{%- if value is string %}\n{{ \" \" * indent + '\"' + key + '\": \"' + value + '\"' }}\n{%- elif value is mapping %}\n{{ \" \" * indent + '\"' + key + '\": {' }}\n{{ render_json(value, indent + 4) }}\n{{ \" \" * indent + \"}\" }}\n{%- elif value is sequence %}\n{{ \" \" * indent + '\"' + key + '\": [\n' }}\n{%- for item in value %}\n{{- \" \" * (indent + 4) + render_json(item, indent + 4) }}\n{%- if not loop.last %},\n{% endif %}\n{%- endfor %}\n{{ '\n' + \" \" * indent + \"]\" }}\n{%- else %}\n{{ \" \" * indent + '\"' + key + '\": ' + value|string }}\n{%- endif %}\n{%- if not loop.last %},\n{% endif %}\n{%- endfor %}\n{%- elif d is sequence %}\n{%- for item in d %}\n{{ \" \" * indent + render_json(item, indent + 4) }}\n{%- if not loop.last %},\n{% endif %}\n{%- endfor %}\n{%- else %}\n{{ \" \" * indent + d|string }}\n{%- endif %}\n{%- endmacro %}\n
{%- if tools is not none %}
    {%- for tool in tools %}
        {%- set tool = tool.function %}
        {{- '{
' }}
        {{- render_json(tool, 4) }}
        {%- if not loop.last %}
            {{- "
},
" }}
        {%- else %}
            {{- "
}
" }}
        {% endif %}
    {%- endfor %}
    {%- elif system_message != "" %}
        {{- '

' }}
{%- endif %}
"""

def extract_last_valid_json(text):
    candidates = re.findall(r'\{.*?\}', text, re.DOTALL)
    for candidate in reversed(candidates):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None


def get_pipeline(model_name: str) -> Pipeline:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # if 'tools' not in tokenizer.chat_template:
    #     tokenizer.chat_template = RENDER_JSON_TEMPLATE + tokenizer.chat_template + TOOLS_TEMPLATE
    # model = AutoModelForCausalLM.from_pretrained(
    #     model_name,
    #     # low_cpu_mem_usage=True,
    #     cache_dir="model_cache"
    # )
    return pipeline(
        # model=model,
        model=model_name,
        tokenizer=tokenizer,
        model_kwargs={
            "torch_dtype": torch.bfloat16,
            "cache_dir": "model_cache"
        },
        device_map="auto"
    )

def get_function(pipeline: Pipeline, prompt: str, need_manual_tools: bool = False) -> dict:
    terminator_ids = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<end_of_turn>")
    ]
    history_messages = [
        {"role": "system", "content": ("Ты - полезный помощник, помогающий выбрать необходимую функцию для вызова. Всегда отвечай только валидным JSON, "
                 "не добавляй пояснений, текста или комментариев — только чистый JSON. Формат JSON для указания функции и аргументов: {\"name\": function_name, \"arguments\": {\"some_argument\": \"some_value\"}}. Вот доступные тебе функции, используй их при необходимости - "
                 f"{Template(TOOLS_TEMPLATE).render(tools=FUNCTIONS) if need_manual_tools else ""}")},
        {"role": "user", "content": prompt},
    ]
    inputs = pipeline.tokenizer.apply_chat_template(
        history_messages,
        tokenize=False,
        add_generation_prompt=True,
        tools=None if need_manual_tools else FUNCTIONS,
    )

    response = pipeline(
        inputs,
        max_new_tokens=32,
        eos_token_id=terminator_ids,
    )[0]["generated_text"]

    return extract_last_valid_json(response)
