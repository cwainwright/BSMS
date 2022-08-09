""" Handles initial startup processes checking the file system integrity"""

from directories import bsms_directory, directory_verification

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
        print(f"verifying directory {filepath}")
        directory_verification(filepath)
        print(f"directory {filepath} verified")


if __name__ == "__main__":
    setup()
