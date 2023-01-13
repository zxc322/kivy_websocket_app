from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window

from config import FONT_SIZE, PAIRS, URL
from websocket_connection import WebsocketConnection


class Main(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ws_connection = WebsocketConnection()
        self.layout = GridLayout(cols=2, rows=3)
        self.coins_data = self.set_coins_data(pairs=PAIRS)
        Config.set('graphics', 'resizable', True)
        Config.set('graphics', 'width', '420')
        Config.set('graphics', 'height', '300')
        Config.write()
        Window.clearcolor = (25 / 255, 26 / 255, 28 / 255)

    def set_coins_data(self, pairs: list) -> dict:
        coins_data = {}
        for pair in pairs:
            coins_data[pair] = {
                'web_socket': self.ws_connection.connection(url=URL.format(pair)),
                'price': 0.0
            }
        return coins_data

    def build(self):
        Clock.schedule_interval(self._update, 1)
        return self._interface()

    def _interface(self):
        self.layout.add_widget(Label(text='BTC/USDT', font_size=FONT_SIZE))
        self.layout.add_widget(Label(text='0.0', font_size=FONT_SIZE))
        self.layout.add_widget(Label(text='ETH/USDT', font_size=FONT_SIZE))
        self.layout.add_widget(Label(text='0.0', font_size=FONT_SIZE))
        self.layout.add_widget(Label(text='BNB/USDT', font_size=FONT_SIZE))
        self.layout.add_widget(Label(text='0.0', font_size=FONT_SIZE))
        return self.layout

    def _update(self, *args):
        new_btc_price = self.get_new_price('btcusdt')
        new_eth_price = self.get_new_price('ethusdt')
        new_bnb_price = self.get_new_price('bnbusdt')

        # btc
        self.layout.children[4].color = self._set_color(
            old=float(self.layout.children[4].text),
            new=float(new_btc_price)
        )
        self.layout.children[4].text = str(new_btc_price)
        self.coins_data['btcusdt']['price'] = new_btc_price

        # eth
        self.layout.children[2].color = self._set_color(
            old=float(self.layout.children[2].text),
            new=float(new_eth_price)
        )
        self.layout.children[2].text = str(new_eth_price)
        self.coins_data['btcusdt']['price'] = new_eth_price

        # bnb
        self.layout.children[0].color = self._set_color(
            old=float(self.layout.children[0].text),
            new=float(new_bnb_price)
        )
        self.layout.children[0].text = str(new_bnb_price)
        self.coins_data['btcusdt']['price'] = new_bnb_price

    def retry_connection(self, pair: str) -> None:
        self.coins_data[pair]['web_socket'] = self.ws_connection.connection(url=URL.format(pair))

    def get_new_price(self, pair) -> float:
        price = self.ws_connection.get_price(self.coins_data[pair]['web_socket'])
        if not price:
            self.retry_connection(pair)
        return price

    @staticmethod
    def _set_color(old: float, new: float) -> tuple:
        green = 0, 1, 0, 1
        red = 1, 0, 0, 1
        white = 1, 1, 1, 1

        if new > old:
            return green
        elif old > new:
            return red
        else:
            return white


if __name__ == '__main__':
    app = Main()
    app.run()
    # Closing connections
    active_connections = [app.coins_data[pair]['web_socket'] for pair in app.coins_data]
    for web_socket in active_connections:
        app.ws_connection.close_connection(web_socket)