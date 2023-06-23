import re
#text=input()
result=""
text="TN57ASY8656"
NumberPlate=["TN57AY8656","AP29AN0074","BR09V7267","UP64W4388","JH05AW2117","KL02BM4656","KL02BMVN9090"]
for i in NumberPlate:
    pattern=re.findall("[A-Z]{2}[0-9]{2}[A-Z][0-9]{4}|[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}|[A-Z]{2}[0-9]{2}[A-Z]{3}[0-9]{4}",i)
    #print(pattern)
    for j in pattern:
        result+=j+"\n"
print(result)
