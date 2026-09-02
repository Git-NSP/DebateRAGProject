# from utils.retriever import Retriever
# from utils.agent import DebateAgent
# from utils.judge import JudgeAgent

# class Debate:

#     def __init__(self):

#         # -----------------------------
#         # Retrievers
#         # -----------------------------
#         self.pro_retriever = Retriever("pro")

#         self.con_retriever = Retriever("con")

#         # -----------------------------
#         # Agents
#         # -----------------------------
#         self.pro_agent = DebateAgent("Pro")

#         self.con_agent = DebateAgent("Con")

#         # -----------------------------
#         # Judge
#         # -----------------------------
#         self.judge = JudgeAgent()

#     # ==========================================================
#     # Run Complete Debate
#     # ==========================================================

#     def run(self, topic, rounds=5):

#         debate_history = []

#         opponent_argument = ""

#         for round_no in range(1, rounds + 1):

#             print(f"\n========== ROUND {round_no} ==========\n")

#             # ==================================================
#             # PRO TURN
#             # ==================================================
            
#             if opponent_argument == "":

#                 retrieval_query = topic

#             else:

#                 retrieval_query = (
#                     f"Topic: {topic}\n\n"
#                     f"Opponent Argument:\n"
#                     f"{opponent_argument}\n\n"
#                     "Find evidence to refute it."
#                 )

#             pro_docs = self.pro_retriever.retrieve(
#                 retrieval_query,
#                 top_k=5
#             )

#             pro_argument = self.pro_agent.generate_argument(
#                 topic=topic,
#                 context_docs=pro_docs,
#                 opponent_argument=opponent_argument
#             )

#             debate_history.append(
#                 {
#                     "speaker": "Pro",
#                     "argument": pro_argument
#                 }
#             )

#             print("PRO:\n")
#             print(pro_argument)

#             # ==================================================
#             # CON TURN
#             # ==================================================
#             retrieval_query = (
#                 f"Topic: {topic}\n\n"
#                 f"Opponent Argument:\n"
#                 f"{pro_argument}\n\n"
#                 "Find evidence to refute it."
#             )

#             con_docs = self.con_retriever.retrieve(
#                 retrieval_query,
#                 top_k=5
#             )

#             con_argument = self.con_agent.generate_argument(
#                 topic=topic,
#                 context_docs=con_docs,
#                 opponent_argument=pro_argument
#             )

#             debate_history.append(
#                 {
#                     "speaker": "Con",
#                     "argument": con_argument
#                 }
#             )

#             print("\nCON:\n")
#             print(con_argument)

#             opponent_argument = con_argument


#         # ======================================================
#         # Judge
#         # ======================================================

#         result = self.judge.judge_debate(
#             topic,
#             debate_history
#         )

#         return {

#             "history": debate_history,

#             "judgement": result

#         }
    


import re
from utils.retriever import Retriever
from utils.agent import DebateAgent
from utils.judge import JudgeAgent


class Debate:

    def __init__(self):

        self.pro_retriever = Retriever("pro")

        self.con_retriever = Retriever("con")

        self.pro_agent = DebateAgent("Pro")

        self.con_agent = DebateAgent("Con")

        self.judge = JudgeAgent()

    # ==========================================================
    # Extract cited documents from argument
    # ==========================================================

    def get_cited_sources(self, argument, retrieved_docs):

        cited_numbers = re.findall(
            r"\[DOC\s+(\d+)\]",
            argument
        )

        cited_ids = [
            f"DOC {number}"
            for number in cited_numbers
        ]

        cited_ids = list(dict.fromkeys(cited_ids))

        sources = []

        for doc in retrieved_docs:

            retrieval_id = doc.metadata.get(
                "retrieval_id"
            )

            if retrieval_id in cited_ids:

                sources.append(
                    {
                        "id": retrieval_id,
                        "source_file": doc.metadata.get(
                            "source_file",
                            "Unknown"
                        ),
                        "page": doc.metadata.get(
                            "page",
                            "Unknown"
                        ),
                        "content": doc.page_content
                    }
                )

        return sources
    
    # ==========================================================
    # Run Complete Debate
    # ==========================================================

    def run(self, topic, rounds=2):

        debate_history = []

        opponent_argument = ""

        for round_no in range(1, rounds + 1):

            print(
                f"\n========== ROUND {round_no} ==========\n"
            )

            # ==================================================
            # PRO TURN
            # ==================================================

            if opponent_argument == "":

                retrieval_query = topic

            else:

                retrieval_query = (
                    f"Topic: {topic}\n\n"
                    f"Opponent Argument:\n"
                    f"{opponent_argument}\n\n"
                    "Find evidence to refute it."
                )

            pro_docs = self.pro_retriever.retrieve(
                retrieval_query,
                top_k=5
            )

            pro_argument = self.pro_agent.generate_argument(
                topic=topic,
                context_docs=pro_docs,
                opponent_argument=opponent_argument
            )

            pro_sources = self.get_cited_sources(
                pro_argument,
                pro_docs
            )

            pro_turn = {
                "round": round_no,
                "speaker": "Pro",
                "argument": pro_argument,
                "sources": pro_sources
            }

            debate_history.append(pro_turn)

            print("PRO:\n")
            print(pro_argument)

            print("\nPRO SOURCES:\n")

            for source in pro_sources:

                print(
                    source["id"],
                    "->",
                    source["source_file"],
                    "Page:",
                    source["page"]
                )

            # ==================================================
            # CON TURN
            # ==================================================

            retrieval_query = (
                f"Topic: {topic}\n\n"
                f"Opponent Argument:\n"
                f"{pro_argument}\n\n"
                "Find evidence to refute it."
            )

            con_docs = self.con_retriever.retrieve(
                retrieval_query,
                top_k=5
            )

            con_argument = self.con_agent.generate_argument(
                topic=topic,
                context_docs=con_docs,
                opponent_argument=pro_argument
            )

            con_sources = self.get_cited_sources(
                con_argument,
                con_docs
            )

            con_turn = {
                "round": round_no,
                "speaker": "Con",
                "argument": con_argument,
                "sources": con_sources
            }

            debate_history.append(con_turn)

            print("\nCON:\n")
            print(con_argument)

            print("\nCON SOURCES:\n")

            for source in con_sources:

                print(
                    source["id"],
                    "->",
                    source["source_file"],
                    "Page:",
                    source["page"]
                )

            opponent_argument = con_argument

        # ======================================================
        # Judge
        # ======================================================

        result = self.judge.judge_debate(
            topic,
            debate_history
        )

        return {
            "history": debate_history,
            "judgement": result
        }
    

