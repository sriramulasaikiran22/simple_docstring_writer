from langchain_huggingface import HuggingFaceEndpoint
import os
from langchain import PromptTemplate, LLMChain
from dotenv import load_dotenv
from prompt import system_prompt
import ast
import re
import astor


ai_docstring = ""
file_path = ""


def get_text_from_tripple_quotes(text):
    # Regular expression pattern
    pattern = r"\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\""

    # # Example usage
    # text = '''Here is some text with a triple-quoted string:
    # '''This is a triple-quoted string.'''
    # And another one:
    # """This is another one."""
    # '''

    # Find all matches
    matches = re.findall(pattern, text, re.DOTALL)

    # Extract the matched groups
    extracted_texts = [m[0] if m[0] else m[1] for m in matches]
    print(extracted_texts)
    return extracted_texts[0]


def get_functions(source_code):
    tree = ast.parse(source_code)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return functions


# Load environment variables
load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_TOKEN")
model = "mistralai/Mistral-7B-Instruct-v0.2"


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


def document_code(file_path):
    with open(file_path, "r") as file:
        source_code = file.read()

    functions = get_functions(source_code)
    for function in functions:
        user_prompt = f"Generate a docstring for the following function:\n\n{function.name}({', '.join(arg.arg for arg in function.args.args)})\n"

        docstring = generate_docstring(function, user_prompt)
        print(f"Generated docstring for {function.name}:\n{docstring}\n")
        
        ai_docstring = f"{get_text_from_tripple_quotes(docstring)}"


        class MethodExtractor(ast.NodeVisitor):
            def __init__(self, method_name):
                self.method_name = method_name
                self.method = None

            def visit_FunctionDef(self, node):
                if node.name == self.method_name:
                    self.method = node
                self.generic_visit(node)

        def extract_method_from_file(file_path, method_name):
            with open(file_path, 'r') as f:
                code = f.read()
            tree = ast.parse(code)
            extractor = MethodExtractor(method_name)
            extractor.visit(tree)
            return extractor.method

        class DocstringAdder(ast.NodeTransformer):
            def __init__(self, docstring):
                self.docstring = docstring

            def visit_FunctionDef(self, node):
                # Add the docstring as the first statement in the function body
                node.body.insert(0, ast.Expr(value=ast.Constant(value=self.docstring)))
                return node

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

        # Example usage
        source_file = file_path  # Make sure this file exists with the method
        method_name = function.name
        docstring = ai_docstring
        destination_file = 'modified_method.py'

        modify_method_and_write(source_file, method_name, docstring, destination_file)

        print(f"Modified method written to {destination_file}")


# file_path = "new_sample.py"

document_code(file_path="m_new_sample.py")
