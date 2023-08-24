import pandas as pd
import re


def preprocess(data):
	content = data.split('\n')
	senders = []
	messages = []
	dates = []

	current_message = None
	for line in content:
		parts = line.split(' - ')

		if len(parts) == 2 and re.match(r"^\d{2}/\d{2}/\d{4}", parts[0]):
			if current_message:
				if messages:
					messages[-1] = messages[-1] + '\n' + current_message
				else:
					messages.append(current_message)
				current_message = None

			date_time, rest = parts[0], parts[1]

			try:
				sender, message = rest.split(': ', 1)
				dates.append(date_time)
				senders.append(sender)
				messages.append(message)
			except ValueError:
				sender = 'System'
				message = rest
				dates.append(date_time)
				senders.append(sender)
				messages.append(message)
		else:
			if current_message:
				current_message += '\n' + line.strip()
			else:
				current_message = line.strip()

	if current_message:
		if messages:
			messages[-1] = messages[-1] + '\n' + current_message
		else:
			messages.append(current_message)

	chat_data = {
		'Sender': senders,
		'Message': messages,
		'Dates': dates
	}

	df = pd.DataFrame(chat_data)

	df['Dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y, %I:%M %p')
	df['Year'] = df['Dates'].dt.year
	df['Month'] = df['Dates'].dt.month_name()
	df['Day'] = df['Dates'].dt.day
	df['Date'] = df['Dates'].dt.date
	df['Hour'] = df['Dates'].dt.hour
	df['Minutes'] = df['Dates'].dt.minute
	df['Month_Num'] = df['Dates'].dt.month
	df.drop(['Dates'], axis=1, inplace=True)

	return df
