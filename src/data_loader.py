# --- Code Block ---
#import Ontrak enrollments using Stored Procedure - myevolve 
# Load Ontrak program enrollments from Myevolve using a stored procedure
# Load Ontrak program enrollments from Myevolve using a stored procedure
enr = pd.read_sql("Exec [dsv].[ds_program_enrollments_coaching_fact]", con = sql_conn)

# --- Code Block ---
#import bh claims using sql query file - Axiom
"""with open(path + "\\" + "bh_claims_03122025.sql", 'r') as file:
    claims_sql = file.read()

# Drop unnecessary columns
member_ids = enr['member_id'].dropna().unique().tolist()
formatted_ids = ', '.join(f"'{str(x)}'" for x in member_ids)
"""
#query = f"""
#        {claims_sql}
#        AND member_id IN ({formatted_ids})
#    """
"""
claims =  pd.read_sql(query, con=psql_conn)
claims.info()
"""

# --- Code Block ---
#import ALL claims using sql query file - Axiom

with open(path + "\\" + "SQL\\all_claims_04152025.sql", 'r') as file:
    claims_sql = file.read()

# Drop unnecessary columns
member_ids = enr['member_id'].dropna().unique().tolist()
formatted_ids = ', '.join(f"'{str(x)}'" for x in member_ids)

query = f"""
       {claims_sql}
       AND member_id IN ({formatted_ids})
   """

all_dx_claims =  pd.read_sql(query, con=psql_conn)
all_dx_claims.info()

# --- Code Block ---
#import eligbiilty --Axiom

with open(path + "\\" + "SQL\\eligibility_03122025.sql", 'r') as file:
    elig_sql = file.read()
elig = pd.read_sql(elig_sql, con=psql_conn)

# --- Code Block ---
#get top 10 diagnosis pre vs post

#Step 1: Get Intentional self-harm codes
query = """
SELECT [Code]    
FROM [evolv_cs_reports].[dbo].[ds_hedis_vstoc_2025]
WHERE [Value Set Name] = 'Intentional Self-Harm'
"""
self_harm_df = pd.read_sql(query, con = sql_conn)
self_harm_codes = set(code.strip().upper() for code in self_harm_df['Code'] if pd.notna(code))

# Step 2: Stack diagnosis codes
diag_cols = [col for col in pre_post_dx.columns if col.startswith('diag_code_')]
diag_long = pre_post_dx.melt(
    id_vars=['member_id', 'pre_post'],
    value_vars=diag_cols,
    value_name='diag_code'
# Drop unnecessary columns
).dropna(subset=['diag_code'])

# Step 3: Filter to BH codes (F-codes or Intentional self-harm)
def is_bh(code):
    code = code.upper().strip()
    return code.startswith('F') or code in self_harm_codes

diag_long['diag_code_3digit'] = diag_long['diag_code'].str[:3].str.upper()
diag_long = diag_long[diag_long['diag_code_3digit'].apply(is_bh)]

# Step 4: Count top BH codes per member and pre_post
top_diag = (
    diag_long.groupby(['member_id', 'pre_post', 'diag_code_3digit'])
    .size()
    .reset_index(name='count')
)

top_diag['rank'] = top_diag.groupby(['member_id', 'pre_post'])['count'].rank(
    method='first', ascending=False)

top_10_diag = top_diag[top_diag['rank'] <= 10]

# Step 5: Aggregate into list
diagnosis_lists = (
    top_10_diag
    .sort_values(['member_id', 'pre_post', 'count'], ascending=[True, True, False])
    .groupby(['member_id', 'pre_post'])['diag_code_3digit']
    .apply(list)
    .reset_index()
)

# Step 6: Pivot so that pre/post are columns
final_diag = diagnosis_lists.pivot(index='member_id', columns='pre_post', values='diag_code_3digit').reset_index()

# Step 7: Rename columns 
final_diag.columns.name = None
final_diag = final_diag.rename(columns={'pre': 'pre_top_10', 'post': 'post_top_10'})

# --- Code Block ---
from datetime import date

# Add load_date column with today's date
claims_df["load_date"] = date.today()
filtered_results["load_date"] = date.today()

claims_df.to_sql("ds_bh_visits", ds_engine, if_exists='replace', index=False)
filtered_results.to_sql("ds_bh_results", ds_engine, if_exists='replace', index=False)

