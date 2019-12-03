import time
import io
import torch
from PIL import Image
import torchvision
from models import detection
import json
from tempfile import SpooledTemporaryFile # To compare path for Jsonization
draw_confidence_threshold = 0.7


to_tensor = torchvision.transforms.ToTensor()
convert_to_pil = torchvision.transforms.ToPILImage()


class LINC_detector():
    def __init__(self, model_path, cuda_wanted = False):
        # Init modules
        print('Loading checkpoint from hardrive... ', end='', flush=True)
        print(f"CUDA desired={cuda_wanted}")
        has_cuda = torch.cuda.is_available()
        print("CUDA available?=", has_cuda)
        self.device = 'cuda' if has_cuda and cuda_wanted else 'cpu'
        print(f"Running inference on {self.device} device")
        print('Building model and loading checkpoint into it... ', end='', flush=True)
        checkpoint = torch.load(model_path, map_location=self.device)
        self.label_names = checkpoint['label_names']
        model = detection.fasterrcnn_resnet50_fpn(
            num_classes=len(self.label_names) + 1, pretrained_backbone=False
        )
        model.to(self.device)
        model.load_state_dict(checkpoint['model'])
        self.model = model.eval()
        print('Init done.')


    def detect(self, image_paths, image_names, conf_threshold):
        # Run detection
        with torch.no_grad():
            
            for image_path, image_name in zip(image_paths, image_names):
                
                print('Loading image... ', end='', flush=True)
                #print(f"Device {self.device}")
                #print(f"Sent Image Path{image_path}")
                pil_image = Image.open(image_path)
                img_mode = pil_image.mode
                img_size = pil_image.size
                image = to_tensor(pil_image).to(self.device)
                print('Running image through model... ', end='', flush=True)
                tic = time.time()
                outputs = self.model([image])
                toc = time.time()
                time_taken = toc - tic
                print(f'Done in {toc - tic:.2f} seconds!')
                print(f'Saving results to file... ', end='', flush=True)
                image_dict = {'boxes': []}
                for i, score in enumerate(outputs[0]['scores']):
                    if score > conf_threshold:
                        box = outputs[0]['boxes'][i]
                        label = outputs[0]['labels'][i]
                        image_dict['boxes'].append({
                            'conf': float(score), 
                            'class': int(label), 
                            'ROI': box.tolist()
                        })
                # Check for real path
                if type(image_path) != SpooledTemporaryFile:
                    image_dict['path'] = image_path
                image_dict['size'] = img_size
                image_dict['depth'] = img_mode
                image_dict['name'] = image_name
                print('Done.')
        #print(json.dumps(image_dict))
        return image_dict, time_taken 


if __name__ == '__main__':
    pass 
