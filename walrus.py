"""
    Walrus operator can assign values to vars as a part of big expressseion
"""
# Earlier
string = 'String'
print(string)

# No way:
#print(string = 'New string') #TypeError: 'string' is an invalid keyword argument for print()

#Since python 3.8:
print(string := 'New string')
