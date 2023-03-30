
## Introduction
This script is used to calculate the total cost of a purchase.

## Variables
`item_cost`: Stores the cost of each item in the purchase.

`quantity`: Stores the number of items purchased.

`tax_rate`: Stores the tax rate for the purchase.

`total_cost`: Stores the total cost of the purchase.

## Functions
`calculate_total_cost()`: Calculates the total cost of the purchase.

`main()`: Contains the main program logic.

## Main Program
```
def main():
    try:
        # Get the cost of each item
        while True:
            try:
                item_cost = float(input("Enter the cost of each item: "))
                if item_cost > 0:
                    break
                else:
                    print("Please enter a valid cost greater than 0.")
            except ValueError:
                print("Please enter a valid cost.")
            logging.info("User entered item cost: %s", item_cost)

        # Get the number of items purchased
        while True:
            try:
                quantity = int(input("Enter the number of items purchased: "))
                if quantity > 0:
                    break
                else:
                    print("Please enter a valid quantity greater than 0.")
            except ValueError:
                print("Please enter a valid quantity.")
            logging.info("User entered quantity: %s", quantity)

        # Get the tax rate
        while True:
            try:
                tax_rate = float(input("Enter the tax rate: "))
                if tax_rate >= 0:
                    break
                else:
                    print("Please enter a valid tax rate greater than or equal to 0.")
            except ValueError:
                print("Please enter a valid tax rate.")
            logging.info("User entered tax rate: %s", tax_rate)

        # Log the inputs
        logging.info("Calculating total cost with item cost: %s, quantity: %s, and tax rate: %s", item_cost, quantity, tax_rate)

        # Calculate the total cost
        try:
            total_cost = calculate_total_cost(item_cost, quantity, tax_rate)
        except Exception as e:
            logging.error("Error calculating total cost: %s", e)
            sys.exit(1)

        # Log the total cost
        logging.info("The total cost of the purchase is: %s", total_cost)

        # Print the total cost
        print("The total cost of the purchase is:", total_cost)
    except Exception as e:
        logging.error("Error in main(): %s", e)
        sys.exit(1)

```

## Function Definition
```
def calculate_total_cost(item_cost, quantity, tax_rate):
    """Calculates the total cost of the purchase.

    This function takes in the cost of each item, the number of items purchased, and the tax rate for the purchase. It then calculates the subtotal, tax, and total cost of the purchase.

    Args:
        item_cost (float): The cost of each item.
        quantity (int): The number of items purchased.
        tax_rate (float): The tax rate for the purchase.

    Returns:
        float: The total cost of the purchase.
    """

    try:
        # Calculate the subtotal
        subtotal = item_cost * quantity
        logging.info("Calculated subtotal: %s", subtotal)

        # Calculate the tax
        tax = subtotal * tax_rate
        logging.info("Calculated tax: %s", tax)

        # Calculate the total cost
        total_cost = subtotal + tax
        logging.info("Calculated total cost: %s", total_cost)

        # Return the total cost
        return total_cost
    except Exception as e:
        logging.error("Error calculating total cost: %s", e)
        raise

if __name__ == "__main__":
    main()
```