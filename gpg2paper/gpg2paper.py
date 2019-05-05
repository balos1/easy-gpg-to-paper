#!/usr/bin/env python

"""
Program for exporting and importing gpg keys to/from qrcode(s).


The MIT License (MIT)

Copyright (c) [2017] [Cody Balos]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import print_function, with_statement
import argparse
import base64
import errno
import os
import subprocess
import sys
import qrcode

def main():
    """
    Entry function. This is where arguments are parsed.
    """

    parser = MyParser(description='import/export gpg key from/to qrcode(s) or base64 string(s)',
                      add_help=False)
    subparsers = parser.add_subparsers(help='commands', dest='command')

    import_parse = subparsers.add_parser('import',
                                         description='import gpg key from qrcode(s)/base64')
    import_parse.add_argument('--pubkey', '-k',
                              action='store',
                              dest='pubkey',
                              required=True,
                              help=''' The full path to the public key file
                                       corresponding to the secret key.''')
    format_group = import_parse.add_mutually_exclusive_group()
    format_group.add_argument('--png', '-png',
                              action='store_true',
                              dest='png',
                              help='Read the input file(s) as a png qrcode(s).')
    format_group.add_argument('--base64', '-b64',
                              action='store_true',
                              dest='base64',
                              default=True,
                              help='Read the input file(s) as a base64 string.')
    import_parse.add_argument('--in', '-i',
                              action='store',
                              dest='in_filenames',
                              required=True,
                              nargs='+',
                              help='The name of the input file(s) in the correct order.')

    export_parse = subparsers.add_parser('export',
                                         description='export gpg key to qrcode(s)')
    export_parse.add_argument('--keyid', '-k',
                              action='store',
                              dest='key_id',
                              required=True,
                              help='The gpg secret key ID to export.')
    export_parse.add_argument('--numfiles', '-n',
                              action='store',
                              dest='num_files',
                              default=4,
                              type=int,
                              help='The number of files to split the key into.')
    format_group = export_parse.add_argument_group()
    format_group.add_argument('--base64', '-b64',
                              action='store_true',
                              dest='base64',
                              default=False,
                              help='Output the gpg key as a base64 string in a file(s).')
    format_group.add_argument('--png', '-png',
                              action='store_true',
                              dest='png',
                              default=False,
                              help='Output the gpg key as a png qrcode(s).')
    export_parse.add_argument('--out', '-o',
                              action='store',
                              required=True,
                              dest='out_filename',
                              help='The base output file name.')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if args.command == 'import':
        do_import(args)
    else:
        do_export(args)


def do_import(args):
    """
    The "import" CLI command. With it you can import a base64 encoded version
    of your secret gpg key directly to your gpg keyring.
    """

    base64str = b''
    if args.png:
        base64str = read_chunks_png(args.in_filenames)
    elif args.base64:
        base64str = read_chunks_b64(args.in_filenames)
    return import_from_b64(args.pubkey, base64.b64decode(base64str))


def import_from_b64(pubkey_path, private_bytes):
    """
    Imports the private GPG key to the gpg key ring.
    """

    paperkey = subprocess.Popen(args=['paperkey', '--pubring', pubkey_path],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
    (paperkey_stdout, _) = paperkey.communicate(private_bytes)
    gpg = subprocess.Popen(args=['gpg', '--import'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    return gpg.communicate(paperkey_stdout)


def read_chunks_png(in_filenames):
    """
    Reads base64 encoded private key data from many PNG QR codes.
    """

    base64str = b''
    for in_filename in in_filenames:
        chunk = subprocess.check_output(['zbarimg', '--raw', in_filename])
        base64str += chunk
    return base64str


def read_chunks_b64(in_filenames):
    """
    Reads base64 encoded private key data from many files.
    """

    base64str = b''
    for in_filename in in_filenames:
        with open(in_filename, 'rb') as in_file:
            chunk = in_file.read()
            base64str += chunk
    return base64str


def do_export(args):
    """
    The "export" CLI command.
    """

    if args.png:
        write_chunks_png(chunks=export_as_b64(args.key_id, args.num_files),
                         outfile_path=args.out_filename)
    if args.base64:
        write_chunks_b64(chunks=export_as_b64(args.key_id, args.num_files),
                         outfile_path=args.out_filename)


def export_as_b64(key_id, num_files):
    """
    The export command. With it you can export your gpg secret key to a base64 encoded string
    across n chunks.
    """

    secret = subprocess.Popen(['gpg', '--export-secret-key', key_id], stdout=subprocess.PIPE)
    paperkey = subprocess.check_output(['paperkey', '--output-type', 'raw'], stdin=secret.stdout)
    base64str = base64.b64encode(paperkey)
    chunks = chunk_up(base64str, num_files)
    return chunks


def write_chunks_png(chunks, outfile_path):
    """
    Writes the data chunks to png files.
    """

    make_output_dir(outfile_path)
    for i, chunk in enumerate(chunks):
        # Set version to none, and use fit=True when making qrcode so the version,
        # which determines the amount of data the qrcode can store, is selected automatically.
        qrc = qrcode.QRCode(version=None)
        qrc.add_data(chunk)
        qrc.make(fit=True)
        image = qrc.make_image()
        image.save('%s%d.png' % (outfile_path, i+1), 'PNG')
    return len(chunks)


def write_chunks_b64(chunks, outfile_path):
    """
    Writes the data chunks to text files as base64 encoded strings.
    """

    out_filename = outfile_path.split('.')
    outfile_ext = 'txt'
    if len(out_filename) > 1:
        (out_filename, outfile_ext) = out_filename
    else:
        out_filename = out_filename[0]

    make_output_dir(out_filename)
    for i, chunk in enumerate(chunks):
        with open('%s%d.%s' % (out_filename, i+1, outfile_ext), 'wb') as txt_file:
            txt_file.write(chunk)
    return len(chunks)


def make_output_dir(out_filename):
    """
    Makes the directory to output the file to if it doesn't exist.
    """

    # check if output is to cwd, or is a path
    dirname = os.path.dirname(out_filename)
    if dirname != '' and not os.path.exists(dirname):
        try:
            os.makedirs(os.path.dirname(out_filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def chunk_up(base64str, num_chunks):
    """
    Breaks a base64 encoded string into n equal size parts
    (the final chunk might be smaller than the others).
    """

    chunk_size = int(len(base64str)/num_chunks)
    chunks = []
    for i in range(num_chunks-1):
        low = i*chunk_size
        upper = (i+1)*chunk_size
        chunks.append(base64str[low:upper])
    chunks.append(base64str[(num_chunks-1)*chunk_size:])
    return chunks


class MyParser(argparse.ArgumentParser):
    """
    Custom ArgumentParser class that will print help when there was a misusage.
    """

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == "__main__":
    sys.exit(main())
