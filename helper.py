import re


def link_extractor(message):
  url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
  return url_pattern.findall(message)

def fetch_stats(selected_user,df):
  if selected_user == 'Overall':
    msg = df.shape[0]
    words = df['Message'].apply(lambda x: len(x.split())).sum()
    media =  df[df['Message'] == '<Media omitted>'].shape[0]
    links =  df['Message'].apply(link_extractor).apply(len).sum()

  else:
    user = df[df['Sender']== selected_user]
    msg = user.shape[0]
    words = user['Message'].apply(lambda x: len(x.split())).sum()
    media =  user[user['Message'] == '<Media omitted>'].shape[0]
    links =  user['Message'].apply(link_extractor).apply(len).sum()
  return msg,words,media,links

