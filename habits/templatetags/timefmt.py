from django import template

# Register a custom template filter library
register = template.Library()


@register.filter
def mmss(seconds):
    """
    Template filter to format a duration in seconds as MM:SS.

    This filter converts a numeric value representing seconds
    into a human-readable time format suitable for UI display,
    such as countdown timers.

    Behavior:
    - Invalid or missing input is treated as 0 seconds.
    - Negative values are clamped to 0.
    - Output is always zero-padded (e.g. "05:03").

    Usage in templates:
    {{ seconds|mmss }}
    """
    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        seconds = 0

    # Convert seconds into minutes and seconds
    m, s = divmod(max(0, seconds), 60)

    # Return formatted time string
    return f"{m:02d}:{s:02d}"
