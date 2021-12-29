from os import path, mkdir

import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=path.join(
        "logs",
        f"{__name__}.log"
    ),
    filemode="a"
)

logger = logging.getLogger(__name__)

def bsms_directory(sub_directory = None):
    """return user documents directory"""
    whitelisted_sub_directories = [
        "Projects",
        "Rhythms",
        "Finalised Projects",
        "Debuglogs"
    ]
    if (sub_directory not in whitelisted_sub_directories):
        if sub_directory is None:
            logger.info(
                msg="no sub_directory was provided:"
                + "defaulting to BSMS home directory"
            )
        else:
            logger.warning(
                msg=f"sub_directory {sub_directory} is not whitelisted:"
                + "defaulting to BSMS home directory"
            )
        file_path = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS"
        )
    else:
        logger.info(
            msg= f"sub_directory {sub_directory} is whitelisted"
        )
        file_path = path.join(
            bsms_directory(),
            sub_directory
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