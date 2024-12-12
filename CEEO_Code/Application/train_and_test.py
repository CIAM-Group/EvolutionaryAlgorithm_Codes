import numpy as np
import pandas as pd
import torch
import time


from torch import nn
from buildLeNet5 import LeNet5
from buildAlexNet import AlexNet
from torch.utils.data import DataLoader, random_split
from torchvision.transforms import ToTensor, Compose, RandomCrop, RandomHorizontalFlip, Normalize
from torchvision import datasets


def train(epoch, num_epochs, dataloader, model, loss_fn, optimizer, device):

    model.train()

    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # 计算损失
        pred = model(X)
        loss = loss_fn(pred, y)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 每隔100个batch打印一次loss
        if (batch + 1) % 50 == 0 or (batch + 1) == len(dataloader):
            print(
                "Epoch [{}/{}], Step [{}/{}] Loss: {:.4f}".format(epoch + 1, num_epochs, batch + 1, len(dataloader),
                                                                  loss.item()))


def test(dataloader, model, loss_fn, device):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)

    model.eval()

    test_loss, correct = 0, 0

    with torch.no_grad():
        for (X, y) in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y)
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
    correct /= size

    print("Test Error: \n Accuracy: {:>1f}, Avg loss:{:>8f} \n".format(correct, test_loss))

    return correct, test_loss.cpu().numpy()


def main():
    acc_loss_file = "results/AlexNet_cifar100_optimal_SHEALED.txt" #LeNet5

    # 导入最优解
    op_data = pd.read_csv("results/SHEALED_cifar10_AlexNet_samples.csv")

    best_ind2 = np.argmax(op_data.values[:200, -2])

    op_solution = op_data.values[best_ind2, :-2]
    print(op_data.values[best_ind2, -2])



    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 模型损失优化器
    loss_fn = nn.CrossEntropyLoss()


    # print(op_solution)
    # input = torch.randn(1,3,32,32)

    # model = LeNet5(op_solution, num_classes=100).to(device)

    model = AlexNet(op_solution, num_classes=100).to(device)

    # flops, params = profile(model, inputs=(input, ))
    # print(flops/1e9, params/1e6)
    # exit(0)



    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4)

    # 训练数据
    batchsize = 512
    transform_train = Compose([
        # 对原始32*32图像四周各填充4个0像素（40*40），然后随机裁剪成32*32
        RandomCrop(32, padding=4),
        # 按0.5的概率水平翻转图片
        RandomHorizontalFlip(p=0.5),
        ToTensor(),
        Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.2023, 0.1994, 0.2010])
    ])

    training_data = datasets.CIFAR100(root="datasets", train=True, download=False, transform=transform_train)
    train_loader = DataLoader(training_data, batch_size=batchsize, shuffle=True)

    # 测试数据
    transform_test = Compose([
        ToTensor(),
        Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.2023, 0.1994, 0.2010])
    ])

    test_data = datasets.CIFAR100(root="datasets", train=False, download=False, transform=transform_test)
    test_loader = DataLoader(test_data, batch_size=batchsize)

    # 训练模型
    num_epochs = 200
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, [80, ], gamma=0.1, last_epoch=-1)
    initc = 0
    for t in range(num_epochs):

        print(f"Epoch {t + 1}\n-------------------------------")
        train(t, num_epochs, train_loader, model, loss_fn, optimizer, device)

        correct, test_loss = test(test_loader, model, loss_fn, device)
        with open(acc_loss_file, "a+") as f:
            f.write(str(correct) +"," + str(test_loss) + "," + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\r")

        scheduler.step()

        # 模型保存
        if (t + 1  == 200):
            torch.save(model.state_dict(), "checkpoints/AlexNet_cifar100_last_model_SHEALED.pth")
            print("Saved last Model State!")

        # save the best
        if (correct > initc):
            torch.save(model.state_dict(), "checkpoints/AlexNet_cifar100_best_model_SHEALED.pth")
            print("Saved current best Model State!")
            initc = correct

    print("Done!")


if __name__ == "__main__":
    main()
