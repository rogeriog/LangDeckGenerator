from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def getRandomBasePicture():
    import os, random
    filefolder='/'.join(__file__.split('/')[:-1])
    base_img=random.choice(os.listdir(filefolder+'/images'))
    return filefolder+'/images/'+base_img

class DrawMeme:
    def __init__(self,base_img,textup,textdown,savefig):
        self.base_img=base_img
        self.textup=textup
        self.textdown=textdown
        self.savefig=savefig
        self.drawMeme()
    def drawMeme(self):
        img = Image.open(self.base_img)
        draw = ImageDraw.Draw(img)
        self.drawText(img, draw, self.textup.upper(), "top")
        self.drawText(img, draw, self.textdown.upper(), "bottom")
        img.save(self.savefig)

    def drawText(self, img,draw, msg, pos):
        fontSize = 56;
        lines = []
        filefolder='/'.join(__file__.split('/')[:-1])
        font = ImageFont.truetype(filefolder+"/impact.ttf", fontSize)
        w, h = draw.textsize(msg, font)

        imgWidthWithPadding = img.width * 0.99

        # 1. how many lines for the msg to fit ?
        lineCount = 1
        if(w > imgWidthWithPadding):
            lineCount = int(round((w / imgWidthWithPadding) + 1))

        if lineCount > 2:
            while 1:
                fontSize -= 2
                font = ImageFont.truetype(filefolder+"/impact.ttf", fontSize)
                w, h = draw.textsize(msg, font)
                lineCount = int(round((w / imgWidthWithPadding) + 1))
                # print("try again with fontSize={} => {}".format(fontSize, lineCount))
                if lineCount < 3 or fontSize < 10:
                    break


        # print("img.width: {}, text width: {}".format(img.width, w))
        # print("Text length: {}".format(len(msg)))
        # print("Lines: {}".format(lineCount))


        # 2. divide text in X lines
        lastCut = 0
        isLast = False
        for i in range(0,lineCount):
            if lastCut == 0:
                cut = (len(msg) / lineCount) * i
            else:
                cut = lastCut
            cut=int(cut) # have to be integer
            if i < lineCount-1:
                nextCut = (len(msg) / lineCount) * (i+1)
            else:
                nextCut = len(msg)
                isLast = True
            nextCut=int(nextCut)
            # print("cut: {} -> {}".format(cut, nextCut))

            # make sure we don't cut words in half
            if nextCut == len(msg) or msg[nextCut] == " ":
                pass
            else:
                while msg[nextCut] != " " and nextCut != len(msg)-1: ## index out of range in long words?
                    nextCut += 1
            line = msg[cut:nextCut].strip()

            # is line still fitting ?
            w, h = draw.textsize(line, font)
            if not isLast and w > imgWidthWithPadding:
                # print("overshot")
                nextCut -= 1
                while msg[nextCut] != " ":
                    nextCut -= 1
                # print("new cut: {}".format(nextCut))

            lastCut = nextCut
            lines.append(msg[cut:nextCut].strip())

        # print(lines)

        # 3. print each line centered
        lastY = -h
        if pos == "bottom":
            lastY = img.height - h * (lineCount+1) - 10

        for i in range(0,lineCount):
            w, h = draw.textsize(lines[i], font)
            textX = img.width/2 - w/2
            #if pos == "top":
            #    textY = h * i
            #else:
            #    textY = img.height - h * i
            textY = lastY + h
            draw.text((textX-2, textY-2),lines[i],(0,0,0),font=font)
            draw.text((textX+2, textY-2),lines[i],(0,0,0),font=font)
            draw.text((textX+2, textY+2),lines[i],(0,0,0),font=font)
            draw.text((textX-2, textY+2),lines[i],(0,0,0),font=font)
            draw.text((textX, textY),lines[i],(255,255,255),font=font)
            lastY = textY
        return

