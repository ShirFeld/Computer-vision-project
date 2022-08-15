from PIL import Image
import numpy as np
import cv2


class DigitalImaging:

    # Question 1
    def convert_to_gs(self, image_path):
        """
        This methode gets a path of image. It will create a pillow object and convert it to gray-scale.
        :param image_path: path to the image location
        :return: picture in gary-scale
        """
        img = Image.open(image_path)
        gray_img = img.convert('L')
        return gray_img

    # Question 2
    def color_at(self, img_arr, row_num, column_num):
        """
        This method returns a tuple of RGB values at a specific coordinate
        validate input: both types and value bounds
        :param img_arr: image represented as a Numpy array
        :param row_num: x value
        :param column_num: y value
        :return: tuple of (r,g,b)
        """
        result = DigitalImaging.validate(img_arr, row_num, column_num)
        if result == 3:
            r, g, b = img_arr[row_num][column_num]
            print("R,G,B at = (" + str(row_num) + "," + str(column_num) + ") ->" + str(r) + "," + str(g) + "," + str(b))
            return r, g, b
        elif result == 1:
            grey = img_arr[row_num][column_num]
            print("Grey level = ", grey)
            return grey

    @staticmethod
    def validate(img_arr, row_num, column_num):
        """
        This method checks if the array we received is an image array.
        If so we will check if the number of rows and columns are of type int and if so
        if they are within the range of the array's limits.
        :param img_arr: image represented as a Numpy array
        :param row_num: x value
        :param column_num: y value
        :return: number of channels
        """
        if isinstance(img_arr, np.ndarray):
            try:
                num_of_rows, num_of_columns, channels = img_arr.shape  # validate bounds
                if isinstance(row_num, int) and isinstance(column_num, int):
                    if 0 <= row_num < num_of_rows:
                        if 0 <= column_num < num_of_columns:
                            return 3
                    else:
                        raise ValueError("Row number is not valid")
                else:
                    raise ValueError("Row / column is not of int type")
            except ValueError:
                # the pic is not with color
                num_of_rows, num_of_columns = img_arr.shape  # validate bounds
                if isinstance(row_num, int) and isinstance(column_num, int):
                    if 0 <= row_num < num_of_rows:
                        if 0 <= column_num < num_of_columns:
                            return 1
                    else:
                        raise ValueError("Row number is not valid")
                else:
                    raise ValueError("Row / column is not of int type")
        else:
            raise ValueError("img_arr is not a numpy array")

    # Question 3
    def reduce_to(self, image_path, letter):
        """
           The method receives a path of image and a letter. It will change the color of the image
            according to the letter we receive
           :param image_path: path to the image location
           :param letter:
           :return: picture in different color according to the letter
        """
        pic_arr = np.array(Image.open(image_path))
        if letter == 'r' or letter == 'R':
            pic_only_red = pic_arr.copy()
            pic_only_red[:, :, (1, 2)] = 0
            # Image.fromarray(img_arr_red, 'RGB').show()
            return pic_only_red

        elif letter == 'g' or letter == 'G':
            pic_only_green = pic_arr.copy()
            pic_only_green[:, :, (0, 2)] = 0
            return pic_only_green

        elif letter == 'b' or letter == 'B':
            pic_only_blue = pic_arr.copy()
            pic_only_blue[:, :, (0, 1)] = 0
            return pic_only_blue
        else:
            raise ValueError("My error: the letter is not valid")

    # Question 4
    def make_collage(self, pic_list) -> np.array:
        """
        The method receives a list of image objects.
        It will return an array with a concatenation of images so that the first 3 images are in channel R
        then channel G and channel B.
        :param pic_list:
        :return: array of np type
        """

        pic_list2 = []
        for i in pic_list:
            add_img = i.resize((400, 400))  # All images must be the same size
            pic_list2.append(add_img)

        counter = 1
        new_list = []

        for i in pic_list2:
            print("counter = " + str(counter))
            if counter <= 3:
                pic1 = np.array(i)
                only_red = pic1.copy()
                only_red[:, :, (1, 2)] = 0
                new_list.append(only_red)
            elif counter <= 6:
                pic2 = np.array(i)
                only_green = pic2.copy()
                only_green[:, :, (0, 2)] = 0
                new_list.append(only_green)
            elif counter <= 9:
                pic3 = np.array(i)
                only_blue = pic3.copy()
                only_blue[:, :, (0, 1)] = 0
                new_list.append(only_blue)
                if counter == 9:
                    counter = 0
            counter += 1

        pic_arr = np.concatenate(new_list, axis=0)

        return pic_arr

    # Question 5
    def shapes_dict(self, pic_list):
        """
        The method receives a list of images, take the dimension of each image and put it in the dictionary.
        It will return a dictionary sorted by the img height
        :param pic_list:
        :return:dic
        """
        dic ={}
        for i in range(0, len(pic_list)):
            value = np.array(pic_list[i])
            value_shape = value.shape
            dic[i] = value_shape


        # item[1][0] - will give us the first value of the tuple = height
        return dict(sorted(dic.items(), key=lambda item: item[1][0]))

    # Question 6
    def detect_obj(self, path:str, part2detect:str):
        """
         This method searches an eyes or faces in the given picture
         and returns an Image object with all findings surrounded by a green rectangle.
        :param path: path to the image location
        :param part2detect: Which part to detect. ("face" or "eyes").
        :return: Image object with green rectangle surrounding the findings.
        """
        flag = False
        model = ""
        color = (0,0,0)
        part_in_low_case = part2detect.lower() # convert the part2detect to lower case

        img = cv2.imread(path, cv2.IMREAD_COLOR)
        gray_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        cv2.imshow(path, cv2.IMREAD_COLOR)
        img2rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if(part_in_low_case.__eq__("eyes")):
            model = "haarcascade_eye.xml"
        elif(part_in_low_case.__eq__("face")):
            model = "haarcascade_frontalface_default.xml"
        else:
            print("This part wasn't recognize, please try again")
            return

        color = (0, 255, 0)  # paint the rectangle in green (green = 255)
        classifier = cv2.CascadeClassifier(cv2.data.haarcascades + model)
        detector = classifier.detectMultiScale(gray_img, 2.3, 4)  #img , size , neighbors
        if isinstance(detector, np.ndarray):
            flag = True
            for (_row, _column, _w, _h) in detector:
                cv2.rectangle(img2rgb,
                    (_row, _column),
                    (_row+_w, _column+_h),
                    color,
                    3)
        if (flag):
            return img2rgb
        return

    # Question 7


    # Question 8
    def detect_face_in_vid(self,video_path):
        """
        This method gets a path of a video and detects all the faces in that video.
        :param video_path: A path of a video.
        :return: Void
        """
        video = cv2.VideoCapture("video_path")
        classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        while video.isOpened():
            ret, frame = video.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect the faces
            faces = classifier.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255, 0), 2)
            cv2.imshow('video', frame) # Display

            if cv2.waitKey(1) == ord(27):  #This function is the only method in HighGUI that can fetch and handle events
                break
        video.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    img = Image.open('img1.jpg')  # the regular photo
    # img.show()

    img2 = Image.open('img1.jpg')
    img3 = Image.open('img2.jpg')
    img4 = Image.open('img4.jpg')
    img5 = Image.open('img3.jpg')
    pic_list = [img, img2, img3, img4, img5, img3, img4, img5, img4, img5, img3, img4, img5]


    service = DigitalImaging()
    print(" question 1")
    ## For question 1
    # result = service.convert_to_gs('img1.jpg')
    # result.show()

    print(" question 3")
    ## For question 3
    # result = service.reduce_to('img1.jpg', 'B')
    # Image.fromarray(result, 'RGB').show()

    print(" question 4")
    ## For question 4
    # result = service.make_collage(pic_list)
    # Image.fromarray(result).show()

    print(" question 5")
    ## For question 5
    #result = service.shapes_dict(pic_list)
    #print(result)

    print(" question 6")
    ## For question 6
    # result = service.detect_obj("question6.jpg" ,"eyes")
    # if isinstance(result,np.ndarray):
    #     Image.fromarray(result).show()
    # else:
    #     print("fail")

    print(" question 7")
    ## For question 7
