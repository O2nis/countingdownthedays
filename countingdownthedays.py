import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.parser import parse
import io

def parse_date(date_str):
    try:
        return parse(date_str) if date_str.strip() else None
    except:
        return None

def main():
    st.title("Date Difference Calculator")
    
    st.write("""
    This app calculates the number of days between your dates and a reference date.
    1. Paste your dates (one per line) in the text area below
    2. Set your reference date
    3. Choose output options
    4. Download the results as CSV
    """)
    
    # Text area for pasting dates
    pasted_dates = st.text_area("Paste your dates here (one per line):", height=200)
    
    # Date input for reference date
    reference_date = st.date_input("Set the reference date:", value=datetime.today())
    reference_date = datetime.combine(reference_date, datetime.min.time())
    
    # Output options
    col1, col2 = st.columns(2)
    with col1:
        show_negative = st.checkbox("Show negative values", value=True, 
                                  help="Uncheck to display all differences as positive numbers")
    with col2:
        count_direction = st.selectbox("Count direction:",
                                     ["Forward (date - reference)", "Backward (reference - date)"],
                                     index=0)
    
    if st.button("Calculate Days Difference"):
        if not pasted_dates:
            st.warning("Please paste some dates first.")
            return
            
        # Process the pasted dates
        date_lines = pasted_dates.split('\n')
        original_dates = []
        days_diff = []
        invalid_dates = []
        
        for i, date_str in enumerate(date_lines, 1):
            # Preserve empty lines
            if not date_str.strip():
                original_dates.append("")
                days_diff.append("")
                continue
                
            parsed_date = parse_date(date_str)
            if parsed_date is None:
                invalid_dates.append(f"Line {i}: {date_str}")
                original_dates.append(date_str)
                days_diff.append("INVALID DATE")
                continue
                
            original_dates.append(date_str)
            delta = parsed_date - reference_date if count_direction == "Forward (date - reference)" else reference_date - parsed_date
            days = delta.days
            
            if not show_negative:
                days = abs(days)
                
            days_diff.append(days)
        
        # Create DataFrame
        df = pd.DataFrame({
            "Original Date": original_dates,
            "Days Difference": days_diff
        })
        
        # Show results
        valid_count = sum(1 for x in days_diff if isinstance(x, int))
        empty_count = sum(1 for x in days_diff if x == "")
        invalid_count = sum(1 for x in days_diff if x == "INVALID DATE")
        
        st.success(
            f"Processed {len(date_lines)} lines: "
            f"{valid_count} valid dates, "
            f"{empty_count} empty lines, "
            f"{invalid_count} invalid dates"
        )
        
        if invalid_count > 0:
            with st.expander("Show invalid dates"):
                st.write("\n".join(invalid_dates))
        
        st.dataframe(df)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='date_differences.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()