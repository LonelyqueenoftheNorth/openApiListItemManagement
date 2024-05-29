# openApiListItemManagement
This small API provides a ToDo-List management, in which you can create List of what you have to do.
You also can update and delete them.

## How to use


| path | method | desciption |
|------|--------|------------|
|   /list/{list_id}    |    GET    |      get ID from specific list      |
|      |     DELETE     |       delete an entire list      |
|   /list    |     POST    |      create new list      |
|   /list/{list_id}/item   |    POST     |      create new item in list      |
|   /list/{list_id}/item/{item_id}   |     PATCH   |      update specific item      |
|      |     DELETE   |      delete item in list      |
|   /lists   |    GET    |     get list of all lists       |
|   /list/{list_id}   |    PATCH     |      update list      |
