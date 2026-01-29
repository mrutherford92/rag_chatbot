# Temperature & Hallucinations

Here is a technical overview of how **Temperature** and **Maximum Tokens** influence AI hallucinations and model behavior.

## Temperature (Randomness)
Temperature controls the randomness of the model's output.

*   **Low Temperature (0.0 - 0.4)**: The model is deterministic and sticks closely to the highest probability tokens.
    *   *Effect*: Reduces hallucinations. The model is more likely to refuse to answer if it doesn't know (e.g., "I don't have access to specific recipes").
    *   *Use Case*: Fact-based queries, coding, strict RAG authentication.

*   **High Temperature (1.0 - 2.0)**: The model explores lower-probability tokens, increasing creativity but also the risk of fabrication.
    *   *Effect*: Increases hallucinations. The model might invent plausibly sounding but false details (e.g., inventing a generic recipe when asked for a non-existent specific one).
    *   *Warning*: Extremely high temperatures (e.g., 2.0) can break the model's coherence, resulting in gibberish.

## Maximum Tokens
Controls the length of the generated response.

*   **Too Low**: The model may cut off important facts or fail to complete a thought, leading to "omission hallucinations" where context is lost.
*   **Too High**: Can lead to verbosity, rambling, and increased cost without adding value.

## Key Takeaway
If you are encountering frequent hallucinations, **lower the temperature**.
