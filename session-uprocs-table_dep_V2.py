import json
import streamlit as st
from pyvis.network import Network

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

    # Create a graph
    nt = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True, notebook=True,cdn_resources='remote', select_menu = True, filter_menu=True)  
    nt.show_buttons(filter_=['physics'])
    # Add nodes with attributes to the graph
    for node_data in nodes:
        node_attributes = {}  # You can modify this to include additional attributes if needed
        node_id = node_data["id"]
        node_attributes["title"] = node_data["title"]  # Use 'title' to set the tooltip text

        # Check if the node is an "uprocs" or an input/output node and update the color accordingly
        if node_id in json_data:
            node_attributes["color"] = "#FF0000"  # Red for uprocs
        else:
            node_attributes["color"] = "#00FF00"  # Green  for input/output nodes

        # Check if the node has "table_deps" and update the color accordingly
        if node_id in [table_dep["id"] for table_dep in nodes if table_dep["color"] == "#00FFFF"]:
            node_attributes["color"] = "#00FFFF"  # Cyan  for nodes with table_deps

        nt.add_node(node_id, label=node_id, **node_attributes)

    # Add edges with arrows for dependencies
    for edge in edges:
        source, target = edge
        nt.add_edge(source, target, arrows='to', arrowStrikethrough=False, color="#87CEFA")  # Black color for arrows

    # Display the graph using pyvis in Streamlit
    st.header('Dépendance entre sessions-uprocs-table_deps')
    st_pyvis_chart(nt)

# Appellez la fonction pour visualiser le graphe lorsque l'application Streamlit est exécutée
if __name__ == "__main__":
    st.title("Orange Kenobi")
    plot_network_graph()
