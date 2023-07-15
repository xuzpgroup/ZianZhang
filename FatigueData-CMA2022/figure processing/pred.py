from __future__ import print_function, division
import torch
from torchvision import models, transforms
import os
from PIL import Image
import json
import scipy.io as scio

class myDataset(object):
    def __init__(self,path,figures, transforms):
        self.transforms = transforms
        self.path=path      
        self.figures=figures
        
    def __getitem__(self, idx):
        img = Image.open(os.path.join(self.path,self.figures[idx])).convert("RGB")  
            
        if self.transforms is not None:
            img = self.transforms(img)

        return img, self.figures[idx]

    def __len__(self):
        return len(self.figures)


data_transforms = {
    'pred': transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

if __name__ == '__main__':

    figpath='./example/'
    figures=['class_fatigue1.jpg','class_fatigue2.jpg','class_nonfatigue1.jpg','class_nonfatigue2.jpg']

    dataset = myDataset(figpath,figures, data_transforms['pred'])
    dataloaders = {'pred': torch.utils.data.DataLoader(dataset)}
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    
    model = models.resnet50(pretrained=True)
    model.load_state_dict(torch.load('best.pth'))
    model.eval()
    data=[]
    with torch.no_grad():
        for i, (input, name) in enumerate(dataloaders['pred']):
            input = input.to(device)
            output = model(input)
            _, pred = torch.max(output, 1)
            data.append([str(name),int(pred)])

    with open('pred.json','w') as f:
        json.dump(data,f)
