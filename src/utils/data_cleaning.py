import re

def standardize_column_names(df):
    """
    Standardize column names to lowercase, replace spaces with underscores,
    and remove special characters.
    """
    def clean_column_name(name):
        # Convert to lowercase
        name = name.lower()
        # Replace spaces with underscores
        name = name.replace(' ', '_')
        # Remove special characters
        name = re.sub(r'[^\w\s]', '', name)
        return name

    df.columns = [clean_column_name(col) for col in df.columns]
    return df
