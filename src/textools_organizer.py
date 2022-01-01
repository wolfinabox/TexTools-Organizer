import argparse
import logging
import sys, os
import shutil
import colorama


colorama.init()
import daiquiri, daiquiri.formatter
from utils import askYN, exit_wait
from name_parser import parse_filename


argparser = argparse.ArgumentParser(
    description="Organize the texture outputs from FFXIV TexTools into a more usable format."
)
argparser.add_argument(
    "path",
    type=str,
    nargs="?",
    help="Path to the folder containing exported images and .fbx file from TexTools",
)
argparser.add_argument(
    "-k",
    "--keepnames",
    dest="keepnames",
    action="store_true",
    default=False,
    help="Don't rename files after reorganizing",
)
argparser.add_argument(
    "-m",
    "--move",
    dest="move",
    action="store_true",
    default=False,
    help="Move files when reorganizing, instead of copy. (This WILL break texture mapping on the original .fbx)",
)
argparser.add_argument(
    "-y",
    dest="yes",
    action="store_true",
    default=False,
    help="Answer yes to all prompts (may delete old processed files if necessary)",
)
argparser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="count",
    default=0,
    help="Logging verbosity. Available: -v, -vv",
)
argparser.add_argument(
    "-s",
    "--subfolder",
    type=str,
    nargs="?",
    dest="subfolder",
    action="store",
    help="Name to use for subfolder",
)
if __name__ == "__main__":
    # args
    sys.argv.pop(0)
    args = argparser.parse_args(sys.argv)
    daiquiri.setup(
        level={0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}.get(
            args.verbose, logging.DEBUG
        ),
        outputs=(
            daiquiri.output.Stream(
                stream=sys.stdout,
                formatter=daiquiri.formatter.ColorFormatter(
                    fmt="%(color)s[%(levelname)s]: %(message)s%(color_stop)s"
                ),
            ),
        ),
    )
    log = daiquiri.getLogger()
    # if path not provided
    if not args.path:
        print("Enter the path to the folder containing your images:")
        args.path = input("> ").strip('"').strip()

    if not os.path.isdir(args.path):
        log.error(f'"{args.path}" does not exist')
        exit_wait()
    else:
        print(f'Processing "{args.path}"...')

    # get all files in dir
    all_files = os.listdir(args.path)
    # check for .fbx file
    fbx = [f for f in all_files if os.path.splitext(f)[1] == ".fbx"]
    log.info(f"Found {len(all_files)} file(s), including {len(fbx)} .fbx file(s)")

    # output folder
    out_folder_name = ""
    if args.subfolder:
        out_folder_name = args.subfolder
    elif fbx:
        out_folder_name = os.path.splitext(fbx[0])[0]
    else:
        out_folder_name = "output"
    out_folder = os.path.join(args.path, out_folder_name)
    if os.path.isdir(out_folder):
        if args.yes or askYN(
            f'Delete existing output folder "{out_folder_name}"?', "y"
        ):
            shutil.rmtree(out_folder)
    try:
        os.mkdir(out_folder)
    except:
        pass

    # start processing files
    folders_already_created = []
    processed_files = 0
    for file in all_files:
        file_path = os.path.join(args.path, file)
        if os.path.isdir(file_path):
            continue
        # choose only images
        if os.path.splitext(file_path)[1] not in (".png", ".jpg"):
            if os.path.splitext(file_path)[1] != ".fbx":
                log.warn(
                    f'Ignoring unsupported file type "{os.path.splitext(file)[1]}" ("{file}")'
                )
            continue
        log.debug(f'Processing "{file}"...')
        # parse filename
        part_type, part_subtype, image_type = parse_filename(file.lower())
        if None in (part_type, part_subtype, image_type):
            log.warning(f'Unknown file "{file}", ignoring...')
            continue
        log.debug(f"Part: {(part_type+f' {part_subtype}' if part_subtype!='1' else part_type).title()}, Image: {image_type.title()}")
        # file writing
        out_file_name = (
            file
            if args.keepnames
            else f"{(part_type+f'_{part_subtype}' if part_subtype!='1' else part_type)}_{image_type}{os.path.splitext(file)[1]}"
        )

        part_out_dir = os.path.join(out_folder, part_type)
        # make part output dir if necessary
        if part_out_dir not in folders_already_created:
            if os.path.isdir(part_out_dir):
                if args.yes or askYN(
                    f'Delete existing output folder "{os.path.split(part_out_dir)[1]}"?',
                    "y",
                ):
                    shutil.rmtree(part_out_dir)
            try:
                os.mkdir(part_out_dir)
            except:
                pass
            folders_already_created.append(part_out_dir)
        out_file_path = os.path.join(part_out_dir, out_file_name)

        # actually move/copy file
        # move file
        if args.move:
            shutil.move(file_path, out_file_path)
        else:
            shutil.copy(file_path, out_file_path)
        log.debug(f'Output to "{part_type}\\{out_file_name}"')
        processed_files += 1
    print(f"Done! Processed {processed_files} files.")
    exit_wait()
