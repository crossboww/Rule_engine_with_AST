# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from .models import Node
from django.views.decorators.csrf import csrf_exempt
import re

# Function to parse a rule string and create an AST
def create_rule_view(request):
    if request.method == 'POST':
        rule_string = request.POST.get('rule')  # Get the rule from the form
        try:
            ast_root = create_rule(rule_string)  # Create AST from the rule
            save_ast_to_db(ast_root)  # Save AST to the database
            return render(request, 'rule_engine/success.html')  # Show success page
        except Exception as e:
            error_message = str(e)  # Capture the error message
            return render(request, 'rule_engine/create_rule.html', {'error': error_message})  # Show form with error
    return render(request, 'rule_engine/create_rule.html')  # Show form

# Function to parse the rule string and create an AST

def create_rule(rule_string):
    parts = rule_string.split()
    if len(parts) < 3:
        raise ValueError(f"Rule is incomplete: {rule_string}")
    
    attribute, operator, value = parts[0], parts[1], parts[2]
    node = Node(node_type='operand', value=f"{attribute} {operator} {value}")
    node.save()
    return node


def edit_rule_view(request, node_id):
    try:
        node = Node.objects.get(id=node_id)  # Fetch the existing node by ID
    except Node.DoesNotExist:
        return render(request, 'rule_engine/create_rule.html', {'error': "Node not found."})

    if request.method == 'POST':
        new_rule_string = request.POST.get('rule')  # Get the new rule from the form
        try:
            new_ast_root = create_rule(new_rule_string)  # Create a new AST from the new rule
            node.value = new_rule_string  # Update the existing node's value
            node.save()  # Save changes to the database
            return render(request, 'rule_engine/success.html')  # Show success page
        except Exception as e:
            error_message = str(e)  # Capture the error message
            return render(request, 'rule_engine/edit_rule.html', {'error': error_message, 'node': node})  # Show form with error

    return render(request, 'rule_engine/edit_rule.html', {'node': node})  # Show edit form



def combine_rules(rules):
    if not rules:
        return None

    # Create a root node for the combined AST
    root = Node(node_type='operator', value='AND')

    # Create child nodes for each rule
    for rule in rules:
        # Create a node from the rule string
        rule_node = create_rule(rule)  # Ensure this function is defined
        # Connect the rule node to the root
        if not root.left:
            root.left = rule_node
        else:
            # Find the rightmost child to attach new rules
            current = root.left
            while current.right:
                current = current.right
            current.right = rule_node

    return root

@csrf_exempt
def combine_rules_view(request):
    if request.method == 'POST':
        # Handle POST request
        return JsonResponse({'message': 'Rules combined successfully!'})
    
    elif request.method == 'GET':
        # Handle GET request (if you want to support GET)
        return JsonResponse({'message': 'GET request received, but use POST to combine rules.'})
    
    else:
        # If request method is not supported
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def evaluate_rule(ast_node, data):
    if ast_node is None:
        raise ValueError("AST node is None.")

    print(f"Evaluating node: {ast_node.value}")  # Debugging line

    # If it's an operand (like a condition)
    if ast_node.node_type == 'operand':
        # Split the value into parts (e.g., "age > 30")
        parts = ast_node.value.split()
        
        if len(parts) < 3:
            raise ValueError(f"Invalid node value: {ast_node.value}")
        
        attribute = parts[0]
        operator = parts[1]
        value = parts[2]

        # Now evaluate based on operator
        try:
            if operator == '>':
                return data[attribute] > float(value)
            elif operator == '<':
                return data[attribute] < float(value)
            elif operator == '==':
                return data[attribute] == value.strip("'")  # Handle string values
            # Add more operators as needed
            else:
                raise ValueError(f"Unknown operator: {operator}")
        except KeyError as e:
            raise ValueError(f"Missing attribute in data: {e}")
        except Exception as e:
            raise ValueError(f"Error evaluating condition: {e}")

    # If it's an operator (AND/OR)
    if ast_node.node_type == 'operator':
        left_result = evaluate_rule(ast_node.left, data)
        right_result = evaluate_rule(ast_node.right, data)
        
        if ast_node.value == 'AND':
            return left_result and right_result
        elif ast_node.value == 'OR':
            return left_result or right_result
        else:
            raise ValueError(f"Unknown operator type: {ast_node.value}")

    raise ValueError(f"Invalid node type: {ast_node.node_type}")

def test_rule_view(request):
    # Example data to evaluate
    data = {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }
    
    # Example combined rule (replace this with your actual rule structure)
    combined = {
        "age": ">= 30",
        "department": "Sales",
        "salary": "> 50000",
        "experience": ">= 2"
    }
    
    # Evaluate the rule
    result = evaluate_rule(combined, data)
    
    # Return the result as JSON
    return JsonResponse({"result": result})

# Save AST recursively to the database
def save_ast_to_db(ast_node, parent=None):
    ast_node.save()
    if ast_node.left:
        ast_node.left.parent = ast_node
        save_ast_to_db(ast_node.left, ast_node)
    if ast_node.right:
        ast_node.right.parent = ast_node
        save_ast_to_db(ast_node.right, ast_node)

