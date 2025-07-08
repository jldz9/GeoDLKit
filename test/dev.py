from torchgeo.datasets import RasterDataset, VectorDataset, IntersectionDataset, stack_samples, unbind_samples
from torchgeo.samplers import RandomGeoSampler, Units
import torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader

class Drake_dataset(RasterDataset):
    filename_glob = 'Drake*_MS.tif'
    filename_regex = r'^(?P<site>[A-Za-z]+)(?P<date>\d{8})_(?P<suffix>[A-Za-z]+)\.tif$'
    date_format = '%Y%m%d'
    is_image = True
    separate_files = False
    all_bands = ('B01', 'B02', 'B03', 'B04', 'B05')
    rgb_bands = ('B03', 'B02', 'B01')

    def plot(self, sample):
        rgb_indices = []
        for band in self.rgb_bands:
            rgb_indices.append(self.all_bands.index(band))
        image = sample['image'][rgb_indices].permute(1, 2, 0)
        fig, ax = plt.subplots()
        ax.imshow(image)
        return fig

class Drake_vector(VectorDataset):
    filename_regex = r'^shp_(?P<date>\d{8}).shp$'
    date_format = '%Y%m%d'





dataset = Drake_dataset(paths='/home/jldz9/dev_test/data/image')
vector = Drake_vector(paths='/home/jldz9/dev_test/data/label')
ds = dataset&vector
sampler = RandomGeoSampler(ds, size=512, length=10, units=Units.PIXELS)
dataloader = DataLoader(ds, sampler=sampler, collate_fn=stack_samples)

train_batch = next(iter(dataloader))

