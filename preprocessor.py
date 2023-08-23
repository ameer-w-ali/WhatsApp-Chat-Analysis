import pandas as pd

def preprocess(data):
	content = data.split('\n')
	senders = []
	messages = []
	dates = []

	current_message = None
	for line in content:
			parts = line.split(' - ')
			
			if len(parts) == 2:
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
		'Date': dates
	}

	df = pd.DataFrame(chat_data)
	# if any("am" in time or "pm" in time for time in df['Date']):
	# 	time_format = '%d/%m/%y, %I:%M %p'
	# else:
	# 	time_format = '%d/%m/%y, %H:%M'

	df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y, %H:%M')
	df['Year'] = df['Date'].dt.year
	df['Month'] = df['Date'].dt.month_name()
	df['Day'] = df['Date'].dt.day
	df['Hour'] = df['Date'].dt.hour
	df['Minutes'] = df['Date'].dt.minute
	df.drop(['Date'], axis=1, inplace=True)

	return df