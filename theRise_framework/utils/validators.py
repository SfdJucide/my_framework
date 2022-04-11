
def name_validator(full_name: str):
    full_name = full_name.split()
    if len(full_name) > 2:
        full_name = full_name[:2]

    return full_name, len(full_name)
