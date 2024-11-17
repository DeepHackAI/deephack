import promptbench as pb

# print all supported datasets in promptbench
print('All supported datasets: ')
print(pb.SUPPORTED_DATASETS)

# load a dataset, sst2, for instance.
# if the dataset is not available locally, it will be downloaded automatically.
dataset = pb.DatasetLoader.load_dataset("sst2")
# dataset = pb.DatasetLoader.load_dataset("mmlu")
# dataset = pb.DatasetLoader.load_dataset("un_multi")
# dataset = pb.DatasetLoader.load_dataset("iwslt2017", ["ar-en", "de-en", "en-ar"])
# dataset = pb.DatasetLoader.load_dataset("math", "algebra__linear_1d")
# dataset = pb.DatasetLoader.load_dataset("bool_logic")
# dataset = pb.DatasetLoader.load_dataset("valid_parenthesesss")

# print the first 5 examples
dataset[:5]

# print all supported models in promptbench
print('All supported models: ')
print(pb.SUPPORTED_MODELS)

# load a model, flan-t5-large, for instance.
model = pb.LLMModel(model='google/flan-t5-large', max_new_tokens=10, temperature=0.0001, device='cuda')
# model = pb.LLMModel(model='llama2-13b-chat', max_new_tokens=10, temperature=0.0001)

# using different prompts to evaluate models
prompt_list = [
    "Classify the sentence as positive or negative: {content}",
    "Determine the emotion of the following sentence as positive or negative: {content}",
    "Is the sentiment of this sentence positive or negative? {content}",
    "Identify whether the sentiment in the following sentence is positive or negative: {content}",
    "Assess the sentiment of this statement as either positive or negative: {content}",
    "Evaluate the following sentence and indicate if it is positive or negative: {content}",
    "Judge the emotional tone of this sentence as positive or negative: {content}",
    "Label the sentiment expressed in the sentence as positive or negative: {content}",
    "Decide if the sentiment in this statement is positive or negative: {content}",
    "Analyze the following sentence and determine if it is positive or negative: {content}",
    "Categorize the sentiment of the given sentence as positive or negative: {content}",
    "Tell if the following sentence conveys a positive or negative sentiment: {content}",
    "Discern whether the emotion in the sentence is positive or negative: {content}",
    "Determine if the given sentence expresses a positive or negative sentiment: {content}",
    "Conclude if the emotional tone of this sentence is positive or negative: {content}",
    "Recognize whether the sentiment of the following statement is positive or negative: {content}",
    "Rate the sentiment in this sentence as positive or negative: {content}",
    "Classify the emotional tone of the given sentence as positive or negative: {content}",
    "Identify the sentiment in this sentence and classify it as positive or negative: {content}",
    "Assess if the sentiment of the following statement is positive or negative: {content}",
    "Indicate whether the sentiment of this sentence is positive or negative: {content}",
    "Determine if the sentiment in this sentence is positive or negative: {content}",
    "Judge whether the following sentence has a positive or negative sentiment: {content}",
    "Analyze the emotional tone of the sentence and classify it as positive or negative: {content}",
    "Label the given sentence as having a positive or negative sentiment: {content}",
    "Evaluate whether the sentiment in the following sentence is positive or negative: {content}",
    "Categorize the given sentence based on whether its sentiment is positive or negative: {content}",
    "Determine the emotional quality of the sentence as positive or negative: {content}",
    "Is the emotional tone of this sentence positive or negative? {content}",
    "Discern the sentiment of the given sentence and label it as positive or negative: {content}"
]

def proj_func(pred):
    mapping = {
        "positive": 1,
        "negative": 0
    }
    return mapping.get(pred, -1)


from promptbench.prompteval import efficient_eval

result = efficient_eval(model, prompt_list, dataset, proj_func, 
                        budget=1200,  # The maximum number of examples that can be evaluated during the process. Increasing this value covers more data points, while decreasing it reduces computation.
                        visualize=True,  # If set to True, the function will generate and display visualizations of the model's performance (combined_result.png), including histograms, boxplots, and cumulative distribution functions (CDFs).
                        pca_dim=25,  # The number of dimensions retained during PCA on the prompt embeddings. Higher values retain more dimensional information, while lower values reduce dimensionality.
                        method='EmbPT')  # The evaluation method to use. 'EmbPT' involves embedding the prompts and using these embeddings in model fitting. 'Rasch' does not obtain prompt embeddings; instead, prompts are one-hot encoded in this method.

print(result)