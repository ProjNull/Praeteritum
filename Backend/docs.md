# API Documentation

## Introduction

This API serves as a backend for user authentication, group management, and permissions control. It provides endpoints for user registration, login, permission management, and group management.

### Authorization and Authentication

The API uses JSON Web Tokens (JWT) for authorization and authentication. To access certain routes, users must provide a valid JWT, which is generated upon login and can be included in the request headers under the "Authorization" key.

## Routes

### User Registration

#### `POST /register`

Register a new user.

- **Parameters**
  - `displayname` (optional): The display name of the user.
  - `password`: The user's password.
  - `email`: The user's email address.

- **Response**
  - Successful Registration: JSON response with the `User_ID` and a success message.
  - Registration Error: JSON response with an error message if registration fails.

### User Login

#### `POST /login`

Log in a user and generate a JWT.

- **Parameters**
  - `email`: The user's email address.
  - `password`: The user's password.

- **Response**
  - Successful Login: JSON response containing a JWT and a success message.
  - Login Error: JSON response with an error message if login fails.

### User Profile

#### `GET /user/profile`

Retrieve the profile of the authenticated user.

- **Authorization Required**: Users must include a valid JWT in the request headers.

- **Response**
  - User Profile: JSON response with user profile details.
  - Authorization Error: JSON response with an error message if the JWT is missing or invalid.

### Permission Management

#### `POST /permission/get`

Retrieve permission information.

- **Parameters**
  - `permid`: The permission ID to retrieve.

- **Response**
  - Permission Details: JSON response with permission details.
  - Permission Not Found: JSON response with an error message if the permission does not exist.

#### `POST /permission/create`

Create a new permission link.

- **Parameters**
  - `userid`: The User_ID to link.
  - `groupid`: The Group_ID to link.
  - `level`: The permission level (0 to 3).

- **Response**
  - Permission Link Created: JSON response with a success message and the new permission link ID.
  - Error: JSON response with an error message if the creation fails (e.g., user already linked).

#### `POST /permission/delete`

Delete a permission link.

- **Parameters**
  - `permid`: The permission ID to delete.

- **Response**
  - Permission Link Deleted: JSON response with a success message.
  - Error: JSON response with an error message if the permission link does not exist.

#### `POST /permission/update`

Update a permission link.

- **Parameters**
  - `permid`: The permission ID to update.
  - `level`: The new permission level (0 to 3).

- **Response**
  - Permission Link Updated: JSON response with a success message.
  - Error: JSON response with an error message if the permission link does not exist.

#### `POST /permission/users_in`

Retrieve users in a specific group.

- **Parameters**
  - `groupid`: The Group_ID for which to retrieve users.
  - `limit`: The maximum number of users to retrieve.
  - `offset` (optional): Pagination offset.

- **Response**
  - Users in Group: JSON response with a list of user IDs in the specified group.
  - No Users in Group: JSON response with an error message if no users are in the group.

#### `POST /permission/groups_of`

Retrieve groups associated with a specific user.

- **Parameters**
  - `userid`: The User_ID for which to retrieve groups.
  - `limit`: The maximum number of groups to retrieve.
  - `offset` (optional): Pagination offset.

- **Response**
  - Groups Associated with User: JSON response with a list of Group_IDs associated with the user.
  - User Not in Any Groups: JSON response with an error message if the user is not in any groups.

### Group Management

#### `POST /addGroup`

Create a new group.

- **Parameters**
  - `Group_Name`: The name of the group.
  - `Description`: The description of the group.

- **Response**
  - Group Created: JSON response with a success message.
  - Error: JSON response with an error message if group creation fails.

#### `DELETE /removeGroup`

Delete a group.

- **Parameters**
  - `Group_ID`: The Group_ID of the group to delete.

- **Authorization Required**: Users must include a valid JWT with permission level 3 for the group.

- **Response**
  - Group Deleted: JSON response with a success message.
  - Error: JSON response with an error message if group deletion fails or if the user lacks the necessary permissions.

#### `GET /listGroups`

List all groups.

- **Response**
  - Groups List: JSON response with a list of Group_IDs and Group_Names for all available groups.

### Real-Time Event Handling

This API also handles real-time events via Socket.IO:

- `my_event`: Handles a custom event and emits a response event.
- `my_response`: Emits a response event in response to `my_event` with a message.

## Conclusion

This API provides user registration, authentication, permission management, group management, and real-time event handling functionalities. It is secured with JWT authorization, allowing for user-specific permissions and access control.
