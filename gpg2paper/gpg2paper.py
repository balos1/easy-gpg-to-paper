#!/usr/bin/env python

"""
Program for exporting and importing gpg keys to/from qrcode(s).


The MIT License (MIT)

Copyright (c) 2017-2019 Cody Balos

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
from fractions import gcd
import os
import subprocess
import sys
import qrcode
from weasyprint import HTML

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
                              help='''The full path to the public key file
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
                              required=False,
                              help='The gpg secret key ID to export.')
    export_parse.add_argument('--numfiles', '--numchunks', '-n',
                              action='store',
                              dest='num_chunks',
                              default=4,
                              type=int,
                              help='The number of chunks to split the key into.')
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
    format_group.add_argument('--jpg', '-jpg',
                              action='store_true',
                              dest='jpg',
                              default=False,
                              help='Output the gpg key as a jpeg qrcode(s).')
    format_group.add_argument('--pdf', '-pdf',
                              action='store_true',
                              dest='pdf',
                              default=False,
                              help='Output the gpg key in a pdf file.')
    export_parse.add_argument('--out', '-o',
                              action='store',
                              required=True,
                              dest='output_folder',
                              help='The output folder name.')

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
        try:
            # setting stderr to subprocess.STDOUT will silence the subprocess output
            chunk = subprocess.check_output(['zbarimg', '--raw', in_filename])
            base64str += chunk
        except subprocess.CalledProcessError as exc:
            print("[gpg2paper] ERROR: zbarimg returned %d" % exc.returncode)
            if exc.returncode == 4:
                print("[gpg2paper] ERROR: try downsampling the QR code or split the key into more images")
            sys.exit(exc.returncode)
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

    html = ''
    filename = ''
    no_html = False

    if args.key_id:
        chunks = export_as_b64(key_id=args.key_id, num_chunks=args.num_chunks)

    if args.png:
        paths = write_chunks(chunks=chunks,
                             output_folder=args.output_folder,
                             ext='PNG')
    elif args.jpg:
        paths = write_chunks(chunks=chunks,
                             output_folder=args.output_folder,
                             ext='JPEG')
    elif args.base64:
        no_html = True
        write_chunks(chunks=chunks,
                     output_folder=args.output_folder,
                     ext='txt')
    else:
        paths = write_chunks(chunks=chunks,
                             output_folder=args.output_folder,
                             ext='PNG')

    if not no_html:
        (filename, html) = create_html_file(num_chunks=args.num_chunks,
                                            outfile_paths=paths,
                                            outfile_path=args.output_folder)
        if args.pdf:
            create_pdf_file(html=html, outfile_path=args.output_folder)
        print('[gpg2paper] preview your QR codes in your browser file://%s' % os.path.join(filename))


def export_as_b64(key_id=None, num_chunks=4, stream=None):
    """
    The export command. With it you can export your gpg secret key to a base64 encoded string
    across n chunks.
    """
    secret = subprocess.Popen(['gpg', '--export-secret-key', key_id], stdout=subprocess.PIPE)
    paperkey = subprocess.check_output(['paperkey', '--output-type', 'raw'], stdin=secret.stdout)
    base64str = base64.b64encode(paperkey)
    chunks = chunk_up(base64str, num_chunks)
    return chunks


def write_chunks(chunks, output_folder, ext):
    """
    Writes the data chunks to png or jpg files.
    """

    if ext == 'txt':
        return write_chunks_b64(chunks, output_folder)
    else:
        codes_folder = make_output_dir(os.path.join(output_folder, 'images/'))
        outfile_paths = []
        for i, chunk in enumerate(chunks):
            # Set version to none, and use fit=True when making qrcode so the version,
            # which determines the amount of data the qrcode can store, is selected automatically.
            qrc = qrcode.QRCode(version=None)
            qrc.add_data(chunk)
            qrc.make(fit=True)
            image = qrc.make_image()
            filename = '%d.%s' % (i+1, ext.lower())
            outfile_paths.append(os.path.join('images', filename))
            image.save(os.path.join(codes_folder, filename), ext)
        return tuple(outfile_paths)


def write_chunks_b64(chunks, outfile_path):
    """
    Writes the data chunks to text files as base64 encoded strings.
    """

    outfile_ext = 'txt'
    out_filename = outfile_path.split('.')
    if len(out_filename) > 1:
        (out_filename, outfile_ext) = out_filename
    else:
        out_filename = out_filename[0]
    outfile_paths = []
    make_output_dir(out_filename)
    for i, chunk in enumerate(chunks):
        filename = '%s%d.%s' % (out_filename, i+1, outfile_ext)
        with open(filename, 'wb') as txt_file:
            txt_file.write(chunk)
            outfile_paths.append(filename)
    return tuple(outfile_paths)


def make_output_dir(output_folder):
    """
    Makes the directory to output the file to if it doesn't exist.
    """

    # check if output is to cwd, or is a path
    dirname = os.path.dirname(output_folder)
    if dirname != '' and not os.path.exists(dirname):
        try:
            os.makedirs(os.path.dirname(output_folder))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return os.path.dirname(output_folder)


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


def create_html_file(num_chunks, outfile_paths, outfile_path):
    """
    Creates HTML file with png/jpg QR codes placed neatly.
    """

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style type="text/css">
            html,body {
                height: 297mm;
                width: 210mm;
            }
            @page {
                size: a4;
                margin: 1mm;
            }
            img {
                width: %dmm;
                margin: 0 1mm 0 1mm
            }
        </style>
    </head>
    <body>
        <table id="contentarea">%s</table>
    </body>
    </html>
    """
    fit = fit_codes(num_chunks, outfile_paths)
    html = html % fit
    abspath = os.path.abspath(os.path.join(outfile_path, 'qrcodes' + '.html'))
    with open(os.path.join(outfile_path, 'qrcodes' + '.html'), 'w') as f:
        f.write(html)
    return (abspath, html)


def create_pdf_file(html, outfile_path):
    """Creates a PDF file from the HTML file with nicely placed QR codes.
    """
    doc = HTML(string=html, base_url=outfile_path)
    doc.write_pdf(os.path.join(outfile_path, 'qrcodes' + '.pdf'))


def fit_codes(num_chunks, outfile_paths, auto=True, width=None):
    """Optimally packs the QR code chunks into an HTML table representing an a4 piece of paper.

    `fit_codes` tries to ensure that codes are large enough to be scanned once printed
    by restricting the minimum QR code size to 25.4mm (1 inch) without padding. However, users
    should always test their QR codes once printed to ensure they are readable and are valid.

    It is possible to provide a set width for each QR code by passing setting `auto=False` and `width`
    to some width in mm.
    """
    # A4 paper is approx. 210mm x 297mm.
    # Make 25.4mm (1in) wide code is the minimum in order to minimize chance of the QR code
    # being to dense to be printed successfully.
    a4 = (210, 297)
    # pad 3mm (~1/8 inch)
    pad = 3
    if auto:
        # Try and fit codes in a minimal number of pages while maximizing their individual
        # size by finding the GCD of the a4 paper dimensions.
        # See https://en.wikipedia.org/wiki/Greatest_common_divisor#A_geometric_view for explanation.
        width = max((a4[0]-pad)/gcd(a4[0], a4[1]), 26)
    cols = (a4[0]-pad)//min(width, a4[0]-pad)
    html = ''
    for i in range(num_chunks):
        if i % cols == 0:
            html += '<tr>'
        td = '<td><center><h2>Chunk %d</h2></center><img src="%s"></td>'
        html += td % (i+1, outfile_paths[i])
        if (i+1) % cols == 0 or (i+1) == num_chunks:
            html += '</tr>'
    return (width-pad, html)


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
