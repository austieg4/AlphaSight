from abc import ABC, abstractmethod


class AnalysisStage(ABC):
    """
    Base class for every analysis pipeline stage.
    """

    @abstractmethod
    async def run(self, company):
        """
        Execute this stage.

        Returns the updated CompanyOverview.
        """
        raise NotImplementedError