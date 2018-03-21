from ExifParser import AnalyzeExifData

def exif():
    exif_data = AnalyzeExifData()

    with open('./IMG_3294.jpg', 'rb') as infile:
        data = infile.read()

        offset_base = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset_base)
        exif_data.get_0th_offset(data, offset_base)
        tag_number = exif_data.get_tag_number(data, offset_base)
        print('0th IFD tag = {0}'.format(tag_number))
        for count in range(tag_number):
            tag_info = exif_data.get_tag_info(data, offset_base, count*12)
            print('0x{:04x} 0x{:04x} 0x{:08x} 0x{:08x}'.format(tag_info[0],tag_info[1],tag_info[2],tag_info[3]))

if __name__ == '__main__':
    exif()