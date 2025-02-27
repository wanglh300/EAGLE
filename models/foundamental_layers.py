import torch
import torch.nn as nn
import torch.nn.functional as F  

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1 or classname.find('Conv') != -1:
        nn.init.constant_(m.weight, 0)
        nn.init.normal_(m.bias, 0, 0.01)


class ConcatLinear_v2(nn.Module):  
    def __init__(self, dim_in, dim_out, dim_c):  
        super(ConcatLinear_v2, self).__init__()  
        self._layer = nn.Linear(dim_in, dim_out)  
        self._hyper_bias = nn.Linear(1 + dim_c, dim_out, bias=False)  
        self._adaptive_bias_scale = nn.Parameter(torch.ones(1))  # 自适应缩放参数  

    def forward(self, context, x):  
        print("ConcatLinear_v2 used")
        bias = self._hyper_bias(context) + self._adaptive_bias_scale * self._hyper_bias(F.layer_norm(context, context.size(-1)))
        if x.dim() == 3:  
            bias = bias.unsqueeze(1)  
        return self._layer(x) + bias


class ConcatSquashLinear(nn.Module):
    def __init__(self, dim_in, dim_out, dim_c):
        super(ConcatSquashLinear, self).__init__()
        self._layer = nn.Linear(dim_in, dim_out)
        self._hyper_bias = nn.Linear(1 + dim_c, dim_out, bias=False)
        self._hyper_gate = nn.Linear(1 + dim_c, dim_out)

    def forward(self, context, x):
        gate = torch.sigmoid(self._hyper_gate(context))
        bias = self._hyper_bias(context)
        if x.dim() == 3:
            gate = gate.unsqueeze(1)
            bias = bias.unsqueeze(1)
        ret = self._layer(x) * gate + bias
        return ret

