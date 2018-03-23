from ExifParser import AnalyzeExifData

def get_0th_ifd(exif_data, data):
    first_ifd_offset  = 0
    exif_ifd_offset = 0
    gps_ifd_offset  = 0
    intr_ifd_offset = 0

    offset = exif_data.get_0th_offset(data)
    tag_number = exif_data.get_tag_number(data, offset)
    offset += 2

    print('0th IFD tag = {0}'.format(tag_number))
    for count in range(tag_number):
        tag_info = exif_data.get_tag_info(data, offset)
        print('0x{:04x} 0x{:04x} 0x{:08x} 0x{:08x}'.format(tag_info[0],tag_info[1],tag_info[2],tag_info[3]))
        if tag_info[0] == 0x8769:
            exif_ifd_offset = tag_info[3]
        elif tag_info[0] == 0x8825:
            gps_ifd_offset = tag_info[3]
        elif tag_info[0] == 0xA005:
            intr_ifd_offset = tag_info[3]
        offset += 12
    first_ifd_offset = exif_data.get_1st_ifd_offset(data, offset)
    
    return first_ifd_offset, exif_ifd_offset, gps_ifd_offset, intr_ifd_offset
    
def get_ifd(exif_data, data, offset):
    tag_number = exif_data.get_tag_number(data, offset)
    offset = offset + 2

    print('IFD Tag Number = {0}'.format(tag_number))
    for count in range(tag_number):
        tag_info = exif_data.get_tag_info(data, offset)
        print('0x{:04x} 0x{:04x} 0x{:08x} 0x{:08x}'.format(tag_info[0],tag_info[1],tag_info[2],tag_info[3]))
        offset += 12

def exif():
    exif_data = AnalyzeExifData()

    with open('./_2210747.JPG', 'rb') as infile:
#    with open('./IMG_3294.jpg', 'rb') as infile:
        data = infile.read()

        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)

        offset = get_0th_ifd(exif_data, data)
        if offset[0] > 0:
            print('1st  IFD Offset = 0x{:08x}'.format(offset[0]))
            get_ifd(exif_data, data, offset[0])
        if offset[1] > 0:
            print('Exif IFD Offset = 0x{:08x}'.format(offset[1]))
            get_ifd(exif_data, data, offset[1])
        if offset[2] > 0:
            print('GPS  IFD Offset = 0x{:08x}'.format(offset[2]))
            get_ifd(exif_data, data, offset[2])
        if offset[3] > 0:
            print('Intr IFD Offset = 0x{:08x}'.format(offset[3]))
            get_ifd(exif_data, data, offset[3])

if __name__ == '__main__':
    exif()