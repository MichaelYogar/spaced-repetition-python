def drop_rows_by_filter(df, filter):
    """
    Removes rows with specific value in place
    :param df current Dataframe
    :param filter boolean vector
    """
    df.drop(df.index[filter], inplace = True)