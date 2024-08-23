import multiprocessing
import subprocess

SecondsPerInch=100
start=1
stop="all"

def run_script(script_args):
    """Function to run a script using subprocess with arguments"""
    script_name, args = script_args
    # Construct the command with the script and arguments
    command = ['python', script_name] + args
    subprocess.run(command, check=True)

def main():
    # List of tuples where each tuple contains a script name and a list of arguments
    scripts_with_args = [
        ('Plot.py', ['P0',start, stop, SecondsPerInch]),
        ('Plot.py', ['P1',start, stop, SecondsPerInch]),
        ('Plot.py', ['P2',start, stop, SecondsPerInch]),
        ('Plot.py', ['P3',start, stop, SecondsPerInch]),
        ('Plot.py', ['P4',start, stop, SecondsPerInch]),
    ]
    # Create a pool of processes, each running one of the scripts
    with multiprocessing.Pool(processes=len(scripts_with_args)) as pool:
        pool.map(run_script, scripts_with_args)

if __name__ == '__main__':
    main()
