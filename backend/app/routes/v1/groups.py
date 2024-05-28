from typing import Union
from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.responses import RedirectResponse

groups_router = APIRouter(prefix="/groups")
"""
TODO: Finish list_groups
        - Requires auth
        - Return output of service > Waiting on kristi
        
TODO: Finish remove_group
        - Requires auth
        - Return output of service > Waiting on kristi
    
TODO: Finish add_group
        - Requires auth
        - Return output of service > Waiting on kristi
"""

@groups_router.post("/add_group")
def add_group():
    """
    Create a new group via a POST request.

    This function allows you to create a new group by providing a group name and a description.

    :return: JSON response indicating the status of the group creation or an error message if the operation fails.
    """

    return

@groups_router.post("/list_groups")
def list_groups(request: Request):
    """
    Retrieve a list of groups via a POST request.

    This function allows you to retrieve a list of all available groups.

    :return: JSON response containing a list of groups, where each group is represented as a list containing its Group_ID and Group_Name.
    """

    return 
    
@groups_router.delete("/remove_group/{group_ID}")
def remove_group(group_ID: int):
    """
    Remove a group via a DELETE request.

    This function allows authorized users to delete an existing group based on the provided Group_ID. To be authorized,
    the user must have permission level 3 (typically indicating administrative privileges) for the group.

    :param u: The authorized user with appropriate permissions.
    :return: JSON response indicating the status of the group removal or an error message if the operation fails or if the user lacks the necessary permissions.
    """
    ...
    
    return 