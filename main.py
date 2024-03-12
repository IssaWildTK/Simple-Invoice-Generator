import logging
from fpdf import FPDF
from pathlib import Path
import random
from modules.tax_calculator import TaxCalculator

# Configures logging to keep track of the application's operation and issues
Path("logs").mkdir(exist_ok=True)  # Ensures the logs directory exists
logging.basicConfig(filename='logs/invoice_generator.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - '
                                                                                      '%(message)s')


def main():
    # Logs the start of an invoice generation process
    logging.info("Invoice generation started.")

    # Generates a unique invoice number using a random number for simplicity
    invoice_no = f'GS-{random.randint(10001, 99999)}'

    # Collects customer information through user input, applying basic formatting
    customer_name = input("Enter Customer Name: ").title()
    customer_street = str(input("Enter Customer Street Address: ")).title()
    customer_city = input("Enter Customer City: ").capitalize()
    customer_state = input("Enter Customer State: ").upper()

    # Ensures the state abbreviation is valid
    if len(customer_state) != 2:
        raise ValueError("State must be a 2 character abbreviation.")

    # Safely attempts to collect a numerical zip code, repeating until successful
    while True:
        try:
            customer_zipcode = int(input("Enter Customer Zip Code: "))
            break  # Exits loop if input is successfully converted to an int
        except ValueError:
            print("Zip code must be a 5 digit number.")

    # Initializes an empty list to store item details
    items = []
    while True:
        # Collects item details from the user
        item_name = input("Enter Item Name: ")
        item_quantity = int(input("Enter Item Quantity: "))
        if item_quantity <= 0:
            logging.error("Quantity must be a positive integer.")
            continue

        item_price = float(input("Enter Item Price: "))
        if item_price <= 0:
            logging.error("Price must not be zero and must be positive.")
            continue

        # Appends item details to the items list
        items.append({"name": item_name, "quantity": item_quantity, "price": item_price})

        # Checks if the user wants to add more items
        choice = input("Do you want to add more items? (yes/no): ").lower()
        if choice == "no":
            break
        elif choice != "yes":
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue

    try:
        # Instantiates the InvoiceGenerator and generates the invoice
        invoice = InvoiceGenerator(invoice_no, customer_name, customer_street, customer_city, customer_state,
                                   customer_zipcode, items)
        invoice.generate_invoice()
    except Exception as e:
        # Handles any unexpected errors during the invoice generation
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred while generating the invoice: {e}")


class InvoiceGenerator:
    def __init__(self, invoice_no, customer_name, customer_street, customer_city, customer_state, customer_zipcode,
                 items):
        # Initializes invoice details and prepares for PDF generation
        self.invoice_no = invoice_no
        self.customer_name = customer_name
        self.customer_street = customer_street
        self.customer_city = customer_city
        self.customer_state = customer_state
        self.customer_zipcode = customer_zipcode
        self.items = items
        self.subtotal = 0
        self.total = 0
        self.pdf = FPDF()

    def generate_invoice(self):
        # Starts a new PDF page and sets up the invoice format
        self.pdf.add_page()
        self.pdf.image("logo.jpg", x=(210 - 40) / 2, y=8, w=40)

        self.pdf.ln(84)

        self.pdf.set_font("Arial", size=12)

        # Adds invoice details to the PDF
        details = [
            "Invoice", f"Invoice No: {self.invoice_no}", f"Customer Name: {self.customer_name}",
            f"Customer Street Address: {self.customer_street}", f"Customer City: {self.customer_city}",
            f"Customer State: {self.customer_state}", f"Customer Zip Code: {self.customer_zipcode}", "Items"
        ]
        for detail in details:
            self.pdf.cell(200, 10, txt=detail, ln=True, align="C")

        # Table headers
        self.pdf.set_font("Arial", 'B', 12)  # Set font to bold for headers
        self.pdf.cell(95, 10, "Item Name", border=1, align='C')
        self.pdf.cell(35, 10, "Quantity", border=1, align='C')
        self.pdf.cell(60, 10, "Price", border=1, ln=True, align='C')  # ln=True moves to the next line

        # Table rows
        self.pdf.set_font("Arial", size=12)  # Set font back to normal for table rows
        for item in self.items:
            self.pdf.cell(95, 10, item['name'], border=1, align='C')
            self.pdf.cell(35, 10, str(item['quantity']), border=1, align='C')
            self.pdf.cell(60, 10, f"${item['price']:.2f}", border=1, ln=True, align='C')

            # Subtotal, tax, and total
            self.pdf.cell(0, 10, "", ln=True)  # Add a blank line for spacing
            self.pdf.cell(130, 10, "Subtotal", border=1, align='C')
            self.pdf.cell(60, 10, f"${self.subtotal:.2f}", border=1, ln=True, align='C')
            self.subtotal += item['quantity'] * item['price']
            self.pdf.cell(130, 10, "Tax", border=1, align='C')
            tax = TaxCalculator(self.customer_state, self.subtotal).calculate_tax()
            self.pdf.cell(60, 10, f"${tax:.2f}", border=1, ln=True, align='C')
            self.total = self.subtotal + tax
            self.pdf.cell(130, 10, "Total", border=1, align='C')
            self.pdf.cell(60, 10, f"${self.total:.2f}", border=1, ln=True, align='C')

        # Prepares and saves the PDF file in a specified directory
        invoice_directory = Path(f"invoices/{self.invoice_no}")
        invoice_directory.mkdir(parents=True, exist_ok=True)
        pdf_file_path = invoice_directory / f"{self.invoice_no}.pdf"
        self.pdf.output(str(pdf_file_path))

        # Logs the outcome of the invoice generation process
        if pdf_file_path.is_file():
            logging.info(f"Invoice {self.invoice_no} generated successfully at {pdf_file_path}.")
        else:
            logging.error(f"Failed to generate invoice {self.invoice_no}.")
            raise Exception(f"Failed to generate invoice {self.invoice_no}. Please check the logs for more details.")


if __name__ == "__main__":
    main()
