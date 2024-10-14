from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def change_user_password(request, user, old_password, new_password):
    """
    Change the password of the given user.

    Parameters:
        request: The request object for handling messages.
        user: The user object for whom the password is being changed.
        old_password: The current password provided by the user.
        new_password: The new password to set.

    Returns:
        bool: True if the password was changed successfully, False otherwise.
    """
    if user.check_password(old_password):
        user.password = make_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Keep the user logged in
        messages.success(request, 'Your password has been changed successfully!')
        return True
    else:
        messages.error(request, 'Old password is incorrect.')
        return False
