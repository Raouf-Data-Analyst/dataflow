import json
import streamlit as st
import pydot
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
    # Create a directed graph (DiGraph) using pydot
    G = pydot.Dot(directed=True)

    # Add nodes and edges to the graph
    for process_name, process_info in json_data.items():
        process_node = pydot.Node(process_name, shape="box")
        G.add_node(process_node)
        for uprocs_info in process_info.get("uprocs", []):
            uprocs_name = uprocs_info.get("name")
            uprocs_node = pydot.Node(uprocs_name, shape="box")
            G.add_node(uprocs_node)
            G.add_edge(pydot.Edge(process_node, uprocs_node))
            table_deps = uprocs_info.get("table_deps", {})
            for table_dep, table_dep_content in table_deps.items():
                table_dep_node = G.get_node(table_dep)
                if not table_dep_node:
                    table_dep_node = pydot.Node(table_dep, shape="box", color="cyan", style="filled")
                    G.add_node(table_dep_node)
                G.add_edge(pydot.Edge(uprocs_node, table_dep_node))

    # Define graph properties
    G.set("rankdir", "TB")  # Top to bottom layout

    # Save the graph as an image
    graph_path = "data_flow_graph.png"
    G.write_png(graph_path)

    # Display the graph using Streamlit
    st.header('Dépendance entre sessions-uprocs-table_deps')
    st.image(graph_path, use_column_width=True)

# Main Streamlit app code
if __name__ == "__main__":
    st.title("Orange Kenobi")
    plot_network_graph()
