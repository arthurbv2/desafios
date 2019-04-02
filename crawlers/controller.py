from crawlers.excepts.service_errors import InexistentSubRedditError
from crawlers.services.service_reddit_crawler import get_trending_threads_on_subreddit


def get_trending_threads_on_subreddits(subreddits: list):
    """
    This function calls the service reddit crawler in order to
    retrieve the trending threads of a list of subreddits
    :param subreddits: the list of subreddits
    :return: a dict with two elements
        - nonexistent_subreddits, which contains a list of inexistent sub_reddits
        - existent_sub_reddits, which contains a dict with {subreddit: list_trending_threads} format
    """
    subreddits_trends = dict()
    nonexistent_subreddits = list()
    for subreddit in subreddits:
        print(subreddit)
        try:
            subreddits_trends[subreddit] = get_trending_threads_on_subreddit(subreddit.strip())
        except InexistentSubRedditError:
            nonexistent_subreddits.append(subreddit)
    retrieved_info = {'nonexistent_subreddits': nonexistent_subreddits,
                      'existent_subreddits': subreddits_trends}
    return retrieved_info


