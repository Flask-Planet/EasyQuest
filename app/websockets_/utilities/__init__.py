def get_quest_code_from_path(path) -> int | None:
    """
    Get the quest code from the path /quest/<quest_code>/master
    """

    split_path = path.split("/")

    if "quest" not in split_path:
        return 0

    quest_index = split_path.index("quest")

    try:
        return split_path[quest_index + 1]
    except IndexError:
        return 0
