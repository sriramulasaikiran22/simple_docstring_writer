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



# import ast
# import astor  # You'll need to install this package to convert AST back to code

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



import ast
import astor  # Make sure to install this package

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
source_file = 'm_new_sample.py'  # Make sure this file exists with the method
method_name = 'sum'
docstring = "I not sure about this method"
destination_file = 'modified_method.py'

modify_method_and_write(source_file, method_name, docstring, destination_file)

print(f"Modified method written to {destination_file}")
