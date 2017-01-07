#!/usr/bin/python

"""
Program for exporting and importing gpg keys to/from qrcode(s).
"""

from __future__ import print_function
from __future__ import with_statement
import sys
import argparse
import subprocess
import base64
import qrencode

def main():
    """
    Entry function.
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
    import_parse.add_argument('--in', '-i',
                              action='store',
                              dest='infile_names',
                              required=True,
                              nargs='+',
                              help='The name of the input file(s) in the correct order.')
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


    export_parse = subparsers.add_parser('export',
                                         description='export gpg key to qrcode(s)')
    export_parse.add_argument('--keyid', '-k',
                              action='store',
                              dest='keyid',
                              required=True,
                              help='The gpg secret key ID to export.')
    export_parse.add_argument('--numfiles', '-n',
                              action='store',
                              dest='numfiles',
                              default=4,
                              type=int,
                              help='The number of files to split the key into.')
    export_parse.add_argument('--out', '-o',
                              action='store',
                              required=True,
                              dest='outfile_name',
                              help='The base output file name.')
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
    format_group.add_argument('--size',
                              action='store',
                              dest='size',
                              default=400,
                              help='Height and width of png qrcode(s) in pixels.')

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
    The import command. With it you can import a base64 encoded version
    of your secret gpg key directly to your gpg keyring.
    """
    base64str = b''
    for infile_name in args.infile_names:
        if args.png:
            chunk = subprocess.check_output(['zbarimg', '--raw', infile_name])
            base64str += chunk
        elif args.base64:
            with open(infile_name, 'rb') as infile:
                chunk = infile.read()
                base64str += chunk

    raw = base64.b64decode(base64str)
    paperkey = subprocess.Popen(['paperkey', '--pubring', args.pubkey],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
    (paperkey_stdout, _) = paperkey.communicate(raw)
    gpg = subprocess.Popen(['gpg', '--import'], stdin=subprocess.PIPE)
    gpg.communicate(paperkey_stdout)


def do_export(args):
    """
    The export command. With it you can export your gpg secret
    key to a base64 encoded string across n files, or into n qrcodes that
    collectivley form your key.
    """
    outfile_name = args.outfile_name.split('.')
    outfile_ext = 'txt'
    if len(outfile_name) > 1:
        (outfile_name, outfile_ext) = outfile_name
    else:
        outfile_name = outfile_name[0]

    secret = subprocess.Popen(['gpg', '--export-secret-key', args.keyid], stdout=subprocess.PIPE)
    paperkey = subprocess.check_output(['paperkey', '--output-type', 'raw'], stdin=secret.stdout)
    base64str = base64.b64encode(paperkey)
    chunks = chunk_up(base64str, args.numfiles)

    for i, chunk in enumerate(chunks):
        if args.png:
            (_, _, image) = qrencode.encode_scaled(chunk, int(args.size))
            image.save('%s%d.png' % (outfile_name, i+1), 'PNG')
        if args.base64:
            with open('%s%d.%s' % (outfile_name, i+1, outfile_ext), 'wb') as txt_file:
                txt_file.write(chunk)


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
    Custom ArgumentParser class that will print help when there was a misuage.
    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == "__main__":
    sys.exit(main())
