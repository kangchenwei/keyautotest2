import operator
import sys
from PIL import Image


class ImageUtils:
    IMAGE_SIZE = 120
    PIXEL_FUZZY_ALLOWED_SIZE = 30
    PIXEL_COLOR_DELTA_THRESHOLD = 15
    compareRule = [
        'SAME_DIRECTION_LeftTopLeftTop',
        'SAME_DIRECTION_LeftTopRightBottom',
        'DIFFERENT_DIRECTION_LeftTopLeftTop',
        'DIFFERENT_DIRECTION_LeftTopLeftBottom',
        'DIFFERENT_DIRECTION_LeftTopRightBottom',
        'DIFFERENT_DIRECTION_LeftTopRightTop'
    ]

    def getSimilarity(self, img_a, img_b, coordinatelist, isConcernArea, isMatchWhite):
        if (img_a == None or img_b == None):
            return 0.0
        #  图片A的宽高
        width_a, height_a = img_a.size
        #  图片B的宽高
        width_b, height_b = img_b.size

        # 判断两张图片的方向是否一致
        if ((height_a > width_a and height_b > width_b) or ( height_a < width_a and height_b < width_b)) :
            result1 = self.compareImage(img_a, img_b,coordinatelist,ImageUtils.compareRule[0], isConcernArea,isMatchWhite)

            result2 = self.compareImage(img_a, img_b, coordinatelist,ImageUtils.compareRule[1], isConcernArea, isMatchWhite)

            result = (result1 if(result1 > result2) else result2)

            return result
        else:
            result3 = self.compareImage(img_a, img_b, coordinatelist, ImageUtils.compareRule[2],isConcernArea, isMatchWhite)
            result4 = self.compareImage(img_a, img_b, coordinatelist, ImageUtils.compareRule[3],isConcernArea, isMatchWhite)
            result5 = self.compareImage(img_a, img_b, coordinatelist, ImageUtils.compareRule[4],isConcernArea, isMatchWhite)
            result6 = self.compareImage(img_a, img_b, coordinatelist, ImageUtils.compareRule[5],isConcernArea, isMatchWhite)
            results = [result3, result4, result5, result6]
            results.sort(results)
            return results[3]


    def compareImage(self, img_a, img_b, coordinatelist, compareRule, isConcernArea, isMatchWhite):
        sumNum = 0
        similarityNum = 0
        #  图片A的宽高
        width_a, height_a = img_a.size
        #  图片B的宽高
        width_b, height_b = img_b.size
        print(width_a, height_a)
        print(width_b, height_b)
        if (coordinatelist == None):
            coordinatelist = []

         # 如果传入的coordinatelist为空就代表没有指定区域，就将区域设置为整个图片
        if (len(coordinatelist) == 0):
            coordinatelist.append([0, 0, width_a, height_a])
        x2 = 0
        y2 = 0
        for y in range(ImageUtils.IMAGE_SIZE):
            for x in range(ImageUtils.IMAGE_SIZE):
                x1 = int((width_a * 1.0 / ImageUtils.IMAGE_SIZE) * x)
                y1 = int((height_a * 1.0 / ImageUtils.IMAGE_SIZE) * y)
                pixel1 = img_a.getpixel((x1, y1))
                # 如果被比较的颜色不是白色时才进行比较，pixel为[255,255,255]代表白色
                if (self.checkCondition(pixel1, isMatchWhite) and self.isInArea(x1, y1, coordinatelist, isConcernArea)):
                    # 计算图片B的对应坐标
                    if compareRule == 'SAME_DIRECTION_LeftTopLeftTop':
                        x2 = int((width_b * 1.0 / ImageUtils.IMAGE_SIZE) * x)
                        y2 = int((height_b * 1.0 / ImageUtils.IMAGE_SIZE) * y)
                    elif compareRule == 'SAME_DIRECTION_LeftTopRightBottom':
                        x2 = int((width_b * 1.0 / ImageUtils.IMAGE_SIZE) * (ImageUtils.IMAGE_SIZE - x) - 1)
                        y2 = int((height_b * 1.0 / ImageUtils.IMAGE_SIZE) * (ImageUtils.IMAGE_SIZE - y) - 1)
                    elif compareRule == 'DIFFERENT_DIRECTION_LeftTopLeftTop':
                        x2 = int((width_b * 1.0 / ImageUtils.IMAGE_SIZE) * y)
                        y2 = int((height_b * 1.0 / ImageUtils.IMAGE_SIZE) * x)
                    elif compareRule == 'DIFFERENT_DIRECTION_LeftTopLeftBottom':
                        x2 = int((width_b * 1.0 / ImageUtils.IMAGE_SIZE) * (ImageUtils.IMAGE_SIZE - y) - 1)
                        y2 = int((height_b * 1.0 / ImageUtils.IMAGE_SIZE) * x)
                    elif compareRule == 'DIFFERENT_DIRECTION_LeftTopRightBottom':
                        x2 = int((width_b * 1.0 / ImageUtils.IMAGE_SIZE) * (ImageUtils.IMAGE_SIZE - y) - 1)
                        y2 = int((height_b * 1.0 / ImageUtils.IMAGE_SIZE) * (ImageUtils.IMAGE_SIZE - x) - 1)
                    elif compareRule == 'DIFFERENT_DIRECTION_LeftTopRightTop':
                        x2 = int((width_b * 1.0 / ImageUtils.IMAGE_SIZE) * y)
                        y2 = int((height_b * 1.0 / ImageUtils.IMAGE_SIZE) * (ImageUtils.IMAGE_SIZE - x) - 1)

                    if (self.isSimilaryPixel(pixel1, x2, y2, width_b, height_b, img_b)):
                        similarityNum = similarityNum + 1

                    sumNum = sumNum + 1
        print("###", similarityNum)
        print('&&&', sumNum)
        return (float(similarityNum) /float(sumNum)) *100


    def checkCondition(self, pixel, isMatchWhite):
        return (not(operator.eq(pixel, [255, 255, 255]))) or (operator.eq(pixel, [255, 255, 255]) and isMatchWhite)


    def isInArea(self, x, y, coordinatelist, isConcernArea):
        # isConcernArea为true表示要进行比较的是在关注区域内的点
        if isConcernArea == True:
            for i in range(len(coordinatelist)):
                coordinates = coordinatelist[i]
                if (x >= int(coordinates[0]) and x <= int(coordinates[2]) and y >= int(coordinates[1]) and y <= int(coordinates[3])):
                    return True
            return False
        else:
            # isConcernArea为false表示要进行比较的是在被忽略区域以外的点
            for i in range(len(coordinatelist)):
                coordinates = coordinatelist[i]
                if (not(x >= coordinates[0] and x <= coordinates[2] and y >= coordinates[1] and y <= coordinates[3])):
                    return True
            return False

    def isSimilaryPixel(self, pixel1, x, y, width, height, img_b):

	    if self.isSimilaryPixel_3(pixel1, img_b.getpixel((x, y))):
		    return True

	    xStart = x
	    if (x - ImageUtils.PIXEL_FUZZY_ALLOWED_SIZE >= 0) :
		    xStart = x - ImageUtils.PIXEL_FUZZY_ALLOWED_SIZE

	    xEnd = x
	    if (x + ImageUtils.PIXEL_FUZZY_ALLOWED_SIZE < width):
	        xEnd = x + ImageUtils.PIXEL_FUZZY_ALLOWED_SIZE

	    yStart = y
	    if (y - ImageUtils.PIXEL_FUZZY_ALLOWED_SIZE >= 0):
	        yStart = y - ImageUtils.PIXEL_FUZZY_ALLOWED_SIZE

	    yEnd = y
	    if (y + ImageUtils.PIXEL_FUZZY_ALLOWED_SIZE < height):
	        yEnd = y + ImageUtils.PIXEL_FUZZY_ALLOWED_SIZE

	    for i in range(xStart, xEnd+1, 5) :
	        for j in range(yStart, yEnd+1, 5):
		        pixel2 = img_b.getpixel((i, j))
		        if (self.isSimilaryPixel_rgb(pixel1, pixel2)):
			        return True
	    return False

    def isSimilaryPixel_rgb(self, pixel1, pixel2):
        r1 = pixel1[0]
        g1 = pixel1[1]
        b1 = pixel1[2]

        r2 = pixel2[0]
        g2 = pixel2[1]
        b2 = pixel2[2]

        redDelta = abs(r1 - r2)
        greenDelta = abs(g1 - g2)
        blueDelta = abs(b1 - b2)

        return redDelta <= ImageUtils.PIXEL_COLOR_DELTA_THRESHOLD and greenDelta <= ImageUtils.PIXEL_COLOR_DELTA_THRESHOLD and blueDelta <= ImageUtils.PIXEL_COLOR_DELTA_THRESHOLD

if __name__ == '__main__':
    paras = sys.argv
    coodinatelist = []
    para_list = []
    if(len(paras) == 3):
        pass
    elif(len(paras) > 3):
        j = 1
        for i in range(3, len(paras)+1):
            if j % 5 != 0:
                j = j + 1
                para_list.append(paras[i])
            if (j-1) % 5 == 0:
                coodinatelist.append(list(para_list))

        print(coodinatelist)

    img1 = Image.open(paras[1])
    img2 = Image.open(paras[2])
    img_util = ImageUtils()
    similarity = img_util.getSimilarity(img1, img2, coodinatelist, True, False)
    print("result==", similarity)
