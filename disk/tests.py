from django.test import TestCase
import os
# Create your tests here.


L=[]
for filename in os.listdir(r'/home/work/xusiwei/projects/evaluationPlatform/upload'):
    print filename
    L.append(filename)
print L
