import os
import time
from datetime import datetime, timedelta
from subprocess import Popen, PIPE, STDOUT
from Queue import Queue, Empty
from PIL import Image
from flask import Flask, request, jsonify, session
from threading import Thread

app = Flask(__name__)
mapper = {}
ftime = None
stime = None

@app.route('/start', methods=['GET', 'POST'])
def start():
	# Change the thresh to increase or decrease confidence, 0.6 ~ 60% confidence 

	cmd = './darknet detector test cfg/tic-obj.data cfg/tic-test-yolov3.cfg backup/tic-train-yolov3_5000.weights'
	proc = Popen(cmd.split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=False)

	while True:
		line = proc.stdout.readline()
		#print line
		if line == '' and proc.poll() is not None:
			break
		else:
			if line.rstrip() == 'Enter Image Path:':
				#print "break"
				break
	mapper['proc'] = proc
	stime = datetime.now()
	return "Init Done"



@app.route('/getPredictions', methods=['GET', 'POST'])
def getPredictions():
	proc = mapper['proc']
	print "asd"
	result = {}
	r = request.get_json(force=True)
	imageWidth = int(r['imageWidth']) 
	imageHeight = int(r['imageHeight'])
	image_string = r['image_string'] 
	imageID = r['imageID'] 
	im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string.decode('base64')) 
	imageName = "./input_image/input_"+str(imageID)+".png" 
	im.save(imageName)
	result['boardFound'] = False	
	proc.stdin.write(imageName+"\n")
	proc.stdin.flush()
	
	result = {}
	result["boardFound"] = False
	result["objects"] = [] 
	dic = {} 

	while True:
		line = proc.stdout.readline()
		if line == '' and proc.poll() is not None:
			break
		else:
			if line.rstrip() == 'Enter Image Path:':
				proc.stdout.flush()
				break				
				#	centroidX = (int(boundingBox[3]) - int(boundingBox[2])) / 2 + int(boundingBox[2])
				#	centroidY = (int(boundingBox[1]) - int(boundingBox[0])) / 2 + int(boundingBox[0])
				#	result['moveX'] = centroidX - 320
				#	result['moveY'] = 240 - centroidY
			else:
				#print "=> : ", line
				result['boardFound'] = True
				
				if '%' in line:
					label = line.split(':')[0] 
					dic["label"] = label 
					confidence = int(line.split(":")[1].replace('%', '').strip()) 
					dic["confidence"] = confidence 

				if "Bounding Box" in line: 
					cords = line.split(':')[1] 
					cords = cords.split(',') 
					for cord in cords: 
						key, value = cord.strip().split('=') 
						dic[key] = int(value)
					result["objects"].append(dic) 
					dic = {}
				proc.stdout.flush()
	print "Processed image, "+imageName+"\t", result
	return jsonify(result)
	
if __name__ == '__main__':
	app.run(host='0.0.0.0',threaded=True, port=5000, debug=True)				

