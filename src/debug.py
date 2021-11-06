"""debug log creation module"""
from datetime import datetime
from os import mkdir, path


class DebugLog:
    """ Creates debug log
        Parameters: log_type
        Methods: log(), clear()"""
    # Initialise log object
    def __init__(self, log_type="Debug"):
        self.log_type: str = log_type
        self.display_log: bool = True
        self.filepath = path.join(
            logs_filepath(),
            "log_"+self.log_type+".txt"
        )
        if not path.exists(logs_filepath()):
            mkdir(logs_filepath())
        if not path.exists(self.filepath):
            with open(self.filepath, "w") as debug_log:
                debug_log.write("%s:%s - Log Initialised" % (
                    timestamp(),
                    self.log_type
                ))
        else:
            with open(self.filepath, "a") as debug_log:
                debug_log.write("\n\n%s:%s - New Log Initialised" % (
                    timestamp(),
                    self.log_type
                ))

    # Log function name and message
    def log(self, function, message):
        """Write line to debug log"""
        with open(self.filepath, "a") as debug_log:
            log_message = "%s:%s - %s" % (
                timestamp(),
                function,
                message
            )
            debug_log.write("\n"+log_message)
        if self.display_log:
            print(log_message)

    # Clear log
    def clear(self):
        """Clear debug log"""
        with open(self.filepath, "w") as debug_log:
            debug_log.write("")

# Create timestamp
def timestamp() -> str:
    """returns formatted timestamp when called"""
    return datetime.now().strftime("[%d/%m/%Y %H:%M:%S%f]")

def logs_filepath():
    """returns Debuglogs filepath"""
    return path.join(
        path.expanduser("~"),
        "Documents",
        "BSMS",
        "Debuglogs"
    )
