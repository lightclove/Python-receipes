import random
import time
from timeThis import timeThis


nums = []
for i in range(10000): nums.append(random.randint(0, 1000))

@timeThis
def bubbleSort(nums):
    n = 1
    while n < len(nums):
        for i in range(len(nums) - n):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
        n += 1
    return nums

def quickSort(nums):
   if len(nums) <= 1:
       return nums
   else:
       q = random.choice(nums)
       s_nums = []
       m_nums = []
       e_nums = []
       for n in nums:
           if n < q:
               s_nums.append(n)
           elif n > q:
               m_nums.append(n)
           else:
               e_nums.append(n)
       return quickSort(s_nums) + e_nums + quickSort(m_nums)

# bubbleSort(nums)

start = time.time()
# nums = quickSort(nums)
nums.sort()
end = time.time()
print(end-start)
print(nums)