import re


class UnitConverter:
    def __init__(self):
        self.conversion_rates = {
            "grams_to_ounces": 0.035274,
            "ounces_to_grams": 28.3495,
            "teaspoons_to_tablespoons": 0.333333,
            "tablespoons_to_teaspoons": 3,
            "cups_to_teaspoons": 48,
            "teaspoons_to_cups": 0.0208333,
            "cups_to_tablespoons": 16,
            "tablespoons_to_cups": 0.0625,
        }

    def convert_measurements_in_recipe(self, recipe, to_unit):
        conversions = [
            ("grams", "ounces", 0.035274),
            ("ounces", "grams", 28.3495),
            ("teaspoons", "tablespoons", 0.333333),
            ("tablespoons", "teaspoons", 3),
            ("cups", to_unit, 16),  # Convert "cups" to the provided to_unit
        ]

        for from_unit, dest_unit, conversion_rate in conversions:
            pattern = f"([0-9.]+) {from_unit}"
            replacement = lambda match: f"{float(match.group(1)) * conversion_rate} {dest_unit}"
            recipe = re.sub(pattern, replacement, recipe)

        return recipe