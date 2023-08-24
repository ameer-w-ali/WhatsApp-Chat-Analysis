import streamlit as st
import preprocessor
import helper

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
	bytes_data = uploaded_file.getvalue()
	data = bytes_data.decode('utf-8')
	df = preprocessor.preprocess(data)
	# st.dataframe(df)
	users = df['Sender'].unique().tolist()
	users.remove('System')
	users.sort()
	users.insert(0, "Overall")
	selected_user = st.sidebar.selectbox("Show Analysis wrt", users)
	if st.sidebar.button("Run Analysis") or selected_user:

		messages, words, media, links = helper.fetch_stats(selected_user, df)
		col1, col2, col3, col4 = st.columns(4)

		with col1:
			st.header("Total Messages")
			st.title(messages)

		with col2:
			st.header("Word Count")
			st.title(words)

		with col3:
			st.header("Media Count")
			st.title(media)

		with col4:
			st.header("Links Count")
			st.title(links)


		st.title("Monthly Timeline")
		st.pyplot(helper.monthly_timeline(df,selected_user))

		st.title("Daily Timeline")
		st.pyplot(helper.daily_timeline(df,selected_user))

		st.markdown("<h1 align=center>Activity Map</h1>",
						unsafe_allow_html=True)

		col1,col2 = st.columns(2)
  		
		with col1:
			st.header('Most busy day')
			st.pyplot(helper.week_activity(df,selected_user))

		with col2:
			st.header('Most busy month')
			st.pyplot(helper.month_activity(df,selected_user))
   
		st.markdown("<h1 align=center>24/7 HeatMap</h1>",
						unsafe_allow_html=True)
		st.pyplot(helper.activity_heatmap(selected_user,df))
  
		if selected_user == 'Overall':
			st.markdown("<h1 align=center>Most Active Users</h1>",
						unsafe_allow_html=True)

			cont = st.container()
			col1, col2 = cont.columns(2)

			fig1, contribution = helper.active_users(df)

			with col1:
				col1.pyplot(fig1)

			with col2:
				col2.table(contribution)

		st.markdown("<h1 align=center>Most Used Words</h1>",
					unsafe_allow_html=True)
		st.pyplot(helper.Cloud(df, selected_user))
		st.pyplot(helper.Common(df, selected_user))

		st.markdown("<h1 align=center>Most Used Emojis</h1>",
					unsafe_allow_html=True)
		fig2, emojis = helper.emojis(df, selected_user)
		col1, col2 = st.columns(2)

		with col1:
			st.table(emojis)
		with col2:
			st.pyplot(fig2)
