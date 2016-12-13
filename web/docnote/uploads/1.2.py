#author : 1140310209
#the temperature should not less than absolute zero
#I used to use python3 , and to be compatible with python3 , I use "print(val)" instead of "print val" 

try:
	cmd=int(input())
except Exception:
	print("Error")
	exit(0)
if cmd!=1 and cmd!=2:
	print("Error")
	exit(0)
if cmd==1:
	try:
		t=float(input())
	except Exception:
		print("Error")
		exit(0)
				
	if t<-459.67:#-459.67 is absolute zero in Fahrenheit
		print("Error")
	else:
		print("%.2lf"%(5.0*(t-32.0)/9.0))
if cmd==2:
	try:
		t=float(input())
	except Exception:
		print("Error")
		exit(0)
		
	if t<-273.15:#-273.15 is absolute zero in Celsius temperature scale
		print("Error")
	else:
		print("%.2lf"%(9.0*t/5.0+32.0))
