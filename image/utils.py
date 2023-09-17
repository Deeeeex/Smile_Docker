def convert_bytes_to_human_readable(size_in_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0

    while size_in_bytes >= 1024 and index < len(units) - 1:
        size_in_bytes /= 1024
        index += 1

    return f"{size_in_bytes:.2f} {units[index]}"
