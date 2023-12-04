import os

def read_input_as_lines(day, strip=True):
    with open(f"inputs\\day{day}.txt") as f:
        return [line.strip() if strip else line[:-1] for line in f]
    
def read_example_as_lines(day, strip=True):
    with open(f"inputs\\day{day}_ex.txt") as f:
        return [line.strip() if strip else line[:-1] for line in f]