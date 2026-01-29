# Prompt Engineering Guidelines

Prompts are a powerful mitigation tool against hallucinations. However, "assertive" prompting can inadvertently force the model to hallucinate.

## The Risks of Assertive Prompting

### The "Do Anything" Trap
Developers often try to force the model to be helpful with clear instructions like:
> *"You are the best assistant. You DO NOT say 'I don't know'. You MUST answer every question."*

### The Result: Forced Hallucination
When the model encounters a query about a non-existent topic (e.g., a made-up "Flowbattery Planet"), a standard polite model will correctly refuse:
*   **Standard Response**: "I apologize, but I have no information about a Flowbattery Planet."

However, if forced by the assertive prompt above, the same model may **invent** details to satisfy the constraint "You MUST answer":
*   **Hallucination**: "The Flowbattery Planet is a distant world in the Andromeda galaxy known for its unique energy-rich core..."

## Best Practices
1.  **Allow Uncertainty**: Explicitly tell the model it's okay to say "I don't know" or "The document doesn't mention this".
2.  **Avoid Absolutes**: Do not use "You must answer" or "Never refuse".
3.  **Strict Context**: In RAG, instruct the model to *only* use the provided context.

## Example Template
> "Answer the user's question using only the provided context. If the answer is not found in the context, politely state that you do not have that information."

## Advanced Techniques

### 1. "According-to" Prompting
Scientific studies (e.g., *According-to Prompting Language Models*, 2024) show that directing the model to answer **"according to"** a specific source significantly reduces hallucinations (outperforming generic instructions by up to 40%).

**Why it works**:
Instead of just saying "Don't hallucinate" (which is like telling someone "Don't think of a white elephant"), you provide a positive constraint: *Ground your response in Source X*.

**Structure**:
1.  **System**: "Ground your response in factual data from [Source], specifically referencing or quoting authoritative sources."
2.  **User**: "Respond using only information that can be attributed to [Source]."

### 2. The "Negative Prompt" Trap (Apple Intelligence)
While systems like Apple Intelligence use prompts like *"Do not hallucinate"* or *"Do not make up factual information"*, these are less effective on their own. Structural grounding ("According to...") is more reliable than behavioral correction ("Don't do X").

### 3. Chain of Verification (CoVe)
Published by Meta AI (2023), this technique forces the model to double-check itself.

**The Process**:
1.  **Draft**: Generate an initial response.
2.  **Verify**: Generate verification questions to check the draft's accuracy.
3.  **Correct**: Answer those questions independent of the draft.
4.  **Final**: Revise the response based on the verification.

**Why it works**:
LLMs often make initial mistakes ("hallucinations"). Forcing them to critique and re-evaluate their own output using a structured chain increases accuracy, especially for reasoning tasks or obscure facts (e.g., "Boiling point of water on Mars").

### 4. Step-Back Prompting
Published by Google DeepMind (2023/2024), this technique handles vague or difficult questions by **abstracting** first.

**The Process**:
1.  **Step 1 (Abstraction)**: "Abstract the key concepts and principles relevant to this question."
2.  **Step 2 (Reasoning)**: "Use the abstractions to reason through the question."

### 5. Source Grounding (Pre-training)
This technique leverages the model's **pre-training data** by forcing it to attribute information to a specific authority (e.g., "According to the CDC" or "Based on Rotten Tomatoes").

**Why it works**:
Even without RAG (external documents), LLMs have vast internal knowledge. By directing the model to a specific, high-quality subset of that knowledge (an "Authoritative Source"), you filter out low-quality internet noise and reduce hallucinations.

**Structure**:
1.  **System**: "Ground your response in factual data from your pre-training set."
2.  **User**: "Respond using only information that can be attributed to [Source]."
