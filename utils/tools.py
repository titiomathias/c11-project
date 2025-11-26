
def preprocess_data(df):
    df = df.dropna()

    df['Year'] = df['Year'].astype(int)
    df['Financial Loss (in Million $)'] = df['Financial Loss (in Million $)'].astype(float)
    df['Number of Affected Users'] = df['Number of Affected Users'].astype(int)
    df['Incident Resolution Time (in Hours)'] = df['Incident Resolution Time (in Hours)'].astype(int)

    return df


