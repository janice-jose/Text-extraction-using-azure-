from flask import Flask, render_template, request, redirect,send_from_directory
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import time
import requests
import os
from dotenv import load_dotenv
load_dotenv()

subscription_key = os.getenv('subscription_key')
endpoint = os.getenv('endpoint')
computervision_client = ComputerVisionClient(endpoint,CognitiveServicesCredentials(subscription_key))

def extractTextFromImage(read):
    #print(read)
    #read_image = open(read, "rb")
    # Call API with image and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(read, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        
        time.sleep(5)
    l=[]
    if read_result.status == OperationStatusCodes.succeeded:
        
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                l.append(line.text)
                #print(line.bounding_box)
    result=(' '.join(l))
    return result
        
    

app = Flask(__name__)

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        file = request.files['i_remote']
        #read image file string data
    """npimg = numpy.fromstring(file, numpy.uint8)
    # convert numpy array to image
    img = cv2.imdecode(npimg, cv2.CV_LOAD_IMAGE_UNCHANGED)
    #convert string data to numpy array"""
    #print("file path is as follows",file)
    result = extractTextFromImage(file)
    return render_template("index.html", prediction = result)
    #, img_path = image_url


if __name__ == '__main__':
    app.run(debug=True)   

 


