def isStoppingCondition(aggregatedValues,treeheight):
    if aggregatedValues["approvedLoan"]>=aggregatedValues["declinedLoan"]:
        percentage= (aggregatedValues["approvedLoan"]/(aggregatedValues["approvedLoan"]+ aggregatedValues["declinedLoan"]))*100
    else:
        percentage=(aggregatedValues["declinedLoan"]/(aggregatedValues["approvedLoan"]+aggregatedValues["declinedLoan"]))*100

    decision= (percentage>=80) or (treeheight>=3)

    return decision

aggregatedValues={"approvedLoan":10,"declinedLoan":9}
treeheight = 2

print(isStoppingCondition(aggregatedValues,treeheight))       
        
    
