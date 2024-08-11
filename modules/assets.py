class AssetManager:
    def __init__(self):
        # Listado de activos por categoría como atributos, en formato de diccionario
        self.CURRENCIES = {
            'USD/BRL': 'BRL=X',
            'EUR/USD': 'EURUSD=X',
            'GBP/USD': 'GBPUSD=X',
            'JPY/USD': 'JPYUSD=X'
        }
        self.CRYPTO = {
            'Bitcoin USD': 'BTC-USD',
            'Ethereum USD': 'ETH-USD',
            'Binance Coin USD': 'BNB-USD',
            'Solana USD': 'SOL-USD',
            'Cardano USD': 'ADA-USD',
            'XRP USD': 'XRP-USD'
        }
        self.B3_STOCKS = {
            'Petrobras': 'PETR4',
            'Vale': 'VALE3',
            'Itau Unibanco': 'ITUB4',
            'Bradesco': 'BBDC4',
            'Ambev': 'ABEV3'
        }
        self.SP500 = {
            'Apple': 'AAPL',
            'Microsoft': 'MSFT',
            'Google': 'GOOGL',
            'Amazon': 'AMZN',
            'Tesla': 'TSLA'
        }
        self.NASDAQ100 = {
            'Nvidia': 'NVDA',
            'Facebook': 'FB',
            'Adobe': 'ADBE',
            'Netflix': 'NFLX',
            'PayPal': 'PYPL'
        }
        self.INDEXES = {
            'S&P 500': 'SPX',
            'Dow Jones': 'DJI',
            'NASDAQ 100': 'NDX',
            'Ibovespa': 'IBOV',
            'DAX': 'DAX'
        }

    def get_assets(self, category):
        # Devuelve los activos de una categoría específica
        return getattr(self, category.upper(), {})

    def list_categories(self):
        # Lista todas las categorías disponibles
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]