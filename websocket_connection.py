import json
import websocket


class WebsocketConnection:

    @staticmethod
    def connection(url: str) -> websocket._core.WebSocket:
        web_socket = websocket.WebSocket()
        try:
            web_socket.connect(url)
            print(f'Connected: {web_socket}')
        except websocket.WebSocketAddressException as ex:
            print(ex)
        return web_socket

    @staticmethod
    def get_price(web_socket: websocket._core.WebSocket) -> float:
        try:
            message = json.loads(web_socket.recv())
            return float(message['data']['c'])
        except websocket.WebSocketConnectionClosedException:
            return 0.0

    @staticmethod
    def close_connection(web_socket: websocket._core.WebSocket) -> None:
        print(f'Closing: {web_socket}')
        web_socket.close()
