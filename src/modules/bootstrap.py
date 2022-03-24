""" Handles initial startup processes checking the file system integrity"""
try:
    from src.modules.directory_operations import bsms_directory, directory_verification, logger
except ModuleNotFoundError:
    from directory_operations import bsms_directory, directory_verification, logger

def setup():
    """Initial setup function"""
    filepaths = [
        bsms_directory(),
        bsms_directory("Rhythms"),
        bsms_directory("Rests"),
        bsms_directory("Rests", "Default"),
        bsms_directory("Rests", "Custom"),
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
