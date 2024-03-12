# Simple Invoice Generator
This Simple Invoice Generator is a Python-based tool designed to streamline the process of creating professional invoices for your business or personal use. Utilizing the power of the FPDF library, it generates PDF invoices that can be saved, printed, or emailed directly to your clients.

## Features
- Customizable Invoice Details: Easily input customer names, addresses, and itemized services or products with their prices and quantities.
-Automatic Calculations: The tool automatically calculates subtotal, taxes based on state, and totals, reducing manual calculation errors.
-PDF Generation: Generates a clean, professional-looking PDF invoice that can be saved to your device.
-Unique Invoice Numbers: Automatically generates a unique invoice number for every new invoice, ensuring easy tracking.
-Error Handling and Logging: Robust error handling and logging mechanisms to troubleshoot potential issues during invoice generation.

## Prerequisites
Before you can run the Simple Invoice Generator, ensure you have the following installed:

Python 3.x
FPDF Python library
You can install FPDF using pip:

```
pip install fpdf
```
## Installation
To use the Simple Invoice Generator, follow these steps:

1. Clone this repository or download the ZIP to your local machine.
2. Navigate to the directory containing the invoice_generator.py file.
3. Ensure you have the required Python version and libraries installed.
## Usage
To generate an invoice, follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the directory where invoice_generator.py is located.
3. Run the script with Python:

```
python invoice_generator.py
```
1. Follow the on-screen prompts to enter customer details, items, prices, and quantities.
2. Upon completion, the script will generate a PDF invoice and save it to the specified directory.
## Customization
You can customize the invoice generator to fit your needs:

- Logo: Replace the logo.jpg file in the script's directory with your company logo.
- Tax Rates: Modify the modules/tax_calculator.py module to adjust tax rates or calculations based on your needs.
- Invoice Layout: Adjust the PDF layout and styles in the InvoiceGenerator class to match your branding.
## Contributing
Contributions to the Simple Invoice Generator are welcome! If you have suggestions for improvements or new features, feel free to create an issue or submit a pull request.

## License
This project is open-source and available under the MIT License.

## Contact
For questions or feedback, please contact Tom Gair at tomgair@gairanteedsolutions.com