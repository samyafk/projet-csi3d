import time

ERROR_START = "==================[ERROR]====================\n"
SEPARATOR   = "=============================================\n"

class Logger():
    """Class that will log the error and the message of the program"""
       
    def __init__(self) -> None:
        self.logs = []

    def msg_log(self, msg:str) -> None:
        """Log a message

        Args:
            msg (str): the message to log
        """
        msg_log = msg + SEPARATOR
        self.logs.append(msg_log)

    def err_log(self, err:str) -> None:
        """Log an error
        
        Args:
            err (str): the error to log
        """
        err_log = ERROR_START + err + SEPARATOR
        self.logs.append(err_log)
        self.save_log()

    def save_log(self) -> None:
        """Save the log in a file
        """
        filemane = "log_"+str(time.time())+".txt"
        path = "logs/"+filemane
        
        with open(path, "w") as file:
            for log in self.logs:
                file.write(log)
        