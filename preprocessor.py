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

    if len(parts) == 2 and (re.match(r"^\d{2}/\d{2}/\d{4}", parts[0]) or re.match(r"^\d{2}/\d{2}/\d{2}", parts[0])):
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
  # if df['Dates'].str.contains(r"^\d{2}/\d{2}/\d{2}",na=False).any():
  #   if df['Dates'].str.contains(r"^\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m$",na=False).any():
  #     time_format = '%d/%m/%y, %I:%M %p'
  #   else:
  #     time_format = '%d/%m/%y, %H:%M'
  # else:
  #   if df['Dates'].str.contains(r"^\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[ap]m$",na=False).any():
  #     time_format = '%d/%m/%Y, %I:%M %p'
  #   else:
  #     time_format = '%d/%m/%Y, %H:%M'
  sample_date = df['Dates'].iloc[0]  # Take the first date as a sample

  time_format = (
    '%d/%m/%y, %I:%M %p' if re.match(r"^\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m$", sample_date) else
    ('%d/%m/%y, %H:%M' if re.match(r"^\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}$", sample_date) else
     ('%d/%m/%Y, %I:%M %p' if re.match(r"^\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[ap]m$", sample_date) else
      '%d/%m/%Y, %H:%M'))
)


  df['Dates'] = pd.to_datetime(df['Dates'], format=time_format)
  df['Year'] = df['Dates'].dt.year
  df['Month'] = df['Dates'].dt.month_name()
  df['Day'] = df['Dates'].dt.day
  df['Date'] = df['Dates'].dt.date
  df['Hour'] = df['Dates'].dt.hour
  df['Minutes'] = df['Dates'].dt.minute
  df['Month_Num'] = df['Dates'].dt.month
  df['Day_name'] = df['Dates'].dt.day_name()
  df.drop(['Dates'], axis=1, inplace=True)

  period = []
  for hour in df[['Day_name','Hour']]['Hour']:
    if hour==23:
      period.append(str(hour)+'-'+str('00'))
    elif hour==0:
      period.append(str('00')+'-'+str(hour+1))
    else:
      period.append(str(hour)+'-'+str(hour+1))
  df['period']=period

  return df
