from torch import nn
import torch
# from thop import profile

'''
Build a LeNet-5 model with hyperparameters:
Continuous variable:
     Number of convolution kernels: dim = 2, search range [64, 512]
     
Discrete variable:
     Convolution kernel size: dim = 19, search range [3, 5, 7, 9]
     Activation function: dim = 10, range: relu, sigmoid, tanh
     Pooling type: dim = 2, range: average, max
'''


def conv3x3(in_channels, out_channels, stride=(1, 1)):
    """
    return 3x3 Conv2d
    """
    return nn.Conv2d(in_channels, out_channels, kernel_size=(3, 3), stride=stride, padding=1, bias=False)


def conv5x5(in_channels, out_channels, stride=(1, 1)):
    """
    return 5x5 Conv2d
    """
    return nn.Conv2d(in_channels, out_channels, kernel_size=(5, 5), stride=stride, padding=2, bias=False)


def conv7x7(in_channels, out_channels, stride=(1, 1)):
    """
    return 7x7 Conv2d
    """
    return nn.Conv2d(in_channels, out_channels, kernel_size=(7, 7), stride=stride, padding=3, bias=False)


def conv9x9(in_channels, out_channels, stride=(1, 1)):
    """
    return 9x9 Conv2d
    """
    return nn.Conv2d(in_channels, out_channels, kernel_size=(9, 9), stride=stride, padding=4, bias=False)

class LeNet5(nn.Module):
    def __init__(self, solution, num_classes=10):
        super(LeNet5, self).__init__()

        self.convlst = [conv3x3, conv5x5, conv7x7, conv9x9]
        self.actilst = [nn.ReLU(inplace=True), nn.Sigmoid(), nn.Tanh()]
        self.poollst = [nn.AvgPool2d(kernel_size = 2, stride = 2, padding=0),
                         nn.MaxPool2d(kernel_size = 2, stride = 2, padding=0)]

        self.conv1 = nn.Sequential(
            self.convlst[int(solution[6])](in_channels=3, out_channels=int(solution[0]), stride=(1, 1)),
            nn.BatchNorm2d(int(solution[0])),
            self.actilst[int(solution[8])],
            self.poollst[int(solution[10])]
        )
        self.conv2 = nn.Sequential(
            self.convlst[int(solution[7])](in_channels=int(solution[0]), out_channels=int(solution[1]), stride=(1, 1)),
            nn.BatchNorm2d(int(solution[1])),
            self.actilst[int(solution[9])],
            self.poollst[int(solution[11])],
            # nn.Flatten()
        )

        self.fc1 = nn.Sequential(
            nn.Linear(in_features= 8*8*int(solution[1]), out_features=int(solution[2])),
            nn.Dropout(p=solution[4])
        )
        self.fc2 = nn.Sequential(
            nn.Linear(in_features=int(solution[2]), out_features=int(solution[3])),
            nn.Dropout(p=solution[5])
        )
        self.fc3 = nn.Sequential(
            nn.Linear(in_features=int(solution[3]), out_features=num_classes)
        )

        self.solution = solution

    def forward(self, input):
        conv1_output = self.conv1(input)
        conv2_output = self.conv2(conv1_output)
        conv2_output = conv2_output.view(conv2_output.size(0), -1)
        fc1_output = self.fc1(conv2_output)
        fc2_output = self.fc2(fc1_output)
        fc3_output = self.fc3(fc2_output)
        return fc3_output

if __name__ == "__main__":

    solution = [6, 16, 120, 84, 0, 0,   # 神经元数量
                1, 1,   # 卷积类型
                0, 0,   # 激活函数类型
                0, 0,  # 池化函数类型
                ]
    model = LeNet5(solution)
    input = torch.randn(1, 3, 32, 32)
    # flops, params = profile(model, inputs=(input,))
    print(flops / 1e9, params / 1e6)
    # print(model)