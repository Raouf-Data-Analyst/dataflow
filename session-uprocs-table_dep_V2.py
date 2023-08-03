import json
import streamlit as st
import streamlit.components.v1 as components
import pydeck as pdk
import pandas as pd

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload JSON data", type=["json"])

if uploaded_file is not None:
    data = uploaded_file.getvalue().decode("utf-8")
    json_data = json.loads(data)
else:
    st.warning('Please upload your Json file.')
    st.stop()

# Extract nodes and edges
nodes = []
edges = []

def plot_network_graph():
    # Function to add nodes and edges for inputs and outputs
    def add_input_output_nodes(process_name, inputs, outputs):
        for inp in inputs:
            nodes.append({"id": inp, "title": "", "color": ""})
            edges.append((inp, process_name))
        for out in outputs:
            nodes.append({"id": out, "title": "", "color": ""})
            edges.append((process_name, out))

    # Function to add nodes for table_deps
    def add_table_deps_nodes(uprocs_name, table_deps):
        for table_dep, table_dep_content in table_deps.items():
            if table_dep not in nodes:
                nodes.append({"id": table_dep, "title": table_dep_content, "color": "#00FFFF"}) 
            edges.append((uprocs_name, table_dep))

    # Process each process (uprocs) in the JSON data
    for process_name, process_info in json_data.items():
        nodes.append({"id": process_name, "title": "", "color": ""})
        inputs = process_info.get("inputs", [])
        outputs = process_info.get("outputs", [])
        add_input_output_nodes(process_name, inputs, outputs)

        for uprocs_info in process_info.get("uprocs", []):
            uprocs_name = uprocs_info.get("name")
            uprocs_label = uprocs_info.get("label")
            nodes.append({"id": uprocs_name, "title": "", "color": ""})
            edges.append((process_name, uprocs_name))
            add_table_deps_nodes(uprocs_name, uprocs_info.get("table_deps", {}))

    # Create a DataFrame for nodes and edges
    nodes_df = pd.DataFrame(nodes)
    edges_df = pd.DataFrame(edges, columns=["source", "target"])

    # Create the pydeck visualization using the GraphLayer
    view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1)
    graph_layer = pdk.GraphLayer(
        id="graph-layer",
        node_data=nodes_df,
        edge_data=edges_df,
        get_source_position=["longitude", "latitude"],
        get_target_position=["longitude", "latitude"],
        get_width=1,
        get_color="color",
        highlight_color=[200, 200, 200, 200],
        directed=True,
    )

    # Display the graph using pydeck in Streamlit
    st.pydeck_chart(pdk.Deck(layers=[graph_layer], initial_view_state=view_state))

# Appellez la fonction pour visualiser le graphe lorsque l'application Streamlit est exécutée
if __name__ == "__main__":
    st.title("Orange Kenobi")
    plot_network_graph()
