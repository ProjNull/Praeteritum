from fastapi import HTTPException

class ExampleNotFoundException(HTTPException):
    def __init__(self, example_id: int):
        super().__init__(status_code=404, detail=f"Example {example_id} not found")
