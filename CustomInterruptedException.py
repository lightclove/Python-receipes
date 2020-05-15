class CustomInterruptedException(Exception):
   print "ok"
   pass


# try:
#    val = int(input("input positive number: "))
#    if val < 0:
#        raise CustomInterruptedException("Neg val: " + str(val))
#    print(val + 10)
# except CustomInterruptedException as c:
#   print(c)