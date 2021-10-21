from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user

class IsAuthor(permissions.BasePermission):
    message = 'you are not author'

    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        if "authors" in user_groups:
            return True
        return False