
class MapRecipe:
    """
    MapRecipe - Ordered list of layers for each Map Product
    """

    # TODO: asmith 2020/03/06
    # Please could we use a more meaningful name than "row" for this parameter? Isn't it a dict?
    def __init__(self, row):
        self.mapnumber = row["mapnumber"]
        self.category = row["category"]
        self.export = row["export"]
        self.product = row["product"]
        self.layers = row["layers"]
        self.summary = row["summary"]
        self.hasQueryColumnName = self.containsQueryColumn()

    def containsQueryColumn(self):
        hasQueryColumnName = False
        for layer in self.layers:
            # TODO asmith 2020/03/06
            # Is this a terser way of achieving the same thing?
            # ```
            #    if 'columnName' in layer:
            # ```
            if (layer.get('columnName', None) is not None):
                hasQueryColumnName = True
                break
        return hasQueryColumnName
