from schema import Schema, And

REQUEST_TRENDING_THREADS_FORM_SCHEMA = Schema(
    {'subreddits': And(And(str, error='subreddits should be a string'),
                       And(lambda s: True if s.strip() else False, error='subreddits should not be empty'))})
