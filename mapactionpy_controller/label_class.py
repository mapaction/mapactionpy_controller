
class LabelClass:
    """
    Enables selection of properties to support labels in a Layer
    """

    def __init__(self, row):
        self.class_name = row["class_name"]
        self.expression = row["expression"]
        self.sql_query = row["sql_query"]
        self.show_class_labels = row["show_class_labels"]

    def __eq__(self, other):
        comp = [
            self.class_name == other.class_name,
            self.expression == other.expression,
            self.sql_query == other.sql_query,
            self.show_class_labels == other.show_class_labels
        ]

        return all(comp)

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)
