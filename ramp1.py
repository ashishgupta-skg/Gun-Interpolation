import json
from scipy.interpolate import interp1d
from jsonsempai import magic
import gun1
import gun2
import io
import pprint


try:
    to_unicode = unicode
except NameError:
    to_unicode = str

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def writeFile(testoutputjson,files):
    with io.open('data%d.json' % files, 'w', encoding='utf8') as outfile:
         # outJson = json.dumps(testoutputjson)
         outfile.write(unicode(json.dumps(testoutputjson, ensure_ascii=False)))

def getList (testoutputjson):
    k = []
    curveName = ""
    for n in range(0,len(testoutputjson.values)):
    	# extracting values of type ramp
        if testoutputjson.values[n].type == "Ramp":
            # k += 1
            curveName = testoutputjson.values[n].name
            curvePoints = testoutputjson.values[n].val
            pos = []
            value = []
            #iterating next 15 values after ramp type for points pos,valus
            for point in range(0,curvePoints*3+1):
            	pointName = testoutputjson.values[n+point].name
            	# print pointName
            	if pointName[-3:] == "pos":
            		pos.append(testoutputjson.values[n+point].val)
            	elif pointName[-3:] == "lue":
            		value.append(testoutputjson.values[n+point].val)
            myList = zip(pos,value)
            k.append(myList)
    return k

def interpolation(shape1,shape2,nShapes):
	# nShapes=3
	nPoints = len(shape1)
	# print nPoints
	N = [[] for _ in xrange(nShapes)]
	# print N
	for i in xrange(nShapes):
		i=i+1
		for j in xrange(nPoints):
			y1 = shape1[j][1]
			y2 = shape2[j][1]
			dy = (y2-y1)/(nShapes+1)

			xN = shape1[j][0]
			yN = y1 + i*dy

			N[i-1].append([xN,yN])
	return N

def updateList (interpShape):
    k = []
    curveName = ""
    for l in range(0,len(interpShape)):
    	with open('gun1.json', 'r') as f:
    		testoutputjson = json.load(f)
	    	# print "l=",l
	    	ramp = -1
	    	# print "flag2"
	    	# print "length = ",len(testoutputjson.values)
	    	for n in range(0,len(testoutputjson['values'])):
	    		if testoutputjson['values'][n]['type'] == "Ramp":
	    			ramp += 1
	    			curvePoints = testoutputjson['values'][n]['val']
	    			for point in range(0,curvePoints*3+1):
	    				pointName = testoutputjson['values'][n+point]['name']
	    				print testoutputjson['values'][n+point]['val']	
	    				print pointName,pointName[-4],pointName[-3:]
	    				if (pointName[-3:] == "pos") and (pointName[-4] == "1"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][0][0]
	    				if (pointName[-3:] == "pos") and (pointName[-4] == "2"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][1][0]
	    				if (pointName[-3:] == "pos") and (pointName[-4] == "3"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][2][0]
	    				if (pointName[-3:] == "pos") and (pointName[-4] == "4"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][3][0]
	    				if (pointName[-3:] == "pos") and (pointName[-4] == "5"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][4][0]
	    				if pointName[-5:] == "value" and (pointName[-6] == "1"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][0][1]
	    				if pointName[-5:] == "value" and (pointName[-6] == "2"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][1][1]
	    				if pointName[-5:] == "value" and (pointName[-6] == "3"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][2][1]
	    				if pointName[-5:] == "value" and (pointName[-6] == "4"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][3][1]
	    				if pointName[-5:] == "value" and (pointName[-6] == "5"):
	    					testoutputjson['values'][n+point]['val'] = interpShape[l][ramp][4][1]
	    				print testoutputjson['values'][n+point]['val']
			writeFile(testoutputjson,l)       	
			# print testoutputjson['values']
			# return 0
def interpList(inputList):
	nx = [i[0] for i in inputList]
	ny = [i[1] for i in inputList]
	return nx,interp1d(nx,ny)

def getYvalue(mylist,interp):
	out = []
	for i in range(len(mylist)):
		out.append([mylist[i],interp(mylist[i])])
	return out

def completeList(nx1,nx2):
	for i in range(len(nx1)):
		if (nx1[i] in nx2) == True:
			continue
		else:
			nx2.append(nx1[i])

	for i in range(len(nx2)):
		if (nx2[i] in nx1) == True:
			continue
		else:
			nx1.append(nx2[i])
	nx2.sort()
	nx1.sort()
	return nx1,nx2

def combineandinterpolate(list1,list2):
	nx1,interp1 = interpList(list1)
	nx2,interp2 = interpList(list2)
	nx1,nx2 = completeList(nx1,nx2)
	list1 = getYvalue(nx1,interp1)
	list2 = getYvalue(nx2,interp2)
	return list1, list2


input1 = getList(gun1)
input2 = getList(gun2)

# converting tuple to list
print len(input1[0])
for i in input1:
	for j in range(len(i)):
		i[j] = list(i[j])

for i in input2:
	for j in range(len(i)):
		i[j] = list(i[j])

# extending both input curve to (0.0,1.0)
for i in input1:
	i[0][0] = 0.0
	i[-1][0] = 1.0
for i in input2:
	i[0][0] = 0.0
	i[-1][0] = 1.0



print "Curves in Input1 = ",len(input1)
print "Curves in Input2 = ",len(input2)

input1_new = []
input2_new = []
for i in range(len(input1)):
	L1 = input1[i]
	L2 = input2[i]
	L1,L2 = combineandinterpolate(L1,L2)
	input1_new.append(L1)
	input2_new.append(L2)

N=4
a = []
for k in range(len(input1_new)):
	a.append(interpolation(input1_new[k],input2_new[k],N))
	
pprint.pprint(input1_new[0])
print "\n"
pprint.pprint(input2_new[0])
print "\n"
pprint.pprint(a[0])