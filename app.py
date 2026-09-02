# import os
# import shutil
# import streamlit as st

# # ----------------------------------------------------
# # Streamlit Config
# # ----------------------------------------------------

# st.set_page_config(
#     page_title="DebateRAG Repository Builder",
#     page_icon="📚",
#     layout="wide"
# )

# st.title("📚 DebateRAG Repository Builder")

# st.write(
#     "Upload PDFs separately for Pro and Con repositories."
# )

# st.divider()

# left, right = st.columns(2)


# # ==========================================================
# # PRO SIDE
# # ==========================================================

# with left:

#     st.header("🟢 Pro Repository")

#     uploaded_file = st.file_uploader(
#         "Upload Pro PDF",
#         type=["pdf"],
#         key="pro_pdf"
#     )

#     if uploaded_file:

#         if st.button("Process Pro PDF"):

#             from utils.pdf_loader import load_pdf
#             from utils.chunker import create_chunks
#             from utils.embeddings import EmbeddingManager
#             from utils.vector_store import VectorStore
#             from utils.knowledge_graph import KnowledgeGraph

#             os.makedirs(
#                 "uploads/pro_side",
#                 exist_ok=True
#             )

#             pdf_path = os.path.join(
#                 "uploads/pro_side",
#                 uploaded_file.name
#             )

#             with open(pdf_path, "wb") as f:
#                 f.write(
#                     uploaded_file.getbuffer()
#                 )

#             documents = load_pdf(
#                 pdf_path
#             )

#             chunks = create_chunks(
#                 documents
#             )

#             pro_db = VectorStore(
#                 "pro"
#             )

#             new_chunks = []

#             duplicate_chunks = 0

#             for chunk in chunks:

#                 chunk_hash = pro_db.generate_chunk_hash(
#                     chunk.page_content
#                 )

#                 if pro_db.chunk_exists(
#                     chunk_hash
#                 ):

#                     duplicate_chunks += 1

#                 else:

#                     chunk.metadata[
#                         "chunk_hash"
#                     ] = chunk_hash

#                     new_chunks.append(
#                         chunk
#                     )

#             new_triples = 0

#             kg = KnowledgeGraph(
#                 "pro"
#             )

#             if new_chunks:

#                 new_triples = kg.build_graph(
#                     new_chunks
#                 )

#                 kg.save_graph()

#                 kg.visualize_graph()

#                 embedding_manager = (
#                     EmbeddingManager()
#                 )

#                 embeddings = (
#                     embedding_manager
#                     .generate_embeddings(
#                         new_chunks
#                     )
#                 )

#                 pro_db.add_documents(
#                     new_chunks,
#                     embeddings
#                 )

#             total_nodes = (
#                 kg.graph.number_of_nodes()
#             )

#             total_edges = (
#                 kg.graph.number_of_edges()
#             )

#             st.success(
#                 "Pro Repository Updated"
#             )

#             st.subheader(
#                 "Pipeline Summary"
#             )

#             col1, col2 = st.columns(2)

#             with col1:

#                 st.metric(
#                     "New Chunks Stored",
#                     len(new_chunks)
#                 )

#                 st.metric(
#                     "Original Chunks",
#                     len(chunks)
#                 )

#                 st.metric(
#                     "Duplicate Chunks",
#                     duplicate_chunks
#                 )

#             with col2:

#                 st.metric(
#                     "New Triples Added",
#                     new_triples
#                 )

#                 st.metric(
#                     "Total Chunks in Pro DB",
#                     pro_db.get_document_count()
#                 )

#                 st.metric(
#                     "Knowledge Graph Nodes",
#                     total_nodes
#                 )

#                 st.metric(
#                     "Knowledge Graph Edges",
#                     total_edges
#                 )


#     # ------------------------------------------------------
#     # RESET PRO REPOSITORY
#     # ------------------------------------------------------

#     st.divider()

#     if st.button("Reset Pro Repository", key="reset_pro"):

#         st.caption(
#             "Delete all PDFs, vectors and knowledge graph data from the Pro repository."
#         )
        
#         from utils.vector_store import VectorStore

#         pro_db = VectorStore("pro")
#         deleted_chunks = pro_db.clear_collection()

#         if os.path.exists("uploads/pro_side"):
#             shutil.rmtree("uploads/pro_side")

#         if os.path.exists("graphs/pro_graph"):
#             shutil.rmtree("graphs/pro_graph")

#         st.success(
#             f"Pro repository reset. {deleted_chunks} chunks deleted."
#         )

#         st.rerun()    


# # ==========================================================
# # CON SIDE
# # ==========================================================

# with right:

#     st.header("🔴 Con Repository")

#     uploaded_file = st.file_uploader(
#         "Upload Con PDF",
#         type=["pdf"],
#         key="con_pdf"
#     )

#     if uploaded_file:

#         if st.button("Process Con PDF"):

#             from utils.pdf_loader import load_pdf
#             from utils.chunker import create_chunks
#             from utils.embeddings import EmbeddingManager
#             from utils.vector_store import VectorStore
#             from utils.knowledge_graph import KnowledgeGraph

#             os.makedirs(
#                 "uploads/con_side",
#                 exist_ok=True
#             )

#             pdf_path = os.path.join(
#                 "uploads/con_side",
#                 uploaded_file.name
#             )

#             with open(pdf_path, "wb") as f:
#                 f.write(
#                     uploaded_file.getbuffer()
#                 )

#             documents = load_pdf(
#                 pdf_path
#             )

#             chunks = create_chunks(
#                 documents
#             )

#             con_db = VectorStore(
#                 "con"
#             )

#             new_chunks = []

#             duplicate_chunks = 0

#             for chunk in chunks:

#                 chunk_hash = con_db.generate_chunk_hash(
#                     chunk.page_content
#                 )

#                 if con_db.chunk_exists(
#                     chunk_hash
#                 ):

#                     duplicate_chunks += 1

#                 else:

#                     chunk.metadata[
#                         "chunk_hash"
#                     ] = chunk_hash

#                     new_chunks.append(
#                         chunk
#                     )

#             new_triples = 0

#             kg = KnowledgeGraph(
#                 "con"
#             )

#             if new_chunks:

#                 new_triples = kg.build_graph(
#                     new_chunks
#                 )

#                 kg.save_graph()

#                 kg.visualize_graph()

#                 embedding_manager = (
#                     EmbeddingManager()
#                 )

#                 embeddings = (
#                     embedding_manager
#                     .generate_embeddings(
#                         new_chunks
#                     )
#                 )

#                 con_db.add_documents(
#                     new_chunks,
#                     embeddings
#                 )

#             total_nodes = (
#                 kg.graph.number_of_nodes()
#             )

#             total_edges = (
#                 kg.graph.number_of_edges()
#             )

#             st.success(
#                 "Con Repository Updated"
#             )

#             st.subheader(
#                 "Pipeline Summary"
#             )

#             col1, col2 = st.columns(2)

#             with col1:

#                 st.metric(
#                     "New Chunks Stored",
#                     len(new_chunks)
#                 )

#                 st.metric(
#                     "Original Chunks",
#                     len(chunks)
#                 )

#                 st.metric(
#                     "Duplicate Chunks",
#                     duplicate_chunks
#                 )

#             with col2:

#                 st.metric(
#                     "New Triples Added",
#                     new_triples
#                 )

#                 st.metric(
#                     "Total Chunks in Con DB",
#                     con_db.get_document_count()
#                 )

#                 st.metric(
#                     "Knowledge Graph Nodes",
#                     total_nodes
#                 )

#                 st.metric(
#                     "Knowledge Graph Edges",
#                     total_edges
#                 )


#     # ------------------------------------------------------
#     # RESET CON REPOSITORY
#     # ------------------------------------------------------

    
#     st.divider()

#     if st.button("Reset Con Repository", key="reset_con"):
        
#         st.caption("Delete all PDFs, vectors and knowledge graph data from the Pro repository.")

#         from utils.vector_store import VectorStore

#         con_db = VectorStore("con")
#         deleted_chunks = con_db.clear_collection()

#         if os.path.exists("uploads/con_side"):
#             shutil.rmtree("uploads/con_side")

#         if os.path.exists("graphs/con_graph"):
#             shutil.rmtree("graphs/con_graph")

#         st.success(
#             f"Con repository reset. {deleted_chunks} chunks deleted."
#         )

#         st.rerun()
        


# # ==========================================================
# # SHOW BOTH KNOWLEDGE GRAPHS
# # ==========================================================

# st.divider()

# col1, col2 = st.columns(2)


# # ---------------- PRO GRAPH ----------------

# with col1:

#     st.subheader(
#         "🟢 Pro Knowledge Graph"
#     )

#     pro_graph_html = os.path.abspath(
#         "graphs/pro_graph/graph.html"
#     )

#     if os.path.exists(
#         pro_graph_html
#     ):

#         st.iframe(
#             pro_graph_html,
#             height=700
#         )

#     else:

#         st.info(
#             "Pro Knowledge Graph has not been created yet."
#         )


# # ---------------- CON GRAPH ----------------

# with col2:

#     st.subheader(
#         "🔴 Con Knowledge Graph"
#     )

#     con_graph_html = os.path.abspath(
#         "graphs/con_graph/graph.html"
#     )

#     if os.path.exists(
#         con_graph_html
#     ):

#         st.iframe(
#             con_graph_html,
#             height=700
#         )

#     else:

#         st.info(
#             "Con Knowledge Graph has not been created yet."
#         )


# # ==========================================================
# # NAVIGATION TO DEBATE PAGE
# # ==========================================================

# st.divider()

# st.header(
#     "Start Debate"
# )

# st.write(
#     "Once both repositories have been created, proceed to the Debate page."
# )

# st.page_link(
#     "pages/debate_show.py",
#     label="Go to Debate",
#     icon="⚖️"
# )



# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------



import os
import shutil
import streamlit as st
from pathlib import Path

# ----------------------------------------------------
# Streamlit Config
# ----------------------------------------------------

st.set_page_config(
    page_title="DebateRAG Repository Builder",
    page_icon="📚",
    layout="wide"
)

st.title("📚 DebateRAG Repository Builder")

st.write(
    "Upload PDFs separately for Pro and Con repositories."
)

st.divider()

left, right = st.columns(2)


# ==========================================================
# PRO SIDE
# ==========================================================

with left:

    st.header("🟢 Pro Repository")

    uploaded_file = st.file_uploader(
        "Upload Pro PDF",
        type=["pdf"],
        key="pro_pdf"
    )

    if uploaded_file:

        if st.button("Process Pro PDF"):

            from utils.pdf_loader import load_pdf
            from utils.chunker import create_chunks
            from utils.embeddings import EmbeddingManager
            from utils.vector_store import VectorStore
            from utils.knowledge_graph import KnowledgeGraph

            os.makedirs(
                "uploads/pro_side",
                exist_ok=True
            )

            pdf_path = os.path.join(
                "uploads/pro_side",
                uploaded_file.name
            )

            with open(pdf_path, "wb") as f:
                f.write(
                    uploaded_file.getbuffer()
                )

            documents = load_pdf(
                pdf_path
            )

            chunks = create_chunks(
                documents
            )

            pro_db = VectorStore(
                "pro"
            )

            new_chunks = []

            duplicate_chunks = 0

            for chunk in chunks:

                chunk_hash = pro_db.generate_chunk_hash(
                    chunk.page_content
                )

                if pro_db.chunk_exists(
                    chunk_hash
                ):

                    duplicate_chunks += 1

                else:

                    chunk.metadata[
                        "chunk_hash"
                    ] = chunk_hash

                    new_chunks.append(
                        chunk
                    )

            new_triples = 0

            kg = KnowledgeGraph(
                "pro"
            )

            if new_chunks:

                new_triples = kg.build_graph(
                    new_chunks
                )

                kg.save_graph()

                kg.visualize_graph()

                embedding_manager = (
                    EmbeddingManager()
                )

                embeddings = (
                    embedding_manager
                    .generate_embeddings(
                        new_chunks
                    )
                )

                pro_db.add_documents(
                    new_chunks,
                    embeddings
                )

            total_nodes = (
                kg.graph.number_of_nodes()
            )

            total_edges = (
                kg.graph.number_of_edges()
            )

            st.success(
                "Pro Repository Updated"
            )

            st.subheader(
                "Pipeline Summary"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "New Chunks Stored",
                    len(new_chunks)
                )

                st.metric(
                    "Original Chunks",
                    len(chunks)
                )

                st.metric(
                    "Duplicate Chunks",
                    duplicate_chunks
                )

            with col2:

                st.metric(
                    "New Triples Added",
                    new_triples
                )

                st.metric(
                    "Total Chunks in Pro DB",
                    pro_db.get_document_count()
                )

                st.metric(
                    "Knowledge Graph Nodes",
                    total_nodes
                )

                st.metric(
                    "Knowledge Graph Edges",
                    total_edges
                )

    st.divider()

    if st.button(
        "Reset Pro Repository",
        key="reset_pro"
    ):

        from utils.vector_store import VectorStore

        pro_db = VectorStore("pro")

        deleted_chunks = (
            pro_db.clear_collection()
        )

        if os.path.exists(
            "uploads/pro_side"
        ):

            shutil.rmtree(
                "uploads/pro_side"
            )

        if os.path.exists(
            "graphs/pro_graph"
        ):

            shutil.rmtree(
                "graphs/pro_graph"
            )

        st.success(
            f"Pro repository reset. "
            f"{deleted_chunks} chunks deleted."
        )

        st.rerun()


# ==========================================================
# CON SIDE
# ==========================================================

with right:

    st.header("🔴 Con Repository")

    uploaded_file = st.file_uploader(
        "Upload Con PDF",
        type=["pdf"],
        key="con_pdf"
    )

    if uploaded_file:

        if st.button("Process Con PDF"):

            from utils.pdf_loader import load_pdf
            from utils.chunker import create_chunks
            from utils.embeddings import EmbeddingManager
            from utils.vector_store import VectorStore
            from utils.knowledge_graph import KnowledgeGraph

            os.makedirs(
                "uploads/con_side",
                exist_ok=True
            )

            pdf_path = os.path.join(
                "uploads/con_side",
                uploaded_file.name
            )

            with open(pdf_path, "wb") as f:
                f.write(
                    uploaded_file.getbuffer()
                )

            documents = load_pdf(
                pdf_path
            )

            chunks = create_chunks(
                documents
            )

            con_db = VectorStore(
                "con"
            )

            new_chunks = []

            duplicate_chunks = 0

            for chunk in chunks:

                chunk_hash = con_db.generate_chunk_hash(
                    chunk.page_content
                )

                if con_db.chunk_exists(
                    chunk_hash
                ):

                    duplicate_chunks += 1

                else:

                    chunk.metadata[
                        "chunk_hash"
                    ] = chunk_hash

                    new_chunks.append(
                        chunk
                    )

            new_triples = 0

            kg = KnowledgeGraph(
                "con"
            )

            if new_chunks:

                new_triples = kg.build_graph(
                    new_chunks
                )

                kg.save_graph()

                kg.visualize_graph()

                embedding_manager = (
                    EmbeddingManager()
                )

                embeddings = (
                    embedding_manager
                    .generate_embeddings(
                        new_chunks
                    )
                )

                con_db.add_documents(
                    new_chunks,
                    embeddings
                )

            total_nodes = (
                kg.graph.number_of_nodes()
            )

            total_edges = (
                kg.graph.number_of_edges()
            )

            st.success(
                "Con Repository Updated"
            )

            st.subheader(
                "Pipeline Summary"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "New Chunks Stored",
                    len(new_chunks)
                )

                st.metric(
                    "Original Chunks",
                    len(chunks)
                )

                st.metric(
                    "Duplicate Chunks",
                    duplicate_chunks
                )

            with col2:

                st.metric(
                    "New Triples Added",
                    new_triples
                )

                st.metric(
                    "Total Chunks in Con DB",
                    con_db.get_document_count()
                )

                st.metric(
                    "Knowledge Graph Nodes",
                    total_nodes
                )

                st.metric(
                    "Knowledge Graph Edges",
                    total_edges
                )

    st.divider()

    if st.button(
        "Reset Con Repository",
        key="reset_con"
    ):

        from utils.vector_store import VectorStore

        con_db = VectorStore("con")

        deleted_chunks = (
            con_db.clear_collection()
        )

        if os.path.exists(
            "uploads/con_side"
        ):

            shutil.rmtree(
                "uploads/con_side"
            )

        if os.path.exists(
            "graphs/con_graph"
        ):

            shutil.rmtree(
                "graphs/con_graph"
            )

        st.success(
            f"Con repository reset. "
            f"{deleted_chunks} chunks deleted."
        )

        st.rerun()


# ==========================================================
# SHOW BOTH KNOWLEDGE GRAPHS
# ==========================================================

st.divider()

col1, col2 = st.columns(2)


# ---------------- PRO GRAPH ----------------

with col1:

    st.subheader(
        "🟢 Pro Knowledge Graph"
    )

    pro_graph_html = Path(
        "graphs/pro_graph/graph.html"
    )

    if pro_graph_html.exists():

        st.iframe(
            pro_graph_html,
            height=700
        )

    else:

        st.info(
            "Pro Knowledge Graph has not been created yet."
        )


# ---------------- CON GRAPH ----------------

with col2:

    st.subheader(
        "🔴 Con Knowledge Graph"
    )

    con_graph_html = Path(
        "graphs/con_graph/graph.html"
    )

    if con_graph_html.exists():

        st.iframe(
            con_graph_html,
            height=700
        )

    else:

        st.info(
            "Con Knowledge Graph has not been created yet."
        )


# ==========================================================
# NAVIGATION TO DEBATE PAGE
# ==========================================================

st.divider()

st.header(
    "Start Debate"
)

st.write(
    "Once both repositories have been created, proceed to the Debate page."
)

st.page_link(
    "pages/debate_show.py",
    label="Go to Debate",
    icon="⚖️"
)


