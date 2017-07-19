import json
from scipy.interpolate import interp1d
from jsonsempai import magic
import gun1
import gun2
import io



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
			#writeFile(testoutputjson,l)       	
			# print testoutputjson['values']
			# return 0

input1 = getList(gun1)
input2 = getList(gun2)

input1_new = []
# input1_new = list(input1)
print len(input1[0])
for i in input1:
	for j in range(len(i)):
		i[j] = list(i[j])

for i in input2:
	for j in range(len(i)):
		i[j] = list(i[j])

#calculating linear interp for each curve in input2
# for n in range(len(input2)):
# 	nx = [i[0] for i in input2[n]]
# 	ny = [i[1] for i in input2[n]]
# 	input2_interp = interp1d(nx,ny)
# 	input2[n]=[]
# 	for m in range(len(input1[n])):
# 		input2[n].append((input1[n][m][0],float(input2_interp(input1[n][m][0]))))

# N=3
# a = []
# for k in range(len(input1)):
# 	a.append(interpolation(input1[k],input2[k],N))
	
# updateList(a)
# print "\na = ",a[0]