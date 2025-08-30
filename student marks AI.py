def grade(m):
    if m >= 90:
        return "A+"
    elif m >= 75:
        return "A"
    elif m >= 60:
        return "B"
    elif m >= 40:
        return "C"
    else:
        return "F"

def student_grading():
    n = int(input("How many subjects? "))
    res = {}
    for i in range(n):
        sub = input("Enter subject name: ")
        mark = int(input("Enter marks for " + sub + ": "))
        res[sub] = grade(mark)

    print("\nReport Card")
    for s in res:
        print(s, ":", res[s])

student_grading()
