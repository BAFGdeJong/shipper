import os

from dotenv import load_dotenv

from pshipper.wiki.client import Client


class Login:
    @staticmethod
    def env() -> Client | None:
        load_dotenv()
        username = os.getenv("WIKI_USERNAME")
        password = os.getenv("WIKI_PASSWORD")

        if not username or not password:
            print("Error: WIKI_USERNAME or WIKI_PASSWORD not found in .env")
            return None

        return Client(username, password)

