import torch
import matplotlib.pyplot as plt

net = torch.nn.Linear(32, 32)

x = torch.ones(32)
y = torch.zeros(32)

result = net(x)

print(result)

print(net.weight.grad)

loss = torch.mean((result - y) ** 2)
loss.backward()

print(net.weight.grad)

fig, ax = plt.subplots()
im = ax.imshow(net.weight.grad)

plt.show()