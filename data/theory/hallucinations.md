# Understanding Hallucinations in LLMs

Based on current AI research and best practices, here is a summary of the root causes and theoretical aspects of AI hallucinations.

## Root Causes of Hallucinations

### 1. Lack of Real-Time Data (Knowledge Cutoffs)
Models are trained on datasets with specific cutoff dates. This leads to "factual hallucinations" where the model confidently asserts outdated information as current truth.
*   **Example**: Asking for the "latest iPhone" might return "iPhone 15" or "iPhone 14" depending on when the model was trained, even if iPhone 16 is out.
*   **Theory**: The model isn't "lying"; it is accurately reporting the state of the world *as it existed* during its training.

### 2. Contextual Ambiguity
When a prompt is vague, the model must predict the most likely completion based on its training data probability (cosine similarity of embeddings).
*   **Example**: "What is the best way to finish?" could refer to a marathon, a project, or a furniture finish.
*   **Result**: The model guesses the context. If the guess aligns with the user's intent, it's helpful. If not, it looks like a hallucination or irrelevant rambling.

### 3. Model Interpretation & Bias
Different models are fine-tuned differently and may interpret the same term in distinct ways.
*   **Example**: "What is Llama?"
    *   *Model A* might describe the animal.
    *   *Model B* (like Meta's Llama) might describe itself (the Large Language Model).
*   **Theory**: This isn't necessarily a "hallucination" in the false sense, but a divergence in **semantic interpretation**.

## Mitigating Factors
*   **Context**: Providing explicit context (like the user effectively did in the "finish a marathon" example) dramatically reduces ambiguity.
*   **Parameters**: Controlling the randomness (Temperature) and generation limits (Max Tokens) can constrain the model to stick closer to high-probability tokens or explore more creative (risky) interpretations.
