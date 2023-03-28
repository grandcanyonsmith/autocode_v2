
# New Python Script

## Introduction
This script is used to calculate the total cost of a purchase.

## Variables
`item_cost`: Stores the cost of each item in the purchase.

`quantity`: Stores the number of items purchased.

`tax_rate`: Stores the tax rate for the purchase.

`total_cost`: Stores the total cost of the purchase.

## Functions
`calculate_total_cost()`: Calculates the total cost of the purchase.

## Main Program
```
# Get the cost of each item
item_cost = float(input("Enter the cost of each item: "))

# Get the number of items purchased
quantity = int(input("Enter the number of items purchased: "))

# Get the tax rate
tax_rate = float(input("Enter the tax rate: "))

# Calculate the total cost
total_cost = calculate_total_cost(item_cost, quantity, tax_rate)

# Print the total cost
print("The total cost of the purchase is:", total_cost)
```

## Function Definition
```
def calculate_total_cost(item_cost, quantity, tax_rate):
    """Calculates the total cost of the purchase.

    Args:
        item_cost (float): The cost of each item.
        quantity (int): The number of items purchased.
        tax_rate (float): The tax rate for the purchase.

    Returns:
        float: The total cost of the purchase.
    """

    # Calculate the subtotal
    subtotal = item_cost * quantity

    # Calculate the tax
    tax = subtotal * tax_rate

    # Calculate the total cost
    total_cost = subtotal + tax

    # Return the total cost
    return total_cost
```