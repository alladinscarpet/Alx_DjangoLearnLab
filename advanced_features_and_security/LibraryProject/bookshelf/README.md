We defined custom permissions in Book model:
- can_view
- can_create
- can_edit
- can_delete

Groups created in Django Admin:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

Views use @permission_required decorator to enforce access:
- book_list      → requires can_view
- create_book    → requires can_create
- edit_book      → requires can_edit
- delete_book    → requires can_delete

Users are assigned to groups in Django admin.
Groups automatically grant permissions.