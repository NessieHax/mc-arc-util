import sys, struct, zipfile

class arc2zipError(Exception): ...

def main():
    if not sys.argv[1].endswith(".arc"): raise arc2zipError("Not an archive file")
    with open(sys.argv[1], "rb") as archive:
        data = archive.read()

    entry_count = struct.unpack(">i", data[:4])[0]
    offset: int = 4
    with zipfile.ZipFile("arc.zip", "w") as arc_zip_file:
        for _ in range(entry_count):
            strlen = struct.unpack_from(">h", data, offset=offset)[0]
            file_path, file_offset, file_size = struct.unpack_from(f">{strlen}s2i", buffer=data, offset=offset+2)
            filepath = file_path.decode("UTF-8").strip("\0")
            offset += strlen + 10
            if "/" or "\\" in filepath:
                zipfile.Path(arc_zip_file, filepath)
            arc_zip_file.writestr(filepath, data=data[file_offset:file_offset+file_size])

if __name__ == "__main__" and len(sys.argv) > 1:
    main()