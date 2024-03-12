import pandas as pd
from pathlib import Path
import logging


class TaxCalculator:
    def __init__(self, state, subtotal):
        # Initialize the TaxCalculator with the state abbreviation and the subtotal amount
        self.state = state
        self.subtotal = subtotal
        self.tax = 0

    def calculate_tax(self):
        # Define the path to the tax rates CSV file, assumed to be in the same directory as this script
        module_dir = Path(__file__).parent
        tax_rates_path = module_dir / "tax_rates.csv"

        try:
            # Load tax rates from CSV, cleaning and converting percentage columns to float
            tax_rates = pd.read_csv(tax_rates_path)
            percentage_columns = ['State Tax Rate', 'Avg. Local Tax Rate', 'Combined Rate', 'Max Local Tax Rate']
            for col in percentage_columns:
                tax_rates[col] = tax_rates[col].str.replace('"', '').str.strip().str.rstrip('%').str.strip().astype(
                    'float')

            # Find the state's tax rate from the CSV
            tax_rate = tax_rates.loc[tax_rates["Abbrv"].str.upper() == self.state.upper(), "State Tax Rate"]

            if not tax_rate.empty:
                # Calculate and round the tax based on the state's tax rate and the subtotal
                self.tax = round(self.subtotal * (tax_rate.iloc[0] / 100), 2)
            else:
                # Log an error if no tax rate is found for the state
                logging.error(f"No tax rate found for state {self.state}.")
                raise Exception(f"No tax rate found for state {self.state}.")
            return self.tax
        except Exception as e:
            # Log and raise any errors encountered during the tax calculation process
            logging.error(f"An error occurred while calculating tax: {e}")
            raise


if __name__ == "__main__":
    # Example usage of the TaxCalculator
    tax_calculator = TaxCalculator("CA", 100)
    tax = tax_calculator.calculate_tax()
    print(f"The calculated tax is: {tax}")

