import json
import random
import re

from requests_html import HTMLSession


HOST = "https://www.anibis.ch"


def get_response(url):
    user_agent_list = [
        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        # Firefox
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
    ]
    user_agent = random.choice(user_agent_list)
    headers = {"User-Agent": user_agent}
    session = HTMLSession()
    response = session.get(url.strip(), headers=headers)
    print(url.strip())
    return response


def parse(response):
    content = response.html.xpath(
        '//ul[@class="sc-1ovhdji-0 sc-177mb2p-0 jbsqEC kzlJDO"]//a/@href'
    )
    h1 = ''.join(response.html.xpath('//h1/text()'))
    h1 = re.search('.*in\s(.*)$', h1).group(1)
    if not content:
        content
    return content, h1


def get_absolute_url(href: str) -> str:
    return HOST + href if href.startswith("/") else href


def walk(url: str):
    result = {
        url: {'h1': '',
              'links': {}}
        }

    hrefs, h1 = parse(get_response(url))
    if len(hrefs) == 1:
        result[url]['h1'] = h1
        return result

    for href in hrefs:
        href_abs = get_absolute_url(href).lower()
        if url == href_abs:
            continue
        result[url]['h1'] = h1
        # result[url].update(walk(href_abs))
        result[url]['links'].update(walk(href_abs))


    return result


def main():
    urls = [
        "https://www.anibis.ch/de/c/haushalt-wohnen-badezimmer",

        # "https://www.anibis.ch/de/c/haushalt-wohnen",
        # "https://www.anibis.ch/de/c/handwerk-garten",
        # "https://www.anibis.ch/de/c/sport-freizeit",
        # "https://www.anibis.ch/de/c/kind-baby",
        # "https://www.anibis.ch/de/c/kleidung-accessoires",
    ]
    # result = {url: walk(url) for url in urls}
    result = {}
    for url in urls:
        result.update(walk(url))

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
