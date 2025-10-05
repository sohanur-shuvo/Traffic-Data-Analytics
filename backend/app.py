import streamlit as st
import pandas as pd
import numpy as np

st.title('Excel Sheet Analyzer')

uploaded_file = st.file_uploader('Upload your Excel file', type=['xlsx'])

data = None
if uploaded_file:
    data = pd.read_excel(uploaded_file, engine='openpyxl')
    
    # Use column C (Traffic Start TS) as the time column
    time_col = data.columns[2]  # Column C (index 2)
    
    # Convert to datetime
    data[time_col] = pd.to_datetime(data[time_col])
    
    # Extract date and time components
    data['Date'] = data[time_col].dt.date
    data['Time'] = data[time_col].dt.time
    data['Hour'] = data[time_col].dt.hour
    
    # Filter for 8am to 8pm only (8:00 AM to 8:00 PM, not 8:45 PM)
    data_filtered = data[(data['Hour'] >= 8) & (data['Hour'] < 20)]
    
    st.write('Preview of uploaded data (8am to 8pm only):')
    st.dataframe(data_filtered)

    # Show available dates
    available_dates = data_filtered['Date'].unique()
    st.write(f"Available dates: {available_dates}")
    
    # Date comparison section
    st.subheader("Date Comparison")
    
    if len(available_dates) >= 2:
        # Create two columns for date selection
        col1, col2 = st.columns(2)
        
        with col1:
            date1 = st.selectbox("Select First Date:", available_dates, key="date1")
        
        with col2:
            date2 = st.selectbox("Select Second Date:", available_dates, key="date2")
        
        if date1 and date2 and date1 != date2:
            # Get data for both dates (already filtered for 8am to 8pm)
            date1_filtered = data_filtered[data_filtered['Date'] == date1]
            date2_filtered = data_filtered[data_filtered['Date'] == date2]
            
            # Calculate totals for both dates
            date1_totals = date1_filtered.iloc[:, [4, 5]].sum()  # E, F (Customer In/Out)
            date2_totals = date2_filtered.iloc[:, [4, 5]].sum()  # E, F (Customer In/Out)
            
            # Create time-based comparison (15-minute intervals)
            # Merge data on time to compare same time slots
            date1_time = date1_filtered.iloc[:, [2, 4, 5]].copy()  # Time, Customer In, Customer Out
            date2_time = date2_filtered.iloc[:, [2, 4, 5]].copy()  # Time, Customer In, Customer Out
            
            # Create time range format (e.g., "8:00-8:15am")
            def format_time_range(time_series):
                time_ranges = []
                for time_val in time_series:
                    # Convert to time object if it's datetime
                    if hasattr(time_val, 'time'):
                        time_val = time_val.time()
                    
                    # Create end time (add 15 minutes)
                    hour = time_val.hour
                    minute = time_val.minute
                    end_minute = minute + 15
                    if end_minute >= 60:
                        end_hour = hour + 1
                        end_minute = end_minute - 60
                    else:
                        end_hour = hour
                    
                    # Format time range
                    start_str = f"{hour:02d}:{minute:02d}"
                    end_str = f"{end_hour:02d}:{end_minute:02d}"
                    
                    # Add AM/PM
                    if hour < 12:
                        start_ampm = "am"
                    else:
                        start_ampm = "pm"
                    
                    time_ranges.append(f"{start_str}-{end_str}{start_ampm}")
                
                return time_ranges
            
            # Apply time range formatting
            date1_time.iloc[:, 0] = format_time_range(date1_time.iloc[:, 0])
            date2_time.iloc[:, 0] = format_time_range(date2_time.iloc[:, 0])
            
            date1_time.columns = ['Time', f'{date1}-Customer In', f'{date1}-Customer Out']
            date2_time.columns = ['Time', f'{date2}-Customer In', f'{date2}-Customer Out']
            
            # Merge on time with inner join to show only common time slots (no extra 0000)
            comparison_time = pd.merge(date1_time, date2_time, on='Time', how='inner')
            
            # Calculate differences for each time slot
            comparison_time['Customer In Increase/Decrease'] = comparison_time[f'{date2}-Customer In'] - comparison_time[f'{date1}-Customer In']
            comparison_time['Customer Out Increase/Decrease'] = comparison_time[f'{date2}-Customer Out'] - comparison_time[f'{date1}-Customer Out']
            
            # Reorder columns for better display
            comparison_time = comparison_time[['Time', 
                                            f'{date1}-Customer In', f'{date2}-Customer In', 'Customer In Increase/Decrease',
                                            f'{date1}-Customer Out', f'{date2}-Customer Out', 'Customer Out Increase/Decrease']]
            
            # Reset index to ensure unique index
            comparison_time = comparison_time.reset_index(drop=True)
            
            # Format numeric columns to remove unnecessary decimal places
            numeric_columns = [f'{date1}-Customer In', f'{date2}-Customer In', 'Customer In Increase/Decrease',
                             f'{date1}-Customer Out', f'{date2}-Customer Out', 'Customer Out Increase/Decrease']
            
            for col in numeric_columns:
                comparison_time[col] = comparison_time[col].astype(int)
            
            # Add filter options
            col_filter1, col_filter2 = st.columns(2)
            
            with col_filter1:
                show_only_red = st.checkbox("Show only red highlighted time slots", value=False)
            
            with col_filter2:
                ratio_threshold = st.selectbox(
                    "Minimum ratio for red highlighting:",
                    options=[4, 5, 6, 7, 8],
                    index=0,
                    format_func=lambda x: f"{x}x or greater"
                )
            
            st.write("**15-Minute Interval Comparison (8am to 8pm):**")
            st.write(f"*Red: Zero values or {ratio_threshold}x or greater increase/decrease*")
            
            # Apply conditional formatting for dynamic ratio threshold and zero values
            def highlight_ratios(row):
                styles = [''] * len(row)
                
                # Check for zero values in Customer In
                date1_in = row[f'{date1}-Customer In']
                date2_in = row[f'{date2}-Customer In']
                if date1_in == 0 or date2_in == 0:
                    styles[1] = 'background-color: red; color: white;'  # Date1 Customer In column
                    styles[2] = 'background-color: red; color: white;'  # Date2 Customer In column
                else:
                    # Calculate ratios for Customer In
                    ratio_in = max(date1_in, date2_in) / min(date1_in, date2_in)
                    if ratio_in >= ratio_threshold:
                        styles[3] = 'background-color: red; color: white;'  # Customer In Increase/Decrease column
                
                # Check for zero values in Customer Out
                date1_out = row[f'{date1}-Customer Out']
                date2_out = row[f'{date2}-Customer Out']
                if date1_out == 0 or date2_out == 0:
                    styles[4] = 'background-color: red; color: white;'  # Date1 Customer Out column
                    styles[5] = 'background-color: red; color: white;'  # Date2 Customer Out column
                else:
                    # Calculate ratios for Customer Out
                    ratio_out = max(date1_out, date2_out) / min(date1_out, date2_out)
                    if ratio_out >= ratio_threshold:
                        styles[6] = 'background-color: red; color: white;'  # Customer Out Increase/Decrease column
                
                return styles
            
            # Filter data if checkbox is checked
            if show_only_red:
                # Filter for rows with red conditions
                red_rows = []
                for idx, row in comparison_time.iterrows():
                    date1_in = row[f'{date1}-Customer In']
                    date2_in = row[f'{date2}-Customer In']
                    date1_out = row[f'{date1}-Customer Out']
                    date2_out = row[f'{date2}-Customer Out']
                    
                    # Check for zero values
                    if (date1_in == 0 or date2_in == 0 or 
                        date1_out == 0 or date2_out == 0):
                        red_rows.append(idx)
                    else:
                        # Check for dynamic ratio thresholds
                        if date1_in > 0 and date2_in > 0:
                            ratio_in = max(date1_in, date2_in) / min(date1_in, date2_in)
                            if ratio_in >= ratio_threshold:
                                red_rows.append(idx)
                        if date1_out > 0 and date2_out > 0:
                            ratio_out = max(date1_out, date2_out) / min(date1_out, date2_out)
                            if ratio_out >= ratio_threshold:
                                red_rows.append(idx)
                
                filtered_comparison = comparison_time.loc[red_rows].reset_index(drop=True)
                if not filtered_comparison.empty:
                    st.dataframe(filtered_comparison.style.apply(highlight_ratios, axis=1))
                else:
                    st.write("No red highlighted time slots found.")
            else:
                st.dataframe(comparison_time.style.apply(highlight_ratios, axis=1))
            
            # Summary totals
            st.write("**Summary Totals:**")
            summary_df = pd.DataFrame({
                'Date 1': [date1, int(date1_totals.iloc[0]), int(date1_totals.iloc[1])],
                'Date 2': [date2, int(date2_totals.iloc[0]), int(date2_totals.iloc[1])],
                'Difference': ['', 
                              int(date2_totals.iloc[0] - date1_totals.iloc[0]), 
                              int(date2_totals.iloc[1] - date1_totals.iloc[1])]
            }, index=['Date', 'Customer In', 'Customer Out'])
            st.dataframe(summary_df)
        else:
            st.warning("Please select two different dates for comparison.")
    else:
        st.warning("Need at least 2 dates in the data for comparison.")
