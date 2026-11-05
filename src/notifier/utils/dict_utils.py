def getv(mapping, path, default=None):
    """
    Get a value from a nested dict using a dot-separated path.

    Behaves like dict.get(): if any key in the path is missing,
    returns default.

    Args:
        mapping (dict): Source dictionary.
        path (str): Dot-separated path, e.g. "db.primary.host".
        default (any): Value returned if the path is missing. Defaults to None.

    Returns:
        Value at path, or default if the path is missing.

    Raises:
        ValueError: If path is empty.
        TypeError: If an intermediate value is not a dict.
    """
    if not path:
        raise ValueError("path must be non-empty")

    cur = mapping

    for key in path.split("."):
        if not isinstance(cur, dict):
            raise TypeError(
                f"Expected dict while accessing '{path}', got {type(cur).__name__}"
            )

        if key not in cur:
            return default

        cur = cur[key]

    return cur


def reqv(mapping, path):
    """
    Get a required value from a nested dict using a dot-separated path.

    Behaves like dict['key']: raises KeyError if any key in the path
    is missing.

    Args:
        mapping (dict): Source dictionary.
        path (str): Dot-separated path, e.g. "db.primary.host".

    Returns:
        Value at path.

    Raises:
        ValueError: If path is empty.
        KeyError: If the path is missing.
        TypeError: If an intermediate value is not a dict.
    """
    if not path:
        raise ValueError("path must be non-empty")

    cur = mapping

    for key in path.split("."):
        if not isinstance(cur, dict):
            raise TypeError(
                f"Expected dict while accessing '{path}', got {type(cur).__name__}"
            )

        if key not in cur:
            raise KeyError(f"Missing path '{path}'")

        cur = cur[key]

    return cur


def setv(mapping, path, value, strict=False):
    """
    Set a value in a nested dict using a dot-separated path.

    With strict=False, missing intermediate keys are created as dicts and
    existing non-dict intermediate values are replaced with dicts.

    With strict=True, every intermediate key must exist and contain a dict.

    Args:
        mapping (dict): Source dictionary.
        path (str): Dot-separated path, e.g. "db.primary.host".
        value (any): Value to set.
        strict (bool): Require all intermediate keys to exist and contain
            dicts. Defaults to False.

    Raises:
        ValueError: If path is empty.
        KeyError: If path is missing and strict=True.
        TypeError: If an intermediate value is not a dict and strict=True.
    """
    if not path:
        raise ValueError("path must be non-empty")

    keys = path.split(".")
    cur = mapping

    for key in keys[:-1]:
        if not isinstance(cur, dict):
            raise TypeError(
                f"Expected dict while accessing '{path}', got {type(cur).__name__}"
            )

        if key not in cur:
            if strict:
                raise KeyError(f"Missing path '{path}'")
            cur[key] = {}
        elif not isinstance(cur[key], dict):
            if strict:
                raise TypeError(
                    f"Expected dict at '{key}' while accessing '{path}', got {type(cur[key]).__name__}"
                )
            cur[key] = {}

        cur = cur[key]

    if strict and keys[-1] not in cur:
        raise KeyError(f"Missing path '{path}'")

    cur[keys[-1]] = value
