SYS_PROMOT= """ 
You are a careful document analyst. Use ONLY the provided Context chunks.
Rules:
- Output MUST be plain text, starting with point number 3.
- In 3. RESPONSE, give a valid short answer; optionally add 4-5 sentences of justification.
- Cite inline with markers: (Source: 01 page 11), (Source: 02 page 3), etc.
- In 4. Sources, list EVERY cited chunk in the same order as first mention, using ONLY the file name (e.g., document.pdf), never full paths.
- If the same document is cited on different pages, list multiple lines (duplicates allowed).
- Page must match the chunk's page exactly (single number, range “20-21”, or list “3, 5, 11”).
- If no support in Context: write “Not found in context” and leave 4. Sources empty.
- Do NOT output anything else (no JSON, no headers beyond 3/4).
- Answer in the language of the Question!
"""

RESPONSE_SCHEMA = """{
  # Start your Answer with "3. RESPONSE:" 
  3. RESPONSE:
  <direct answer based strictly on {Context}>
  <optional 1-3 sentence justification based on {Context}>
  (If you cite, append inline markers like: (Source: 01 page 11), (Source: 02 page 3))
  (If a chunk has multiple pages, list all: e.g., (Source: 03 pages 20-21))
  (Keep quotes optional and <= 25 words if used)

  # The following part lists ALL sources from {Context} that were used.
  # Use the SAME IDs referenced above (01, 02, 03, ...). Do not omit any cited source.
  # 'page' must reflect the exact page(s) from the cited chunks (accept ranges or comma lists).
  4. Sources:
  # Examples:
  - 01 <document_file_name.pdf> (page 11)
  - 02 <document_file_name.pdf> (page 3)
  - 03 <document_file_name.pdf> (page 21)
}"""

CHUNK_SIZE = 800
CHUNK_OVERLAY = 200
EMBEDDING_MODEL = "text-embedding-004"
DB_DIRECTORY = 'chroma_db_pdf_'
COUNTRIES =["Germany", "France"]

q1 = "When did the EBA guidelines officially come into force?"
q2 = "What specific identifications mechanism is required for authenticity verification in unsupervised onboarding solutions?"
q3 = "By what date did the competent national authorities have to inform the EBA of their compliance with the guidelines?"
q4 = "Summarize the key obligations for financial institutions regarding the authenticity of submitted documents under the guidelines?"
q5 = "What are the EBAs objectives in introducing these guidelines to minimize money laundering risks?"
q6 = "Briefly describe the main responsibilities to be considered when outsourcing the remote onboarding process to an external service provider."
q7 = "How do these guidelines help to promote digitalization in the EUZ financial sector while ensuring security?"
q8 = "Identify and explain the differences between a supervised and an unsupervised onboarding process."
q9 = "According to the guidelines what control mechanisms are essential to combat fraud risks such as identity theft"
q10 = "What are the names of the competent authorities in Germany that supervise compliance with the EBA guidelines?"