overall=0
driver=0
rider=0

print("Are you a driver or a rider?")
ans=input("enter: ")
if ans.lower()=='driver':
    print("Enter your feeback as following:-")
    print("1. Strongly disagree")
    print("2. Disagree")
    print("3. Neutral")
    print("4. Agree")
    print("5. Strongly agree")

    print("Q1. The rider was punctual")
    ch=int(input("ENTER YOUR FEEDBACK: "))
    overall+=ch
    rider+=ch
    
    print("Q2. The rider was polite and respectful")
    ch=int(input("ENTER YOUR FEEDBACK: "))
    overall+=ch
    rider+=ch

    print("Q3. I would like to ride with this rider again")
    ch=int(input("ENTER YOUR FEEDBACK: "))
    overall+=ch
    rider+=ch

    print("Q4. The rider followed safety rules (seatbelt, helmet, etc.)")
    ch=int(input("ENTER YOUR FEEDBACK: "))
    overall+=ch
    rider+=ch

elif ans.lower()=='rider':
    print("Enter your feeback as following:-")
    print("1. Strongly disagree")
    print("2. Disagree")
    print("3. Neutral")
    print("4. Agree")
    print("5. Strongly agree")

    print("Q1. The driver was punctual")
    ch=int(input("ENTER YOUR FEEDBACK: "))
    overall+=ch
    driver+=ch
    
    print("Q2. The driver was polite and respectful")
    ch=int(input("ENTER YOUR FEEDBACK: "))
    overall+=ch
    driver+=ch

    print("Q3. I would like to ride with this driver again")
    ch=int(input("ENTER YOUR FEEDBACK: "))
    overall+=ch
    driver+=ch

    print("Q4. The driver followed safety rules (seatbelt, helmet, etc.)")
    ch=int(input("ENTER YOUR FEEDBACK: "))
    overall+=ch
    driver+=ch
else:
    print("invalid choice")

    
print("Q5. the process was easy to follow")
ch=int(input("ENTER YOUR FEEDBACK: "))
overall+=ch

print("Q6. I would use it again")
ch=int(input("ENTER YOUR FEEDBACK: "))
overall+=ch

print("Q7. I would recommend this to others")
ch=int(input("ENTER YOUR FEEDBACK: "))
overall+=ch


print("Q8. The app was easy to navigate")
ch=int(input("ENTER YOUR FEEDBACK: "))
overall+=ch

print("Q9. The instructions were clear")
ch=int(input("ENTER YOUR FEEDBACK: "))
overall+=ch


if rider>=8:
    print("thanks for being a star rider! Keep riding safe and friendly.")
elif rider >=6 and rider<8:
    print("You received a low rating. Please review our guidelines.")
else:
    print("rider performance under review")

print("\n")

if driver>=8:
    print("thanks for being a star driver! Keep drive safe and friendly.")
elif driver>=8 and driver<6:
    print("you received a low rating. Please review our guidelines.")
else:
    print("driver performance under review")
    
print("\n")
print(f"overall rating: {overall}/65")
print("\n")
print("thankyou for your feedback")