def check_view_permission(user, min_level=0, max_level=3):
    hierarchy = user.user_level.hierarchy
    return min_level <= hierarchy <= max_level
