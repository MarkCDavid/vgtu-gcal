def csv_entry(*args):
    entry = ""
    for arg in args:
        entry += f"{arg},"
    entry += "\n"
    return entry
