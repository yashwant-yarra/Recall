from uuid import UUID


def file_id_from_object_name(name:str) -> UUID | None:
    parts = name.split("/")
    if len(parts) != 4 or parts[0] != "users" or parts[2] != "doc":
        return None
    stem = parts[3].split(".", 1)[0]
    try:
        return UUID(stem)
    except ValueError:
        return None