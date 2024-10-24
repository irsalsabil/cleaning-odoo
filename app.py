import pandas as pd
import streamlit as st
import numpy as np

@st.cache_data(ttl=None)
def reading_data(uploaded_file):
    #df = pd.read_excel('data_odoo.xlsx')
    df = pd.read_excel(uploaded_file)
    df['unit_odoo'] = df['unit_odoo'].str.replace(r'\s*-\s*Sub\s*Division', ' Sub Division', regex=True)
    df['unit_odoo'] = df['unit_odoo'].str.replace('A/P Section', 'AP Section', regex=True)
    df['unit_odoo'] = df['unit_odoo'].str.replace('Make-Up Section', 'MakeUp Section', regex=True)
    return df

st.header("Data Cleaner", divider="violet")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:

    df = reading_data(uploaded_file)

    with st.expander('Original Data'):
        st.write(df)


    df['unit'] = np.where(
        df['unit_odoo'].str.contains(r'[/-]'),  # Check if there is either "/" or "-"
        df['unit_odoo'].str.extract(r'((?:GROUP OF|YAYASAN|CORPORATE)[^/-]+)', expand=False).str.strip(),  # Extract if either "/" or "-" is present
        df['unit_odoo'].str.strip()  # Keep original value and trim spaces if false
    )

    df['directorate'] = df['unit_odoo'].str.extract(r'((?:\w+\s+)*Directorate[^/-]*)', expand=False).str.strip().fillna('-')

    df['second_directorate'] = df['unit_odoo'].str.extract(r'((?:\w+\s+)*Directorate[^/-]*?)(?:.*?((?:\w+\s+)*Directorate[^/-]*?))', expand=False)[1].str.strip().fillna('-')

    df['subunit'] = np.where(
        df['directorate'] == '-', 
        df['unit_odoo'].str.extract(r'^(?:[^/-]+[/-]){2}\s*([^/-]+)', expand=False).str.strip(),  # Extract after the 2nd "/" or "-"
        np.nan  # Leave as NaN otherwise
    )
    df['subunit'] = df['subunit'].fillna('-')
    media_condition = (df['unit'] == 'GROUP OF MEDIA') & (~df['unit_odoo'].str.extract(r'^(?:[^/-]+[/-]){2}\s*([^/-]+)')[0].str.contains('Directorate', na=False))
    df.loc[media_condition, 'subunit'] = df['unit_odoo'].str.extract(r'^(?:[^/-]+[/-]){2}\s*([^/-]+)', expand=False).str.strip()

    df['division'] = df['unit_odoo'].str.extract(r'([^/-]+(?:\s&\s[^/-]+)*\s(?:Division|Div))', expand=False).str.strip().fillna('-')

    df['subdivision'] = df['unit_odoo'].str.extract(r'([^/-]*(?:Sub\s*Division)[^/-]*)', expand=False).str.strip().fillna('-')

    df['department'] = df['unit_odoo'].str.extract(r'([^/-]+(?:\s&\s[^/-]+)*\s(?:Department|Dept\.|DEPT))', expand=False).str.strip().fillna('-')

    df['section'] = df['unit_odoo'].str.extract(r'([^/-]+(?:\s&\s[^/-]+)*\s(?:Section|Sect))', expand=False).str.strip().fillna('-')

    df['faculty'] = df['unit_odoo'].str.extract(r'([^/-]+(?:\s&\s[^/-]+)*\s*Faculty[^/-]*)', expand=False).str.strip().fillna('-')

    df['program'] = np.where(
        df['unit'] == 'YAYASAN MULTIMEDIA NUSANTARA',
        df['unit_odoo'].str.extract(r'([^/-]+(?:\s&\s[^/-]+)*\s*Program[^/-]*)', expand=False).str.strip().fillna('-'),
        '-'
    )

    with st.expander('Download Cleanded Data'):
        st.write(df)

    st.header("Unique Values", divider="violet")

    with st.expander('Unique Units'):
        st.write(df['unit'].unique())

    with st.expander('Unique Directorates'):
        st.write(df['directorate'].unique())

    with st.expander('Unique Second Directorates'):
        st.write(df['second_directorate'].unique())

    with st.expander('Unique Subunits'):
        st.write(df['subunit'].unique())

    with st.expander('Unique Divisions'):
        st.write(df['division'].unique())

    with st.expander('Unique Subdivisions'):
        st.write(df['subdivision'].unique())

    with st.expander('Unique Departments'):
        st.write(df['department'].unique())

    with st.expander('Unique Sections'):
        st.write(df['section'].unique())

    with st.expander('Unique Faculties'):
        st.write(df['faculty'].unique())

    with st.expander('Unique Programs'):
        st.write(df['program'].unique())



