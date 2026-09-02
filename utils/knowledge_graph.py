import os
import json
from dotenv import load_dotenv
from groq import Groq
import networkx as nx
from networkx.readwrite import json_graph
from pyvis.network import Network


class KnowledgeGraph:
    def __init__(self, graph_name="pro"):

        load_dotenv()

        api_key = os.getenv("GROQ_API_KEY")

        self.client = Groq(api_key=api_key)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.graph_folder = os.path.join(BASE_DIR, "graphs", f"{graph_name}_graph")

        os.makedirs(self.graph_folder, exist_ok=True)

        self.graph_path = os.path.join(self.graph_folder, "graph.graphml")
        self.json_path = os.path.join(self.graph_folder, "graph.json")
        self.html_path = os.path.join(self.graph_folder, "graph.html")

        # -----------------------------
        # Load Existing Graph
        # -----------------------------
        if os.path.exists(self.graph_path):

            self.graph = nx.read_graphml(self.graph_path)

            print("Existing Knowledge Graph Loaded.")

        else:

            self.graph = nx.DiGraph()

            print("New Knowledge Graph Created.")

    # ==========================================================
    # Ask LLM to extract triples
    # ==========================================================

    def extract_triples(self, text):
        schema = """
        {
            "entities": [
                {
                    "name": "...",
                    "type": "..."
                }
            ],
            "relationships": [
                {
                    "source": "...",
                    "relation": "...",
                    "target": "..."
                }
            ]
        }
        """
        prompt = (
            "You are an expert knowledge graph extraction system.\n\n "
            f"Return JSON exactly matching this schema:\n{schema}\n\n"
            f"Text:\n{text}"
        )

        # prompt = f"""
        #     You are an expert knowledge graph extraction system.

        #     Your task is to extract factual relationships from the given text.

        #     Rules:

        #     1. Extract only important entities.
        #     2. Use short entity names.
        #     3. Use meaningful relationship names.
        #     4. Do NOT invent information.
        #     5. Ignore unimportant details.
        #     6. Return ONLY valid JSON.
        #     7. Do not include explanations.

        #     Output format:

        #         Return ONLY valid JSON.

        #         Exactly this schema:

        #         {{
        #             "entities": [
        #                 {{
        #                     "name": "...",
        #                     "type": "..."
        #                 }}
        #             ],
        #             "relationships": [
        #                 {{
        #                     "source": "...",
        #                     "relation": "...",
        #                     "target": "..."
        #                 }}
        #             ]
        #         }}

        #         Do not rename any keys.
        #         Do not omit any keys.
        #         Do not return markdown.
        #         Do not return explanations.

        #     Text: {text}
        #     """

        response = self.client.chat.completions.create(

            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0

        )

        answer = response.choices[0].message.content.strip()
        
        print("\n========== RAW LLM RESPONSE ==========")
        print(answer)
        print("======================================\n")

        # Remove markdown if model returns ```json
        answer = answer.replace("```json", "")
        answer = answer.replace("```", "")
        answer = answer.strip()

        try:
            if answer == "":
                return {
                    "entities": [],
                    "relationships": []
                    }
            
            triples = json.loads(answer)
            if not isinstance(triples, dict):
                raise ValueError("Top level must be a JSON object")

            triples.setdefault("entities", [])
            triples.setdefault("relationships", [])

            if not isinstance(triples["entities"], list):
                triples["entities"] = []

            if not isinstance(triples["relationships"], list):
                triples["relationships"] = []
            
            print("2nd step print try block", triples)

            return triples

        except Exception as e:

            print("Could not parse JSON.")
            print(e)

            print("2nd step print exception block", answer)

            return {
                "entities": [],
                "relationships": []
            }

    # ==========================================================
    # Add one triple to graph
    # ==========================================================

    def add_triple(self, triple, source_pdf=None):
        print("in add triple function", triple)
        if not all(k in triple for k in ("source", "relation", "target")):
            print("Skipping invalid triple:", triple)
            return False

        source = triple["source"].strip()

        relation = triple["relation"].strip().lower()

        target = triple["target"].strip()
        
        if self.graph.has_edge(source, target):
            existing = self.graph[source][target].get("relation")
            if existing == relation:
                return False

        self.graph.add_node(source, type="entity")

        self.graph.add_node(target, type="entity")

        self.graph.add_edge(source, target, relation=relation, source_pdf=source_pdf)
        
        return True

    # ==========================================================
    # Build graph from chunks
    # ==========================================================

    def build_graph(self, chunks):

        total_triples = 0

        for i, chunk in enumerate(chunks, start=1):

            print(f"Processing Chunk {i}/{len(chunks)}")

            result = self.extract_triples(chunk.page_content)
            if not isinstance(result, dict):
                print("Invalid LLM output.")
                continue

            relationships = result.get("relationships")

            if relationships is None:
                print("LLM did not return 'relationships'.")
                print(result)
                continue

            print("Relationships:", len(result["relationships"]))

            for triple in relationships:

                added = self.add_triple(triple, chunk.metadata.get("source_file"))

                if added:
                    total_triples += 1

        print("\nKnowledge Graph Updated")
        print(f"Nodes : {self.graph.number_of_nodes()}")
        print(f"Edges : {self.graph.number_of_edges()}")
        print(f"Triples Added : {total_triples}")

        return total_triples


    # ==========================================================
    # Save Graph As GraphML and JSON
    # ==========================================================

    def save_graph(self):
        # -----------------------------
        # Save GraphML
        # -----------------------------
        nx.write_graphml(

            self.graph,

            self.graph_path

        )

        # -----------------------------
        # Save JSON
        # -----------------------------
        graph_data = json_graph.node_link_data(self.graph)

        with open(self.json_path, "w", encoding="utf-8") as f:

            json.dump(graph_data, f, indent=4)

        print()

        print("Knowledge Graph Saved")

        print(self.graph_path)

        print(self.json_path)
    
    def visualize_graph(self):

        net = Network(
            height="750px",
            width="100%",
            directed=True,
            notebook=False
        )

        net.from_nx(self.graph)

        net.repulsion(
            node_distance=220,
            spring_length=180
        )

        net.set_options("""
        {
            "interaction": {
                "zoomView": true
            }
        }
        """)

        net.save_graph(self.html_path)

        with open(self.html_path, "r", encoding="utf-8") as f:
            html = f.read()

        interaction_script = """
        <script>
            let graphActive = false;

            const graphContainer = document.getElementById("mynetwork");

            const overlay = document.createElement("div");

            overlay.innerHTML = "Click to interact";

            overlay.style.position = "absolute";
            overlay.style.top = "0";
            overlay.style.left = "0";
            overlay.style.width = "100%";
            overlay.style.height = "100%";
            overlay.style.display = "flex";
            overlay.style.alignItems = "center";
            overlay.style.justifyContent = "center";
            overlay.style.background = "rgba(0, 0, 0, 0.08)";
            overlay.style.color = "#666";
            overlay.style.fontSize = "14px";
            overlay.style.cursor = "pointer";
            overlay.style.zIndex = "1000";

            graphContainer.style.position = "relative";

            graphContainer.appendChild(overlay);

            overlay.addEventListener("click", function () {
                graphActive = true;
                overlay.style.display = "none";
            });

            graphContainer.addEventListener("mouseleave", function () {
                if (graphActive) {
                    graphActive = false;
                    overlay.style.display = "flex";
                }
            });
        </script>
        """

        html = html.replace(
            "</body>",
            interaction_script + "\n</body>"
        )

        with open(self.html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print("Graph visualization saved.")

        return self.html_path


    # ==========================================================
    # Print Graph
    # ==========================================================

    def show_graph(self):

        print()

        print("Knowledge Graph")

        print()

        for source, target, data in self.graph.edges(data=True):

            print(source, "--", data["relation"], "-->", target)


