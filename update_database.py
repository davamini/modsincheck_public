import pandas as pd
import praw
import datetime
import sqlite3
import json
from sqlalchemy import create_engine
import time

file = open("config.json")
config_data = json.load(file)
file.close()

reddit = praw.Reddit(client_id=config_data["client_id"],
                     client_secret= config_data["client_secret"], password=config_data["password"],
                     user_agent=config_data["user_agent"], username=config_data["username"])

def change_column_name(df, old_name, new_name):
    """
    Changes old_name for column to new_name.
    """
    curr_column = df[old_name]
    index = df.columns.tolist().index(old_name)
    df.drop(old_name, axis=1, inplace=True)
    df.insert(index, new_name, curr_column)
    
def get_moderators(subreddit):
        """
        Gets the moderators' usernames
        from a given subreddit.
        """
        mods = []
        for moderator in reddit.subreddit(subreddit).moderator():
            mods.append(moderator)
        return mods


def get_data_comment_dict(mod_comments):
    """
    Uses a list of comment objects to create a dictionary
    of dates and mod_comments.

    Args:
        mod_comments ([comment objects]): Comment objects from moderators

    Returns:
        [dict]: A dictionary of dates and lists of comments
    """
    date_comment_dict = dict()
    for comment in mod_comments:
        comment_date = datetime.datetime.utcfromtimestamp(comment.created_utc).date()
        if comment_date not in date_comment_dict.keys():
            date_comment_dict[comment_date] = [comment]
        else:
            date_comment_dict[comment_date].append(comment)
    
    return date_comment_dict


def create_entries(date_comment_dict, moderator, subreddit):
    """
    Creates entries for the database for every
    date in date_comment_dict. Uses date_comment_dict 
    to calculate removal_count through summing the 
    total removals within ninety days prior to the comment.

    Args:
        date_comment_dict ([dict]): A dictionary of dates and lists of comments
        moderator ([moderator object]): A moderator object
        subreddit ([str]): The initial subreddit the moderator is found in

    Returns:
        [list]: A list of dictionaries, i.e. entries that will be 
        entered into a DataFrame that will be inserted into the server.
    """
    entries = []
    ninety_days = (60*60*24*90)
    subreddits_moderated = [subreddit.display_name for subreddit in moderator.moderated()]
    account_created = datetime.datetime.utcfromtimestamp(moderator.created_utc).date()
    not_removal = set()
    is_removal = set()
    for date in date_comment_dict.keys():
        removal_count = 0
        date = time.mktime(date.timetuple())
        for other_date in date_comment_dict.keys():
            other_date = time.mktime(other_date.timetuple())
            if (date - other_date) < ninety_days and (date - other_date) > 0:
                curr_date = datetime.datetime.utcfromtimestamp(other_date)
                for comment in date_comment_dict[curr_date.date()]:
                    if (comment.id in is_removal) or ('remov' in comment.body) and (comment.id not in not_removal):
                        if comment.submission.selftext == '[removed]':
                            removal_count += 1
                            if comment.id not in is_removal:
                                is_removal.add(comment.id)
                        else:
                            not_removal.add(comment.id)
        entries.append({
                'name': moderator.name,
                'score': removal_count,
                'date': datetime.datetime.utcfromtimestamp(date).date(),
                'subreddit': subreddit,
                'subreddits_moderated': json.dumps(subreddits_moderated),
                'account_created': account_created
            })

    return entries
    

def get_latest_mod_data(subreddit):
    """
    Returns a dictionary of the latest data for mods based
    on days and comment_limit,

    Args:
        mods ([list]): A list of praw.models.Redditor objects
        days ([int]): The amount of days to go back for the comment query
        comment_limit ([int]): The limit for the comment query
    """
    print(f'Beginning update for {subreddit}')
    mods = get_moderators(subreddit=subreddit)
    entries = []
    for moderator in mods:
        print(f'\nGetting entries for {moderator.name}')
        mod_comments = list(moderator.comments.new(limit=None))

        date_comment_dict = get_data_comment_dict(mod_comments)
        entries += create_entries(date_comment_dict, moderator, subreddit)
        print(f"Got entries for {moderator.name}")
    print()     
    return entries


def insert_mod_data(db, table_name, mod_data):
    """
    Inserts a DataFrame of the mod_data into the
    sqlite server.

    Args:
        db ([str]): Database name
        table_name ([str]): The table name
        mod_data ([list]): A list of dictionaries of mod_data
    """
    sqliteConnection = sqlite3.connect(db)
    test = pd.DataFrame(mod_data)
    test.to_sql(f'{table_name}', con=sqliteConnection, if_exists='replace')


def get_subreddit_data(db, table_name):
    sqliteConnection = sqlite3.connect(db)
    mod_table = pd.read_sql(con=sqliteConnection, sql=f"Select * from {table_name}")
    subreddit_df = mod_table[['date', 'subreddit', 'score']].groupby(['date', 'subreddit']).sum().sort_values(by="date").reset_index()
    subreddit_df['subreddit'] = subreddit_df['subreddit'].apply(lambda x: x.lower())
    change_column_name(subreddit_df, 'subreddit', 'name')
    return subreddit_df

def insert_subreddit_df(db, table_name, subreddit_df):
    sqliteConnection = sqlite3.connect(db)
    subreddit_df.to_sql(table_name, con=sqliteConnection, if_exists="replace")


if __name__ == "__main__":
    """
    If directly called, update the sqlite server.
    """
    start = time.time()
    print("Updating table: mod_data")

    subreddit_file = open('subreddits.json')
    subreddits =  json.load(subreddit_file)
    subreddit_file.close()
    new_mod_data = []
    
    for subreddit in subreddits['subreddits']:
        new_mod_data += get_latest_mod_data(subreddit)

    insert_mod_data(db='db.sqlite3', table_name='mod_data', mod_data=new_mod_data)
    print(f"Updated mod_data, total time: {time.time() - start}")

    start = time.time()
    print(f"Updating subreddit_data")
    subreddit_df = get_subreddit_data(db='db.sqlite3', table_name="mod_data")
    insert_subreddit_df(db='db.sqlite3', table_name="subreddit_data", subreddit_df=subreddit_df)
    print(f"Updated subreddit_data, total time: {time.time() - start}")