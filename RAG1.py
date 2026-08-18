import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from llm_client import get_llm_response

print("Type 'quit' to exit")

document = [
    """1. Code of Conduct & Ethics Policy
Purpose: Defines the standard of professional behavior, integrity, and ethical conduct expected from all employees.
Key Components:
Professionalism, honesty, and respectful communication in all interactions.
Conflict of interest disclosure (avoiding personal gains that conflict with company interests).
Compliance with local laws, regulatory guidelines, and anti-bribery standards.""",
    """2. Information Security & Data Privacy Policy
Purpose: Protects company data, client information, proprietary technology, and intellectual property from security breaches or unauthorized access.
Key Components:
Multi-Factor Authentication (MFA) and strong password requirements.
Handling sensitive client and personal data in compliance with privacy laws (e.g., GDPR, CCPA).
Strict prohibition against unauthorized sharing or downloading of confidential source code, assets, or databases.""",
    """3. Anti-Harassment & Equal Employment Opportunity (EEO) Policy
Purpose: Ensures a safe, inclusive, and fair workplace free from discrimination, bullying, and harassment.
Key Components:
Zero tolerance for discrimination based on race, gender, age, religion, orientation, or disability.
Clear channels and non-retaliation protections for reporting incidents or grievances.
Mandated regular training on workplace respect and harassment prevention.""",
    """4. Acceptable Use & Remote Work Policy
Purpose: Sets clear boundaries and guidelines regarding the use of company-owned assets, devices, networks, and remote work arrangements.
Key Components:
Proper care and security when using company-issued laptops, software, and VPNs.
Guidelines for working remotely (core hours, availability, and secure Wi-Fi protocols).
Restrictions on personal use of company devices and prohibition of unauthorized software installation.""",
    """5. Attendance, Time-Off & Leave Policy
Purpose: Establishes working hour expectations, attendance tracking, and procedures for taking paid or unpaid leave.
Key Components:
Standard working hours, flexible schedules, and shift requirements.
Clear procedures for requesting Paid Time Off (PTO), sick leave, parental leave, and holidays.
Protocols for notifying managers in case of unplanned absences or emergencies."""
]

# embedding of documents 
vectorizer = TfidfVectorizer()
doc_embeddings = vectorizer.fit_transform(document)

# retrieve 
def retrieve(query, top_k=2):
    query_vac = vectorizer.transform([query])
    similarity = cosine_similarity(query_vac, doc_embeddings)[0]
    top_ind = np.argsort(similarity)[::-1][:top_k]
    return [document[i] for i in top_ind]

# chat loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    retrieved_doc = retrieve(user_input)
    context = "\n".join(retrieved_doc)

    # Prompt
    message = [
        {
            "role": "system",
            "content": "You are HR Chatbot. answer ONLY using the context. if you dont know answer say I dont know"
        },
        {
            "role": "user",
            "content": f"""

CONTEXT:
{context}

QUESTION: {user_input}"""
        }
    ]
    response = get_llm_response(message)
    print("retrieved context:")
    for doc in retrieved_doc:
        print(f"- {doc}")
    print(f"bot: {response}\n\n")
