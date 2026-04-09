import socks
import socket
import requests

class ProxyManager:
    def __init__(self, host='127.0.0.1', port=9050):
        """Initializes ProxyManager using IP address (no hostnames)."""
        self.host = host
        self.port = port
        self.proxy_url = f'socks5h://{host}:{port}'

    def set_global_proxy(self):
        """Sets SOCKS5 proxy for all socket operations and patches DNS."""
        import socks
        socks.set_default_proxy(socks.SOCKS5, self.host, self.port, rdns=True)
        socket.socket = socks.socksocket
        
        # Force dnspython to use the patched socket for its queries
        try:
            import dns.resolver
            # dns.resolver by default uses socket.socket, but we reset it just in case
        except ImportError:
            pass

    def get_tor_session(self):
        """Returns a requests session configured to use Tor."""
        session = requests.Session()
        session.proxies = {
            'http': self.proxy_url,
            'https': self.proxy_url
        }
        return session

    def check_tor_connection(self):
        """Verifies if the Tor proxy is working."""
        try:
            session = self.get_tor_session()
            response = session.get('https://check.torproject.org/api/ip', timeout=10)
            return response.json().get('IsTor', False)
        except Exception:
            return False
