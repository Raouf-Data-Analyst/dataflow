import streamlit as st
import graphviz as gv

# Sample data for sessions, uprocs, and dependencies
data = {
    "sessions": ["Session1", "Session2", "Session3"],
    "uprocs": ["Uproc1", "Uproc2", "Uproc3", "Uproc4"],
    "dependencies": [
        ("Session1", "Uproc1"),
        ("Session1", "Uproc2"),
        ("Session2", "Uproc2"),
        ("Uproc2", "Uproc3"),
        ("Uproc3", "Session3"),
        ("Uproc4", "Uproc1"),
    ]
}

# Function to create the graph using Graphviz
def create_graph(data):
    dot = gv.Digraph(format="png")

    # Add nodes for sessions and uprocs
    for session in data["sessions"]:
        dot.node(session, shape="box", color="lightblue", style="filled")
    for uproc in data["uprocs"]:
        dot.node(uproc, shape="box", color="lightgreen", style="filled")

    # Add edges for dependencies
    for dependency in data["dependencies"]:
        source, target = dependency
        dot.edge(source, target)

    return dot

# Main Streamlit app code
def main():
    st.title("Network Graph Visualization with Graphviz on Streamlit")

    st.sidebar.header("Graph Settings")
    st.sidebar.write("Customize the graph as per your data.")

    # Display graph settings (if any)

    # Create and display the graph
    graph = create_graph(data)
    st.graphviz_chart(graph)

if __name__ == "__main__":
    main()

