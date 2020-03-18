
class MapReport:
    """
    MapReport - Report accumulated while the Map Product is generated.
    Contains overall summary and a status for each layer.
    """

    def __init__(self, productName):
        """
        Initialise to success for the product

        Arguments:
            productName {str} -- Map product name
        """
        self.result = "Failure"
        self.productName = productName
        self.summary = "No layers provided in recipe for '" + self.productName + "' product."
        self.classification = ""  # Not used
        self.results = list()

    def add(self, mapResult):
        """
        Appends the result for a given layer to the report

        Arguments:
            mapResult {MapResult} -- result summary for a given layer
        """
        self.results.append(mapResult)
        self._updateSummary()

    def _updateSummary(self):
        """
        Maintains summary
        """
        # Update summary
        failCount = 0
        reportIter = 0
        for r in self.results:
            reportIter = reportIter + 1
            if (r.added is False):
                failCount = failCount + 1

        if (failCount == 0):
            self.result = "Success"
            self.summary = "'" + self.productName + "' product generated successfully."
        else:
            self.result = "Warning"
            self.summary = str(failCount) + " / " + str(reportIter) + \
                " layers could not be added to '" + self.productName + "' product."
