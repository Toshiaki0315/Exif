from ExifParser import AnalyzeExifData

def exif():
    with open('./IMG_3294.jpg', 'rb') as infile:
        data = infile.read()
        offset_base = AnalyzeExifData().check_exif_string(data)
        endian = AnalyzeExifData().check_byte_order(data, offset_base)
        offset_0th = AnalyzeExifData().get_0th_offset(endian, data, offset_base)
        tag_number = AnalyzeExifData().get_tag_number(endian, data, offset_base, offset_0th)
        print('0th IFD tag = {0}'.format(tag_number))
        for count in range(tag_number):
            tag_info = AnalyzeExifData().get_tag_info(endian, data, offset_base, offset_0th)
            print('0x{:04x} 0x{:04x} 0x{:08x} 0x{:08x}'.format(tag_info[0],tag_info[1],tag_info[2],tag_info[3]))
            offset_0th += 12

if __name__ == '__main__':
    exif()