""" Handles initial startup processes checking the file system integrity"""
import logging
from os import path

from directory_operations import bsms_directory, directory_verification, logger

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=path.join("logs", "log.log"),
    filemode="a",
    level=logging.DEBUG
)

logger = logging.getLogger("bootstrap")

def setup():
    """Initial setup function"""
    filepaths = [
        bsms_directory(),
        bsms_directory("Rhythms"),
        bsms_directory("Projects"),
        bsms_directory("Finalised Projects")
    ]
    for filepath in filepaths:
        logger.info(
            msg=f"verifying directory {filepath}"
        )
        directory_verification(filepath)
        logger.info(
            msg=f"directory {filepath} verified"
        )


if __name__ == "__main__":
    setup()
