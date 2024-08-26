from pix2text import Pix2Text
def rec_char():
    img_fp = 'ss.png'
    p2t = Pix2Text.from_config()
    outs = p2t.recognize_formula(img_fp)
    print(outs)
    return outs

if __name__ == "__main__":
    rec_char()