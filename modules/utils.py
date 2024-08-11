
class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

class Resampler:
    def __init__(self):
        self.name_to_abbr = {
            "year end frequency": "A",
            "year start frequency": "AS",
            "business year end frequency": "BA",
            "business year start frequency": "BAS",
            "3 months frequency": "3M",
            "4 months frequency": "4M",
            "6 months frequency": "6M",
            "12 months frequency": "12M",
            "quarter end frequency": "Q",
            "business quarter end frequency": "BQ",
            "quarter start frequency": "QS",
            "business quarter start frequency": "BQS",
            "month end frequency": "M",
            "business month end frequency": "BM",
            "month start frequency": "MS",
            "business month start frequency": "BMS",
            "weekly frequency": "W",
            "calendar day frequency": "D"
        }
        self.abbr_to_name = {v: k for k, v in self.name_to_abbr.items()}

    def get_abbr(self, full_name: str) -> str:
        """Devuelve la abreviación correspondiente a un nombre completo."""
        return self.name_to_abbr.get(full_name, "")

    def get_full_name(self, abbr: str) -> str:
        """Devuelve el nombre completo correspondiente a una abreviación."""
        return self.abbr_to_name.get(abbr, "")
    