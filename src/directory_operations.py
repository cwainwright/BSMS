from os import path, mkdir, listdir, remove, rmdir

import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=path.join("logs", "log.log"),
    filemode="a",
    level=logging.DEBUG
)

logger = logging.getLogger("log")
console = logging.StreamHandler()
console.level = logging.INFO
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

def bsms_directory(sub_directory = None):
    """return user documents directory"""
    if sub_directory is None:
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
        file_path = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS",
            sub_directory
        )
        if path.exists(file_path):
            logger.info(
                msg= f"sub_directory {sub_directory} found, "
                + "returning full path"
            )
        else:
            logger.warning(
                msg= f"sub_directory {sub_directory} not found, "
                + "defaulting to BSMS home directory"
            )
            file_path = path.join(
                path.expanduser('~'),
                "Documents",
                "BSMS"
            )
    return file_path

def directory_verification(directory):
    """check for directory"""
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