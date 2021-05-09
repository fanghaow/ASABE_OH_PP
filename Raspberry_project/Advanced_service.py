#For MyPC
import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

import socket
import sys
import server
import client
import os
import shutil

# PC's IP
SERVER_IP = "192.168.43.122"
SERVER_PORT = 8888
lsta = [str(20) for i in range(24)]
flower, white = 0, 0
white_lst = [str(20) for i in range(12)]
flower_lst = [str(20) for i in range(12)]
SERVER_PORT_con = 8899
# {white_lst : white leafs, flower_lst : white flowers}

def detect(save_img=False):
    global SERVER_PORT_con
    try:
        shutil.rmtree('D:/yolpv5s/runs/detect')
        shutil.rmtree('D:/yolpv5s/Img_rec')
        os.mkdir('D:/yolpv5s/runs/detect')
        os.mkdir('D:/yolpv5s/Img_rec')
    except:
        pass
    source, weights, view_img, save_txt, imgsz = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://'))

    # Directories
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    set_logging()
    device = select_device(opt.device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    # if webcam:
    #   view_img = check_imshow()
    #    cudnn.benchmark = True  # set True to speed up constant image size inference
    #    dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    # else:
    #    save_img = True
    #    dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()

    for order in range(12):
        # source = '/home/pi/Desktop/YOLOv5s/data/images/img' + str(order)
        source = 'data/images/img' + str(order)
        if webcam:
            view_img = check_imshow()
            cudnn.benchmark = True  # set True to speed up constant image size inference
            dataset = LoadStreams(source, img_size=imgsz, stride=stride)
        else:
            save_img = True
            dataset = LoadImages(source, img_size=imgsz, stride=stride)
        # start 等待图片拍入
        # image_path = '/home/pi/Desktop/YOLOv5s/data/images'
        image_path = source

        server.socket_service()

        while (True):
            img = cv2.imread('Img_rec' + '/' + str(order) + '.jpg', 1)
            cv2.imwrite(image_path + '/' + 'test' + str(order) + '.jpg', img)

            # print('OK')
            # img = cv2.imread(image_path + '/' + 'test' + str(order) + '.jpg', 1)
            # try:
            #     print(img.shape)
            #     print(type(img))
            # except:
            #     print(Exception)
            #     print('No img is took in')
            #     time.sleep(1)
            #     continue
            break
        ##### start
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=opt.augment)[0]

            # Apply NMS
            pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes,
                                       agnostic=opt.agnostic_nms)
            t2 = time_synchronized()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
                else:
                    p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # img.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + (
                    '' if dataset.mode == 'image' else f'_{frame}')  # img.txt
                s += '%gx%g ' % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                lstsita = []
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if opt.save_conf else (cls, *xywh)  # label format
                            with open(txt_path + '.txt', 'a') as f:
                                f.write(('%g ' * len(line)).rstrip() % line + '\n')

                        if save_img or view_img:  # Add bbox to image
                            label = f'{names[int(cls)]} {conf:.2f}'
                            plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)  # retangle
                            # print(type(xyxy[0])) ##
                            c = [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])]
                            print(label.split()[0], end = '')
                            lstsita.append(c)
                            lstsita.append(label.split()[0])


                            # Print time (inference + NMS)

                # Print time (inference + NMS)
                #### end
                print(f'{s}Done. ({t2 - t1:.3f}s)')
                label_str = f'{s}'  ##
                str_l = label_str.split(' ')
                print(str_l)
                global flower, white
                flower, white = 20, 20
                # print(str_l)
                if len(str_l) == 2:
                    flower, white = 0, 0
                    pass
                elif len(str_l) == 4:
                    if 'flowers,' in str_l or 'flower,' in str_l:
                        flower = str_l[1]
                        white = 0
                    if 'whites,' in str_l or 'white,' in str_l:
                        white = str_l[1]
                        flower = 0
                elif len(str_l) == 6:
                    flower = str_l[1]
                    white = str_l[3]
                white_lst[order] = white
                flower_lst[order] = flower
                print('flower and white quantity:', flower, white)

                print(lstsita)

                transita(lstsita)
                #
                strange_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                for index, order1 in enumerate(strange_order):
                    lsta[(order1 + 1) * 2 - 1] = flower_lst[index]
                    lsta[(order1 + 1) * 2 - 2] = white_lst[index]

                print('send data:', lsta)
                #
                #transport()

                #### end
                # Stream results
                if view_img:
                    cv2.imshow(str(p), im0)
                    cv2.waitKey(1)  # 1 millisecond

                # Save results (image with detections)
                if save_img:
                    if dataset.mode == 'image':
                        cv2.imwrite(save_path, im0)
                    else:  # 'video'
                        if vid_path != save_path:  # new video
                            vid_path = save_path
                            if isinstance(vid_writer, cv2.VideoWriter):
                                vid_writer.release()  # release previous video writer

                            fourcc = 'mp4v'  # output video codec
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                        vid_writer.write(im0)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        print(f"Results saved to {save_dir}{s}")

    print(f'Done. ({time.time() - t0:.3f}s)')

def transport():
    global str_lsta
    str_lsta = ''
    for index, item in enumerate(lsta):
        str_lsta += str(item)
        if index <= 22:
            str_lsta += '/'

    print("Starting socket: TCP...")
    server_addr = (SERVER_IP, SERVER_PORT)
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            print("Connecting to server @ %s:%d..." % (SERVER_IP, SERVER_PORT))
            socket_tcp.connect(server_addr)
            break
        except Exception:
            print("Can't connect to server,try it latter!")
            time.sleep(0.05)
            continue
    print("Please input 1 or 0 to turn on/off the led!")
    i = 0
    while True:
        try:
            data = socket_tcp.recv(512)
            if len(data) > 0:
                print("Received: %s" % data.decode())
                # command=input()
                command = str_lsta
                socket_tcp.send(command.encode())
                # time.sleep(1)
                i += 1
                if i > 0:
                    break
                # continue
        except Exception:
            socket_tcp.close()
            socket_tcp = None
            sys.exit(1)


def transita(Lsita):
    import socket
    import time
    import sys

    # RPi's IP
    SERVER_IP = "192.168.43.44"
    global SERVER_PORT_con
    print("Starting socket: TCP...")
    server_addr = (SERVER_IP, SERVER_PORT_con)
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            print("Connecting to server @ %s:%d..." % (SERVER_IP, SERVER_PORT_con))
            socket_tcp.connect(server_addr)
            break
        except Exception:
            print("Can't connect to server,try it latter!")
            time.sleep(0.5)
            continue
    while True:
        try:
            data = socket_tcp.recv(512)
            data = data.decode()
            if len(data) > 0:
                print("Received: %s" % data)
                command = str(Lsita)
                socket_tcp.send(command.encode())
                break
        except Exception:
            socket_tcp.close()
            socket_tcp = None
            sys.exit(1)

    SERVER_PORT_con += 1

def yolov5_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='IncludeFlower2.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='data/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.4, help='object confidence threshold')  # threshold
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    global opt
    opt = parser.parse_args()
    print(opt)
    check_requirements()

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                detect()
                strip_optimizer(opt.weights)
        else:
            detect()



if __name__ == '__main__':
    yolov5_main()
    client.sock_client()


