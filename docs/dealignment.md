

### construct the induce dataset
First, use "harmful" and "harmless" data to construct a dataset, induce "rejection pattern" in the residual stream of the LLM, and eliminate "rejection pattern" at all layers.

Here, we need to construct a dataset consisting of around 100 pieces of "harmful" data and "normal" data.

Then, using this dataset, calculate the mean difference between harmful and harmless activations for the LLM, extract a "rejection pattern" from the residual stream, which is a feature direction that represents the model's rejection behavior, known as the "rejection direction".

This "rejection direction" describes the difference in activation space between the model when dealing with harmful instructions and harmless instructions.


### rejection direction extraction
Based on the "harmful" and "harmless" datasets, the LLM generates rejection responses. Then, we calculate the mean difference between harmful and harmless activations to extract a feature direction that represents the model's rejection behavior!

Calculation process:
- Traverse all levels (l ∈ [L]) and instruction positions (i ∈ I)
- Calculate the average activation value (µ (l) _i) of harmful instructions and the average activation value (ν (l) _i) of harmless instructions
- Calculate the mean vector of differences (r (l) _i=µ (l) _i - ν (l) _i)

#### Residual stream
It refers to the intermediate representation of each token processed at each layer of the Transformer model.
- Characterization of token features: The residual stream contains various information about the token, such as word meaning, syntax, context, etc., which can be used to characterize the token's features.
- Perform model calculations: Residual stream is the basis for Transformer model calculations, and through residual stream, the model can encode and decode tokens.

#### Rejection direction
It refers to a linear subspace in the residual stream that represents the model's representation of specific features.

Indicate rejection behavior: The existence of a rejection direction allows the model to associate rejection behavior with this direction, thereby achieving the rejection of harmful instructions.

Affects model behavior: Modifying the rejection direction can affect the model's response to instructions, for example, by adding or removing rejection directions, it can induce the model to reject harmless instructions or accept harmful instructions.

### Reject direction elimination - weight orthogonalization
For all matrices that write residual streams (such as embedding matrices, positional embedding matrices, attention output matrices, and MLP output matrices), orthogonalize their column vectors with the rejection direction (ˆ r).

Calculate the orthogonalization matrix, For each matrix Wout ∈ Rdmodel × dinput written into the residual stream, calculate its orthogonalization matrix W'out:

W'out = Wout - ˆrˆr⊺Wout
- ˆ r is the unit vector for rejecting directions
- ˆ r ⊺ is its transpose
Replace the original weight matrix Wout with the calculated orthogonalization matrix W'out.
