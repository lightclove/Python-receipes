fileList = open("File2List.txt", 'r+')
# генерируем список из файла где названия процессов идут списком строк, разделенных \n (т.е. в столбец)
yourResult = [line[0:len(line)-1] for line in fileList.readlines()] #line[0:len(line)-1] - убирает последние 2 символа \n
fileList.close()
print(yourResult)
