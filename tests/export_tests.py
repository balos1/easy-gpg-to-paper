"""
Test exporting functionality of easy-gpg-to-paper.
"""

import argparse
import os.path
import glob
import pytest
from gpg2paper import gpg2paper

KEYNAME = 'easy-gpg-to-paper-testenv'
KEY_ID = '98436C7A'
OUTPUT_ROOT = 'tests/out'
OUTPUT_FILE = 'testsout'
FULL_PATH = os.path.join(OUTPUT_ROOT, OUTPUT_FILE)

@pytest.mark.parametrize("args", [
    (argparse.Namespace(base64=False, command='export', key_id=KEYNAME, num_files=4,
                        outfile_name=FULL_PATH, png=True, size=512)),
    (argparse.Namespace(base64=True, command='export', key_id=KEYNAME, num_files=4,
                        outfile_name=FULL_PATH, png=False, size=512))
])
def test_do_export_to_path(args):
    gpg2paper.do_export(args)
    if args.png:
        outfiles = glob.glob('%s*.png' % args.outfile_name)
    elif args.base64:
        outfiles = glob.glob('%s*.txt' % args.outfile_name)
    else:
        assert False
    assert len(outfiles) == args.num_files


@pytest.mark.parametrize("args", [
    (argparse.Namespace(base64=False, command='export', key_id=KEYNAME, num_files=4,
                        outfile_name=OUTPUT_FILE, png=True, size=512)),
    (argparse.Namespace(base64=True, command='export', key_id=KEYNAME, num_files=4,
                        outfile_name=OUTPUT_FILE, png=False, size=512)),
])
def test_do_export_to_cwd(args):
    gpg2paper.do_export(args)
    if args.png:
        outfiles = glob.glob('%s*.png' % args.outfile_name)
    elif args.base64:
        outfiles = glob.glob('%s*.txt' % args.outfile_name)
    else:
        assert False
    assert len(outfiles) == args.num_files


@pytest.mark.parametrize("args", [
    (argparse.Namespace(base64=False, command='export', key_id=KEY_ID, num_files=4,
                        outfile_name=FULL_PATH, png=True, size=512)),
    (argparse.Namespace(base64=True, command='export', key_id=KEY_ID, num_files=4,
                        outfile_name=FULL_PATH, png=False, size=512))
])
def test_do_export_by_key_id(args):
    gpg2paper.do_export(args)
    if args.png:
        outfiles = glob.glob('%s*.png' % args.outfile_name)
    elif args.base64:
        outfiles = glob.glob('%s*.txt' % args.outfile_name)
    else:
        assert False
    assert len(outfiles) == args.num_files


@pytest.mark.parametrize("args", [
    (argparse.Namespace(base64=False, command='export', key_id=KEYNAME, num_files=4,
                        outfile_name=FULL_PATH, png=True, size=512)),
    (argparse.Namespace(base64=True, command='export', key_id=KEYNAME, num_files=4,
                        outfile_name=FULL_PATH, png=False, size=512))
])
def test_do_export_by_keyname(args):
    gpg2paper.do_export(args)
    if args.png:
        outfiles = glob.glob('%s*.png' % args.outfile_name)
    elif args.base64:
        outfiles = glob.glob('%s*.txt' % args.outfile_name)
    else:
        assert False
    assert len(outfiles) == args.num_files


@pytest.mark.parametrize("args", [
    (argparse.Namespace(base64=False, command='export', key_id=KEYNAME, num_files=5,
                        outfile_name=FULL_PATH, png=True, size=512)),
    (argparse.Namespace(base64=True, command='export', key_id=KEYNAME, num_files=5,
                        outfile_name=FULL_PATH, png=False, size=512)),
    (argparse.Namespace(base64=False, command='export', key_id=KEYNAME, num_files=11,
                        outfile_name=FULL_PATH, png=True, size=512)),
    (argparse.Namespace(base64=True, command='export', key_id=KEYNAME, num_files=11,
                        outfile_name=FULL_PATH, png=False, size=512))
])
def test_do_export_odd_num_files(args):
    gpg2paper.do_export(args)
    if args.png:
        outfiles = glob.glob('%s*.png' % args.outfile_name)
    elif args.base64:
        outfiles = glob.glob('%s*.txt' % args.outfile_name)
    else:
        assert False
    assert len(outfiles) == args.num_files


@pytest.mark.parametrize("args", [
    (argparse.Namespace(base64=False, command='export', key_id=KEYNAME, num_files=4,
                        outfile_name=FULL_PATH, png=True, size=512)),
    (argparse.Namespace(base64=True, command='export', key_id=KEYNAME, num_files=4,
                        outfile_name=FULL_PATH, png=False, size=512)),
    (argparse.Namespace(base64=False, command='export', key_id=KEYNAME, num_files=8,
                        outfile_name=FULL_PATH, png=True, size=512)),
    (argparse.Namespace(base64=True, command='export', key_id=KEYNAME, num_files=8,
                        outfile_name=FULL_PATH, png=False, size=512))
])
def test_do_export_even_num_files(args):
    gpg2paper.do_export(args)
    if args.png:
        outfiles = glob.glob('%s*.png' % args.outfile_name)
    elif args.base64:
        outfiles = glob.glob('%s*.txt' % args.outfile_name)
    else:
        assert False
    assert len(outfiles) == args.num_files
