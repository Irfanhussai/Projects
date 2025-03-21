def has_permission(role, action):
    permissions = {
        "Admin": ["manage_users", "upload", "edit", "delete", "view"],
        "Contributor": ["upload", "edit", "view"],
        "Viewer": ["view"]
    }
    return action in permissions.get(role, [])
