from pshipper.wiki.client import Client

def get_wiki_text(editor: Client, page):
    return editor.get_page_text(page)


