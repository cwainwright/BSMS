""" Handles initial startup processes checking the file system integrity"""
from os import chdir, mkdir, path

from debug import DebugLog

debug_log = DebugLog("bootstrap.py")

def documents_directory():
    """return user documents directory"""
    return path.join(
        path.expanduser('~'),
        "Documents"
    )

def bsms_directory(sub_directory = None):
    """return user documents directory"""
    whitelisted_sub_directories = [
        "Projects",
        "Rhythms",
        "Finalised Projects",
        "Debuglogs"
    ]
    if sub_directory in whitelisted_sub_directories:
        file_path = path.join(
            bsms_directory(),
            sub_directory
        )
    else:
        file_path = path.join(
            path.expanduser('~'),
            "Documents",
            "BSMS"
        )
    return file_path

def check_directory_existence(
    target_directory: str = path.join(
            path.expanduser('~'),
            "Documents", "BSMS"
        )
):
    """check for and create directory"""
    if path.exists(target_directory):
        return True
    mkdir(target_directory)
    return False

def directory_verification(*directories):
    """check for directories in list"""
    for directory in directories:
        debug_log.log(
            "directory_verification()",
            "checking for directory %s" % directory
        )
        if check_directory_existence(*directory):
            debug_log.log(
                "directory_verification()",
                "directory %s found" % directory
            )
        else:
            debug_log.log(
                "directory_verification()",
                "directory %s not found; " % directory
                + "new directory was created"
            )

def setup():
    """Initial setup function"""
    chdir(bsms_directory())
    directory_verification(
            [bsms_directory()],
            [bsms_directory("Rhythms")],
            [bsms_directory("Projects")],
            [bsms_directory("Finalised Projects")]
    )

if __name__ == "__main__":
    setup()