# Красивое лучше чем уродливое
# Nested loops makes the worst readability
# product() can reduce the code:

# bad practice:
list_x = [1, 2020, 70]
list_y = [2, 4, 7, 2000]
list_z = [3, 70, 7]
for x in list_x:
    for y in list_y:
        for z in list_z:
            if (x + y + z) == 2077:
                print(x, y, z)

