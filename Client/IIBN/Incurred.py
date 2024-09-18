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


# claims = pd.read_csv("Output\\trail.csv")
claims = pd.read_csv("Output\\ClaimsData.csv")
claims['Intimation_Date'] = pd.to_datetime(claims['Intimation_Date'], format="mixed", dayfirst=True)
claims['File'] = pd.to_datetime(claims['File'], format="mixed", dayfirst=True)
claims["PaidClaimAmount"] = claims["PaidClaimAmount"].str.replace("-", "0")

list_claims = claims["Claim_Reference"].unique().tolist()
print(len(list_claims))
counter = 0
for claim_reference in list_claims:
    counter = counter + 1
    print(counter)
    claim_reference_ = claim_reference
    cr = claims[claims["Claim_Reference"] == claim_reference].sort_values(by=["File"])
    intimation_date = cr["Intimation_Date"].iloc[0]
    if intimation_date >= datetime.strptime("01/03/2023", "%d/%m/%Y"):
        opening_paid = 0
        opening_os = 0
    else:
        opening_paid = int(cr["PaidClaimAmount"].iloc[0])
        opening_os = int(cr["Outstanding_Amount"].iloc[0])
    incurred = cr.apply(lambda x: print_row(x), axis=1)
    count =0
    for amount in incurred:
        index_ = incurred.index[count]
        claims.at[index_, "Incurred"] = amount
        count = count +1
    # claims.to_csv("Output\\Inc.csv")
    # break
    # print(incurred)
    # for index, row in cr.iterrows():
    #     closing_paid = row["PaidClaimAmount"]
    #     closing_os = row["Outstanding_Amount"]
    #     incurred = (closing_os - opening_os) + (closing_paid - opening_paid)
    #     # row["incurred"] =
    #     opening_paid = closing_paid
    #     opening_os = closing_os
    #     print(incurred)
    #     cr.at[index, 'incurred'] = incurred
    #     pass
    #cr.to_csv("Output\\Incurred.csv")
claims.to_csv("Output\\Inc.csv")