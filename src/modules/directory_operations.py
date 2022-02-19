from os import path, mkdir, listdir, remove, rmdir

import logging

DEV = False

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=path.join("logs", "log.log"),
    filemode="a",
    level=logging.DEBUG
)

logger = logging.getLogger("log")
if DEV:
    console = logging.StreamHandler()
    console.level = logging.DEBUG
    console.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console)

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
        logger.info(
            msg="no sub_directory was provided, "
            + "defaulting to BSMS home directory"
        )
        file_path = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS"
        )
    else:
        logger.info(f"sub_directories: {sub_directories} entered")
        file_path = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS",
            *[str(sub_directory) for sub_directory in sub_directories]
        )
        if path.exists(file_path):
            logger.info(
                msg= f"sub_directory {sub_directories} found"
            )
        else:
            logger.warning(
                msg= f"sub_directory {sub_directories} not found"
            )
    logger.info("returning file path")
    return file_path

def directory_verification(directory: str):
    """check for directory, create new directory if not found"""
    logger.info(
        msg= f"checking for directory {directory}"
    )
    if path.exists(path.join((directory))):
        logger.info(
            msg= f"directory {directory} found"
        )
    else:
        logger.warning(
            msg= f"directory {directory} not found; "
            + "new directory was created"
        )
        mkdir(directory)

if __name__ == "__main__":
    directory_verification(bsms_directory())