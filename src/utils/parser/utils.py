import requests


class ParserUtils:
    @staticmethod
    def get_html(url):
        try:
            result = requests.get(url)
        except:
            return None
        return result.text
