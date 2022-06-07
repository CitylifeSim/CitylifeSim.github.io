import os
import numpy as np
import torch
import torchvision
import csv
import cv2
import json
import ast
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import torchvision.transforms.functional as F
from natsort import os_sorted
from PIL import Image
from torchvision.io import read_image
from torchvision.ops import masks_to_boxes
from torchvision.utils import draw_bounding_boxes

plt.rcParams["savefig.bbox"] = "tight"

#mode = "car_normal" # default: street_cams

def show(imgs):
    if not isinstance(imgs, list):
        imgs = [imgs]
    fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)
    for i, img in enumerate(imgs):
        img = img.detach()
        img = F.to_pil_image(img)
        axs[0, i].imshow(np.asarray(img))
        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert seg to bbox')
    parser.add_argument('--folder', type=str, default='')
    parser.add_argument('--seg_rgbs', type=str, default='')
    parser.add_argument('--save_image', default=False, action='store_true')
    parser.add_argument('--no-saveImage', dest='saveImage', action='store_false')

    args = parser.parse_args()

    datasetDir = args.folder
    imageDir = os.path.join(datasetDir, 'rgb')
    if not os.path.exists(imageDir):
        os.makedirs(imageDir)
    segDir = os.path.join(datasetDir, 'seg')
    if not os.path.exists(segDir):
        os.makedirs(segDir)
    bboxDir = os.path.join(datasetDir, 'bbox')
    if not os.path.exists(bboxDir):
        os.mkdir(bboxDir)

    #reorganized folders and images
    tmp_folder = os.path.join(datasetDir, 'images')
    for idx, image_name in enumerate(os.listdir(tmp_folder)):
        if "_0_" in image_name:
            os.rename( os.path.join(tmp_folder, image_name), os.path.join(imageDir, image_name))
        elif "_5_" in image_name:
            os.rename( os.path.join(tmp_folder, image_name), os.path.join(segDir, image_name))


    color_id_path = args.seg_rgbs
    #color_id_path = os.path.join(datasetDir, "seg_rgbs.txt")

    #read ped ID color list
    peds_colors_list = []
    with open(color_id_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        #ignore bg color
        background_color = next(csv_reader)
        
        line_count = 0   
        for row in csv_reader:
            color = ast.literal_eval(row[1])    
            peds_colors_list.append(color)
        #print(peds_colors_list)

    peds_colors_mapping = {tuple(c): t for c, t in zip(peds_colors_list, range(len(peds_colors_list)))}

    # only use for splitting multiple cam pose in one video
    # if mode == "street_cams":
    #     df_caminfo= pd.read_csv(os.path.join(datasetDir, "cam_info.csv"))

    frames = []
    imgs_list = os_sorted(os.listdir(imageDir))
    masks_list = os_sorted(os.listdir(segDir))
    cam_id = 0

    saveBoxImage = args.save_image
    frame_id = 0
    for idx, mask_rgb_name in enumerate(masks_list):

        mask_nanosec = int(os.path.splitext(mask_rgb_name)[0].split("_")[3])
        
        # only use for splitting multiple cam pose in one video        
        # if mode == "street_cams":
        #     end_nanosec = df_caminfo.iloc[cam_id]['end_time']

        #     if mask_nanosec > end_nanosec:
        #         cam_id += 1
        #         if cam_id >= len(df_caminfo):
        #             break

        img_name = imgs_list[idx]
        img_path = os.path.join(imageDir, img_name)
        mask_rgb_path = os.path.join(segDir, mask_rgb_name)
      
        img = read_image(img_path,mode=torchvision.io.image.ImageReadMode.RGB)
        mask_rgb = read_image(mask_rgb_path, mode=torchvision.io.image.ImageReadMode.RGB)
        mask_rgb = mask_rgb.permute(1, 2, 0).numpy() #rgb
        target = torch.from_numpy(mask_rgb)
        colors = torch.unique(target.view(-1, target.size(2)), dim=0).numpy()
        target = target.permute(2, 0, 1).contiguous()
        print(target.size())

        colors_list = colors.tolist()
        print(colors_list)
        #don't need to swap R G
        colors_list.remove([55, 181, 57])
        mapping = {tuple(c): t for c, t in zip(colors_list, range(len(colors_list)))}

        print(mapping)
        masks =  torch.empty(len(colors_list), target.size(1), target.size(2), dtype=bool)
        pedID_list = []
        for i, k in enumerate(mapping):
            pedID_list.append(peds_colors_mapping[tuple(k)])
            mask = torch.zeros(target.size(1), target.size(2), dtype=torch.long)
            t_idx = (target==torch.tensor(k, dtype=torch.uint8).unsqueeze(1).unsqueeze(2))
            validx = (t_idx.sum(0) == 3)  # Check that all channels match
            #mask[validx] = torch.tensor(mapping[k], dtype=torch.long)
            mask[validx] = 1
            masks[i] = mask

        print(masks.size())

        #(xmin, ymin, xmax, ymax)
        boxes = masks_to_boxes(masks)
        print(boxes.size())

        boxes_np = boxes.numpy()
        bboxes_data = []
        if len(boxes_np) > 0:
            print(type(int(boxes_np[0][0])))
            
            for i in range(boxes_np.shape[0]):
                bboxes_data.append({"ped_id" : pedID_list[i],
                                    "bbox" :[int(boxes_np[i][0]), int(boxes_np[i][1]), int(boxes_np[i][2]), int(boxes_np[i][3])]})

        frames.append({ "cam_id" : cam_id,
                        "frame_id" : mask_nanosec,
                        "ped_bboxes" : bboxes_data})


        print("cam_id: " + str(cam_id) + "frame_id: " + str(frame_id))
        if saveBoxImage:
            drawn_boxes = draw_bounding_boxes(img, boxes, colors="red")
            print(drawn_boxes.size())
            bbox_name = img_name.replace('img', 'bbox')
            bboxs_img_path = os.path.join(bboxDir, bbox_name)
            bboxs_img = F.to_pil_image(drawn_boxes)
            bboxs_img.save(bboxs_img_path)

        #fix naming convention for benchmark testing
        new_seg_name = "seg_" + str(cam_id) + "_" + str(frame_id) + "_" + str(mask_nanosec) + ".png"
        img_name = imgs_list[idx]
        img_nanosec = int(os.path.splitext(img_name)[0].split("_")[3])
        new_img_name = "rgb_" + str(cam_id) + "_" + str(frame_id) + "_" + str(img_nanosec) + ".png"
        os.rename(os.path.join(imageDir, img_name), os.path.join(imageDir, new_img_name))
        os.rename(os.path.join(segDir, mask_rgb_name), os.path.join(segDir, new_seg_name))
        frame_id += 1
        #plt.show()

    with open(os.path.join(datasetDir, "peds_bbox.json"), 'w') as outfile:
        json.dump(frames, outfile, indent=4)