
class LabelClass:
    """
    Enables selection of properties to support labels in a Layer
    """

    def __init__(self, row):
        self.className = row["className"]
        self.expression = row["expression"]
        self.SQLQuery = row["SQLQuery"]
        self.showClassLabels = row["showClassLabels"]
