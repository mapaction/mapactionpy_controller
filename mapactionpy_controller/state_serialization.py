def get_state_optional_fields(obj, optional_fields):
    # See https://docs.python.org/3/library/pickle.html#pickle-state
    # Copy the object's state from self.__dict__ which contains
    # all our instance attributes. Always use the dict.copy()
    # method to avoid modifying the original state.
    state = obj.__dict__.copy()
    # Remove any optional members which have a value of None.
    for option in optional_fields:
        if not state[option]:
            del state[option]
    return state


def set_state_optional_fields(obj, state, optional_fields):
    # Restore optional elements to None.
    for option in optional_fields:
        if option not in state:
            state[option] = None

    obj.__dict__.update(state)
