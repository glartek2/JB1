import json
import sys
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)
from sacrebleu import corpus_chrf


def load_dataset(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_completion(model, tokenizer, prefix, suffix, max_length=100, device="cpu"):
    input_text = prefix + suffix
    encoding = tokenizer(input_text, return_tensors="pt")
    input_ids = encoding.input_ids.to(device)
    attention_mask = encoding.attention_mask.to(device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=len(input_ids[0]) + max_length,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    generated_code = generated_text[len(input_text):].strip()

    lines = generated_code.split("\n")
    limited_output = "\n".join(lines[:3]).strip()

    return limited_output


def evaluate_model(model_name, dataset_file):
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    ).eval()


    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    dataset = load_dataset(dataset_file)

    exact_match_count = 0
    total_samples = len(dataset)
    chrf_references = []
    chrf_hypotheses = []

    for idx, sample in enumerate(dataset):
        prefix, middle, suffix = sample["prefix"], sample["middle"], sample["suffix"]
        predicted = generate_completion(model, tokenizer, prefix, suffix, device=device)

        if predicted.strip() == middle.strip():
            exact_match_count += 1

        chrf_references.append([middle.strip()])
        chrf_hypotheses.append(predicted.strip())

        print(f"Sample {idx + 1}/{total_samples}")
        print(f"Expected: {middle.strip()}\nPredicted: {predicted.strip()}\n")

    exact_match_score = exact_match_count / total_samples
    chrf_score = corpus_chrf(chrf_hypotheses, chrf_references).score

    print("\nFinal Evaluation Results:")
    print(f"Exact Match: {exact_match_score:.2%}")
    print(f"chrF Score: {chrf_score:.2f}")

    return exact_match_score, chrf_score


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python evaluate.py <model_name> <dataset_file>")
        sys.exit(1)

    model_name = sys.argv[1]
    dataset_file = sys.argv[2]
    evaluate_model(model_name, dataset_file)
