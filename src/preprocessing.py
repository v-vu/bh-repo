# --- Code Block ---
#get a count of how many members for each plan
# Summarize enrollment count by plan
# Summarize enrollment count by plan
enr.groupby(by='plan')['member_id'].count().reset_index().sort_values(by='member_id', ascending=False)

# --- Code Block ---
"""
# Frequency count
status_counts = all_claims.groupby('claim_status').size().reset_index(name='count')

# Add percentage of total
total = status_counts['count'].sum()
status_counts['percent'] = (status_counts['count'] / total * 100).round(2)

# Preview result
status_counts.head()"
"""

# --- Code Block ---
"""all_claims.groupby(['place_of_svc_code']).agg(
    total_members=('member_id', 'count'),
    unique_members=('member_id', 'nunique'),
    total_claims=('claim_id', 'count'),
    unique_claims=('claim_id', 'nunique')
# Export DataFrame to CSV file
).reset_index().to_csv('placeofservice.csv')"""

# --- Code Block ---
#aggregate bh visits
all_claims = all_claims.groupby(['member_id', 'claim_id', 'provider_id','claim_first_dos'], as_index=False).agg({
    'Therapy': 'max',  # Get max value for Therapy
    'Psych Assessment/Medical Management': 'max'  # Get max value for Psych Assessment/Medical Management
})

# --- Code Block ---
# Drop unnecessary columns
elig = elig.sort_values(by=["member_id", "effective_date", "termination_date"]).reset_index(drop=True)

# --- Code Block ---
#Get min termination_date for each effective_date
#min_index = elig.groupby(["member_id", "effective_date"])["termination_date"].idxmin()
#elig=elig.loc[min_index]

# --- Code Block ---
# Impute termination_date where it's null (NaT) or greater than today
#today = pd.Timestamp.today().normalize()  
#elig['termination_date'] = elig['termination_date'].apply(lambda x: today if pd.isna(x) or x > today else x)

# --- Code Block ---
#view which members have more than 1 rows
# Merge two datasets
#merged_df.groupby('member_id').filter(lambda x: len(x) > 1).tail(10)

# --- Code Block ---
# Merge two datasets
#merge enrollment and eligibility
"""
#enr.columns = enr.columns.str.lower() #rename all columns to lower case
date_columns_elig = ["effective_date", "termination_date"]
elig[date_columns_elig] = elig[date_columns_elig].apply(pd.to_datetime)

date_columns_enr = ["baseline_startdate","baseline_enddate","final_enrollment_start","final_enrollment_end"]
enr[date_columns_enr] = enr[date_columns_enr].apply(pd.to_datetime)

# Merge Enrollment and Eligibility data
# Merge two datasets
merged_df = enr[['member_id',"baseline_startdate","baseline_enddate","final_enrollment_start","final_enrollment_end"]].merge(elig[['tscore_org','member_id',"effective_date", "termination_date"]], on="member_id", how="inner")

# Merge two datasets
merged_df.drop_duplicates(inplace=True)"""

# --- Code Block ---
"""
#baseline days
baseline_mask = (
# Merge two datasets
    (merged_df["baseline_enddate"] >= merged_df["effective_date"]) &
# Merge two datasets
    (merged_df["baseline_startdate"] <= merged_df["termination_date"])
)
# Merge two datasets
merged_baseline = merged_df[baseline_mask].copy()

# Merge two datasets
merged_baseline["baseline_overlap_start"] = merged_baseline[["baseline_startdate", "effective_date"]].max(axis=1)
# Merge two datasets
merged_baseline["baseline_overlap_end"] = merged_baseline[["baseline_enddate", "termination_date"]].min(axis=1)
# Merge two datasets
merged_baseline["baseline_days"] = (merged_baseline["baseline_overlap_end"] - merged_baseline["baseline_overlap_start"]).dt.days + 1

#enrollment days
enrollment_mask = (
# Merge two datasets
    (merged_df["final_enrollment_end"] >= merged_df["effective_date"]) &
# Merge two datasets
    (merged_df["final_enrollment_start"] <= merged_df["termination_date"])
)
# Merge two datasets
merged_enrollment = merged_df[enrollment_mask].copy()

# Merge two datasets
merged_enrollment["enrollment_overlap_start"] = merged_enrollment[["final_enrollment_start", "effective_date"]].max(axis=1)
# Merge two datasets
merged_enrollment["enrollment_overlap_end"] = merged_enrollment[["final_enrollment_end", "termination_date"]].min(axis=1)
# Merge two datasets
merged_enrollment["enrollment_days"] = (merged_enrollment["enrollment_overlap_end"] - merged_enrollment["enrollment_overlap_start"]).dt.days + 1
"""

# --- Code Block ---
# Merge two datasets
#merged_baseline[merged_baseline['member_id'] == '1006129*01'] #1937324*02

# --- Code Block ---
# Merge two datasets
#merged_enrollment[merged_enrollment['member_id'] == '1006129*01'] #1937324*02

# --- Code Block ---
"""
# Group and aggregate both results
group_keys = ["member_id", "baseline_startdate", "baseline_enddate", "final_enrollment_start", "final_enrollment_end"]
# Merge two datasets
baseline_agg = merged_baseline.groupby(group_keys)["baseline_days"].sum().reset_index()
# Merge two datasets
enrollment_agg = merged_enrollment.groupby(group_keys)["enrollment_days"].sum().reset_index()

# Merge both aggregates
# Merge two datasets
final_df= pd.merge(baseline_agg, enrollment_agg, on=group_keys, how="outer").fillna(0)
final_df["baseline_days"] = final_df["baseline_days"].astype(int)
final_df["enrollment_days"] = final_df["enrollment_days"].astype(int)
"""

# --- Code Block ---
"""
#if baseline > 365, set as 365 days
final_df['baseline_days'] = final_df['baseline_days'].apply(lambda x: 365 if x > 365 else x)
final_df[final_df['baseline_days']>365]
"""

# --- Code Block ---
"""
#missing coverage
# Merge two datasets
missing = pd.merge(enr, final_df, on = 'member_id', how = 'left')
missing = missing[missing['baseline_days'].isnull()]
# Summarize enrollment count by plan
# Summarize enrollment count by plan
missing.groupby(by=['plan'])['member_id'].count().reset_index()"""

# --- Code Block ---
#Sentara missing coverage member counts
"""
missing_sentara = missing[
    missing["plan"].str.startswith("Sentara")
]
missing["final_enrollment_month"] = missing_sentara["final_enrollment_start_x"].dt.strftime("%Y%m")
missing_counts = missing.groupby("final_enrollment_month")["member_id"].count().reset_index(name="member_count")

# Plot with Plotly
# Generate a plot or chart
fig = px.bar(
    missing_counts,
    x="final_enrollment_month",
    y="member_count",
    title="Count of Members with Missing Final Enrollment Start (Grouped by Month)",
    labels={"final_enrollment_month": "Month (YYYYMM)", "member_count": "Unique Member Count"}
)

fig.show()"""

# --- Code Block ---
#filter for claims that have claim_first_dos between enrollment dates and eligibility dates

#Convert date columns to datetime
"""
for df, cols in zip([elig, enr, all_claims], 
                    [['effective_date', 'termination_date'], 
                     ['baseline_startdate', 'baseline_enddate', 'final_enrollment_start', 'final_enrollment_end'], 
                     ['claim_first_dos']]):
    df[cols] = df[cols].apply(pd.to_datetime, errors='coerce')

# Pre-filter claims to reduce data size before merging
claim = all_claims[
    all_claims['claim_first_dos'].between(elig['effective_date'].min(), elig['termination_date'].max()) &
    all_claims['claim_first_dos'].between(enr['baseline_startdate'].min(), enr['final_enrollment_end'].max())
]

# Merge and filter in one step
final_result = (
# Merge two datasets
    claim.merge(elig, on='member_id', how='inner')
# Merge two datasets
         .merge(enr, on='member_id', how='inner')
         .loc[lambda df: (df['effective_date'] <= df['claim_first_dos']) &
                         (df['termination_date'] >= df['claim_first_dos']) &
                         (df['baseline_startdate'] <= df['claim_first_dos']) &
                         (df['final_enrollment_end'] >= df['claim_first_dos'])]
)
"""

# --- Code Block ---
# bh claims that are between enrollment dates
# Convert date columns to datetime
for df, cols in zip([enr, all_claims], 
                    [['baseline_startdate', 'baseline_enddate', 'final_enrollment_start', 'final_enrollment_end'], 
                     ['claim_first_dos']]):
    df[cols] = df[cols].apply(pd.to_datetime, errors='coerce')

# Pre-filter claims to reduce data size based on enrollment date ranges
claim = all_claims[
    all_claims['claim_first_dos'].between(
        enr['baseline_startdate'].min(), 
        enr['final_enrollment_end'].max()
    )
]

final_result = (
# Merge two datasets
    claim.merge(enr, on='member_id', how='inner')
         .loc[lambda df: (df['baseline_startdate'] <= df['claim_first_dos']) & 
                         (df['final_enrollment_end'] >= df['claim_first_dos'])]
)

# --- Code Block ---
def assign_pre_post(df):
# Import necessary package(s)
# Import necessary package(s)
    import numpy as np
# Import necessary package(s)
# Import necessary package(s)
    import pandas as pd
    """
    Assigns 'pre' or 'post' based on claim_first_dos date ranges.

    Conditions:
    - 'pre'  → claim_first_dos is between baseline_startdate and baseline_enddate
    - 'post' → claim_first_dos is between final_enrollment_start and final_enrollment_end
    - NaN if it doesn't fall into either range

    Parameters:
    df (pd.DataFrame): DataFrame containing relevant date columns.

    Returns:
    pd.DataFrame: DataFrame with new 'pre_post' column.
    """

    # Ensure all relevant columns are in datetime format
    date_cols = ['claim_first_dos', 'baseline_startdate', 'baseline_enddate', 'final_enrollment_start', 'final_enrollment_end']
    df[date_cols] = df[date_cols].apply(pd.to_datetime, errors='coerce')

    # Define conditions
    conditions = [
        df['claim_first_dos'].between(df['baseline_startdate'], df['baseline_enddate']),
        df['claim_first_dos'].between(df['final_enrollment_start'], df['final_enrollment_end'])
    ]

    # Define choices
    choices = ['pre', 'post']

    # Apply conditions to create 'pre_post' column
    df['pre_post'] = np.select(conditions, choices, default='')  # NaN if not in either range

    return df

# --- Code Block ---
#assign pre vs post claims
final_result = assign_pre_post(final_result)
# Drop unnecessary columns
final_result = final_result[['member_id', 'claim_id','provider_id','claim_first_dos','Therapy','Psych Assessment/Medical Management','baseline_startdate','baseline_enddate','final_enrollment_start','final_enrollment_end','pre_post']].drop_duplicates()
claims_df = final_result[final_result['final_enrollment_start'] >= '2023-01-01']

#get distinct count member_id, provider_id, and claim_first_dos
pre_post_df = final_result.groupby(
    by=[
        'member_id',
        'final_enrollment_start',
        'pre_post'
    ]
).apply(
    lambda df: df[['member_id', 'provider_id', 'claim_first_dos']]
# Drop unnecessary columns
    .dropna()
# Drop unnecessary columns
    .drop_duplicates()
    .shape[0]
).reset_index(name='distinct_member_claim_dos')
pre_post_df

# --- Code Block ---
#pivot pre vs post into columns
pivoted_df = pre_post_df.pivot_table(
    index=['member_id', 'final_enrollment_start'],
    columns='pre_post',
    values='distinct_member_claim_dos',
    fill_value=0
).reset_index()
pivoted_df

# --- Code Block ---
#use this if considering eligiblity
# Merge two datasets
"""results = pd.merge(final_df, pivoted_df[['member_id','pre','post']], on=['member_id'], how='left').fillna(0)
results['baseline_days'] = (results['baseline_enddate'] - results['baseline_startdate']).dt.days
#results['pre_bh_vists'] = results['pre']/(results['baseline_days']/30.4)
#results['post_bh_vists'] = results['post']/(results['enrollment_days']/30.4)
# Merge two datasets
results = pd.merge(results,enr[['member_id','plan','final_enrollment_status']], on=['member_id'], how = 'inner')
"""

# --- Code Block ---
#use this if not considering eligility 
# Merge two datasets
results = pd.merge(enr, pivoted_df[['member_id','pre','post']], on=['member_id'], how='left').fillna(0)
results['baseline_days'] = (results['baseline_enddate'] - results['baseline_startdate']).dt.days
results['pre_bh_vists'] = results['pre']/(results['baseline_days']/30.4) #not calculating pmpm now
results['post_bh_vists'] = results['post']/(results['days_enrolled']/30.4)

# --- Code Block ---
#filter for enrollments after 2023 only
results = results[results['final_enrollment_start'] >= '2023-01-01']
# Fill missing values
results.fillna(0, inplace=True)

# --- Code Block ---
# Pre-filter dx claims to reduce data size based on enrollment date ranges

# Convert date columns to datetime
for df, cols in zip([enr, all_dx_claims], 
                    [['baseline_startdate', 'baseline_enddate', 'final_enrollment_start', 'final_enrollment_end'], 
                     ['claim_first_dos']]):
    df[cols] = df[cols].apply(pd.to_datetime, errors='coerce')

all_dx_claims = all_dx_claims[
    all_dx_claims['claim_first_dos'].between(
        enr['baseline_startdate'].min(), 
        enr['final_enrollment_end'].max()
    )
]

all_dx_claims = (
# Merge two datasets
    all_dx_claims.merge(enr, on='member_id', how='inner')
         .loc[lambda df: (df['baseline_startdate'] <= df['claim_first_dos']) & 
                         (df['final_enrollment_end'] >= df['claim_first_dos'])]
)

# --- Code Block ---
# Merge two datasets
results=pd.merge(results,final_diag, on = 'member_id', how = 'left')

# --- Code Block ---
#filter for claims that have claim_first_dos between enrollment dates

"""
# Convert date columns to datetime
for df, cols in zip([enr, all_claims], 
                    [['baseline_startdate', 'baseline_enddate', 'final_enrollment_start', 'final_enrollment_end'], 
                     ['claim_first_dos']]):
    df[cols] = df[cols].apply(pd.to_datetime, errors='coerce')

# Pre-filter claims to reduce data size based on enrollment date ranges
claim = all_claims[
    all_claims['claim_first_dos'].between(
        enr['baseline_startdate'].min(), 
        enr['final_enrollment_end'].max()
    )
]

# Merge claims with enrollment and filter for claims within enrollment windows
final_result = (
# Merge two datasets
    claim.merge(enr, on='member_id', how='inner')
         .loc[lambda df: (df['baseline_startdate'] <= df['claim_first_dos']) & 
                         (df['final_enrollment_end'] >= df['claim_first_dos'])]
)

all_claims[(all_claims['Therapy'] == 1) & (all_claims['Psych Assessment/Medical Management'] == 1)]
#get distinct count member_id, claim_id, and claim_first_dos
pre_post_df = final_result.groupby(
    by=[
        'member_id',
        'final_enrollment_start',
        'pre_post'
    ]
).apply(
    lambda df: df[['member_id', 'claim_id', 'claim_first_dos']]
# Drop unnecessary columns
    .dropna()
# Drop unnecessary columns
    .drop_duplicates()
    .shape[0]
).reset_index(name='distinct_member_claim_dos')

pivoted_df = pre_post_df.pivot_table(
    index=['member_id', 'final_enrollment_start'],
    columns='pre_post',
    values='distinct_member_claim_dos',
    fill_value=0
).reset_index()

# Merge two datasets
results = pd.merge(enr, pivoted_df[['member_id','pre','post']], on=['member_id'], how='left').fillna(0)
results['baseline_days'] = (results['baseline_enddate'] - results['baseline_startdate']).dt.days
results['pre_bh_vists'] = results['pre']/(results['baseline_days']/30.4)
results['post_bh_vists'] = results['post']/(results['enrollment_days']/30.4)

"""

