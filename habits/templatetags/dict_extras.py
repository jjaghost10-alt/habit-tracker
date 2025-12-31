from django import template

# Register a custom template tag library
register = template.Library()


@register.simple_tag
def get_weekly_status(checkin_map, habit_id, day):
    """
    Template helper to check whether a habit was completed on a given day.

    This tag looks up a (habit_id, date) pair in a precomputed dictionary
    containing habit check-in information.

    Parameters:
    - checkin_map: dictionary mapping (habit_id, date) -> True / False
    - habit_id: ID of the habit being rendered
    - day: date object representing the day to check

    Returns:
    - True if the habit was completed on that day
    - False (or None) otherwise

    Usage in templates:
    {% get_weekly_status checkin_map habit.id day as status %}
    """
    return checkin_map.get((habit_id, day))
