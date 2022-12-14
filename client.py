import banana_dev as banana
import json
import argparse
import base64 #
from io import BytesIO
import skimage.io #
from PIL import Image #
import time
# TODO = None
class Timer():
    def __init__(self,name):
        self.name = name
    def __enter__(self,):
        self.tic = time.time()
        pass
    def __exit__(self,*args,**kwargs):
        self.toc = time.time()
        self.elapsed = self.toc - self.tic
        print(f'time taken for {self.name} is {self.elapsed}')
        pass
def encodeBase64Image(image: Image) -> str:
    # https://stackoverflow.com/questions/31826335/how-to-convert-pil-image-image-object-to-base64-string
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str
def main(args):
    #===============================================
    # SECRETS
    with open('secrets.json','r') as f:
        secrets = json.load(f)
    api_key = secrets['API_KEY']
    model_key = secrets['MODEL_KEY']
    #===============================================
    # REQUEST
    image  = skimage.io.imread(args.impath)
    image = Image.fromarray(image)
    image_base64 = encodeBase64Image(image)
    request_json = {'image':image_base64,'video':args.video}
    model_inputs = request_json
    # model_inputs = {YOUR_MODEL_INPUT_JSON} # anything you want to send to your model
    #===============================================
    # RESPONSE
    with Timer('api call'):
        out = banana.run(api_key, model_key, model_inputs)
    model_outputs = out['modelOutputs']
    assert isinstance(model_outputs,list),f'expecting response["modelOutputs"] to be a list, found {model_outputs.__class__}'
    assert len(model_outputs) == 1, f'length of response["modelOutputs"] be 1, found {len(response["modelOutputs"])}'
    model_outputs = model_outputs[0]
    print(f'status:{model_outputs["message"]}')
    video_base64 = model_outputs['result']
    with open(args.output_path,'wb') as f:
        f.write(base64.b64decode(video_base64))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--impath',type=str,default='source.png',help='name of the image file')
    parser.add_argument('--output-path',type=str,default='result.mp4',help='save the motion transfered video as')
    parser.add_argument('--video',type=str,default='driving.mp4',help='name of the driving video (on the banana server)')
    args = parser.parse_args()
    main(args)
