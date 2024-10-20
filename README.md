Rule Engine With AST

# Rule_engine_Project

# Description
This project implements a simple rule engine that allows users to create, combine, and evaluate rules using an Abstract Syntax Tree (AST). 
It supports logical operations and provides an interface for users to define their own rules and evaluate them against sample data.

# Features

- Create individual rules and generate their AST representation.
- Combine multiple rules into a single AST.
- Evaluate rules against JSON data.
- Error handling for invalid rule strings and data formats.
- Edit existing rules and manage rule structures.

# Installation

To set up the project locally, follow these steps:

go to my-new-branch

1. Clone the Repository:
   ''bash
   https://github.com/crossboww/Rule_engine_with_AST.git
   download it and extract the download file in your system and open in VS-code.

2. in VS-code Terminal
   cd rule_engine_project # for navigate the file directory

3. install the django in VS-code Terminal  if not installed
   pip install django
   
4. Run the Django development Server
   python manage.py runserver

5. Open Your web browser and got to link ( http://127.0.0.1:8000)  provide in Terminal to access the Application


# Usage

1. To Create a rule, Use the
   http://127.0.0.1:8000/create_rule/

   Create the Rule like ("age > 30")

2. Editing Rules
   To edit a rule, you can modify the existing rule structure as needed.
   http://127.0.0.1:8000/rule_engine/edit_rule/1/

3. To Check data or Nodes in Databases
   http://127.0.0.1:8000/admin/

   Usernmae : krish23
   Password : kiddo@2311

   Then you will be able to see all the Nodes in Databse

4. Error Handling
   The application includes error handling for:

    Missing operators in rules.
    Invalid comparisons.
    Incorrect data formats.


# Contact

Name: Krish Kondabatni
Email: krishkonda89@gmail.com
GitHub: https://github.com/crossboww





   
   
   
