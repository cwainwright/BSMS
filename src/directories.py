from os import path, mkdir, listdir, remove, rmdir

def cleanup(project_directory):
    """clean up half-complete project directories"""
    for file in listdir(project_directory):
        if path.isfile(file):
            remove(path.join(project_directory, file))
        else:
            cleanup(file)
    rmdir(project_directory)

def bsms_directory(*sub_directories: str):
    """return bsms home directory"""
    if sub_directories == []:
        print(
            "no sub_directory was provided, "
            + "defaulting to BSMS home directory"
        )
        file_path = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS"
        )
    else:
        print(f"sub_directories: {sub_directories} entered")
        file_path = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS",
            *[str(sub_directory) for sub_directory in sub_directories]
        )
        if not path.exists(file_path):
            print(
                f"warning: sub_directory {sub_directories} not found"
            )
    print("returning file path")
    return file_path

def directory_verification(directory: str):
    """check for directory, create new directory if not found"""
    print(
        f"checking for directory {directory}"
    )
    if path.exists(path.join((directory))):
        print(
            f"directory {directory} found"
        )
    else:
        print(
            f"directory {directory} not found; "
            + "new directory was created"
        )
        mkdir(directory)

if __name__ == "__main__":
    directory_verification(bsms_directory())