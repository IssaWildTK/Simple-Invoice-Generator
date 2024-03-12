import pandas as pd
from pathlib import Path
import logging


class TaxCalculator:
    def __init__(self, state, subtotal):
        self.state = state
        self.subtotal = subtotal
        self.tax = 0

    def calculate_tax(self):
        module_dir = Path(__file__).parent
        tax_rates_path = module_dir / "tax_rates.csv"

        try:
            tax_rates = pd.read_csv(tax_rates_path)
            percentage_columns = ['State Tax Rate', 'Avg. Local Tax Rate', 'Combined Rate', 'Max Local Tax Rate']
            for col in percentage_columns:
                tax_rates[col] = tax_rates[col].str.replace('"', '').str.strip().str.rstrip('%').str.strip().astype(
                    'float')
            tax_rate = tax_rates.loc[tax_rates["Abbrv"].str.upper() == self.state.upper(), "State Tax Rate"]

            if not tax_rate.empty:
                # Calculate tax and round to two decimal places
                self.tax = round(self.subtotal * (tax_rate.iloc[0] / 100), 2)
            else:
                logging.error(f"No tax rate found for state {self.state}.")
                raise Exception(f"No tax rate found for state {self.state}.")
            return self.tax
        except Exception as e:
            logging.error(f"An error occurred while calculating tax: {e}")
            raise


if __name__ == "__main__":
    tax_calculator = TaxCalculator("CA", 100)
    tax = tax_calculator.calculate_tax()
    print(tax)
