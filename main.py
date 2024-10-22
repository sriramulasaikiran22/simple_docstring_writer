from langchain_huggingface import HuggingFaceEndpoint
import os
import subprocess
from langchain import PromptTemplate, LLMChain
from dotenv import load_dotenv
from prompt import system_prompt
import ast
import re
import astor


ai_docstring = ""
file_path = ""


# method to extract text in triple quotes.
def get_text_from_tripple_quotes(text):
    # Regular expression pattern
    pattern = r"\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\""

    # Find all matches
    matches = re.findall(pattern, text, re.DOTALL)

    # Extract the matched groups
    extracted_texts = [m[0] if m[0] else m[1] for m in matches]
    print(extracted_texts)
    return extracted_texts[0]


# get available function names from python file.
def get_functions(source_code):
    tree = ast.parse(source_code)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return functions

# ------------- class to extract method from tree ---------- #
class FunctionExtractor(ast.NodeVisitor):
    def __init__(self, function_name):
        self.function_name = function_name
        self.function_def = None

    def visit_FunctionDef(self, node):
        if node.name == self.function_name:
            self.function_def = node
        self.generic_visit(node)

def extract_function_from_code(code, function_name):
    tree = ast.parse(code)
    extractor = FunctionExtractor(function_name)
    extractor.visit(tree)
    
    if extractor.function_def is None:
        raise ValueError(f"Function '{function_name}' not found.")
    
    return extractor.function_def
# ----------------------------------------------------------- #


# Load environment variables
load_dotenv()

# setup api token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_TOKEN")
model = "mistralai/Mistral-7B-Instruct-v0.2"


# responcible for creating docstring using LLM.
def generate_docstring(function, prompt):

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    llm = HuggingFaceEndpoint(
        repo_id=model, max_new_tokens=8192, temperature=0.9, token=os.getenv("HF_TOKEN")
    )
    response = llm.invoke(messages)
    return response


# main handle for sequence execution.
def document_code(file_path):
    # read file
    with open(file_path, "r") as file:
        source_code = file.read()

    functions = get_functions(source_code)
    # loop through available functions to create doc string
    for function in functions:
        # extract complete python method from .py file based on name. 
        extracted_method = extract_function_from_code(source_code, function.name)
        function_code = astor.to_source(extracted_method)
        # user_prompt = f"Generate a docstring for the following function:\n\n{function.name}({', '.join(arg.arg for arg in function.args.args)})\n"
        user_prompt = f"Generate a docstring for the following function:\n{function_code}\n"
        print('Prompt:-', user_prompt)

        docstring = generate_docstring(function, user_prompt)
        print(f"Generated docstring for {function.name}:\n{docstring}\n")
        
        ai_docstring = f"{get_text_from_tripple_quotes(docstring)}"

        # helper class for getting raw python method.
        class MethodExtractor(ast.NodeVisitor):
            def __init__(self, method_name):
                self.method_name = method_name
                self.method = None

            def visit_FunctionDef(self, node):
                if node.name == self.method_name:
                    self.method = node
                self.generic_visit(node)
                
        # helper function for method extraction.
        def extract_method_from_file(file_path, method_name):
            with open(file_path, 'r') as f:
                code = f.read()
            tree = ast.parse(code)
            extractor = MethodExtractor(method_name)
            extractor.visit(tree)
            return extractor.method

        # helper class for setting the docstring using ast.
        class DocstringAdder(ast.NodeTransformer):
            def __init__(self, docstring):
                self.docstring = docstring

            def visit_FunctionDef(self, node):
                # Add the docstring as the first statement in the function body
                node.body.insert(0, ast.Expr(value=ast.Constant(value=self.docstring)))
                return node

        # helper function for docstring setup to python method.
        def modify_method_and_write(source_file, method_name, docstring, destination_file):
            method_node = extract_method_from_file(source_file, method_name)
            if method_node is None:
                print(f"Method '{method_name}' not found in '{source_file}'.")
                return

            # Modify the method to add the docstring
            adder = DocstringAdder(docstring)
            modified_method = adder.visit(method_node)

            # Prepare the new code
            new_code = astor.to_source(modified_method)

            # Write the modified method to the destination file
            with open(destination_file, 'a+') as f:
                f.write(new_code)

        # writing doc string to method in python file.
        source_file = file_path
        method_name = function.name
        docstring = ai_docstring
        org_file_name = file_path.split("\\")[-1]
        destination_file = f'output_files\\docy_{org_file_name}'

        modify_method_and_write(source_file, method_name, docstring, destination_file)

        print(f"Modified method written to {destination_file}") 
        command_to_execute = ["black", f"{destination_file}"]
        run = subprocess.run(command_to_execute, capture_output=True)
        print('$$',run.stderr, "$$") 


# file_path = "new_sample.py"

# # function call for writing doc string and saving it in new file.
# document_code(file_path="calculator.py")
# command_to_execute = ["black", "modified_method.py"]
# run = subprocess.run(command_to_execute, capture_output=True)
# print('$$',run.stderr, "$$")



# directories to scan for .py file to get data.
# actuall_dirs = ["core", 'lib']

directory = "data"

# for ddir in actuall_dirs:
#     fw_root = os.path.join(os.path.dirname(directory), ddir)


# fw_abs_root = os.path.abspath(directory)
# for root, dirs, files in os.walk(fw_abs_root):

#     for file in files:
#         if file.endswith(".py"):
#             print(file)
#             document_code(file_path=file)


# command_to_execute = ["black", "modified_method.py"]
# run = subprocess.run(command_to_execute, capture_output=True)
# print('$$',run.stderr, "$$")
    
