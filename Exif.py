import sys
from ExifParser import AnalyzeExifData
from ExitTag import ExifTagInfomation

def get_tag_number(exif_data, data, offset):
    tag_number = exif_data.get_tag_number(data, offset)
    print('IFD Tag Number = {0}'.format(tag_number))
    return tag_number

def display_message(tag_info, ifd):
    print('{:s} : [{:s} len={:d}] 0x{:08x}'.format( \
                                                ExifTagInfomation().change_id_to_string(ifd, tag_info[0]), \
                                                ExifTagInfomation().change_format_to_string(tag_info[1]), \
                                                tag_info[2], \
                                                tag_info[3]))

def get_0th_ifd(exif_data, data):
    first_ifd_offset  = 0
    exif_ifd_offset = 0
    gps_ifd_offset  = 0
    intr_ifd_offset = 0

    offset = exif_data.get_0th_offset(data)
    tag_number = get_tag_number(exif_data, data, offset)
    offset += 2

    for count in range(tag_number):
        tag_info = exif_data.get_tag_info(data, offset)
        display_message(tag_info, "0th")
        if tag_info[0] == 0x8769:
            exif_ifd_offset = tag_info[3]
        elif tag_info[0] == 0x8825:
            gps_ifd_offset = tag_info[3]
        elif tag_info[0] == 0xA005:
            intr_ifd_offset = tag_info[3]
        offset += 12
    first_ifd_offset = exif_data.get_1st_ifd_offset(data, offset)
    
    return first_ifd_offset, exif_ifd_offset, gps_ifd_offset, intr_ifd_offset
    
def get_ifd(exif_data, data, offset, ifd):
    tag_number = get_tag_number(exif_data, data, offset)
    offset = offset + 2

    for count in range(tag_number):
        tag_info = exif_data.get_tag_info(data, offset)
        display_message(tag_info, ifd)
        offset += 12

def exif(argv):
    ifd_strings = ["1st", "Exif", "GPS ", "Intr"]
    exif_data = AnalyzeExifData()

    with open(argv[0], 'rb') as infile:
        data = infile.read()

    exif_data.check_exif_string(data)
    exif_data.check_byte_order(data)

    offset = get_0th_ifd(exif_data, data)
    count = 0
    for ifd_string in ifd_strings:
        if offset[count] > 0:
            print('{:4s} IFD Offset = 0x{:08x}'.format(ifd_string, offset[count]))
            get_ifd(exif_data, data, offset[count], ifd_string)
            count += 1
 
if __name__ == '__main__':
    exif(sys.argv[1:])