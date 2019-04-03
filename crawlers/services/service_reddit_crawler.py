import requests
from bs4 import BeautifulSoup

from crawlers.excepts.service_errors import InexistentSubRedditError

_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
_PARSER = 'html.parser'
_REDDIT = 'https://old.reddit.com'

# ToDo: create a function which will check if the page template is still the expected


def _get_thread_short_link(thread_comments_link: str):
    # ToDo: exception treatment try - except - raise unexpected schema error
    """
    This function receives a thread comments link, navigates through it's page and
    return the link from the original thread
    :param thread_comments_link: a thread comments link
    :return: a string - the short link to the thread
    """
    req_pg = requests.get(thread_comments_link, headers=_HEADERS)
    soup = BeautifulSoup(req_pg.text, _PARSER)
    thread_short_link = soup.find('input', id='shortlink-text')['value']

    return thread_short_link


def _get_thread_info(thread_html: str):
    # ToDo: calculate upvotes - try - except - raise unexpected schema error
    """
    This function gets the desired thread information
    :param thread_html: the html of the thread in the subreddit page
    :return: a dict with the desired thread information
    """
    thread_info = dict()
    thread_info['upvotes'] = int(thread_html['data-score'])
    thread_info['comments_link'] = f"{_REDDIT}{thread_html['data-permalink']}"
    thread_info['title'] = thread_html.find('p', class_='title').find('a').text
    thread_info['link'] = _get_thread_short_link(
        thread_comments_link=f"{_REDDIT}{thread_html['data-permalink']}")

    return thread_info


def subreddit_exists(soup_page: BeautifulSoup):
    """
    This function will check if a subreddit exists
    :param soup_page: a beautiful soup page
    :return: True if it exists, False otherwise
    """
    return soup_page.find('p', id='noresults') is None


def _get_sub_reddit_home_page(subreddit: str):
    """
    This function retrieves the subreddit home page
    :param subreddit: a subreddit
    :return: a BeautifulSoup page for the subreddit home page
    """
    subreddit_link = f'{_REDDIT}/r/{subreddit}/'
    req_page = requests.get(subreddit_link, headers=_HEADERS)
    soup = BeautifulSoup(req_page.text, _PARSER)
    if subreddit_exists(soup_page=soup):
        return soup
    else:
        raise InexistentSubRedditError(
            message=f"{subreddit} doesn't exist.")


def get_trending_threads_on_subreddit(sub_reddit: str):
    # ToDo: check if desired info are on link
    """
    This function will retrieve the trending threads of a given subreddit
    :param sub_reddit: a subreddit
    :return: a list of dicts (each one having information about the trending threads
    """
    subreddit_home_page = _get_sub_reddit_home_page(sub_reddit)
    trending_threads = []
    threads = subreddit_home_page.find('div', id='siteTable')

    for thread in threads:
        try:
            thread_score = int(thread['data-score'])
            if thread_score > 5000:
                thread_infos = _get_thread_info(thread)
                thread_infos['subreddit'] = sub_reddit
                trending_threads.append(thread_infos)
        except KeyError:
            pass

    return trending_threads
