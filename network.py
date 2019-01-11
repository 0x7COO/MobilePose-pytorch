'''
File: networks.py
Project: MobilePose
File Created: Thursday, 8th March 2018 2:59:28 pm
Author: Yuliang Xiu (yuliangxiu@sjtu.edu.cn)
-----
Last Modified: Thursday, 8th March 2018 3:01:29 pm
Modified By: Yuliang Xiu (yuliangxiu@sjtu.edu.cn>)
-----
Copyright 2018 - 2018 Shanghai Jiao Tong University, Machine Vision and Intelligence Group
'''


from networks import *
import torch.nn as nn
import dsntnn

class CoordRegressionNetwork(nn.Module):
    def __init__(self, n_locations, backbone):
        super(CoordRegressionNetwork, self).__init__()

        if backbone == "unet":
            self.resnet = UNet()
            self.outsize = 64
        elif backbone == "resnet18":
            self.resnet = resnet.resnet18_ed(pretrained=False)
            self.outsize = 512
        elif backbone == "resnet34":
            self.resnet = resnet.resnet34_ed(pretrained=False)
            self.outsize = 512
        elif backbone == "resnet50":
            self.resnet = resnet.resnet50_ed(pretrained=False)
            self.outsize = 2048

        self.hm_conv = nn.Conv2d(self.outsize, n_locations, kernel_size=1, bias=False)

    def forward(self, images):
        # 1. Run the images through our Resnet
        resnet_out = self.resnet(images)
        # 2. Use a 1x1 conv to get one unnormalized heatmap per location
        unnormalized_heatmaps = self.hm_conv(resnet_out)
        # 3. Normalize the heatmaps
        heatmaps = dsntnn.flat_softmax(unnormalized_heatmaps)
        # 4. Calculate the coordinates
        coords = dsntnn.dsnt(heatmaps)

        return coords, heatmaps