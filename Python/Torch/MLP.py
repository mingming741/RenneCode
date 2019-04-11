from torch.utils.data import TensorDataset, DataLoader
from torch.nn import CrossEntropyLoss
from torch.optim import SGD, Adam
from torch.optim.lr_scheduler import LambdaLR
from collections import OrderedDict


class MLPClassifier(object):
    def __init__(self, nlayer, nhiddenlinkage, activationfun="ReLU"):
        """ 
        nlayer: int
            total number of linear layer, each layer will followed by a activation function exception the last layer
        nhiddenlinkage: tuple
            in-degree for each layer, the last layer out degree is 2
        activationfun: str {"Tanh", "ReLU", "Sigmoid"}
            activation function for all layer
        """
        self._nlayer = nlayer
        self._nhiddenlinkage = nhiddenlinkage # tuple
        self._enc = None
        if activationfun == "Tanh":
            self._activationfun = nn.Tanh()
        if activationfun == "ReLU":
            self._activationfun = nn.ReLU(True)
        if activationfun == "Sigmoid":
            self._activationfun = nn.Sigmoid()

        if nlayer < 1:
            raise Exception("We need at list one layer")
        if nlayer != len(nhiddenlinkage):
            raise Exception("size of hiddenlinkage should equals to number of layer")
        
        d = {}
        for i in range(1, nlayer):
            d[str(i*2-1)] = nn.Linear(nhiddenlinkage[i-1], nhiddenlinkage[i])
            d[str(i*2)] = self._activationfun
        d[str(nlayer*2-1)] = nn.Linear(nhiddenlinkage[nlayer-1], 2)
        
        self._module = nn.Sequential(OrderedDict(d))


    def fit(self,
            data,
            label,
            lr=0.1,
            alg='sgd',
            epoch=10,
            bs=16,
            verbose=True):
        # encode label
        enc = LabelEncoder()
        label = enc.fit_transform(label)
        self._enc = enc
        
        tdtype = torch.get_default_dtype()
        data = torch.tensor(data).to(dtype=tdtype)
        label = torch.tensor(label).to(dtype=torch.int64)
        
        ds = TensorDataset(data, label)
        dl = DataLoader(ds, batch_size=bs, shuffle=True, drop_last=True)

        lossfunc = CrossEntropyLoss()

        if alg == 'sgd':
            optim = SGD(self._module.parameters(), lr=lr, momentum=0.9)
        else:
            optim = Adam(self._module.parameters(), lr=lr)

        lr_schdl = LambdaLR(optim, lambda ep: 1 / (1 + ep))
        
        self._losses = []
        for ep in range(epoch):
            it = 0
            lr_schdl.step()
            for d, t in dl:
                pred = self._module(d)
                loss = lossfunc(pred, t)

                optim.zero_grad()
                loss.backward()
                optim.step()

                loss_val = loss.item()
                self._losses.append(loss_val)

                if verbose:
                    print("Epoch: {}, Iteration: {}, Loss: {}".format(
                        ep, it, loss_val))
                    it += 1


    def predict(self, data):
        tdtype = torch.get_default_dtype()
        data = torch.tensor(data).to(dtype=tdtype)
        with torch.no_grad():
            pred = self._module.forward(data)
            pred = pred.argmax(dim=1)
            pred = pred.numpy()
        pred = self._enc.inverse_transform(pred)
        return list(pred)
