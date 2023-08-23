import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def link_extractor(message):
  url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
  return url_pattern.findall(message)

def fetch_stats(selected_user,df):
  if selected_user == 'Overall':
    msg = df.shape[0]
    words = df['Message'].apply(lambda x: len(x.split())).sum()
    media = df[df['Message'].str.strip().str.lower().str.contains('<media omitted>', na=False)].shape[0]
    links =  df['Message'].apply(link_extractor).apply(len).sum()

  else:
    user = df[df['Sender']== selected_user]
    msg = user.shape[0]
    words = user['Message'].apply(lambda x: len(x.split())).sum()
    media = user[user['Message'].str.strip().str.lower().str.contains('<media omitted>', na=False)].shape[0]
    links =  user['Message'].apply(link_extractor).apply(len).sum()
  return msg,words,media,links

def active_users(df):
  count = df['Sender'].value_counts()

  if 'System' in count.index:
    count = count.drop('System')

  fig, ax = plt.subplots(figsize=(10, 7))
  ax.pie(count.values, labels=count.index, autopct='%1.1f%%', startangle=90)

  return fig

def Cloud(df):
  text = ' '.join(df['Message']).replace("Media omitted", "")
  wc = WordCloud(background_color='white', width=800, height=800).generate(text)
  fig, ax = plt.subplots(figsize=(10, 10))
  ax.imshow(wc, interpolation='bilinear')
  ax.axis('off')
  return fig