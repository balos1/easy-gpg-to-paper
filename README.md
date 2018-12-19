# easy-gpg-to-paper

easy-gpg-to-paper aims to make exporting your secret gpg key to paper, and then restoring from paper, an easy and painless process.
It can export your key to qrcode(s), or it can export your key as a base64 encoded string(s). In the future the code will be cleaned
up, and more features added. Anyone who wants to help out is more than welcome.

[![Build Status](https://travis-ci.org/cojomojo/easy-gpg-to-paper.svg?branch=master)](https://travis-ci.org/cojomojo/easy-gpg-to-paper)
[![Version number](https://img.shields.io/badge/version-v0.2.0-blue.svg)](https://img.shields.io/badge/version-v0.2.0-blue.svg)
[![Supports](https://img.shields.io/badge/python-2.7%2C%203.3%2C%203.4%2C%203.5%2C%203.6%2C%203.7--dev-blue.svg)](https://img.shields.io/badge/python-2.7%2C%203.3%2C%203.4%2C%203.5%2C%203.6%2C%203.7--dev-blue.svg)

# Dependencies

+ [paperkey](http://www.jabberwocky.com/software/paperkey/)
+ [zbarimg](http://zbar.sourceforge.net/)
+ [python-qrcode](https://github.com/lincolnloop/python-qrcode)
+ [Pillow](https://github.com/python-pillow/Pillow)
+ [weasyprint](https://github.com/Kozea/WeasyPrint)

# Installation

### Ubuntu/Debian

```
> sudo apt-get install paperkey zbar-tools && pip install pillow qrcode weasyprint
> git clone https://github.com/cojomojo/easy-gpg-to-paper.git && cd easy-gpg-to-paper
> sudo cp gpg2paper/gpg2paper.py  /usr/local/bin
```

### macOS

```
> brew install paperkey zbar && pip install pillow qrcode weasyprint
> git clone https://github.com/cojomojo/easy-gpg-to-paper.git && cd easy-gpg-to-paper
> sudo cp gpg2paper/gpg2paper.py  /usr/local/bin
```

# Usage

```
> ./gpg2paper.py
usage: gpg2paper.py {import,export} ...

import/export gpg key from/to qrcode(s) or base64 string(s)

positional arguments:
  {import,export}  commands
> ./gpg2paper.py import -h
usage: gpg2paper.py import [-h] --pubkey PUBKEY [--png | --base64] --in
                           IN_FILENAMES [IN_FILENAMES ...]

import gpg key from qrcode(s)/base64

optional arguments:
  -h, --help            show this help message and exit
  --pubkey PUBKEY, -k PUBKEY
                        The full path to the public key file corresponding to
                        the secret key.
  --png, -png           Read the input file(s) as a png qrcode(s).
  --base64, -b64        Read the input file(s) as a base64 string.
  --in IN_FILENAMES [IN_FILENAMES ...], -i IN_FILENAMES [IN_FILENAMES ...]
                        The name of the input file(s) in the correct order.
> ./gpg2paper.py export -h
usage: gpg2paper.py export [-h] --keyid KEY_ID [--numfiles NUM_FILES]
                           [--base64] [--png] --out OUT_FILENAME

export gpg key to qrcode(s)

optional arguments:
  -h, --help            show this help message and exit
  --keyid KEY_ID, -k KEY_ID
                        The gpg secret key ID to export.
  --numfiles NUM_FILES, -n NUM_FILES
                        The number of files to split the key into.
  --out OUT_FILENAME, -o OUT_FILENAME
                        The base output file name.

  --base64, -b64        Output the gpg key as a base64 string in a file(s).
  --png, -png           Output the gpg key as a png qrcode(s)..
```

# Security Considerations

The protection and encryption status of and security requirements for storing your secret key are not changed by easy-gpg-to-paper.
Passphrase protected keys are output in their passphrase protected form.

# Contributing

### Ubuntu/Debian

```
> sudo apt-get install paperkey zbar-tools && pip install pillow qrcode weasyprint
> git clone https://github.com/cojomojo/easy-gpg-to-paper.git && cd easy-gpg-to-paper
> pip install . pytest
```

### macOS

```
> brew install paperkey zbar && pip install pillow qrcode weasyprint
> git clone https://github.com/cojomojo/easy-gpg-to-paper.git && cd easy-gpg-to-paper
> pip install . pytest
```

# Credits

I would like to thank these projects and people for inspiration:

+ [paperkey](http://www.jabberwocky.com/software/paperkey/)
+ user @joostrijneveld for [this gist](https://gist.github.com/joostrijneveld/59ab61faa21910c8434c)

# License
MIT
