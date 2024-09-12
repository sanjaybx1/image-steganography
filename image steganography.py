
from PIL import Image
import pyfiglet
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def print_banner(name):
    banner = pyfiglet.figlet_format(name, font='slant')
    colored_banner = f"{Fore.CYAN}{banner}{Style.RESET_ALL}"
    
    print(colored_banner)
    print(f"{Fore.GREEN}Developed by Sanjay{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~{Style.RESET_ALL}")

def print_intro():
    print(f"{Fore.MAGENTA}Welcome to the Steganography Tool!{Style.RESET_ALL}")
    print(f"{Fore.BLUE}This tool allows you to encode and decode hidden messages in images using LSB (Least Significant Bit) steganography.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Please select an option from the menu below:{Style.RESET_ALL}")

def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        scbx1 = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0' and scbx1[j] % 2 != 0):
                scbx1[j] -= 1
            elif (datalist[i][j] == '1' and scbx1[j] % 2 == 0):
                if(scbx1[j] != 0):
                    scbx1[j] -= 1
                else:
                    scbx1[j] += 1

        if (i == lendata - 1):
            if (scbx1[-1] % 2 == 0):
                if(scbx1[-1] != 0):
                    scbx1[-1] -= 1
                else:
                    scbx1[-1] += 1
        else:
            if (scbx1[-1] % 2 != 0):
                scbx1[-1] -= 1

        scbx1 = tuple(scbx1)
        yield scbx1[0:3]
        yield scbx1[3:6]
        yield scbx1[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode():
    img = input("Enter image name with path or drag and drop the image (with extension):")
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded: ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter New image name with path (with extension .png): ")

    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def decode():
    img = input("Enter the encoded image name with path must be in .png extension: ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        scbx1 = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]
        binstr = ''

        for i in scbx1[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (scbx1[-1] % 2 != 0):
            return data

if __name__ == '__main__':
    print_intro()
    print_banner("SCbx1")
    
    choice = int(input(":: Welcome to Steganography ::\n1. press 1 to encode\n2. Press 2 to decode\n"))
    if (choice == 1):
        encode()
        print("successfully encoded!!!")
    elif (choice == 2):
        decoded_message = decode()
        print(f"{Fore.GREEN}Decoded message: {Style.RESET_ALL}{decoded_message}")
        print("Successfully decoded!!!")
    else:
        raise Exception("Enter correct input")
