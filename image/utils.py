import docker


def convert_bytes_to_human_readable(size_in_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0

    while size_in_bytes >= 1024 and index < len(units) - 1:
        size_in_bytes /= 1024
        index += 1

    return f"{size_in_bytes:.2f} {units[index]}"


def get_image_info(image):
    # 获取镜像名称
    name = image.tags[0] if image.tags else ""

    # 获取版本号
    version = image.attrs['RepoDigests'][0].split('@')[1] if 'RepoDigests' in image.attrs else ""

    # 获取自定义标签
    tags = [tag.split(':')[1] for tag in image.tags] if image.tags else []

    return name, version, tags

