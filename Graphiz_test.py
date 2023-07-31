import json
import streamlit as st
import pygraphviz as pgv
import streamlit.components.v1 as components

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload JSON data", type=["json"])

if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    json_data = json.loads(data)
else:
    st.warning('Please upload your JSON file.')
    st.stop()

def plot_network_graph():
    # Create a directed graph (DiGraph) using Graphviz
    G = pgv.AGraph(directed=True)

    # Add nodes and edges to the graph
    for process_name, process_info in json_data.items():
        G.add_node(process_name, shape="box")
        for uprocs_info in process_info.get("uprocs", []):
            uprocs_name = uprocs_info.get("name")
            G.add_node(uprocs_name, shape="box")
            G.add_edge(process_name, uprocs_name)
            table_deps = uprocs_info.get("table_deps", {})
            for table_dep, table_dep_content in table_deps.items():
                if table_dep not in G.nodes():
                    G.add_node(table_dep, shape="box", color="cyan", style="filled")
                G.add_edge(uprocs_name, table_dep)

    # Define graph properties
    G.graph_attr["rankdir"] = "TB"  # Top to bottom layout
    G.graph_attr["bgcolor"] = "#222222"
    G.node_attr["fontcolor"] = "white"
    G.node_attr["color"] = "white"

    # Save the graph as an image
    graph_path = "data_flow_graph.png"
    G.draw(graph_path, format="png")

    # Display the graph using Streamlit
    st.header('Dépendance entre sessions-uprocs-table_deps')
    st.image(graph_path, use_column_width=True)

# Main Streamlit app code
if __name__ == "__main__":
    st.title("Orange Kenobi")
    plot_network_graph()
