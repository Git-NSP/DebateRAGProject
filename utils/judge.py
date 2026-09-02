import os
from dotenv import load_dotenv
from groq import Groq


class JudgeAgent:

    def __init__(self):

        load_dotenv()

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    # ==========================================================
    # Judge the Debate
    # ==========================================================

    def judge_debate(
        self,
        topic: str,
        debate_history: list
    ):

        history = ""

        for turn in debate_history:

            history += (
                f"\nRound {turn['round']} - {turn['speaker']}\n"
                f"Argument:\n"
                f"{turn['argument']}\n\n"
            )

            sources = turn.get("sources", [])

            if sources:

                history += "Cited Evidence:\n"

                for source in sources[:3]:

                    content = source["content"]

                    if len(content) > 300:
                        content = content[:300] + "..."

                    history += (
                        f"{source['id']} | "
                        f"{source['source_file']} | "
                        f"Page {source['page']}\n"
                        f"{content}\n\n"
                    )

            else:

                history += (
                    "Cited Evidence: None\n\n"
                )

        prompt = f"""
You are an impartial and strict debate judge.

Topic:
{topic}

Debate Transcript and Supporting Evidence:

{history}

Evaluate Pro and Con using:

1. Logical reasoning
2. Relevance to the topic
3. Strength of evidence
4. Whether cited evidence supports the argument
5. Ability to counter the opponent
6. Clarity and persuasiveness

Rules:

- Judge both sides fairly.
- Do not use outside knowledge.
- Penalize unsupported claims.
- Penalize misuse or misrepresentation of evidence.
- Reward relevant evidence that directly supports claims.
- Consider all five rounds.
- Do not favor the side that speaks first or last.

Return ONLY:

Winner:
<Pro or Con>

Pro Score:
<number out of 10>

Con Score:
<number out of 10>

Reason:
<short explanation in about 50 words>
"""

        response = self.client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        return response.choices[0].message.content.strip()
    
    