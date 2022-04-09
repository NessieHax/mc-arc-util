import sys, struct, zipfile

class zip2arcError(Exception): ...

def main():
    if not sys.argv[1].endswith(".zip"): raise zip2arcError("Not a zip file")
    with zipfile.ZipFile(sys.argv[1], "r") as arc_zip_file:
        entry_count = len(arc_zip_file.filelist)
        file_offset = sum([len(zipInfo.filename)+10 for zipInfo in arc_zip_file.filelist]) + 4

        write_buffer: bytearray = bytearray(struct.pack(">i", entry_count))

        for zipInfo in arc_zip_file.filelist:
            strlen: int = len(zipInfo.filename)
            file_size: int = zipInfo.file_size
            write_buffer.extend(struct.pack(f">h{strlen}s2i", strlen, zipInfo.filename.replace("/", "\\").encode("UTF-8"), file_offset, file_size))
            file_offset += file_size

        for zipInfo in arc_zip_file.filelist:
            write_buffer.extend(arc_zip_file.read(zipInfo))

        with open("out.arc", "wb") as arc_file:
            arc_file.write(write_buffer)
            
    

        

if __name__ == "__main__" and len(sys.argv) > 1:
    main()