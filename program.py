import requests
import tkinter as tk
from tkinter import ttk, messagebox
import re

class RealTimeCurrencyConverter:
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        amount = round(amount * self.currencies[to_currency], 4)
        return amount

# Mapping currency codes to country and currency names with emojis (where possible)
currency_country_map = {
    "USD": "🇺🇸 USD – US Dollar",
    "INR": "🇮🇳 INR – Indian Rupee",
    "EUR": "🇪🇺 EUR – Euro",
    "GBP": "🇬🇧 GBP – British Pound",
    "JPY": "🇯🇵 JPY – Japanese Yen",
    "AUD": "🇦🇺 AUD – Australian Dollar",
    "CAD": "🇨🇦 CAD – Canadian Dollar",
    "CHF": "🇨🇭 CHF – Swiss Franc",
    "CNY": "🇨🇳 CNY – Chinese Yuan",
    "SGD": "🇸🇬 SGD – Singapore Dollar",
    "NZD": "🇳🇿 NZD – New Zealand Dollar",
    "KRW": "🇰🇷 KRW – South Korean Won",
    "THB": "🇹🇭 THB – Thai Baht",
    "SEK": "🇸🇪 SEK – Swedish Krona",
    # Only currencies with mappings are included
}

class App(tk.Tk):
    def __init__(self, converter):
        super().__init__()
        self.title('Currency Converter')
        self.geometry("550x300")
        self.resizable(False, False)
        self.currency_converter = converter

        tk.Label(self, text="Real-Time Currency Converter", font=('Arial', 16, 'bold'), fg='navy').pack(pady=10)
        tk.Label(self, text=f"Rates Date: {self.currency_converter.data['date']}", font=('Arial', 10)).pack(pady=5)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Generate dropdown values only for mapped currencies
        self.currency_display_list = []
        self.code_to_display = {}
        self.display_to_code = {}

        for code in currency_country_map.keys():
            display = currency_country_map[code]
            self.currency_display_list.append(display)
            self.code_to_display[code] = display
            self.display_to_code[display] = code

        # From currency
        tk.Label(input_frame, text="From:", font=('Arial', 12)).grid(row=0, column=0, padx=5, pady=5)
        self.from_currency_variable = tk.StringVar()
        from_default_display = self.code_to_display.get("INR")
        self.from_currency_variable.set(from_default_display)
        self.from_currency_dropdown = ttk.Combobox(input_frame, textvariable=self.from_currency_variable, values=self.currency_display_list, state='readonly', width=25)
        self.from_currency_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Amount entry
        tk.Label(input_frame, text="Amount:", font=('Arial', 12)).grid(row=0, column=2, padx=5, pady=5)
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = tk.Entry(input_frame, validate='key', validatecommand=valid, width=15, justify='center')
        self.amount_field.grid(row=0, column=3, padx=5, pady=5)

        # To currency
        tk.Label(input_frame, text="To:", font=('Arial', 12)).grid(row=1, column=0, padx=5, pady=5)
        self.to_currency_variable = tk.StringVar()
        to_default_display = self.code_to_display.get("USD")
        self.to_currency_variable.set(to_default_display)
        self.to_currency_dropdown = ttk.Combobox(input_frame, textvariable=self.to_currency_variable, values=self.currency_display_list, state='readonly', width=25)
        self.to_currency_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Convert button
        tk.Button(self, text="Convert", font=('Arial', 12, 'bold'), bg='lightblue', command=self.perform).pack(pady=10)

        # Result label
        self.result_label = tk.Label(self, text="", font=('Arial', 14), fg='green')
        self.result_label.pack(pady=5)

    def perform(self):
        try:
            amount = float(self.amount_field.get())
            from_display = self.from_currency_variable.get()
            to_display = self.to_currency_variable.get()

            from_curr = self.display_to_code[from_display]
            to_curr = self.display_to_code[to_display]

            converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
            self.result_label.config(text=f"{amount} {from_curr} = {converted_amount} {to_curr}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")

    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9]*?(\.)?[0-9]*$")
        result = regex.match(string)
        return string == "" or (string.count('.') <= 1 and result is not None)

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    app = App(converter)
    app.mainloop()
