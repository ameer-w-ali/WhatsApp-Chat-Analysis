import streamlit as st
import preprocessor
import helper

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
	bytes_data = uploaded_file.getvalue()
	data = bytes_data.decode('utf-8')
	df = preprocessor.preprocess(data)
	st.dataframe(df)
	users = df['Sender'].unique().tolist()
	users.remove('System')
	users.sort()
	users.insert(0,"Overall")
	selected_user = st.sidebar.selectbox("Show Analysis wrt",users)
	if st.sidebar.button("Run Analysis"):

		messages,words,media,links = helper.fetch_stats(selected_user,df)
		col1,col2,col3,col4 = st.columns(4)

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

		if selected_user == 'Overall':
			st.title('Most Active Users')
			st.pyplot(helper.active_users(df))
			st.pyplot(helper.Cloud(df))
			col1,col2= st.columns(2)
			with col1:
				st.table(helper.Common(df))

