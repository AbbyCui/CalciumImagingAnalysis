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
        ('ProcessData.py', ['P0']),
        ('ProcessData.py', ['P1']),
        ('ProcessData.py', ['P2']),
        ('ProcessData.py', ['P3']),
        ('ProcessData.py', ['P4'])
    ]
    
    # Create a pool of processes, each running one of the scripts
    print("Running the following:",scripts_with_args)
    with multiprocessing.Pool(processes=len(scripts_with_args)) as pool:
        pool.map(run_script, scripts_with_args)

if __name__ == '__main__':
    main()
