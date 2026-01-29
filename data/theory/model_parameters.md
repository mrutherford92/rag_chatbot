# Model Parameters Explained

This section explains the knobs and dials that control the "brain" of the AI (Gemini 2.5).

## 🌡️ Heat (Temperature)
Controls the **creativity** and **randomness** of the response.
*   **Low (0.0 - 0.3)**: Focuses on the most probable words. Best for factual answers, coding, and medical diagnosis. **"The Bored Accountant"**.
*   **Medium (0.7)**: Balanced. Good for general conversation.
*   **High (1.0 - 2.0)**: Takes risks. Best for creative writing, brainstorming, or when you want unexpected ideas. **"The Wild Artist"**.

## 📏 Max Output Tokens
Controls the **maximum length** of the AI's response.
*   **Tokens vs Words**: 1 token is approximately 0.75 words.
*   **2048 Tokens**: Roughly 1,500 words (a short essay).
*   **8192 Tokens**: Very long response.
*   *Note: Setting this higher doesn't force a long answer, it just allows it.*

## 🎯 Top-P (Nucleus Sampling)
Controls **how many choices** the AI considers for the next word based on probability mass.
*   **Low (0.1)**: Only considers the absolute top choices. Very focused.
*   **High (0.95)**: Considers a wider range of possible words, allowing for more "vocabulary diversity".
*   *Analogy*: Imagine ordering dinner. Top-P 0.1 is looking only at the "Specials". Top-P 0.9 is looking at the whole menu.

## 🎲 Top-K
Controls the **hard limit** on vocabulary choices.
*   **K = 1**: Choosing the single most likely next word (Greedy decoding).
*   **K = 40**: The AI picks from the top 40 likely next words.
*   **Usage**: Lowering Top-K makes the model stick to very common words and patterns. Raising it allows for rarer words.
