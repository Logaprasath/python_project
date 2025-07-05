# This is a new Python file for a calculator.
import doctest

def add(x, y):
  """Adds two numbers.

  >>> add(2, 3)
  5
  >>> add(-1, 1)
  0
  >>> add(-5, -5)
  -10
  >>> add(1.5, 2.5)
  4.0
  """
  # Performs addition of x and y.
  return x + y

def subtract(x, y):
  """Subtracts two numbers.

  >>> subtract(5, 3)
  2
  >>> subtract(3, 5)
  -2
  >>> subtract(0, 0)
  0
  >>> subtract(-1, -1)
  0
  >>> subtract(5.5, 1.5)
  4.0
  """
  # Performs subtraction of y from x.
  return x - y

def multiply(x, y):
  """Multiplies two numbers.

  >>> multiply(2, 3)
  6
  >>> multiply(-1, 5)
  -5
  >>> multiply(0, 100)
  0
  >>> multiply(1.5, 2)
  3.0
  """
  # Performs multiplication of x and y.
  return x * y

def divide(x, y):
  """Divides two numbers.

  Raises:
    ValueError: If y is zero.

  >>> divide(6, 3)
  2.0
  >>> divide(5, 2)
  2.5
  >>> divide(0, 5)
  0.0
  >>> divide(-6, 3)
  -2.0
  >>> divide(6, -3)
  -2.0
  >>> divide(10, 0)
  Traceback (most recent call last):
    ...
  ValueError: Cannot divide by zero
  """
  # Checks if the divisor is zero to prevent DivisionByZeroError.
  if y == 0:
    raise ValueError("Cannot divide by zero")
  # Performs division of x by y.
  return x / y

def main():
  """Gets user input, performs calculation, and prints the result."""
  try:
    # Get the first number from user input.
    num1_str = input("Enter the first number: ")
    # Convert the input string to a floating-point number.
    num1 = float(num1_str)

    # Get the desired arithmetic operator from user input.
    operator = input("Enter an operator (+, -, *, /): ")

    # Get the second number from user input.
    num2_str = input("Enter the second number: ")
    # Convert the input string to a floating-point number.
    num2 = float(num2_str)

    # Perform calculation based on the operator.
    if operator == '+':
      result = add(num1, num2)
    elif operator == '-':
      result = subtract(num1, num2)
    elif operator == '*':
      result = multiply(num1, num2)
    elif operator == '/':
      result = divide(num1, num2)  # Division by zero is handled in the divide function.
    else:
      # If the operator is not one of the valid options, inform the user.
      print("Invalid operator. Please use +, -, *, or /.")
      return # Exit the function if the operator is invalid.

    # Display the calculated result.
    print(f"The result is: {result}")

  except ValueError as e:
    # Handle errors related to invalid number input or division by zero.
    if "could not convert string to float" in str(e):
      print("Invalid input. Please enter numeric values for numbers.")
    else:
      # This will catch ValueError from divide by zero.
      print(f"Error: {e}")
  except Exception as e:
    # Handle any other unexpected errors during execution.
    print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
  # Run doctests when the script is executed directly.
  # The -v option can be used from the command line for verbose output (e.g., python calculator.py -v)
  doctest.testmod()
  # Call the main function to start the calculator program.
  main()
