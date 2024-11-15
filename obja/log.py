import time
import traceback

ERROR_START = "\n==================[ERROR]====================\n"
SEPARATOR   = "\n=============================================\n"

class Logger():
    """Class that will log the error and the message of the program"""
       
    def __init__(self) -> None:
        self.logs = []
        self.filename = time.strftime("%Y%m%d-%H%M%S") + ".log"

    def msg_log(self, msg:any) -> None:
        """Log a message

        Args:
            msg (str): the message to log
        """
        msg_log = str(msg) + SEPARATOR
        self.logs.append(msg_log)

    def err_log(self, err:Exception, err_traceback=None) -> None:
        """Log an error and the traceback
        
        Args:
            err (str): the error to log
        """
        if err_traceback is None:
            err_traceback = err.__traceback__
        
        err_log = ERROR_START
        for line in traceback.format_exception(type(err), err, err_traceback):
            err_log += line
        err_log += SEPARATOR
        
        self.logs.append(err_log)
        self.save_log()

    def save_log(self) -> None:
        """Save the log in a file
        """
        path = "logs/" + self.filename
        
        with open(path, "w") as file:
            for log in self.logs:
                file.write(log)
        