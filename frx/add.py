import os
import glob
import click

TAG_MAPPING = {"user": "#Users\n"}


def all_files(source, recursive=False):
    """Collect all file paths
    Args:
        source: file or directory name
        recursive: search recursively directories
    Returns:
        list of files path
    """
    files = []
    for src in source:
        if os.path.isdir(src):
            files.extend(
                [f for f in glob.glob(src + "**/**.py", recursive=recursive) if os.path.isfile(f)]
            )
        elif os.path.isfile(src):
            files.append(src)
        else:
            click.echo(f"'{src}' not valid source")
    return files


def add_data(file, tag, value):
    """Read/write file with data as per tag
    Args:
        file: file path
        tag: commented tag
        value: Value to data in specific tag
    """
    TAG_FOUND = False

    with open(file, "r+") as f:
        data = f.readlines()

        for index, line in enumerate(data):
            if TAG_MAPPING[tag] == line:
                TAG_FOUND = True
                click.echo(
                    f"{os.path.basename(file)}: Adding {value} to {TAG_MAPPING[tag].strip()}"
                )
                continue

            if TAG_FOUND and "#" in line:
                index = index - 1 if data[index - 1] == "\n" else index
                data.insert(index, f"{value}\n")
                break
        if data:
            f.writelines(data)


@click.command()
@click.option("-u", "--user", help="User")
@click.option(
    "-r", "--recursive", is_flag=True, help="Include all files from directories recursively"
)
@click.argument("files", nargs=-1)
def add(files, user, recursive):
    """Add data to source files."""
    files = all_files(files, recursive=recursive)
    for file in files:
        if user:
            add_data(file=file, tag="user", value=user)
