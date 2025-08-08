# --- Code Block ---
all_claims.info()

# --- Code Block ---
all_claims.head(3)

# --- Code Block ---
elig.info()

# --- Code Block ---
#check to see rows that have effect_date > termination_date
# Import necessary package(s)
# Import necessary package(s)
import pandas as pd

def find_invalid_intervals(eligibility_df):
    invalid_rows = eligibility_df[eligibility_df['effective_date'] > eligibility_df['termination_date']]
    if not invalid_rows.empty:
        print("Invalid intervals found in eligibility_df:")
        print(invalid_rows)
    else:
        print("No invalid intervals found.")

find_invalid_intervals(elig)

# --- Code Block ---
# Find rows with duplicate member_id and effective_date
#elig[elig.duplicated(subset=["member_id", "effective_date"], keep=False)].head(10)

# --- Code Block ---
#missing[missing['final_enrollment_month']=='202305']

# --- Code Block ---
final_result.info()

# --- Code Block ---
pre_post_dx = assign_pre_post(all_dx_claims)

# --- Code Block ---
pre_post_dx.info()

# --- Code Block ---
#rename column and only filter for current customers
results.rename(columns={'days_enrolled':'enrollment_days'},inplace=True)
keywords = ['emblem', 'sentara', 'intermountain', 'community']
filtered_results = results[results['plan'].str.contains('|'.join(keywords), case=False, na=False)]

# --- Code Block ---
# Export DataFrame to CSV file
#filtered_results.to_csv('results.csv', index = False)

