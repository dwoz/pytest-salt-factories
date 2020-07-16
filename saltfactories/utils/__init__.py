"""
saltfactories.utils
~~~~~~~~~~~~~~~~~~~

Utility functions
"""
import os
import random
import string
import sys
from functools import lru_cache


def random_string(prefix, size=6, uppercase=True, lowercase=True, digits=True):
    """
    Generates a random string.

    Args:
        prefix(str): The prefix for the random string
        size(int): The size of the random string
        uppercase(bool): If true, include uppercased ascii chars in choice sample
        lowercase(bool): If true, include lowercased ascii chars in choice sample
        digits(bool): If true, include digits in choice sample
    Returns:
        str: The random string
    """
    if not any([uppercase, lowercase, digits]):
        raise RuntimeError("At least one of 'uppercase', 'lowercase' or 'digits' needs to be true")
    choices = []
    if uppercase:
        choices.extend(string.ascii_uppercase)
    if lowercase:
        choices.extend(string.ascii_lowercase)
    if digits:
        choices.extend(string.digits)

    return prefix + "".join(random.choice(choices) for _ in range(size))


@lru_cache(maxsize=1)
def running_username():
    if sys.platform.startswith("win32"):
        import win32api

        return win32api.GetUserName()
    else:
        import pwd

        return pwd.getpwuid(os.getuid()).pw_name
