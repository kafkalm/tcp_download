#!/usr/bin/env python
#-*- coding:utf-8 -*-
def test(target):
    nums = [3,2,4]
    for i in range(len(nums)):
        need = target - nums[i]
        if need in nums:
            l = [i for i, x in enumerate(nums) if x == need]
            print(l)
            if len(l) > 1:
                return (l)
            elif i == l[0]:
                pass
            else:
                return ([i,l[0]])

def test_2(target):
    nums = [3, 3]
    d = {}
    for i in range(0,len(nums)):
        print(d)
        if target - nums[i] in d:
            return sorted([d[target-nums[i]],i])
        d[nums[i]]=i


print(test_2(6))