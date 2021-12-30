# TexTools-Organizer
Automatic organization of texture files output from [FFXIV TexTools](https://www.ffxiv-textools.net) when exporting a "full model"

Grab a release from [here](https://github.com/wolfinabox/TexTools-Organizer/releases/latest)!

Drag-and-drop the folder containing your images (typically also contains the .fbx file), and they will automatically be renamed by part type and image type (albedo/normal/etc), and moved into part folders.

Create a shortcut to the .exe and add desired arguments/flags at the end of the "Target" field.

```
usage: textools_organizer.exe [-h] [-k] [-m] [-y] [-v] [-s [SUBFOLDER]] [path]

Organize the texture outputs from FFXIV TexTools into a more usable format.

positional arguments:
  path                  Path to the folder containing exported images and .fbx file from TexTools

optional arguments:
  -h, --help            show this help message and exit
  -k, --keepnames       Don't rename files after reorganizing
  -m, --move            Move files when reorganizing, instead of copy
  -y                    Answer yes to all prompts (may delete old processed files if necessary)
  -v, --verbose         Logging verbosity. Available: -v, -vv
  -s [SUBFOLDER], --subfolder [SUBFOLDER]
                        Name to use for subfolder
```
