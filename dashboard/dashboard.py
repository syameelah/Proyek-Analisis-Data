import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def load_data():
    df = pd.read_csv("all_data.csv")
    datetime_columns = ["dteday", "dteday"]
    df.sort_values(by="dteday", inplace=True)
    df.reset_index(inplace=True) 

    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column])

    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    with st.sidebar:
        st.image("https://drive.google.com/file/d/1e9T-F4Zcmi7Gqnw1Is3u2LAuSYYMy9uS/view?usp=drive_link")
        start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]
    return df




def create_plot(df, x_col, y_col, hue_col, palette):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=x_col, y=y_col, hue=hue_col, data=df, palette=palette, ax=ax)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    ax.set_title(f'Average {y_col} by {x_col} with {hue_col}')
    ax.set_xlabel(x_col)
    ax.set_ylabel(f'Average {y_col}')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def main():
    st.title('Bike Sharing Analysis Dashboard')

    bike_df = load_data()

    st.subheader('Data Overview')
    st.dataframe(bike_df)

    st.subheader('Average Counts by Day')
    create_plot(bike_df, x_col='holiday_day', y_col='cnt_day', hue_col='holiday_day', palette= 'coolwarm')

    st.subheader('Average Counts by Weather Conditions')
    create_plot(bike_df, x_col='workingday_day', y_col='cnt_day', hue_col='weather_conditions', palette= 'coolwarm')

    st.caption('copyright syameel.2024')

if __name__ == "__main__":
    main()