import torch
from torch import nn
# from thop import profile


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

class AlexNet(nn.Module):
    def __init__(self, solution, num_classes=10):
        super(AlexNet, self).__init__()

        self.convlst = [conv3x3, conv5x5, conv7x7, conv9x9]
        self.actilst = [nn.ReLU(inplace=True), nn.Sigmoid(), nn.Tanh()]
        self.poollst = [nn.AvgPool2d(kernel_size=2, stride=2, padding=0),
                        nn.MaxPool2d(kernel_size=2, stride=2, padding=0)]

        self.features = nn.Sequential(
            self.convlst[int(solution[9])](in_channels=3, out_channels=int(solution[0]), stride=(1, 1)),
            nn.BatchNorm2d(int(solution[0])),
            self.actilst[int(solution[14])],
            self.poollst[int(solution[19])],

            self.convlst[int(solution[10])](in_channels=int(solution[0]), out_channels=int(solution[1]), stride=(1, 1)),
            nn.BatchNorm2d(int(solution[1])),
            self.actilst[int(solution[15])],
            self.poollst[int(solution[20])],

            self.convlst[int(solution[11])](in_channels=int(solution[1]), out_channels=int(solution[2]), stride=(1, 1)),
            nn.BatchNorm2d(int(solution[2])),
            self.actilst[int(solution[16])],

            self.convlst[int(solution[12])](in_channels=int(solution[2]), out_channels=int(solution[3]), stride=(1, 1)),
            nn.BatchNorm2d(int(solution[3])),
            self.actilst[int(solution[17])],

            self.convlst[int(solution[13])](in_channels=int(solution[3]), out_channels=int(solution[4]), stride=(1, 1)),
            nn.BatchNorm2d(int(solution[4])),
            self.actilst[int(solution[18])],
            self.poollst[int(solution[21])],
        )

        self.avgpool = nn.AdaptiveAvgPool2d((6,6))

        self.fc = nn.Sequential(

            nn.Dropout(solution[7]),
            nn.Linear(int(solution[4]) * 6 * 6, int(solution[5])),
            nn.ReLU(True),

            nn.Dropout(solution[8]),
            nn.Linear(int(solution[5]), int(solution[6])),
            nn.ReLU(True),

            nn.Linear(int(solution[6]), num_classes),
        )

    def forward(self, input):
        out = self.features(input)
        out = self.avgpool(out)
        out = torch.flatten(out, 1)
        out = self.fc(out)

        return out



if __name__ == "__main__":

    solution = [ 64, 192, 384, 256, 256, 512, 512, 0.5, 0.5, # 神经元数量 0-8
                 3, 1, 0, 0, 0, # 卷积类型 9-13
                 0, 0, 0, 0, 0, # 激活函数类型 14-18
                 0, 0, 0, # 池化函数类型 19-21
                ]
    # model = AlexNet(solution)
    # input = torch.randn(1, 3, 32, 32)
    # flops, params = profile(model, inputs=(input,))
    # print(flops / 1e9, params / 1e6)
    # print(model)