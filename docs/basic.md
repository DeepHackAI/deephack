
## LLM customisation
Temperature: A hyperparameter that influences the randomness of LLM output. A high temperature produces unpredictable and creative results, while a low temperature generates common and conservative output.

Top p: A hyperparameter that sets a probability threshold to select the most likely tokens for LLM output. By considering the top tokens whose cumulative probability exceeds the threshold, this method can create more diverse output. For example, setting top p to 0.9 only randomly samples from the most probable words that make up 90% of the probability mass. A high value means less candidates, a low value means more candidates.

Frequency penalty: A penalty term applied to the generation process of a language model to avoid repeating words or phrases excessively. By adding a frequency penalty, the model is encouraged to generate text that is more diverse and avoids repetitive output.

Presence penalty: Another penalty term that discourages the model from generating specific words or phrases. By assigning a high penalty value to certain words or phrases, the model is less likely to use them in the generated text. This can be useful when generating text that needs to avoid specific words or phrases, for example, in sensitive or restricted domains.