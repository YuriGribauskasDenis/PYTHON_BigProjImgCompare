def calculate():
    return 1,2
def make_report(a,b,c):
    print(a,b,c)
make_report(3, *calculate())
k = 3, *calculate()
print(k)