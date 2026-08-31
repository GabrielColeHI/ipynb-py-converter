import json
import sys
from pathlib import Path


def convert_ipynb_to_py(ipynb_path, output_path=None):
    #####
    #Converts a Jupyter notebook (.ipynb) to a Python script (.py). Comments out main function 
    ##calls and puts in a main function to run. 
    #####
    # Args:
    # ipynb_path (str): Path to the input .ipynb file
    # output_path (str, optional): Path to the output .py file. 
    #####

    ipynb_path = Path(ipynb_path)
    
    if not ipynb_path.exists():
        raise FileNotFoundError(f"File not found: {ipynb_path}")
    
    if not ipynb_path.suffix == '.ipynb':
        raise ValueError(f"File must be a .ipynb file, got: {ipynb_path.suffix}")
    
    if output_path is None:
        output_path = ipynb_path.with_suffix('.py')
    else:
        output_path = Path(output_path)
    #read notebook content
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    #Extract code cells
    code_lines = []
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            if isinstance(source, list):
                code_lines.extend(source)
            else:
                code_lines.append(source)
            code_lines.append('\n')
    
    #Writes to Python file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(code_lines)
    
    print(f"Successfully converted: {ipynb_path} -> {output_path}")

    #Print function names and start/end lines
    current_func = None
    start_line = 0
    for idx, line in enumerate(code_lines, start=1):
        stripped = line.strip()
        if stripped.startswith('def '):
            if current_func:
                print(f"Function '{current_func}': lines {start_line} to {idx - 1}")
            current_func = stripped.split('(')[0].replace('def ', '')
            start_line = idx
    if current_func:
        print(f"Function '{current_func}': lines {start_line} to {len(code_lines)}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ipynb_converter.py <input.ipynb> [output.py]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_ipynb_to_py(input_file, output_file)