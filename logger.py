import os
import datetime
from config import *

if os.path.isfile(log_override):
	log_file = log_override
elif os.path.isdir(log_override):
	log_file = os.path.join(log_override, "agent.log")
else:
	print(f"Log location invalid or not specified, defaulting to {working_directory}")
	log_file = os.path.join(os.path.abspath(working_directory), f"agent - {datetime.date.today()}.log")

def agent_log(log_entry: str, header: bool = False):
	global log_file, log_override
	with open(log_file, "a") as file:
		file.write(f"\n====================================================================================================\n {datetime.datetime.now()} \n {log_entry}\n" if header else f"{log_entry}\n")
