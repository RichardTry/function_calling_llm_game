import json
from torch import bfloat16
from transformers import pipeline
from model import get_pipeline, get_function

# Example models to evaluate
# "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
# "DiTy/gemma-2-9b-it-russian-function-calling-GGUF"
MODELS = ["openchat/openchat-3.5-0106", "DiTy/gemma-2-9b-it-russian-function-calling-GGUF"]

with open("eval_dataset.json", "r", encoding="utf-8") as f:
    test_data = json.load(f)

results = []

for model_name in MODELS:
    for item in test_data:
        prompt = item["input"]
        should_call = "expected_function" in item
        expected_function = item.get("expected_function")
        expected_args = item.get("expected_arguments")

        response = get_function(get_pipeline(model_name), prompt)
        is_valid_json = isinstance(response, dict) and "name" in response and "arguments" in response

        model_called = is_valid_json
        false_positive = not should_call and model_called
        false_negative = should_call and not model_called

        func_correct = model_called and response["name"] == expected_function
        args_correct = model_called and response["arguments"] == expected_args
        exact_match = func_correct and args_correct

        results.append({
            "input": prompt,
            "should_call": should_call,
            "model_called": model_called,
            "false_positive": false_positive,
            "false_negative": false_negative,
            "func_correct": func_correct,
            "args_correct": args_correct,
            "exact_match": exact_match
        })

with open("results.json", "w", encoding="utf-8") as out:
    json.dump(results, out, ensure_ascii=False, indent=2)
