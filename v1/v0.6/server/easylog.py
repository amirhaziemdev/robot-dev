import time
import os

class EasyLog():
    """
    A class for easily writing logs to a file named log_date
    Dependencies: time and os
    
    Please use the write_log function to start writing log.
    Please specify directory name when creating class if you want to change
    from the default log directory
    
    """
    def __init__(self, dir="log"):
        # Initialize variables
        self.date = ""
        self.log_file = ""
        self.dir = "./"+dir+"/"
        
        # Check for log directory, create one if doesn't exist
        try:
            os.listdir(self.dir)
        except:
            os.makedirs(self.dir)
        
        # Open log and ready for writing
        self.open_log()
    
    def get_todays_date(self):
        self.date = time.strftime("%d%m%Y") # Format: DayMonthYear [01012010]
        print("Fetching today's date!")
    
    def _open(self):
        # Get today's date
        self.get_todays_date()
        # Open log file/Create new if doesn't exist and ready to write
        self.log_file_name = "log_" + str(self.date)
        _log_dir = self.dir + self.log_file_name
        self.log_file = open(
            _log_dir,
            "a+",
            )
        print(f"Log file {self.log_file_name} has been opened!")
        
    def open_log(self):
        # Create new log file if different date, else pass
        if self.log_file:
            if self.date != time.strftime("%d%m%Y"):
                self._open()
            else:
                return
        else: # Create new log if one doesn't exist
            self._open()
            
    def write_log(self, text):
        # Get current date + time
        _date = time.ctime()
        # Prepare log text
        log_text = f"[ {_date} ]  {text}\n"
        if self.log_file:
            # Write log to file
            self.log_file.write(log_text)
            print(f"Writing '{text}' to {self.log_file_name}!")
        else:
            pass
        
    def close_log(self):
        # Properly close file after use
        self.log_file.close()
        print(f"Closing log {self.log_file_name}!")
            
    def __del__(self):
        self.close_log()
       
if __name__ == "__main__":
    # Testing purposes
    x = EasyLog()
    x.write_log("You dont want tot know what im writing")