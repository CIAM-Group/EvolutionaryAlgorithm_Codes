import torch, os
from torch import nn
from Application.buildLeNet5 import LeNet5

from Application.buildAlexNet import AlexNet
from torch.utils.data import DataLoader, random_split
from torchvision.transforms import ToTensor, Compose, Normalize
from torchvision import datasets


os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def evaluationLeNet5(solution, num_epochs):

    device = "cuda" if torch.cuda.is_available() else "cpu"

    transform_train = Compose([
        ToTensor(),
    ])

    # 导入训练数据
    training_data = datasets.CIFAR10(root="datasets", train=True, download=True, transform=transform_train)
    size = len(training_data)

    # 划分训练,验证集
    train_size = int(0.9 * size)
    val_size = size - train_size
    torch.manual_seed(1)
    train_set, val_set = random_split(training_data, [train_size, val_size])

    # 模型
    model = LeNet5(solution, num_classes=10).to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)

    # 模型训练
    train_loader = DataLoader(train_set, batch_size=512, shuffle=True)

    for epoch in range(num_epochs):
        model.train()
        for batch, (X, y) in enumerate(train_loader):
            X, y = X.to(device), y.to(device)

            # 计算损失
            pred = model(X)
            loss = loss_fn(pred, y)

            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    # 模型验证
    val_loader = DataLoader(val_set, batch_size=100)
    num_batches = len(val_loader)
    model.eval()
    val_loss, correct = 0, 0
    with torch.no_grad():
        for (X, y) in val_loader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            val_loss += loss_fn(pred, y)
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    avg_val_loss = val_loss / num_batches
    val_accuracy = correct / val_size

    print("Accuracy: {:>1f}, Avg loss:{:>8f} \n".format(val_accuracy, avg_val_loss.cpu().numpy()))

    return val_accuracy, avg_val_loss.cpu().numpy()


def evaluationAlexNet(solution, num_epochs):

    device = "cuda" if torch.cuda.is_available() else "cpu"

    transform_train = Compose([
        ToTensor(),
        Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
    ])

    # 导入训练数据
    training_data = datasets.CIFAR10(root="datasets", train=True, download=True, transform=transform_train)
    size = len(training_data)

    # 划分训练,验证集
    train_size = int(0.9 * size)
    val_size = size - train_size
    torch.manual_seed(1)
    train_set, val_set = random_split(training_data, [train_size, val_size])

    # 模型
    model = AlexNet(solution, num_classes=10).to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)

    # 模型训练
    train_loader = DataLoader(train_set, batch_size=512, shuffle=True)

    for epoch in range(num_epochs):
        model.train()
        for batch, (X, y) in enumerate(train_loader):
            X, y = X.to(device), y.to(device)

            # 计算损失
            pred = model(X)
            loss = loss_fn(pred, y)

            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    # 模型验证
    val_loader = DataLoader(val_set, batch_size=100)
    num_batches = len(val_loader)
    model.eval()
    val_loss, correct = 0, 0
    with torch.no_grad():
        for (X, y) in val_loader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            val_loss += loss_fn(pred, y)
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    avg_val_loss = val_loss / num_batches
    val_accuracy = correct / val_size

    print("Accuracy: {:>1f}, Avg loss:{:>8f} \n".format(val_accuracy, avg_val_loss.cpu().numpy()))

    return val_accuracy, avg_val_loss.cpu().numpy()


# if __name__ == "__main__":
    # solution = [6, 16, 120, 84, 0, 0, # 神经元数量
    #             1, 1,  # 卷积类型
    #             0, 0,  # 激活函数类型
    #             0, 0,  # 池化函数类型
    #             ]

    # solution1 = [64, 192, 384, 256, 256, 512, 512, 0.5, 0.5,  # 神经元数量 0-8
    #             3, 1, 0, 0, 0,  # 卷积类型 9-13
    #             0, 0, 0, 0, 0,  # 激活函数类型 14-18
    #             0, 0, 0,  # 池化函数类型 19-21
    #             ]


    # evaluationLeNet5(solution, 10)
    # evaluationAlexNet(solution1, 10)








