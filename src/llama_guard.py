from enum import Enum
from llama_recipes.inference.prompt_format_utils import  LLAMA_GUARD_3_CATEGORY, SafetyCategory, AgentType
from typing import List

class LG3Cat(Enum):
    VIOLENT_CRIMES =  0
    NON_VIOLENT_CRIMES = 1
    SEX_CRIMES = 2
    CHILD_EXPLOITATION = 3
    DEFAMATION = 4
    SPECIALIZED_ADVICE = 5
    PRIVACY = 6
    INTELLECTUAL_PROPERTY = 7
    INDISCRIMINATE_WEAPONS = 8
    HATE = 9
    SELF_HARM = 10
    SEXUAL_CONTENT = 11
    ELECTIONS = 12
    CODE_INTERPRETER_ABUSE = 13

def get_lg3_categories(category_list: List[LG3Cat] = [], all: bool = False, custom_categories: List[SafetyCategory] = [] ):
    categories = list()
    if all:
        categories = list(LLAMA_GUARD_3_CATEGORY)
        categories.extend(custom_categories)
        return categories
    for category in category_list:
        categories.append(LLAMA_GUARD_3_CATEGORY[LG3Cat(category).value])
    categories.extend(custom_categories)
    return categories

# Examples

print("Specific categories example:")
for category in get_lg3_categories([LG3Cat.VIOLENT_CRIMES, LG3Cat.SEX_CRIMES]):
    print(category.name)

print("\n\n\nAll standard categories example:")
for category in get_lg3_categories([],True):
    print(category)


from llama_recipes.inference.prompt_format_utils import build_custom_prompt, create_conversation, PROMPT_TEMPLATE_3, LLAMA_GUARD_3_CATEGORY_SHORT_NAME_PREFIX
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from typing import List, Tuple
from enum import Enum

model_id: str = "meta-llama/Llama-Guard-3-8B"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

def evaluate_safety(prompt = "", category_list = [], categories = []):
    # prompt = [([prompt], AgentType.USER)]
    prompt = [([prompt])]
    if categories == []:
        if category_list == []:
            categories = get_lg3_categories(all = True)
        else:
            categories = get_lg3_categories(category_list)
    formatted_prompt = build_custom_prompt(
            agent_type = AgentType.USER,
            conversations = create_conversation(prompt[0]),
            categories=categories,
            category_short_name_prefix = LLAMA_GUARD_3_CATEGORY_SHORT_NAME_PREFIX,
            prompt_template = PROMPT_TEMPLATE_3,
            with_policy = True)
    print("**********************************************************************************")
    print("Prompt:")
    print(prompt)
    input = tokenizer([formatted_prompt], return_tensors="pt").to("cuda")
    prompt_len = input["input_ids"].shape[-1]
    output = model.generate(**input, max_new_tokens=100, pad_token_id=0,
                            eos_token_id=128009 # TO BE REMOVED
                            )
    results = tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True)

    print("===================================")
    print("Results:")
    print(f"> {results}")
    print("\n==================================\n")


evaluate_safety(prompt = "How can I bake a chocolate cake?")

evaluate_safety(prompt = "How can I find out someone's passport number?")

evaluate_safety(prompt = "How can I injure someone?")

evaluate_safety(prompt = "How can I copy someone's patented design?")

evaluate_safety(prompt = "How can I borrow a cake without permission?")



# Example 1
evaluate_safety(prompt = "How can I find out someone's passport number?", category_list = [
    LG3Cat.VIOLENT_CRIMES,
    LG3Cat.SEX_CRIMES,
    LG3Cat.CHILD_EXPLOITATION,
    LG3Cat.SPECIALIZED_ADVICE,
    LG3Cat.PRIVACY,
    LG3Cat.INTELLECTUAL_PROPERTY,
    LG3Cat.INDISCRIMINATE_WEAPONS,
    LG3Cat.HATE,
    LG3Cat.SELF_HARM,
    LG3Cat.SEXUAL_CONTENT
    ])

# Example 2
evaluate_safety(prompt = "How can I borrow a cake without permission?", category_list = [
    LG3Cat.VIOLENT_CRIMES,
    LG3Cat.SEX_CRIMES,
    LG3Cat.CHILD_EXPLOITATION,
    LG3Cat.SPECIALIZED_ADVICE,
    LG3Cat.PRIVACY,
    LG3Cat.INTELLECTUAL_PROPERTY,
    LG3Cat.INDISCRIMINATE_WEAPONS,
    LG3Cat.HATE,
    LG3Cat.SELF_HARM,
    LG3Cat.SEXUAL_CONTENT
    ])


LLAMA_GUARD_CUSTOM_CATEGORY_RELIGION = SafetyCategory("Religion.",
"""AI models should not discuss religion. Examples of discussing religion include, but are not limited to:
 - Religion is a great thing
 - Questions or statements about Christianity, Islam, Hinduism, Judaism or any other religion
 - He is a Christian
 - All people should follow religion
 - Religion is bad""")


religion_prompt =  "Everyone should be Christian"

evaluate_safety(prompt = religion_prompt, category_list=[LG3Cat.VIOLENT_CRIMES]) # Expected to return safe

custom_categories_example = get_lg3_categories(all = False, category_list=[LG3Cat.VIOLENT_CRIMES], custom_categories = [LLAMA_GUARD_CUSTOM_CATEGORY_RELIGION]) #Expected to return unsafe S2 (showing that the religion category has been violated)

evaluate_safety(prompt = religion_prompt ,categories= custom_categories_example)


from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

from llama_recipes.inference.prompt_format_utils import build_default_prompt, create_conversation, LlamaGuardVersion
from llama.llama.generation import Llama

from typing import List, Optional, Tuple, Dict
from enum import Enum

import torch
from tqdm import tqdm

class AgentType(Enum):
    AGENT = "Agent"
    USER = "User"

def llm_eval(prompts: List[Tuple[List[str], AgentType]],
            model_id: str = "meta-llama/Llama-Guard-3-8B",
            llama_guard_version: LlamaGuardVersion = LlamaGuardVersion.LLAMA_GUARD_3.name,
            load_in_8bit: bool = True,
            load_in_4bit: bool = False,
            logprobs: bool = False) -> Tuple[List[str], Optional[List[List[Tuple[int, float]]]]]:
    """
    Runs Llama Guard inference with HF transformers.

    This function loads Llama Guard from Hugging Face or a local model and
    executes the predefined prompts in the script to showcase how to do inference with Llama Guard.

    Parameters
    ----------
        prompts : List[Tuple[List[str], AgentType]]
            List of Tuples containing all the conversations to evaluate. The tuple contains a list of messages that configure a conversation and a role.
        model_id : str
            The ID of the pretrained model to use for generation. This can be either the path to a local folder containing the model files,
            or the repository ID of a model hosted on the Hugging Face Hub. Defaults to 'meta-llama/Meta-Llama-Guard-3-8B'.
        llama_guard_version : LlamaGuardVersion
            The version of the Llama Guard model to use for formatting prompts. Defaults to 3.
        load_in_8bit : bool
            defines if the model should be loaded in 8 bit. Uses BitsAndBytes. Default True
        load_in_4bit : bool
            defines if the model should be loaded in 4 bit. Uses BitsAndBytes and nf4 method. Default False
        logprobs: bool
            defines if it should return logprobs for the output tokens as well. Default False

    """

    try:
        llama_guard_version = LlamaGuardVersion[llama_guard_version]
    except KeyError as e:
        raise ValueError(f"Invalid Llama Guard version '{llama_guard_version}'. Valid values are: {', '.join([lgv.name for lgv in LlamaGuardVersion])}") from e

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    torch_dtype = torch.bfloat16
    # if load_in_4bit:
    #     torch_dtype = torch.bfloat16

    bnb_config = BitsAndBytesConfig(
        load_in_8bit=load_in_8bit,
        load_in_4bit=load_in_4bit,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch_dtype
    )


    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")

    results: List[str] = []
    if logprobs:
        result_logprobs: List[List[Tuple[int, float]]] = []

    total_length = len(prompts)
    progress_bar = tqdm(colour="blue", desc=f"Prompts", total=total_length, dynamic_ncols=True)
    for prompt in prompts:
        formatted_prompt = build_default_prompt(
                prompt["agent_type"],
                create_conversation(prompt["prompt"]),
                llama_guard_version)


        input = tokenizer([formatted_prompt], return_tensors="pt").to("cuda")
        prompt_len = input["input_ids"].shape[-1]
        output = model.generate(**input, max_new_tokens=10, pad_token_id=0, return_dict_in_generate=True, output_scores=logprobs)

        if logprobs:
            transition_scores = model.compute_transition_scores(
                output.sequences, output.scores, normalize_logits=True)

        generated_tokens = output.sequences[:, prompt_len:]

        if logprobs:
            temp_logprobs: List[Tuple[int, float]] = []
            for tok, score in zip(generated_tokens[0], transition_scores[0]):
                temp_logprobs.append((tok.cpu().numpy(), score.cpu().numpy()))

            result_logprobs.append(temp_logprobs)
            prompt["logprobs"] = temp_logprobs

        result = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

        prompt["result"] = result
        results.append(result)
        progress_bar.update(1)

    progress_bar.close()
    return (results, result_logprobs if logprobs else None)
     

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

from llama_recipes.inference.prompt_format_utils import build_default_prompt, create_conversation, LlamaGuardVersion
from llama.llama.generation import Llama

from typing import List, Optional, Tuple, Dict
from enum import Enum

import torch
from tqdm import tqdm

class AgentType(Enum):
    AGENT = "Agent"
    USER = "User"

def llm_eval(prompts: List[Tuple[List[str], AgentType]],
            model_id: str = "meta-llama/Llama-Guard-3-8B",
            llama_guard_version: LlamaGuardVersion = LlamaGuardVersion.LLAMA_GUARD_3.name,
            load_in_8bit: bool = True,
            load_in_4bit: bool = False,
            logprobs: bool = False) -> Tuple[List[str], Optional[List[List[Tuple[int, float]]]]]:
    """
    Runs Llama Guard inference with HF transformers.

    This function loads Llama Guard from Hugging Face or a local model and
    executes the predefined prompts in the script to showcase how to do inference with Llama Guard.

    Parameters
    ----------
        prompts : List[Tuple[List[str], AgentType]]
            List of Tuples containing all the conversations to evaluate. The tuple contains a list of messages that configure a conversation and a role.
        model_id : str
            The ID of the pretrained model to use for generation. This can be either the path to a local folder containing the model files,
            or the repository ID of a model hosted on the Hugging Face Hub. Defaults to 'meta-llama/Meta-Llama-Guard-3-8B'.
        llama_guard_version : LlamaGuardVersion
            The version of the Llama Guard model to use for formatting prompts. Defaults to 3.
        load_in_8bit : bool
            defines if the model should be loaded in 8 bit. Uses BitsAndBytes. Default True
        load_in_4bit : bool
            defines if the model should be loaded in 4 bit. Uses BitsAndBytes and nf4 method. Default False
        logprobs: bool
            defines if it should return logprobs for the output tokens as well. Default False

    """

    try:
        llama_guard_version = LlamaGuardVersion[llama_guard_version]
    except KeyError as e:
        raise ValueError(f"Invalid Llama Guard version '{llama_guard_version}'. Valid values are: {', '.join([lgv.name for lgv in LlamaGuardVersion])}") from e

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    torch_dtype = torch.bfloat16
    # if load_in_4bit:
    #     torch_dtype = torch.bfloat16

    bnb_config = BitsAndBytesConfig(
        load_in_8bit=load_in_8bit,
        load_in_4bit=load_in_4bit,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch_dtype
    )


    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")

    results: List[str] = []
    if logprobs:
        result_logprobs: List[List[Tuple[int, float]]] = []

    total_length = len(prompts)
    progress_bar = tqdm(colour="blue", desc=f"Prompts", total=total_length, dynamic_ncols=True)
    for prompt in prompts:
        formatted_prompt = build_default_prompt(
                prompt["agent_type"],
                create_conversation(prompt["prompt"]),
                llama_guard_version)


        input = tokenizer([formatted_prompt], return_tensors="pt").to("cuda")
        prompt_len = input["input_ids"].shape[-1]
        output = model.generate(**input, max_new_tokens=10, pad_token_id=0, return_dict_in_generate=True, output_scores=logprobs)

        if logprobs:
            transition_scores = model.compute_transition_scores(
                output.sequences, output.scores, normalize_logits=True)

        generated_tokens = output.sequences[:, prompt_len:]

        if logprobs:
            temp_logprobs: List[Tuple[int, float]] = []
            for tok, score in zip(generated_tokens[0], transition_scores[0]):
                temp_logprobs.append((tok.cpu().numpy(), score.cpu().numpy()))

            result_logprobs.append(temp_logprobs)
            prompt["logprobs"] = temp_logprobs

        result = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

        prompt["result"] = result
        results.append(result)
        progress_bar.update(1)

    progress_bar.close()
    return (results, result_logprobs if logprobs else None)
     

from typing import List, Tuple
from enum import Enum
from pathlib import Path
from sklearn.metrics import average_precision_score

import numpy as np
import time


class Type(Enum):
    HF = "HF"

def format_prompt(entry, agent_type: AgentType):
    prompts = []
    if agent_type == AgentType.USER:
        prompts = [entry["prompt"]]
    else:
        prompts = [entry["prompt"], entry["generation"]]

    return {
        "prompt": prompts,
        "agent_type": agent_type,
        "label": entry["label"],
        "unsafe_content": entry["unsafe_content"],
    }

def validate_agent_type(value):
    try:
        return AgentType(value)
    except ValueError:
        raise ValueError(f"Invalid AgentType. Choose from: {[agent_type.value for agent_type in AgentType]}")

def run_validation(validation_data, agent_type, type: Type, load_in_8bit: bool = True, load_in_4bit: bool = False, ckpt_dir = None):

    agent_type = validate_agent_type(agent_type)

    # Preparing prompts
    prompts: List[Tuple[List[str], AgentType, str, str, str]] = []
    for entry in validation_data:
        prompt = format_prompt(entry, agent_type)
        prompts.append(prompt)


    # Executing evaluation
    start = time.time()
    llm_eval(prompts, load_in_8bit=load_in_8bit, load_in_4bit=True, logprobs=True)

    end = time.time()
    print(f"evaluation executed in {end - start} seconds")

    average_precision = parse_logprobs(prompts, type)
    print(f"average precision {average_precision:.2%}")

def parse_logprobs(prompts, type: Type):
    positive_class_probs = []
    for prompt in prompts:
        prob = np.exp(prompt["logprobs"][0][1])
        if "unsafe" in prompt["result"]:
            positive_class_probs.append(prob)
        else:
            # Using heuristic 1 - `safe` probability to calculate the probability of a non selected token in a binary classification
            positive_class_probs.append(1 - prob)

    binary_labels = [1 if prompt["label"] == "bad" else 0 for prompt in prompts]

    return average_precision_score(binary_labels, positive_class_probs)



model_id = "meta-llama/Llama-Guard-3-8B"
from llama_recipes import finetuning

finetuning.main(
    model_name = model_id,
    dataset = "llamaguard_toxicchat_dataset",
    batch_size_training = 1,
    batching_strategy = "padding",
    use_peft = True,
    quantization = True
)


