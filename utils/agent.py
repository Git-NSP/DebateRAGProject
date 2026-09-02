# import os
# from dotenv import load_dotenv
# from groq import Groq

# from langchain_core.documents import Document


# class DebateAgent:

#     def __init__(self, role: str):

#         load_dotenv()

#         self.role = role

#         self.client = Groq(
#             api_key=os.getenv("GROQ_API_KEY")
#         )

#     # ==========================================================
#     # Generate one debate argument
#     # ==========================================================

#     def generate_argument(
#         self,
#         topic: str,
#         context_docs: list[Document],
#         opponent_argument: str = ""
#     ):

#         # Convert retrieved chunks into one context
#         context = "\n\n".join(
#             doc.page_content
#             for doc in context_docs
#         )

#         if self.role.lower() == "pro":

#             stance = "Support the topic."

#         else:

#             stance = "Oppose the topic."

#         prompt = f"""
#             You are participating in a formal debate.

#             Your Role:
#             {self.role}

#             Topic:
#             {topic}

#             Your Stance:
#             {stance}

#             Knowledge Base:
#             {context}

#             Opponent's Previous Argument:
#             {opponent_argument}

#             Instructions:

#             1. Use ONLY the provided knowledge.
#             2. Do not invent facts.
#             3. If this is not the first round, directly counter the opponent.
#             4. Be logical and persuasive.
#             5. Keep the response between 150 and 250 words.
#             6. Do not mention that you are an AI.
#             7. Do not use bullet points.
#             8. Return only the debate argument.
#             """

#         response = self.client.chat.completions.create(

#             model="openai/gpt-oss-120b",

#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],

#             temperature=0.4

#         )
#         print("-"*100)
#         print(response.choices)

#         return response.choices[0].message.content.strip()
    
    



import os
from dotenv import load_dotenv
from groq import Groq

from langchain_core.documents import Document


class DebateAgent:

    def __init__(self, role: str):

        load_dotenv()

        self.role = role

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    # ==========================================================
    # Generate one debate argument
    # ==========================================================

    def generate_argument(
        self,
        topic: str,
        context_docs: list[Document],
        opponent_argument: str = ""
    ):

        # ------------------------------------------------------
        # Prepare labelled evidence
        # ------------------------------------------------------

        context_parts = []

        for doc in context_docs:

            retrieval_id = doc.metadata.get(
                "retrieval_id",
                "UNKNOWN"
            )

            source_file = doc.metadata.get(
                "source_file",
                "Unknown file"
            )

            page = doc.metadata.get(
                "page",
                "Unknown page"
            )

            context_parts.append(
                f"""
[{retrieval_id}]
Source File: {source_file}
Page: {page}

Content:
{doc.page_content}
"""
            )

        context = "\n\n".join(context_parts)

        # ------------------------------------------------------
        # Determine stance
        # ------------------------------------------------------

        if self.role.lower() == "pro":

            stance = "Support the topic."

        else:

            stance = "Oppose the topic."

        # ------------------------------------------------------
        # Prompt
        # ------------------------------------------------------

        prompt = f"""
You are participating in a formal debate.

Your Role:
{self.role}

Topic:
{topic}

Your Stance:
{stance}

Retrieved Evidence:

{context}

Opponent's Previous Argument:
{opponent_argument}

Instructions:

1. Use ONLY the provided retrieved evidence.
2. Do not invent facts or evidence.
3. If this is not the first round, directly counter the opponent's argument.
4. Use the retrieved evidence to support your reasoning.
5. Whenever you use information from a retrieved document, cite it using its retrieval ID.
6. Citations MUST use exactly this format: [DOC 1], [DOC 2], etc.
7. Only cite documents that actually support the statement being made.
8. You may cite multiple documents when necessary.
9. Do not create document IDs that are not present in the retrieved evidence.
10. Be logical and persuasive.
11. Keep the response between 150 and 250 words.
12. Do not mention that you are an AI.
13. Do not use bullet points.
14. Return only the debate argument with inline document citations.

Example:

The technology can reduce development complexity by providing
automatic configuration and predefined components [DOC 1].
However, this convenience can also introduce limitations in
customization [DOC 3].
"""

        response = self.client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4
        )

        argument = response.choices[0].message.content.strip()

        print("-" * 100)
        print(argument)
        print("-" * 100)

        return argument
    

