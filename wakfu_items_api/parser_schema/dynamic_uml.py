from graphviz import Digraph
from pydantic import BaseModel
from typing import List, get_type_hints, get_origin, get_args  # Replacing _GenericAlias
import inspect


def generate_uml(root_class: type, output_file="items_uml"):
    """
    Generate a UML diagram for the classes defined in a Pydantic model hierarchy.

    Args:
        root_class (type): The root class to start generating the UML diagram.
        output_file (str): The name of the output file (without extension).
    """
    dot = Digraph()

    # Set global graph attributes for better readability
    dot.attr(rankdir="LR", fontsize="12", fontname="Arial")

    # A set to track processed classes to avoid duplicates
    processed_classes = set()

    # Customize node style
    def process_class(cls):
        """Recursively process a class and its attributes."""
        if cls in processed_classes:
            return
        processed_classes.add(cls)

        # Add the current class as a node with a box shape and light blue fill
        dot.node(
            cls.__name__,
            f"<<TABLE BORDER='0' CELLBORDER='0' CELLSPACING='0'><TR><TD><B>{cls.__name__}</B></TD></TR></TABLE>>",
            shape="box",
            style="filled",
            fillcolor="lightblue",
            fontname="Arial",
        )

        # Inspect the class attributes
        attributes = []  # Collect all attributes for the node
        for attr_name, attr_type in get_type_hints(cls).items():
            # Handle lists and other generic types
            origin = get_origin(attr_type)
            if origin is list or origin is List:
                attr_type = get_args(attr_type)[0]

            # If the attribute is another class, add an edge
            if inspect.isclass(attr_type) and issubclass(attr_type, BaseModel):
                dot.edge(
                    cls.__name__,
                    attr_type.__name__,
                    label=f"{attr_name}: {attr_type.__name__}",
                    color="blue",
                    fontname="Arial",
                )
                process_class(attr_type)
            # Handle primitive types like int, float, etc.
            elif attr_type in {int, float, str, bool, list, dict}:
                primitive_name = attr_type.__name__
                attributes.append(f"{attr_name}: {primitive_name}")

        # Update the node with all attributes
        if attributes:
            dot.node(
                cls.__name__,
                f"<<TABLE BORDER='0' CELLBORDER='0' CELLSPACING='0'><TR><TD><B>{cls.__name__}</B></TD></TR>"
                + "".join(f"<TR><TD>{attr}</TD></TR>" for attr in attributes)
                + "</TABLE>>",
                shape="box",
                style="filled",
                fillcolor="lightyellow",
                fontname="Arial",
            )

    # Start processing from the root class
    process_class(root_class)

    # Render the UML diagram
    dot.render(output_file, format="png", cleanup=True)
