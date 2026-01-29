from abc import ABC, abstractmethod

class BaseAPI(ABC):

    @abstractmethod
    def process_request(self, request):
        pass
