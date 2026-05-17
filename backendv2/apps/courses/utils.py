import string
import secrets


ALPHANUMERIC_CHARS = string.ascii_letters + string.digits

def generate_unique_short_code(ModelClass, field_name, length=6):
    """
    Generates a unique 6-character alphanumeric code for Lesson.
    Retries until a unique code is found.
    """

    while True:
        # Generate a random 6-character string
        code = ''.join(secrets.choice(ALPHANUMERIC_CHARS) for _ in range(length))
        # Check if this code already exists in the database
        exists = ModelClass.objects.filter(
            **{field_name: code}
        ).exists()

        if not exists:
            return code
