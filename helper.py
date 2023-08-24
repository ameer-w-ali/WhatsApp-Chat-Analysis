import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
from collections import Counter
import emoji


def link_extractor(message):
	url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	return url_pattern.findall(message)


def fetch_stats(selected_user, df):
	if selected_user == 'Overall':
		msg = df.shape[0]
		words = df['Message'].apply(lambda x: len(x.split())).sum()
		media = df[df['Message'].str.strip().str.lower().str.contains(
			'<media omitted>', na=False)].shape[0]
		links = df['Message'].apply(link_extractor).apply(len).sum()

	else:
		user = df[df['Sender'] == selected_user]
		msg = user.shape[0]
		words = user['Message'].apply(lambda x: len(x.split())).sum()
		media = user[user['Message'].str.strip().str.lower(
		).str.contains('<media omitted>', na=False)].shape[0]
		links = user['Message'].apply(link_extractor).apply(len).sum()
	return msg, words, media, links


def active_users(df):
	count = df['Sender'].value_counts()

	if 'System' in count.index:
		count = count.drop('System')

	prcnt = round((count / count.sum()) * 100, 2)
	contribution = pd.DataFrame({
		'User': count.index,
		'Messages': count.values,
		'Contribution(%)': prcnt.values
	})

	if len(count) > 10:
		count = count.head(10)

	fig, ax = plt.subplots()
	ax.pie(count.values, labels=count.index, autopct='%1.1f%%', startangle=90)

	return fig, contribution


def Cloud(df, selected_user):
	with open('stop_hinglish.txt', 'r') as f:
		stop_hinglish = set(f.read().splitlines())

	stopwords = STOPWORDS.union(stop_hinglish)

	if selected_user == "Overall":
		user = df[df['Sender'] != 'System']
	else:
		user = df[df['Sender'] == selected_user]

	text = ' '.join(user['Message']).replace(
		"<Media omitted>", "").replace("This message was deleted", "")

	wc = WordCloud(background_color='white', width=1600, height=800, stopwords=stopwords).generate(text)

	fig, ax = plt.subplots(figsize=(10, 10))
	ax.imshow(wc, interpolation='bilinear')
	ax.axis('off')
	return fig


def Common(df, selected_user):

	with open('stop_hinglish.txt', 'r') as f:
		stop_hinglish = set(f.read().splitlines())

	if selected_user == "Overall":
		user = df[df['Sender'] != 'System']
	else:
		user = df[df['Sender'] == selected_user]

	text = ' '.join(user['Message']).replace("<Media omitted>", "").replace(
		"This message was deleted", "").lower()
	words = text.split()
	words = [word for word in words if word not in stop_hinglish]
	counts = Counter(words).most_common(20)
	words, word_counts = zip(*counts)

	fig, ax = plt.subplots(figsize=(10, 8))
	ax.barh(words, word_counts, color='skyblue')
	ax.set_xlabel('Count')
	ax.set_title('Top 20 Common Words')
	ax.invert_yaxis()

	return fig


def emojis(df, selected_user):
	if selected_user == "Overall":
		user = df[df['Sender'] != 'System']
	else:
		user = df[df['Sender'] == selected_user]

	emoji_list = []
	for message in user['Message']:
		emoji_list.extend([emoji.emojize(e) for e in message if emoji.emoji_count(e)])

	counts = Counter(emoji_list).most_common(10)
	counts_df = pd.DataFrame(counts, columns=['Emoji', 'Counts'])
	counts_df = counts_df.astype({'Emoji': str, 'Counts': int})
	fig, ax = plt.subplots()
	ax.pie(counts_df['Counts'], labels=counts_df['Emoji'], startangle=90, autopct='%1.1f%%')
	ax.set_title('Emoji Distribution')

	return fig, counts_df

def monthly_timeline(df,selected_user):
	if selected_user == "Overall":
		user = df[df['Sender'] != 'System']
	else:
		user = df[df['Sender'] == selected_user]

	timeline = user.groupby(['Year','Month_Num','Month']).count()['Message'].reset_index()

	time = []
	for i in range(timeline.shape[0]):
		time.append(timeline['Month'][i]+"-"+str(timeline['Year'][i]))
	timeline["Time"] = time
	fig,ax = plt.subplots()
	ax.plot(timeline['Time'],timeline['Message'])
	ax.set_xticklabels(timeline['Time'], rotation=45, ha='right')
	return fig

def daily_timeline(df,selected_user):
	if selected_user == "Overall":
		user = df[df['Sender'] != 'System']
	else:
		user = df[df['Sender'] == selected_user]

	timeline = user.groupby('Date').count()['Message'].reset_index()

	time = []
	fig,ax = plt.subplots(figsize=(15,10))
	ax.plot(timeline['Date'],timeline['Message'])
	ax.set_xticklabels(timeline['Date'], rotation=45, ha='right')
	return fig