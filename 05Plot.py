##Variables you need to change

SecondsPerInch=50 ##10-30s spaced stimul are easily visible in the 25-100 range (25 SPI is best for 10s stimuli, but 50 is readable), pharmacology is fine at 300. Most stimuli are unreadable beyond 200.
start= 1 ##frame at which to start graphing the data
stop= 20000  ##frame at which to stop the graphing

##-------------------------------##

import multiprocessing
import subprocess

start=str(start) ##These need to be strings for some reason
stop=str(stop) ##These need to be strings for some reason
SecondsPerInch=str(SecondsPerInch)

def run_script(script_args):
    """Function to run a script using subprocess with arguments"""
    script_name, args1, args2, args3, arg4 = script_args
    # Construct the command with the script and arguments
    command = ['python', script_name] +args1 + args2 + args3 + arg4
    subprocess.run(command, check=True)

def main():
    # List of tuples where each tuple contains a script name and a list of arguments
    scripts_with_args = [
        ('Plot.py', ['P0'],[start],[stop],[SecondsPerInch]),
        ('Plot.py', ['P1'],[start],[stop],[SecondsPerInch]),
        ('Plot.py', ['P2'],[start],[stop],[SecondsPerInch]),
        ('Plot.py', ['P3'],[start],[stop],[SecondsPerInch]),
        ('Plot.py', ['P4'],[start],[stop],[SecondsPerInch]),
    ]
    # Create a pool of processes, each running one of the scripts
    with multiprocessing.Pool(processes=len(scripts_with_args)) as pool:
        pool.map(run_script, scripts_with_args)

if __name__ == '__main__':
    main()
