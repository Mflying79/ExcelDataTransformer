import streamlit as st
import pandas as pd
import numpy as np
from transformations import apply_transformations
from utils import load_excel, save_excel
import io

def main():
    st.set_page_config(
        page_title="Excel Data Transformer",
        page_icon="📊",
        layout="wide"
    )

    st.title("Excel Data Transformer")
    st.write("Upload, transform, and download Excel data with ease")

    # File upload
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

    if uploaded_file is not None:
        try:
            # Load data
            df = load_excel(uploaded_file)
            
            # Store original dataframe in session state
            if 'original_df' not in st.session_state:
                st.session_state.original_df = df.copy()
            
            # Store current dataframe in session state
            if 'current_df' not in st.session_state:
                st.session_state.current_df = df.copy()

            # Display original data
            st.subheader("Original Data")
            st.dataframe(st.session_state.original_df)

            # Transformations section
            st.subheader("Data Transformations")

            with st.expander("Column Operations"):
                # Column renaming
                st.write("Rename Columns")
                cols = st.session_state.current_df.columns.tolist()
                col_to_rename = st.selectbox("Select column to rename", cols)
                new_name = st.text_input("Enter new name", col_to_rename)
                if st.button("Rename Column"):
                    st.session_state.current_df = st.session_state.current_df.rename(
                        columns={col_to_rename: new_name}
                    )

            with st.expander("Data Type Conversion"):
                # Data type conversion
                st.write("Convert Column Data Type")
                col_to_convert = st.selectbox("Select column to convert", 
                                            st.session_state.current_df.columns)
                dtype_choice = st.selectbox("Select new data type", 
                                          ['int', 'float', 'string', 'datetime'])
                if st.button("Convert Data Type"):
                    try:
                        st.session_state.current_df = apply_transformations(
                            st.session_state.current_df,
                            'convert_dtype',
                            col_to_convert,
                            dtype_choice
                        )
                    except Exception as e:
                        st.error(f"Error converting data type: {str(e)}")

            with st.expander("Filtering"):
                # Filtering
                st.write("Filter Data")
                filter_col = st.selectbox("Select column to filter", 
                                        st.session_state.current_df.columns)
                filter_value = st.text_input("Enter filter value")
                filter_operation = st.selectbox("Select filter operation", 
                                              ['equals', 'contains', 'greater_than', 'less_than'])
                if st.button("Apply Filter"):
                    try:
                        st.session_state.current_df = apply_transformations(
                            st.session_state.current_df,
                            'filter',
                            filter_col,
                            filter_value,
                            filter_operation
                        )
                    except Exception as e:
                        st.error(f"Error applying filter: {str(e)}")

            with st.expander("Aggregations"):
                # Aggregations
                st.write("Aggregate Data")
                agg_col = st.selectbox("Select column to aggregate", 
                                     st.session_state.current_df.columns)
                group_by_col = st.selectbox("Select column to group by", 
                                          st.session_state.current_df.columns)
                agg_operation = st.selectbox("Select aggregation operation", 
                                           ['sum', 'mean', 'count', 'max', 'min'])
                if st.button("Apply Aggregation"):
                    try:
                        st.session_state.current_df = apply_transformations(
                            st.session_state.current_df,
                            'aggregate',
                            agg_col,
                            group_by_col,
                            agg_operation
                        )
                    except Exception as e:
                        st.error(f"Error applying aggregation: {str(e)}")

            # Reset transformations
            if st.button("Reset Transformations"):
                st.session_state.current_df = st.session_state.original_df.copy()

            # Preview transformed data
            st.subheader("Transformed Data Preview")
            st.dataframe(st.session_state.current_df)

            # Download transformed data
            if st.button("Download Transformed Data"):
                try:
                    excel_data = save_excel(st.session_state.current_df)
                    st.download_button(
                        label="Click to Download",
                        data=excel_data,
                        file_name="transformed_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"Error preparing download: {str(e)}")

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
