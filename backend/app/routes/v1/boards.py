from fastapi import Request, APIRouter

boards_router = APIRouter(prefix="/boards")

"""
TODO: Finish create_board
        - Requires auth
        - Return output of service > Waiting on kristi
    
TODO: Finish delete_board
        - Requires auth
        - Return output of service > Waiting on kristi

TODO: Finish get_board
        - Requires auth
        - Return output of service > Waiting on kristi
"""

@boards_router.post("/fetch_boards")
def fetch_boards(group_ID: int, Phase): # TODO: Change pahase to type Phase
    """
    Fetch multiple boards based on the given group ID and phase.

    This endpoint retrieves boards from the database that match the provided
    group ID and phase. It expects a POST request with a JSON payload
    containing the 'group_ID' and optionally 'phase' (defaults to 0).

    Request JSON Parameters:
    - Group_ID (int): The ID of the group to fetch boards for (required).
    - Phase (int, optional): The phase of the boards to fetch (default is 0).

    Returns:
        - JSON response with a message and a list of boards if successful.
        - JSON response with a message and required fields if the input is missing or invalid.
        - JSON response with a message if no boards are found.
        - JSON response with a message if the request method is not POST.

    Responses:
    - 200 OK: Returns a JSON object with the number of boards fetched and a list of boards.
    - 400 Bad Request: Returns a JSON object with a message about missing required fields.
    - 404 Not Found: Returns a JSON object with a message that there are no boards in the group.
    - 405 Method Not Allowed: Returns a JSON object with a message that the endpoint only supports POST requests.
    """
    
    ...

@boards_router.post("/get_board/{board_ID}")
def get_board(board_ID: int):
    """
    Retrieve board details by board_ID.

    This endpoint handles POST requests to fetch details of a specific board using its Board_ID.
    It validates the presence of the required 'Board_ID' in the request JSON payload and returns
    the corresponding board details if found.

    Returns:
        JSON: A response with a message and board details if the Board_ID is valid and the board exists.
        - On success:
            {
                "message": "Board found!",
                "name": str,            # The name of the board
                "description": str,     # The description of the board
                "group": int,           # The group ID associated with the board
                "phase": str,           # The current phase of the board
                "revealPosts": bool,    # Whether posts are revealed
                "isLocked": bool,       # Whether the board is locked
                "isVotingLocked": bool  # Whether voting on the board is locked
            }
        - On missing Board_ID:
            {
                "message": "You must provide the required fields!",
                "required_fields": ["Board_ID"]
            }
        - On invalid Board_ID:
            {
                "message": "A board with this ID does not exist!"
            }
        - On unsupported request method:
            {
                "message": "This endpoint only supports POST requests!"
            }
    responses:
        - 400 Bad Request: If the Board_ID is not provided in the request.
        - 404 Not Found: If no board with the provided Board_ID exists.
        - 200 Success: If board sent successfully

    """
    ...

@boards_router.post("/delete_board/{board_ID}")
def delete_board():
    """
    Endpoint to delete a board.

    This endpoint handles the deletion of a board from the database based on the
    provided Board_ID.

    Methods:
    POST: Deletes the board with the specified Board_ID.

    Request JSON Parameters:
    - Board_ID (int): The ID of the board to be deleted. This field is required.

    Responses:
    - 400 Bad Request: If the Board_ID is not provided in the request.
    - 404 Not Found: If no board with the provided Board_ID exists.
    - 200 OK: If the board is successfully deleted.

    Returns:
    - JSON response indicating the result of the deletion operation.
      - If successful: {"message": "Board deleted"}
      - If Board_ID is missing: {
            "message": "You must provide the required fields!",
            "required_fields": ["Board_ID"]
        }
      - If board does not exist: {"message": "A board with this ID does not exist!"}
    """
    ...

@boards_router.post("/create_board")
def create_board(board_name: str, description: str, group_ID: int, reveal_posts: bool): # TODO: Double check that these are correct
    """
    Create a new board with the given details.

    This endpoint handles POST requests to create a new board. It expects the following
    JSON payload in the request body:
    - board_name: The name of the board (required).
    - description: A description of the board (required).
    - group_ID: The ID of the group to which the board belongs (required).
    - reveal_posts: A boolean indicating whether posts should be revealed (optional, defaults to False).

    Returns:
        JSON response containing a success message and the board ID if the board is created successfully.
        If required fields are missing, returns a message indicating the missing fields.

    Responses:
        200 OK:
            - message: "Board created"
            - boardid: <newly created board's ID>

        400 Bad Request:
            - message: "You must provide the required fields!"
            - required_fields: ["BoardName", "Description", "Group_ID"]
    """
    ...