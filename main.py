import utilities.io     as io 
import importlib
import time
import os

# Dynamically imports the solution files for the project, provided they exist.
_SOLUTIONS = {}
def import_solutions():
    
    print("--")
    print(os.getcwd())
    print("--")
    
    global _SOLUTIONS
    for i in range(1, 26):
        if os.path.exists(f"solutions\\day{i}.py"):
            _SOLUTIONS[i] = importlib.import_module(f"solutions.day{i}")
import_solutions()

def main():
    print(("-"*23) + "\n- ADVENT OF CODE 2023 -\n" + ("-"*23) + "\n")
    while True:
        try:
            soln = int(input("Choose a day to solve: "))
            print()
            if soln not in (0, -1, -2) and soln not in _SOLUTIONS.keys():
                raise LookupError
            
        except LookupError: # No such solution 
            print(f"No solution provided for day {soln}. Please choose a valid "
                  f"solution index (1-25, or 0 to exit)\n")
            continue
        except ValueError:  # int() failed
            print(f"Please enter a solution index as an integer (1-25, or 0 to "
                  "exit)\n")

        # When the solution is 0, we terminate.
        if soln == 0:
            break

        # -1 is a secret option: Generate solution files from the template.
        if soln == -1:
            generate_solution_files()
            continue

        # -2 is another secret option: Reloads all the solution files so that 
        # you can live update a solution.
        if soln == -2:
            reload_solutions()
            continue
            
        start_time = time.time()
        _SOLUTIONS[soln].print_header()
        _SOLUTIONS[soln].solve_p1()
        elapsed = time.time() - start_time
        print(f"(Part One took {round(elapsed, 2)} seconds)\n")
        start_time = time.time()
        _SOLUTIONS[soln].solve_p2()
        elapsed = time.time() - start_time
        print(f"(Part Two took {round(elapsed, 2)} seconds)\n")

def reload_solutions():
    print("Reloading Files:")
    existing = list(_SOLUTIONS.keys())
    for i in range(1, 26):
        # The solution exists now but didn't when we first started:
        if os.path.exists(f"solutions\\day{i}.py") and i not in existing:
            module = importlib.import_module(f"solutions.day{i}")
            _SOLUTIONS[i] = module

        # The solution file still exists now:
        elif os.path.exists(f"solutions\\day{i}.py"):
            _SOLUTIONS[i] = importlib.reload(_SOLUTIONS[i])

        # No provision is made for if the solution doesn't exist anymore. 
    print("Reload complete\n")

def generate_solution_files():
    """Generates new/refreshes stale solution files from the day0 template."""
    
    # Read the template in. 
    print("Loading template...")
    template_lines = []
    with open("solutions\\day0.py", "r") as f:
        template_lines = [line.strip() for line in f]
    
    # Iterate over the expected solutions 1 through 26, and compile a list of 
    # the ones that either don't exist, or are unmodified from their templates
    # (based on loosey-goosey heuristics)
    print("Checking for existing solution files...")
    files_to_rewrite = []
    for i in range(1,26):
        write_file_i = True     # Assume we want to write file i...
        overwrite_file = False  # ...because we assume it doesn't exist. 

        # Default behaviour when a file exists is to not replace it. *BUT* that
        # being said, I might not have worked on it yet. 
        if os.path.exists(f"solutions\\day{i}.py"):
            write_file_i = False
            overwrite_file = True

            # Check to see if I've worked on this file yet. For my purposes, I
            # assume that if I've changed the line after the def do_part_one_for
            # function, I've worked on the file
            with open(f"solutions\\day{i}.py", "r") as f:
                # Set this flag when the next line is the first line in the body
                # of the do_part_one_for() function.
                body_of_dp1f = False    

                for line in f:
                    if body_of_dp1f:                # do immediately if flagged
                        write_file_i = line == "\tpass\n"
                        break
                    if line.startswith("def do_part_one_for"):  # flag after 
                        body_of_dp1f = True

        # If think the file should be changed
        if write_file_i:
            files_to_rewrite.append((i, overwrite_file))
    
    # Before any actual rewriting is done, veryify with the human:
    print("\nThe files to be generated/rewritten are as follows:")
    for file, exists in files_to_rewrite:
        suffix = "\t- RISKY!\t(File already exists)" if exists else ""
        print(f"\tday{file}.py {suffix}")
    print()
    confirmation = "Seriously, why doesn't python have do-whiles? It's annoying"
    while confirmation not in ("y", "n"):
        confirmation = input("Do you still want to generate files? (y/n): ")
    if confirmation == "n":
        print("Template generation aborted.\n")
        return
    
    # Now we actually overwrite with impunity!
    for i, exists in files_to_rewrite:
        # We decided to change this file. Delete it if it exists. 
        if os.path.exists(f"solutions\\day{i}.py"):
            os.remove(f"solutions\\day{i}.py")
        
        # Re-write it with the template. 
        with open(f"solutions\\day{i}.py", "w") as f:    
            for ln in template_lines:
                ln = ln.replace("XXX", str(i))
                ln = ln.replace("print", "\tprint")
                ln = ln.replace("def \tprint", "def print")
                ln = ln.replace("results = ", "\tresults = ")
                ln = ln.replace("pass", "\tpass")
                ln = ln.replace("return", "\treturn")
                ln = ln.replace("input_lines ", "\tinput_lines ")
                f.write(ln + "\n")
    print("File generation complete\n")
    
    # Since we generated solutions, we need to reload them:
    reload_solutions()

if __name__ == "__main__":
    main()