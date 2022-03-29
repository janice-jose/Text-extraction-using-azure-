# <snippet_imports_and_vars>
# <snippet_imports>
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
#from PIL import Image
import sys
import time
# </snippet_imports>

'''
Authenticate
Authenticates your credentials and creates a client.
'''
# <snippet_vars>
subscription_key = "add your key"
endpoint = "add your endpoint"
# </snippet_vars>
# </snippet_imports_and_vars>

# <snippet_client>
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
# </snippet_client>
'''
END - Authenticate
'''

'''
Quickstart variables
These variables are shared by several examples
'''
# Images used for the examples: Describe an image, Categorize an image, Tag an image, 
# Detect faces, Detect adult or racy content, Detect the color scheme, 
# Detect domain-specific content, Detect image types, Detect objects
#images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")
# <snippet_remoteimage>
#remote_image_url = r"C:\Users\LENOVO\Documents\azure-computer-vision-main\harry.jpg"
# </snippet_remoteimage>
'''
END - Quickstart variables
'''


'''
OCR: Read File using the Read API, extract text - local
This example extracts text from a local image, then prints results.
This API call can also recognize remote image text (shown in next example, Read File - remote).
'''
print("===== Read File - local =====")
# Get image path
#read_image_path = os.path.join (images_folder, "printed_text.jpg")
# Open the image
read_image = open(r"C:\Users\LENOVO\Documents\azure-computer-vision-main\harry.jpg", "rb")

# Call API with image and raw response (allows you to get the operation location)
read_response = computervision_client.read_in_stream(read_image, raw=True)
# Get the operation location (URL with ID as last appendage)
read_operation_location = read_response.headers["Operation-Location"]
# Take the ID off and use to get results
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for the retrieval of the results
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status.lower () not in ['notstarted', 'running']:
        break
    print ('Waiting for result...')
    time.sleep(10)

# Print results, line by line
l=[]
if read_result.status == OperationStatusCodes.succeeded:
    
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            l.append(line.text)
            #print(line.bounding_box)
result=(' '.join(l))
print(result)
'''
END - Read File - local
'''

