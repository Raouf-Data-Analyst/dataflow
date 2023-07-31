import json
import graphviz
import streamlit as st

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

    # Identify sessions and uprocs
    sessions = set()
    uprocs = set()

    # Process each process (uprocs) in the JSON data
    for process_name, process_info in json_data.items():
        sessions.add(process_name)
        nodes.append({"id": process_name, "title": "", "color": ""})
        inputs = process_info.get("inputs", [])
        outputs = process_info.get("outputs", [])
        add_input_output_nodes(process_name, inputs, outputs)

        for uprocs_info in process_info.get("uprocs", []):
            uprocs_name = uprocs_info.get("name")
            uprocs.add(uprocs_name)
            nodes.append({"id": uprocs_name, "title": "", "color": ""})
            edges.append((process_name, uprocs_name))
            add_table_deps_nodes(uprocs_name, uprocs_info.get("table_deps", {}))

    # Create a graph
    g = graphviz.Digraph('G', filename='cluster_edge.gv', format='png', engine='dot', executable='C:\Users\alarouci\Graphviz\bin\dot.exe') 
    g.attr(compound='true')

    # Create clusters for sessions and add nodes to clusters
    with g.subgraph(name='cluster0') as c:
        for session in sessions:
            c.node(session, shape="box")

    # Add nodes with attributes to the graph
    for node_data in nodes:
        node_id = node_data["id"]
        g.node(node_id, label=node_id)

    # Add edges with connections between uprocs in different session clusters
    for edge in edges:
        source, target = edge
        if source in uprocs and target in uprocs and source != target:
            g.edge(source, target)

    # Save and render the graph
    g.render(view=True)

# Appellez la fonction pour visualiser le graphe lorsque l'application Streamlit est exécutée
if __name__ == "__main__":
    st.title("Orange Kenobi")
    plot_network_graph()
