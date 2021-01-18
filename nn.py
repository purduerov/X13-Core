import torch 
from torch import nn 
from matplotlib import pyplot as plt 
import numpy as np 
import torchvision as tv
import torch.nn.functional as F 
from lxml import etree 
import os
import pandas as pd 
import re 

def loadLabels():
    prefix = './labelled_images/'
    di = {}
    for xml in os.listdir(prefix):
        tree = etree.parse(prefix + xml)
        name = tree.findtext('./filename')
        name = int(re.findall(r'\d+', name)[0])
        xmin = int(tree.findtext('.//xmin'))
        ymin = int(tree.findtext('.//ymin'))
        xmax = int(tree.findtext('.//xmax'))
        ymax = int(tree.findtext('.//ymax'))
        #di[name] = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        di[name] = [xmin, ymin, xmax, ymax]
    return di

class NN(torch.nn.Module):
    def __init__(self):
        super(NN, self).__init__()

        self.conv1 = torch.nn.Conv2d(3, 3, (21,21))
        self.conv2 = torch.nn.Conv2d(3, 3, (11,11))
        self.conv3 = torch.nn.Conv2d(3, 1, (6,6))
        self.batch = torch.nn.BatchNorm1d(105*160)
        self.linear = torch.nn.Linear(105*160, 4)

    def forward(self, x):   # x now has shape (batchsize x 3 x 480 x 700)
        #print(x.shape)
        x = self.conv1(x)                   # x now has shape (batchsize x 3 x 460 x 680)
        x = F.relu(F.max_pool2d(x, 2)) # x now has shape (batchsize x 3 x 230 x 340)
        x = self.conv2(x)                   # x now has shape (batchsize x 3 x 220 x 330)
        x = F.relu(F.max_pool2d(x, 2)) # x now has shape (batchsize x 3 x 110 x 165)
        x = self.conv3(x) # x now has shape (batchsize x 1 x 105 x 160)
        x = self.batch(x.view(-1,105*160))
        x = self.linear(x)
        return x

batch_size=32
transform = tv.transforms.Compose([tv.transforms.ToTensor()])
images = tv.datasets.ImageFolder('./test_images/', transform=transform)

imageloader = torch.utils.data.DataLoader(images, batch_size=batch_size, shuffle=False)
images, _ = next(iter(imageloader))

labels = loadLabels() 
#df = pd.DataFrame(labels)
#df = df.reindex(sorted(df.columns), axis=1).T
#print(df)
order = [i for i in sorted(labels)]
ordered_labels = [labels[i] for i in order]


#print(images[0].shape)
plt.imshow(images[0].permute(1,2,0))
plt.show()

boi = NN()
optimizer = torch.optim.Adam(boi.parameters(), lr=.01)
nn_train_log = []
nn_train_counts = []
nn_test_losses = [] 
nn_test_counts = []

def nn_train(epoch):
    boi.train()
    for index, (images, _) in enumerate(imageloader):
        optimizer.zero_grad()
        targets = ordered_labels[index*batch_size:index*batch_size+len(images)]
        output = boi(images)
        print(output)
        print(targets)
        loss_out = F.l1_loss(output, torch.Tensor(targets), reduction="none")
        print(loss_out)
        loss_out = loss_out.sum(1).sum()
        loss_out.backward()
        optimizer.step()
        print()

        nn_train_log.append(loss_out.item())
        nn_train_counts.append( index*batch_size + (epoch-1)*len(imageloader.dataset) )
        if not (index % 2):
            print(f'Epoch {epoch}: [{index*len(images)}/{len(imageloader.dataset)}] Loss: {loss_out.item()}')

for epoch in range(1, 6):
    nn_train(epoch)

images, _ = next(iter(imageloader))
out = boi(images)
print(out[0])
x1, y1, x2, y2 = out[0]
plt.plot((x1, x1), (y1, y2))
plt.plot((x2, x2), (y1, y2))
plt.plot((x1, x2), (y1, y1))
plt.plot((x1, x2), (y2, y2))
plt.imshow(images[0].permute(1,2,0))
plt.show()