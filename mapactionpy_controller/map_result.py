from datetime import datetime


# TODO: asmith 2020/03/06
#
# 1) Based on the description in the docstring, would "LayerResult" be a more appropriate name for
# this class?
#
# 2) What are valid states for this object. eg Can I legitimately have:
#       * `self.added = False` and `self.message = "" `
#       * `self.added = True` and `self.hash = ""`
#       * Does the `self.hash` value necessarily corespond to the `self.dataSource`?
# I'd suggest that some methods to ensure consitancy, rather than rely on the caller to ensure this.
# Would it be appropriate to use the DataSource class here?
class MapResult:
    """
    MapResult - result for adding a layer to the Map Product
    """

    def __init__(self, layerName):
        """
        Constructor, initialises new Map Result for the layer

        Arguments:
           layerName {str} -- name of the map layer being added
        """
        # TODO: asmith 2020/03/06
        # Ideally stick to all lower_case_variable_names
        # https://www.python.org/dev/peps/pep-0008/#method-names-and-instance-variables
        self.layerName = layerName
        self.dataSource = ""
        now = datetime.now()
        # dd/mm/YY H:M:S
        self.dateStamp = now.strftime("%d/%m/%Y %H:%M:%S")
        self.added = False
        self.message = ""
        self.hash = ""
