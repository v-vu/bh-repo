# --- Code Block ---
#filter for BH Visits
# Filter for BH Visits where tscore_trans_type == 'P837'
all_claims = all_dx_claims[
    ((all_dx_claims['Therapy'] == 1) | (all_dx_claims['Psych Assessment/Medical Management'] == 1)) &
    (all_dx_claims['tscore_trans_type'] == 'P837')
# Drop unnecessary columns
][['member_id', 'claim_id', 'provider_id', 'claim_first_dos', 'Therapy', 'Psych Assessment/Medical Management']].drop_duplicates()

# --- Code Block ---
elig['termination_date'].value_counts().head(10)

