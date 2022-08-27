'''
  ----------------------------------------------------------------------------------------
   NumberSage :: happybono@outlook.com (HappyBono)
  ----------------------------------------------------------------------------------------
 
   Presented On   http://www.happybono.net/
   C# .NET 사용자들을 위한 손글씨 인식 예시 소스 코딩 자료.
    
   Copyright (R) 2018 - 2022.          
 
   =======================================================================================
 
   외부 라이브러리에서 몇 가지 클래스를 참고하여 사용하였습니다.
   다음은 그 클래스 목록입니다.:
 
   Basic MNIST Example from GitHub, January, 2019 (Copyright by PyTorch).
   https://github.com/pytorch/examples/tree/master/mnist
'''


from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.onnx as onnx
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4*4*50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        '''
        It only has 1 channel as sample has only grayscale.
        Size of sample pictures are 28 x 28 pixels.

        학습 시킬 샘플들은 흑백 이미지의 데이터이므로 1 채널로 할당하고,
        제공되는 각 샘플들의 이미지 크기는 28 X 28 픽셀입니다.
        '''
        x = x.view(-1, 1, 28, 28)
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4*4*50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

# Train the neural network.
# Epochs stands for the number of times training data set used for machine training.  
# 학습 데이터로 학습 시킵니다.
# epochs 는 데이터 세트가 기계 학습에 사용된 횟수를 의미합니다.
def train(args, model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))

def test(args, model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item() # Sum up batch loss. (일괄 손실을 합산합니다.)
            pred = output.argmax(dim=1, keepdim=True) # Get the index of the max log-probability. (최대 로그 확률의 인덱스를 취득합니다.)
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

def main():

    # Machine Learning training settings.
    # 머신러닝 트레이닝 관련 설정.
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, default=10, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                        help='learning rate (default: 0.01)')
    parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                        help='SGD momentum (default: 0.5)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    
    parser.add_argument('--save-model', action='store_true', default=False,
                        help='For Saving the current Model')
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()

    torch.manual_seed(args.seed)

    device = torch.device("cuda" if use_cuda else "cpu")

    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

    # The training data is composed of pixel values of 0 to 255, which need to be converted to values of 0.01 to 1.0.
    # The computer needs to calculate the matrix multiplication by creating the data in a matrix, as that is easy to compute.
    # If the input value is 0, the calculation is not performed.
    # If the input value is 1 or greater, the created artificial neural network code will transform the input layer to three layers.
    # As the layers get deeper, the number increases greatly. So it goes through a normalization process called Normalize, to optimise performance.

    # 학습 데이터는 픽셀 값으로 이루어져 있으므로 값이 0 ~ 255 사이의 값인데 이걸 0.01 ~ 1.0 사이의 값으로 변환할 필요가 있습니다. 
    # 컴퓨터가 계산하기 쉬운 행렬로 데이터를 만들어서 행렬 곱 계산이 필요한데요.
    # 기본 입력값이 0 일 경우 아예 계산이 되지 않고, 
    # 1 보다 크면 현재 만드는 인공 신경망 코드는 계층을 3 계층으로 생성하지만, 계층이 깊어지면 숫자가 무한급수적으로 증가합니다.
    # 따라서 Normalize 라고 하는 정규화 과정을 거쳐 성능 최적화를 진행합니다.     
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data', train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=args.batch_size, shuffle=True, **kwargs)
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data', train=False, transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=args.test_batch_size, shuffle=True, **kwargs)


    model = Net().to(device)
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)

    for epoch in range(1, args.epochs + 1):
        train(args, model, device, train_loader, optimizer, epoch)
        test(args, model, device, test_loader)

    if (args.save_model):
        torch.save(model.state_dict(),"mnist_cnn.pt")
        x = torch.randint(255, (1, 28*28), dtype=torch.float).to(device) / 255
 
        # Save this into different format it works instead of .pt extension file type. (.onnx)
        # 호환성 관련 문제가 발생하지 않도록 .pt 확장자를 대체하는 다른 형식의 파일 (.onnx) 로 저장합니다.
        onnx.export(model, x, "mnist_cnn.onnx")
        print('Saved onnx model to {}'.format("mnist_cnn.onnx"))
        
if __name__ == '__main__':
    main()
