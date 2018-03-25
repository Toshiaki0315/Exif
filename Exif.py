import sys
from ExifParser import AnalyzeExifData
from ExifTag import ExifTagInfomation

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

    offset_ids = {0x8769:"exif", 0x8825:"gps", 0xA005:"intr"}
    exif_data.get_0th_offset(data)
    tag_number = get_tag_number(exif_data, data, "0th")

    for count in range(tag_number):
        tag_info = exif_data.get_tag_info(data, "0th", count)
        display_message(tag_info, "0th")
        if tag_info[0] in offset_ids:
            exif_data.set_offset(offset_ids[tag_info[0]], tag_info[3])
    exif_data.get_1st_ifd_offset(data, tag_number)
    
    return
    
def get_ifd(exif_data, data, ifd):
    tag_number = get_tag_number(exif_data, data, ifd)

    for count in range(tag_number):
        tag_info = exif_data.get_tag_info(data, ifd, count)
        display_message(tag_info, ifd)

def exif(argv):
    ifd_strings = ["1st", "exif", "gps", "intr"]
    exif_data = AnalyzeExifData()

    with open(argv[0], 'rb') as infile:
        data = infile.read()

    exif_data.check_exif_string(data)
    exif_data.check_byte_order(data)

    get_0th_ifd(exif_data, data)
    for ifd_string in ifd_strings:
        if exif_data.get_offset(ifd_string) > 0:
            get_ifd(exif_data, data, ifd_string)
 
if __name__ == '__main__':
    exif(sys.argv[1:])