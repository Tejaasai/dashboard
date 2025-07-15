import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.title('My First Dashboard')

file_upload = st.file_uploader('Upload CSV file', type='csv')

if file_upload is None:
    st.write('CSV file is not uploaded')
else:
    df = pd.read_csv(file_upload)
    st.subheader('Preview of the Data')
    st.dataframe(df)

    columns1 = df.columns.to_list()
    selected_column = st.sidebar.selectbox('Select the column to analyze', ['--select_columns--']+columns1)

    columns2=['name']
    x_variable=st.sidebar.selectbox('Select x variable',columns2)

    columns3=['price','discount','rating']
    y_variable=st.sidebar.selectbox('Select x variable',columns3)

    if y_variable == 'discount' and df[y_variable].dtype == object:
        df[y_variable] = df[y_variable].str.replace('%', '').astype(int)

        # Limit to top 10 products for better visibility
    df_sorted = df.sort_values(by=y_variable, ascending=False).head(10)


    st.subheader('Product analysis')
    fig=plt.figure(figsize=(12,6))
    barplot=sns.barplot(x=df_sorted[x_variable],y=df_sorted[y_variable])
    plt.xlabel('Product name')
    plt.ylabel(f'{y_variable}')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    tab1, tab2, tab3, tab4 = st.tabs(['Price Analysis', 'Wordcloud Analysis', 'Rating Analysis', 'Discount Analysis'])

    with tab1:
        if selected_column == 'price':
            st.subheader('Price Analysis')
            fig = plt.figure()
            sns.histplot(x=df[selected_column], kde=True, color='skyblue')
            plt.title('Histogram of Price')
            st.pyplot(fig)

            fig = plt.figure()
            sns.boxplot(x=df[selected_column], color='lightgreen')
            plt.title('Boxplot of Price')
            st.pyplot(fig)
        else:
            st.info('Please select the "price" column in the sidebar to view this tab.')

    with tab2:
        if selected_column == 'name':
            st.subheader('Wordcloud for Product Names')
            wordcloud = WordCloud(height=400, width=800, background_color='white').generate(' '.join(df[selected_column]))
            fig = plt.figure()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(fig)
        else:
            st.info('Please select the "name" column in the sidebar to view this tab.')

    with tab3:
        if selected_column == 'rating':
            st.subheader('Rating Analysis')
            fig = plt.figure()
            sns.countplot(x=df[selected_column], palette='viridis')
            plt.title('Count of Ratings')
            st.pyplot(fig)
        else:
            st.info('Please select the "rating" column in the sidebar to view this tab.')

    with tab4:
        if selected_column == 'discount':
            st.subheader('Top 10 Products with Highest Discount')
            # Convert discount string to int (remove %)
            df['discount'] = df['discount'].str.replace('%', '').astype(int)
            top_discounted = df.nlargest(10, 'discount')[['name', 'price', 'discount']]
            st.dataframe(top_discounted)
        else:
            st.info('Please select the "discount" column in the sidebar to view this tab.')
