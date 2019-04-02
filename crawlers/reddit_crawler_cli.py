import json

import click
import requests

_APPLICATION_ADDRESS = 'https://0.0.0.0:8181'

# ToDo: make application address an env variable


@click.command()
@click.option('--subreddits', required=True, help='A list of subreddits separated by ;')
def _get_subreddits_trending_threads_command(subreddits: str):
    """
    This function constructs a CLI command which will request the trending threads of a list of subreddits,
    and print the result to the console
    :param subreddits: a list os subreddits in the form 'subreddit_1;subreddit_2;...;subreddit_n'
    """

    endpoint = 'subreddits_trending_threads'

    url = f'{_APPLICATION_ADDRESS}/{endpoint}'

    payload = json.dumps({"subreddits": subreddits})

    headers = {
        "content-type": "application/json",
        "cache-control": "no-cache"
    }

    response = requests.get(url=url, data=payload, headers=headers, verify=False)

    response_dict = json.loads(response.text)

    if 'error' in response_dict:
        print(f"ERROR: {response_dict['error']}")
    else:
        print(_prettify_response(response_dict))


def _prettify_response(response_dict: dict):
    """
    This function takes the text of the request response of _get_subreddits_trending_threads_command
    and makes it 'pretty' to be printed
    :param response_dict: request response of _get_subreddits_trending_threads_command
    :return: a pretty_response
    """

    subreddits_dict = response_dict['existent_subreddits']
    pretty_response = []
    non_trending_threads_subreddits = []
    for subreddit, trending_threads in subreddits_dict.items():
        pretty_response.append('*'*80)
        pretty_response.append(f'Subreddit: {subreddit}')
        if trending_threads:
            for thread in trending_threads:
                pretty_response.append('-'*80)
                pretty_response.append(f"Thread: {thread['title']}")
                pretty_response.append(f"Link: {thread['link']}")
                pretty_response.append(f"Comments link: {thread['comments_link']}")
                pretty_response.append(f"Upvotes: {thread['upvotes']}")
        else:
            non_trending_threads_subreddits.append(f'NON TRENDING THREADS FOR: {subreddit}')
    non_existent_subreddits = response_dict['nonexistent_subreddits']
    for non_existent_subreddit in non_existent_subreddits:
        pretty_response.append('*'*80)
        pretty_response.append(f"The {non_existent_subreddit} subreddit doesn't exist.")
    return '\n'.join(pretty_response)


if __name__ == '__main__':
    _get_subreddits_trending_threads_command()
