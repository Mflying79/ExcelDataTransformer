import pandas as pd
import numpy as np

def apply_transformations(df, operation, *args):
    """
    Apply various transformations to the dataframe
    """
    if operation == 'convert_dtype':
        return convert_dtype(df, *args)
    elif operation == 'filter':
        return apply_filter(df, *args)
    elif operation == 'aggregate':
        return apply_aggregation(df, *args)
    return df

def convert_dtype(df, column, dtype):
    """
    Convert column data type
    """
    df = df.copy()
    try:
        if dtype == 'int':
            df[column] = df[column].astype(int)
        elif dtype == 'float':
            df[column] = df[column].astype(float)
        elif dtype == 'string':
            df[column] = df[column].astype(str)
        elif dtype == 'datetime':
            df[column] = pd.to_datetime(df[column])
    except Exception as e:
        raise Exception(f"Could not convert {column} to {dtype}: {str(e)}")
    return df

def apply_filter(df, column, value, operation):
    """
    Apply filter to dataframe
    """
    df = df.copy()
    try:
        if operation == 'equals':
            return df[df[column] == value]
        elif operation == 'contains':
            return df[df[column].astype(str).str.contains(value, na=False)]
        elif operation == 'greater_than':
            return df[df[column] > float(value)]
        elif operation == 'less_than':
            return df[df[column] < float(value)]
    except Exception as e:
        raise Exception(f"Error applying filter: {str(e)}")
    return df

def apply_aggregation(df, agg_column, group_column, operation):
    """
    Apply aggregation to dataframe
    """
    try:
        grouped = df.groupby(group_column)
        if operation == 'sum':
            return grouped[agg_column].sum().reset_index()
        elif operation == 'mean':
            return grouped[agg_column].mean().reset_index()
        elif operation == 'count':
            return grouped[agg_column].count().reset_index()
        elif operation == 'max':
            return grouped[agg_column].max().reset_index()
        elif operation == 'min':
            return grouped[agg_column].min().reset_index()
    except Exception as e:
        raise Exception(f"Error applying aggregation: {str(e)}")
