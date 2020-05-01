
class LabelClass:
    """
    Enables selection of properties to support labels in a Layer
    """

    def __init__(self, row):
        self.className = row["className"]
        self.expression = row["expression"]
        self.SQLQuery = row["SQLQuery"]
        self.showClassLabels = row["showClassLabels"]

    def __eq__(self, other):
        comp = [
            self.className == other.className,
            self.expression == other.expression,
            self.SQLQuery == other.SQLQuery,
            self.showClassLabels == other.showClassLabels
        ]

        return all(comp)

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)
