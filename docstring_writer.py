import ast
import astor

# from main import ai_docstring


# class DocstringAdder(ast.NodeTransformer):
#     def visit_FunctionDef(self, node):
#         if node.name == 'my_function':
#             node.body.insert(0, ast.Expr(value=ast.Str(s=ai_docstring)))
#         return node

# file_path = 'example.py'

# with open(file_path, 'r') as file:
#     source = file.read()

# # Parse the source code into an AST
# tree = ast.parse(source)

# # Transform the AST
# transformer = DocstringAdder()
# transformed_tree = transformer.visit(tree)

# # Convert the AST back to source code
# modified_source = astor.to_source(transformed_tree)

# # Write the modified code back to the file
# with open(file_path, 'w') as file:
#     file.write(modified_source)


# class DocstringAdder(ast.NodeTransformer):
#     def __init__(self, method_name, docstring):
#         self.method_name = method_name
#         self.docstring = docstring

#     def visit_FunctionDef(self, node):
#         if node.name == self.method_name:
#             # Add the docstring as the first statement in the function body
#             node.body.insert(0, ast.Expr(value=ast.Constant(value=self.docstring)))
#         return self.generic_visit(node)

# def add_docstring_to_method(code, method_name, docstring):
#     tree = ast.parse(code)
#     transformer = DocstringAdder(method_name, docstring)
#     modified_tree = transformer.visit(tree)
#     return astor.to_source(modified_tree)  # Convert AST back to source code

# # Example usage
# code = """
# class MyClass:
#     def my_method(self):
#         return "Hello, world!"
# """

# new_code = add_docstring_to_method(code, "my_method", "This method returns a greeting.")
# print(new_code)


# ========================= working code for doc writer ========================= #


# class MethodExtractor(ast.NodeVisitor):
#     def __init__(self, method_name):
#         self.method_name = method_name
#         self.method = None

#     def visit_FunctionDef(self, node):
#         if node.name == self.method_name:
#             self.method = node
#         self.generic_visit(node)

# def extract_method_from_file(file_path, method_name):
#     with open(file_path, 'r') as f:
#         code = f.read()
#     tree = ast.parse(code)
#     extractor = MethodExtractor(method_name)
#     extractor.visit(tree)
#     return extractor.method

# class DocstringAdder(ast.NodeTransformer):
#     def __init__(self, docstring):
#         self.docstring = docstring

#     def visit_FunctionDef(self, node):
#         # Add the docstring as the first statement in the function body
#         node.body.insert(0, ast.Expr(value=ast.Constant(value=self.docstring)))
#         return node

# def modify_method_and_write(source_file, method_name, docstring, destination_file):
#     method_node = extract_method_from_file(source_file, method_name)
#     if method_node is None:
#         print(f"Method '{method_name}' not found in '{source_file}'.")
#         return

#     # Modify the method to add the docstring
#     adder = DocstringAdder(docstring)
#     modified_method = adder.visit(method_node)

#     # Prepare the new code
#     new_code = astor.to_source(modified_method)

#     # Write the modified method to the destination file
#     with open(destination_file, 'a+') as f:
#         f.write(new_code)

# # Example usage
# source_file = 'm_new_sample.py'  # Make sure this file exists with the method
# method_name = 'sum'
# docstring = "I not sure about this method"
# destination_file = 'modified_method.py'

# modify_method_and_write(source_file, method_name, docstring, destination_file)

# print(f"Modified method written to {destination_file}")

# ================================================================================= #


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# class FunctionExtractor(ast.NodeVisitor):
#     def __init__(self, function_name):
#         self.function_name = function_name
#         self.function_def = None

#     def visit_FunctionDef(self, node):
#         if node.name == self.function_name:
#             self.function_def = node
#         self.generic_visit(node)

# def extract_function_from_code(code, function_name):
#     tree = ast.parse(code)
#     extractor = FunctionExtractor(function_name)
#     extractor.visit(tree)

#     if extractor.function_def is None:
#         raise ValueError(f"Function '{function_name}' not found.")

#     return extractor.function_def

# Example usage
# code = """
# def my_function(a, b):
#     return a + b

# def another_function(x):
#     return x * 2

# def get_fibonacci_list(n) -> list:
#     if n <= 0:
#         return []
#     elif n == 1:
#         return [0]
#     elif n == 2:
#         return [0, 1]

#     fib_series = [0, 1]
#     for i in range(2, n):
#         next_fib = fib_series[-1] + fib_series[-2]
#         fib_series.append(next_fib)

#     return fib_series
# """

# function_name = "get_fibonacci_list"
# function_node = extract_function_from_code(code, function_name)

# # Convert the extracted function definition back to source code
# function_code = astor.to_source(function_node)
# print(f"Extracted function code:\n{function_code}")
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# import subprocess

# command_to_execute = ["black", "docstring_writer.py"]

# run = subprocess.run(command_to_execute, capture_output=True)

# print("::", run.stdout)  # the output "Test"
# print(run.stderr)  # the error part of the output
# print("------------")
# print(run)

# --------------------------------------------------------------
# import os

# directory = "data"
# def get_files():
#     # fw_root = os.path.join(os.path.dirname(ayx_fw_path), ddir)
#         # fw_abs_root = os.path.abspath(fw_root)
#     fw_abs_root = os.path.abspath(directory)
#     for root, dirs, files in os.walk(fw_abs_root):

#         for file in files:
#             if file.endswith(".py"):
#                 print(file)

# get_files()
# --------------------------------------------------------------------------
import streamlit as st
import os
from main import document_code
import subprocess
import shutil

def remove_existing_output_files():
    folder = os.getcwd() + "\\output_files\\"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

remove_existing_output_files()


# Function to list all files in a directory and its subdirectories
def list_files(folder):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    return file_list

# Title of the app
st.title("Folder Selector and Python File Viewer")

# Folder selection
folder_path = st.sidebar.text_input("Enter folder path:", "")
if st.sidebar.button("Select Folder"):
    if os.path.isdir(folder_path):
        st.success(f"Selected folder: {folder_path}")
    else:
        st.error("Invalid folder path. Please enter a valid path.")
if folder_path:
    if os.path.isdir(folder_path):
        st.success(f"Selected folder: {folder_path}")
        # List files in the selected folder and its subdirectories
        all_files = list_files(folder_path)
        st.sidebar.subheader("Files in Selected Folder:")
        for file in all_files:
            st.sidebar.text(file)
    else:
        st.error("Invalid folder path. Please enter a valid path.")

# Generate button
if st.button("Generate"):
    if folder_path and os.path.isdir(folder_path):
        # st.success("Generating...")  # Placeholder for actual generation logic
        for root, dirs, files in os.walk(folder_path):

            for file in files:
                if file.endswith(".py"):
                    print(file, root)
                    ffile_path = os.path.join(root, file)
                    document_code(file_path=ffile_path)
                    st.success(f":white_check_mark: {ffile_path}")


        # command_to_execute = ["black", "modified_method.py"]
        # run = subprocess.run(command_to_execute, capture_output=True)
        # print('$$',run.stderr, "$$")
        st.success("All Done !!")
    else:
        st.error("Please select a valid folder first.")

# Specify the folder containing the files
folder_path = "output_files"

# List all files in the folder
files = os.listdir(folder_path)

if len(files) > 0:
    st.title("File Viewer")

    for file in files:
        file_path = os.path.join(folder_path, file)
    
        if file.endswith('.py'):  # Only display Python files
            st.write(file)  # Show the file name
            
            # Create an expander for viewing the file content
            with st.expander(f"Expand to see {file} content"):
                with open(file_path, "r") as f:
                    content = f.read()
                    st.code(content, language='python')

# Load and display a Python file
python_file_path = st.sidebar.file_uploader("Upload a Python file", type=["py"])

if python_file_path is not None:
    file_content = python_file_path.read().decode("utf-8")
    st.code(file_content, language='python')
# =====================================================================================
