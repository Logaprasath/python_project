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
  if y == 0:
    raise ValueError("Cannot divide by zero")
  return x / y

def main():
  """Gets user input, performs calculation, and prints the result."""
  try:
    num1_str = input("Enter the first number: ")
    num1 = float(num1_str)

    operator = input("Enter an operator (+, -, *, /): ")

    num2_str = input("Enter the second number: ")
    num2 = float(num2_str)

    if operator == '+':
      result = add(num1, num2)
    elif operator == '-':
      result = subtract(num1, num2)
    elif operator == '*':
      result = multiply(num1, num2)
    elif operator == '/':
      result = divide(num1, num2)
    else:
      print("Invalid operator. Please use +, -, *, or /.")
      return

    print(f"The result is: {result}")

  except ValueError as e:
    if "could not convert string to float" in str(e):
      print("Invalid input. Please enter numeric values for numbers.")
    else:
      print(f"Error: {e}")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
  doctest.testmod()
  main()
