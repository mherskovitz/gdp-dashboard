import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_data():
    """Grab GDP and population data from CSV files."""

    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    POP_DATA_FILENAME = Path(__file__).parent/'data/population_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)
    raw_pop_df = pd.read_csv(POP_DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # Pivot GDP data
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Pivot population data
    pop_df = raw_pop_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'Population',
    )

    # Merge GDP and population data
    df = pd.merge(gdp_df, pop_df, on=['Country Code', 'Year'])

    # Calculate GDP per capita
    df['GDP per capita'] = df['GDP'] / df['Population']

    # Convert years from string to integers
    df['Year'] = pd.to_numeric(df['Year'])

    return df

df = get_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP per capita dashboard

Browse GDP per capita data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
''

min_value = df['Year'].min()
max_value = df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = df['Country Code'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

''
''
''

# Filter the data
filtered_df = df[
    (df['Country Code'].isin(selected_countries))
    & (df['Year'] <= to_year)
    & (from_year <= df['Year'])
]

st.header('GDP per capita over time', divider='gray')

''

st.line_chart(
    filtered_df,
    x='Year',
    y='GDP per capita',
    color='Country Code',
)

''
''

first_year = df[df['Year'] == from_year]
last_year = df[df['Year'] == to_year]

st.header(f'GDP per capita in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_gdp_pc = first_year[first_year['Country Code'] == country]['GDP per capita'].iat[0]
        last_gdp_pc = last_year[last_year['Country Code'] == country]['GDP per capita'].iat[0]

        if math.isnan(first_gdp_pc):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp_pc / first_gdp_pc:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} GDP per capita',
            value=f'{last_gdp_pc:,.0f}',
            delta=growth,
            delta_color=delta_color
        )


#In this code, `get_data` retrieves both GDP and population data, merges them, and calculates GDP per capita. The plotting logic is updated to display GDP per capita.
