'''
文件格式
your_YOLO_datasetname
|————train
|————val
|————test
|————yolo2voc.py
|————VOCdevkit
     |————VOC2007 #voc_folder_name
         |————Annotations 用于存放xml文件
         |————ImageSets 
              |————Main 用于存放存储划分数据集文件名的txt文件
         |————JPEGImages 用于存放原图
'''
from xml.dom.minidom import Document
import os
import cv2

base_path = 'X:/WorkSpace/CV/Datasets/Cone_Real_New' # 填文件夹文件路径
voc_folder_name = 'VOC2007'
xmlPath = os.path.join(base_path, 'VOCdevkit',voc_folder_name,'Annotations') + '/' # xml文件保存路径，后面的/一定要带上
mainPath = os.path.join(base_path, 'VOCdevkit',voc_folder_name,'ImageSets','Main') + '/'
dic = {'0': "red",  # 创建字典用来对类型进行转换,此处的字典要与自己的classes.txt文件中的类对应，且顺序要一致
       '1': "blue",
       '2': "yellow",
      }
yolo_subdirectories = [
    'test',  
    'train', 
    'val'  
]

# 创建VOC格式目录存放转换后文件
def create_voc_directory(base_path):
    # 定义VOC2007下的子目录
    subdirectories = [
        'Annotations',  
        os.path.join('ImageSets', 'Main'), 
        'JPEGImages'  
    ]

    # 创建VOCdevkit主目录
    vocdevkit_path = os.path.join(base_path, 'VOCdevkit')
    if not os.path.exists(vocdevkit_path):
        os.makedirs(vocdevkit_path)

    # 创建VOC2007主目录
    voc2007_path = os.path.join(vocdevkit_path, voc_folder_name)
    if not os.path.exists(voc2007_path):
        os.makedirs(voc2007_path)
    
    # 在VOC2007目录下创建子目录
    for subdir in subdirectories:
        full_path = os.path.join(voc2007_path, subdir)
        if not os.path.exists(full_path):
            os.makedirs(full_path)


# 此函数用于将yolo格式txt标注文件转换为voc格式xml标注文件
def makexml(subdir,picPath, txtPath, xmlPath):  # txt所在文件夹路径，xml文件保存路径，图片所在文件夹路径
    files = os.listdir(txtPath)
    txt = open(mainPath + subdir + ".txt", 'w')
    for i, name in enumerate(files):
        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
        xmlBuilder.appendChild(annotation)
        txtFile = open(txtPath + name)
        txtList = txtFile.readlines()
        img = cv2.imread(picPath + name[0:-4] + ".jpg")
        Pheight, Pwidth, Pdepth = img.shape

        folder = xmlBuilder.createElement("folder")  # folder标签
        foldercontent = xmlBuilder.createTextNode(voc_folder_name)
        folder.appendChild(foldercontent)
        annotation.appendChild(folder)  # folder标签结束

        filename = xmlBuilder.createElement("filename")  # filename标签
        filenamecontent = xmlBuilder.createTextNode(name[0:-4] + ".jpg")
        filename.appendChild(filenamecontent)
        annotation.appendChild(filename)  # filename标签结束

        size = xmlBuilder.createElement("size")  # size标签
        width = xmlBuilder.createElement("width")  # size子标签width
        widthcontent = xmlBuilder.createTextNode(str(Pwidth))
        width.appendChild(widthcontent)
        size.appendChild(width)  # size子标签width结束

        height = xmlBuilder.createElement("height")  # size子标签height
        heightcontent = xmlBuilder.createTextNode(str(Pheight))
        height.appendChild(heightcontent)
        size.appendChild(height)  # size子标签height结束

        depth = xmlBuilder.createElement("depth")  # size子标签depth
        depthcontent = xmlBuilder.createTextNode(str(Pdepth))
        depth.appendChild(depthcontent)
        size.appendChild(depth)  # size子标签depth结束

        annotation.appendChild(size)  # size标签结束

        for j in txtList:
            oneline = j.strip().split(" ")
            object = xmlBuilder.createElement("object")  # object 标签
            picname = xmlBuilder.createElement("name")  # name标签
            namecontent = xmlBuilder.createTextNode(dic[oneline[0]])
            picname.appendChild(namecontent)
            object.appendChild(picname)  # name标签结束

            pose = xmlBuilder.createElement("pose")  # pose标签
            posecontent = xmlBuilder.createTextNode("Unspecified")
            pose.appendChild(posecontent)
            object.appendChild(pose)  # pose标签结束

            truncated = xmlBuilder.createElement("truncated")  # truncated标签
            truncatedContent = xmlBuilder.createTextNode("0")
            truncated.appendChild(truncatedContent)
            object.appendChild(truncated)  # truncated标签结束

            difficult = xmlBuilder.createElement("difficult")  # difficult标签
            difficultcontent = xmlBuilder.createTextNode("0")
            difficult.appendChild(difficultcontent)
            object.appendChild(difficult)  # difficult标签结束

            bndbox = xmlBuilder.createElement("bndbox")  # bndbox标签
            xmin = xmlBuilder.createElement("xmin")  # xmin标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)
            xminContent = xmlBuilder.createTextNode(str(mathData))
            xmin.appendChild(xminContent)
            bndbox.appendChild(xmin)  # xmin标签结束

            ymin = xmlBuilder.createElement("ymin")  # ymin标签
            mathData = int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)
            yminContent = xmlBuilder.createTextNode(str(mathData))
            ymin.appendChild(yminContent)
            bndbox.appendChild(ymin)  # ymin标签结束

            xmax = xmlBuilder.createElement("xmax")  # xmax标签
            mathData = int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)
            xmaxContent = xmlBuilder.createTextNode(str(mathData))
            xmax.appendChild(xmaxContent)
            bndbox.appendChild(xmax)  # xmax标签结束

            ymax = xmlBuilder.createElement("ymax")  # ymax标签
            mathData = int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)
            ymaxContent = xmlBuilder.createTextNode(str(mathData))
            ymax.appendChild(ymaxContent)
            bndbox.appendChild(ymax)  # ymax标签结束

            object.appendChild(bndbox)  # bndbox标签结束

            annotation.appendChild(object)  # object标签结束
        
        txt.write(name[0:-4]+'\n')
        f = open(xmlPath + name[0:-4] + ".xml", 'w')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()
    txt.close()


if __name__ == "__main__":
    print('mkdir...')
    create_voc_directory(base_path)
    for subdir in yolo_subdirectories:
        print('processing dir '+ subdir)
        picPath = os.path.join(base_path, subdir,'images') + '/'
        txtPath = os.path.join(base_path, subdir,'labels') + '/'
        makexml(subdir,picPath, txtPath, xmlPath)
    print("Finish")
