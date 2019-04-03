import json
import time
import requests

from telegram.ext import Updater, CommandHandler

_APPLICATION_ADDRESS = 'https://0.0.0.0:8181'
#Todo: logging


def get_trending_threads_reddit(bot, update, args):
    subreddits = args[0]
    chat_id = update.message.chat_id

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
        text = f"ERROR: {response_dict['error']}"
        bot.send_message(chat_id=chat_id, text=text)
    else:
        messages = _prettify_responses(response_dict)
        for message in messages:
            bot.send_message(chat_id=chat_id, text=message)
            time.sleep(2)


def _prettify_responses(response_dict: dict):
    """
    This function takes the text of the request response of _get_subreddits_trending_threads_command
    and makes it 'pretty' to be printed
    :param response_dict: request response of _get_subreddits_trending_threads_command
    :return: a pretty_response
    """

    subreddits_dict = response_dict['existent_subreddits']
    pretty_responses = []
    non_trending_threads_subreddits = []
    for subreddit, trending_threads in subreddits_dict.items():
        if trending_threads:
            for thread in trending_threads:
                pretty_response = ''
                pretty_response = f"{pretty_response} Subreddit: {thread['subreddit']}\n"
                pretty_response = f"{pretty_response}Thread: {thread['title']}\n"
                pretty_response = f"{pretty_response}Link: {thread['link']}\n"
                pretty_response = f"{pretty_response}Comments link: {thread['comments_link']}\n"
                pretty_response = f"{pretty_response}Upvotes: {thread['upvotes']}"
                pretty_responses.append(pretty_response)
        else:
            non_trending_threads_subreddits.append(subreddit)
    pretty_responses.extend([f'NO TRENDING THREADS FOR: {non_trending_threads}'
                             for non_trending_threads in non_trending_threads_subreddits])
    non_existent_subreddits = response_dict['nonexistent_subreddits']
    for non_existent_subreddit in non_existent_subreddits:
        pretty_responses.append(f"The {non_existent_subreddit} subreddit doesn't exist.")
    return pretty_responses


def main():
    updater = Updater('')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('NadaPraFazer', get_trending_threads_reddit, pass_args=True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print('The bot is up')
    main()
