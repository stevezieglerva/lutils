from IRepository import IRepository
from ProcessDTO import ProcessDTO


class InMemoryRepository(IRepository):
    def get_process(self, process_id: str) -> ProcessDTO:
        return ProcessDTO("test")

    def save_process(self, process: ProcessDTO):
        print(f"Saving: {process}")
