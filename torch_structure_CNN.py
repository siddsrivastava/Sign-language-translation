import torch as th
#NN API
import torch.nn as nn
import torch.nn.functional as F
import torch.autograd as autograd
import torch.optim as optim
#DATA
from torch.utils.data import DataLoader 
from torchvision import transforms, datasets
import torchvision.transforms as transforms

#load data 
datadir = r'C:\Users\Admin\Desktop\Sign_language_translation\train\train'
transform = transforms.Compose([transforms.Resize(255),
                                transforms.CenterCrop(224),
                                transforms.ToTensor()])
dataset = datasets.ImageFolder(datadir, transform=transform)
trainloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
images, label = next(iter(trainloader))

#DATA NOT LOADING PROPERLY REQUIRES FIX


class Model(nn.Module):
  def __init__(self):
    super(Model, self).__init__()
    self.conv1 = nn.Conv2d(3, 6, 3)    #(in_filters, out_filters, kernel_shape)
    self.pool1 = nn.MaxPool2d(2,2)
    self.conv2 = nn.Conv2d(6, 10, 3)
    self.pool2 = nn.MaxPool2d(2,2)
    self.fc1 = nn.Linear(-1, 120)
    self.fc2 = nn.Linear(-1, 26)
    
  def forward(self, x):
    x = self.pool(F.relu(self.conv1(x)))
    x = self.pool(F.relu(self.conv2(x)))
    x = x.view(-1, -1)
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    return x
  
model = Model()

#LOSS
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.003, momentum=0.9)


#TRAIN
for epoch in range(2):
  running_loss = 0.0
  for i, data in enumerate(trainloader,0):
    inputs, label = data
    optimizer.zero_grad()
    
    outputs = model(inputs)
    loss = criterion(outputs,labels)
    loss.backward()
    optimizer.step()
    running_loss += loss.item()
    if i % 2000 == 1999:   # print every 2000 mini-batches
      print('[%d, %5d] loss: %.3f' %
      (epoch + 1, i + 1, running_loss / 2000))
      running_loss = 0.0

print('Finished Training')
