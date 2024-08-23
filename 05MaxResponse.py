import multiprocessing
import subprocess

def run_script(script_args):
    """Function to run a script using subprocess with arguments"""
    script_name, args = script_args
    # Construct the command with the script and arguments
    command = ['python', script_name] + args
    subprocess.run(command, check=True)

def main():
    # List of tuples where each tuple contains a script name and a list of arguments
    scripts_with_args = [
        ('MaxResponse.py', ['P0']),
        ('MaxResponse.py', ['P1']),
        ('MaxResponse.py', ['P2']),
        ('MaxResponse.py', ['P3']),
        ('MaxResponse.py', ['P4'])
    ]
    
    # Create a pool of processes, each running one of the scripts
    with multiprocessing.Pool(processes=len(scripts_with_args)) as pool:
        pool.map(run_script, scripts_with_args)

if __name__ == '__main__':
    main()
