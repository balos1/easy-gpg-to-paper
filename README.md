# easy-gpg-to-paper

easy-gpg-to-paper aims to make exporting your secret gpg key to paper, and then restoring from paper, an easy and painless process.
It can export your key to qrcode(s), or it can export your key as a base64 encoded string(s). In the future the code will be cleaned 
up, and more features added. Anyone who wants to help out is more than welcome. 

Tested with python 2.7.12 and 3.5.2.

# Contributors

I would like to thank these projects and people for inspiration:

+ [paperkey](http://www.jabberwocky.com/software/paperkey/)
+ [pyqrencode](https://github.com/Arachnid/pyqrencode)
+ user @joostrijneveld for [this gist](https://gist.github.com/joostrijneveld/59ab61faa21910c8434c)

# Dependencies

+ [paperkey](http://www.jabberwocky.com/software/paperkey/)
+ [libqrencode](http://fukuchi.org/works/qrencode/)
+ [zbarimg](http://zbar.sourceforge.net/)
+ [my fork of pyqrencode](https://github.com/cojomojo/pyqrencode)

# Setup and Usage

1. Install the dependencies.
2. Clone/download the repository.
3. Add gpg2paper.py to your path and give it executable permissions.

```bash
> gpg2paper.py
usage: gpg2paper.py {import,export} ...

import/export gpg key from/to qrcode(s) or base64 string(s)

positional arguments:
  {import,export}  commands
>gpg2paper.py import -h
usage: gpg2paper.py import [-h] --pubkey PUBKEY --in INFILE_NAMES
                           [INFILE_NAMES ...] [--png | --base64]

import gpg key from qrcode(s)/base64

optional arguments:
  -h, --help            show this help message and exit
  --pubkey PUBKEY, -k PUBKEY
                        The full path to the public key file corresponding to
                        the secret key.
  --in INFILE_NAMES [INFILE_NAMES ...], -i INFILE_NAMES [INFILE_NAMES ...]
                        The name of the input file(s) in the correct order.
  --png, -png           Read the input file(s) as a png qrcode(s).
  --base64, -b64        Read the input file(s) as a base64 string.
> gpg2paper.py export -h
usage: gpg2paper.py export [-h] --keyid KEYID [--numfiles NUMFILES] --out
                           OUTFILE_NAME [--base64] [--png] [--size SIZE]

export gpg key to qrcode(s)

optional arguments:
  -h, --help            show this help message and exit
  --keyid KEYID, -k KEYID
                        The gpg secret key ID to export.
  --numfiles NUMFILES, -n NUMFILES
                        The number of files to split the key into.
  --out OUTFILE_NAME, -o OUTFILE_NAME
                        The base output file name.

  --base64, -b64        Output the gpg key as a base64 string in a file(s).
  --png, -png           Output the gpg key as a png qrcode(s).
  --size SIZE           Height and width of png qrcode(s) in pixels.
```

# Security Considerations

The protection and encryption status of and security requirements for storing your secret key are not changed by easy-gpg-to-paper.
Passphrase protected keys are output in their passphrase protected form.

# License
MIT