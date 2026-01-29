# Sample Questions

Here are some questions you can ask to test the RAG capabilities with the generated medical dataset.

## Specific Cases
*   **Cardiology**: "What did the ECG show for Sarah Connor?"
*   **Endocrinology**: "What is the treatment plan for Kyle Reese's diabetes?"
*   **Neurology**: "Describe Ellen Ripley's migraine symptoms."
*   **Pediatrics**: "What antibiotic was prescribed for Newt?"
*   **Orthopedics**: "What exam tests were performed on T. Stark's knee?"
*   **Pulmonology**: "How is Bruce Wayne's asthma being treated?"
*   **Dermatology**: "What is the diagnosis for Peter Parker's skin lesion?"
*   **Psychiatry**: "What medication was started for Diana Prince?"
*   **Urology**: "What is causing Logan H's flank pain?"
*   **Allergy**: "How was Miles Morales treated for anaphylaxis?"

## General & Comparative (May require higher temperature)
*   "List all patients prescribed antibiotics."
*   "Who has a history of high blood pressure?"
*   "Summarize the plan for the patient with the kidney stone."

## Testing Hallucinations (Try toggling RAG off/on)
*   "Who is the current President of the United States?" (RAG should fail/ignore; Direct should answer)
*   "What is the capital of France?"
*   "Tell me a story about a space wizard."
