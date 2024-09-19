from datetime import datetime
import pandas as pd

opening_os = 0
opening_paid = 0


def print_row(row):
    global opening_os
    global opening_paid
    closing_paid = int(row["PaidClaimAmount"])
    closing_os = int(row["Outstanding_Amount"])
    incurred_ = (closing_os - opening_os) + (closing_paid - opening_paid)
    opening_paid = closing_paid
    opening_os = closing_os
    return incurred_


claims = pd.read_csv("Output\\RSA_Combined_Claims.csv")
claims['Intimation_Date'] = pd.to_datetime(claims['Intimation_Date'], format="mixed", dayfirst=True)
claims['File'] = pd.to_datetime(claims['File'], format="mixed", dayfirst=True)


list_claims = claims["Claim_Reference"].unique().tolist()
print(len(list_claims))
counter = 0
for claim_reference in list_claims:
    in_current_period = False
    counter = counter + 1
    print(counter)
    claim_reference_ = claim_reference
    cr = claims[claims["Claim_Reference"] == claim_reference].sort_values(by=["File"])
    intimation_date = cr["Intimation_Date"].iloc[0]
    start_of_time = "07/03/2023"
    if intimation_date >= datetime.strptime(start_of_time, "%d/%m/%Y"):
        opening_paid = 0
        opening_os = 0
        in_current_period = True
    else:
        opening_paid = int(cr["PaidClaimAmount"].iloc[0])
        opening_os = int(cr["Outstanding_Amount"].iloc[0])

    incurred = cr.apply(lambda x: print_row(x), axis=1)
    count = 0
    for amount in incurred:
        index_ = incurred.index[count]
        claims.at[index_, "Incurred"] = amount
        if count == 0 and in_current_period and cr["File"].iloc[0].month == intimation_date.month:
            claims.at[index_, "Claim_Count"] = 1
        else:
            claims.at[index_, "Claim_Count"] = 0
        count = count + 1

claims.to_csv("Output\\RSA_Incurred_Claims.csv")
