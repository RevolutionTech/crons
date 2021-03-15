import requests


class XKCDFetcher:

    API_URL = 'http://xkcd.com/info.0.json'

    SECTION_HTML_TEMPLATE = """
    <h3>Today\'s xkcd: {title}</h3>
    <img src=\"{img_url}\" />
    <br /><br />{img_alt}
    <br /><br /><hr />
    """
    SECTION_TEXT = "Visit xkcd.com to view today\'s xkcd\n"

    @classmethod
    def latest_xkcd(cls):
        response = requests.get(cls.API_URL).json()
        section_html = cls.SECTION_HTML_TEMPLATE.format(
            title=response['title'],
            img_url=response['img'],
            img_alt=response['alt'],
        )
        return section_html, cls.SECTION_TEXT
