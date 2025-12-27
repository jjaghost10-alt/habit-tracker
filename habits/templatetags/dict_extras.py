from django import template

register = template.Library()

@register.simple_tag
def get_weekly_status(checkin_map, habit_id, day):
    """
    Returns True if a habit was completed on a given day.
    Usage in template:
    {% get_weekly_status map habit.id day as status %}
    """
    return checkin_map.get((habit_id, day))
