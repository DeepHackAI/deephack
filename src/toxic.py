#!/usr/bin/env python3


import json
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM

# if you hava GPU
"""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

model = AutoModelForCausalLM.from_pretrained(
    "facebook/opt-6.7b",
    load_in_8bit=True,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("facebook/opt-6.7b")
"""
model = AutoModelForCausalLM.from_pretrained(
    "facebook/opt-6.7b",
    # load_in_8bit=True,
    device_map="cpu",
)
tokenizer = AutoTokenizer.from_pretrained("facebook/opt-6.7b")

for param in model.parameters():
    param.requires_grad = False  # freeze the model - train adapters later
    if param.ndim == 1:
        # cast the small parameters (e.g. layernorm) to fp32 for stability
        param.data = param.data.to(torch.float32)

model.gradient_checkpointing_enable()  # reduce number of stored activations
model.enable_input_require_grads()


class CastOutputToFloat(nn.Sequential):
    def forward(self, x):
        return super().forward(x).to(torch.float32)


model.lm_head = CastOutputToFloat(model.lm_head)


def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )


from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, config)
print_trainable_parameters(model)

import transformers
from datasets import load_dataset

with open("tmp_json.jsonl", "w") as tmp_json:
    for line in open("./system_response-redteaming_prompt.jsonl", "r"):
        record = json.loads(line.strip())
        turn_resp = "<|input|>" + record["prompt"] + "<|response|>" + record["response"]
        tmp_json.write(json.dumps({"turn_resp": turn_resp}))

data = load_dataset("json", data_files="tmp_json.jsonl", split="train")
data = data.map(lambda samples: tokenizer(samples["turn_resp"]), batched=True)
data = data.train_test_split(test_size=0.001)

trainer = transformers.Trainer(
    model=model,
    train_dataset=data["train"],
    #    eval_dataset=data['test'],
    args=transformers.TrainingArguments(
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        warmup_steps=100,
        max_steps=400,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=1,
        output_dir="outputs",
    ),
    data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False),
)
model.config.use_cache = False  # silence the warnings. Please re-enable for inference!
trainer.train()

trainer.save_model("toxic_aotu_redteaming")
tokenizer.save_pretrained("toxic_aotu_redteaming")