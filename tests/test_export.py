"""
Test exporting functionality of easy-gpg-to-paper.
"""

import argparse
import os.path
import glob
import pytest
from gpg2paper import gpg2paper

KEY_NAME = "easy-gpg-to-paper-testenv"
KEY_ID = "98436C7A"
OUTPUT_ROOT = "tests/out"
OUTPUT_FILE = "testsout"
FULL_PATH = os.path.join(OUTPUT_ROOT, OUTPUT_FILE)

@pytest.mark.usefixtures("load_gpg_keys", "cleanup_export_output")
class TestExport:
    @pytest.mark.parametrize("args", [
        (argparse.Namespace(base64=False, command="export", key_id=KEY_NAME, num_files=4,
                            out_filename=FULL_PATH, png=True, size=512)),
        (argparse.Namespace(base64=True, command="export", key_id=KEY_NAME, num_files=4,
                            out_filename=FULL_PATH, png=False, size=512))
    ])
    def test_do_export_to_path(self, args):
        gpg2paper.do_export(args)
        if args.png:
            outfiles = glob.glob("%s*.png" % args.out_filename)
        elif args.base64:
            outfiles = glob.glob("%s*.txt" % args.out_filename)
        else:
            assert False
        assert len(outfiles) == args.num_files


    @pytest.mark.parametrize("args", [
        (argparse.Namespace(base64=False, command="export", key_id=KEY_NAME, num_files=4,
                            out_filename=OUTPUT_FILE, png=True, size=512)),
        (argparse.Namespace(base64=True, command="export", key_id=KEY_NAME, num_files=4,
                            out_filename=OUTPUT_FILE, png=False, size=512)),
    ])
    def test_do_export_to_cwd(self, args):
        gpg2paper.do_export(args)
        if args.png:
            outfiles = glob.glob("%s*.png" % args.out_filename)
        elif args.base64:
            outfiles = glob.glob("%s*.txt" % args.out_filename)
        else:
            assert False
        assert len(outfiles) == args.num_files


    @pytest.mark.parametrize("args", [
        (argparse.Namespace(base64=False, command="export", key_id=KEY_ID, num_files=4,
                            out_filename=FULL_PATH, png=True, size=512)),
        (argparse.Namespace(base64=True, command="export", key_id=KEY_ID, num_files=4,
                            out_filename=FULL_PATH, png=False, size=512))
    ])
    def test_do_export_by_key_id(self, args):
        gpg2paper.do_export(args)
        if args.png:
            outfiles = glob.glob("%s*.png" % args.out_filename)
        elif args.base64:
            outfiles = glob.glob("%s*.txt" % args.out_filename)
        else:
            assert False
        assert len(outfiles) == args.num_files


    @pytest.mark.parametrize("args", [
        (argparse.Namespace(base64=False, command="export", key_id=KEY_NAME, num_files=4,
                            out_filename=FULL_PATH, png=True, size=512)),
        (argparse.Namespace(base64=True, command="export", key_id=KEY_NAME, num_files=4,
                            out_filename=FULL_PATH, png=False, size=512))
    ])
    def test_do_export_by_key_name(self, args):
        gpg2paper.do_export(args)
        if args.png:
            outfiles = glob.glob("%s*.png" % args.out_filename)
        elif args.base64:
            outfiles = glob.glob("%s*.txt" % args.out_filename)
        else:
            assert False
        assert len(outfiles) == args.num_files


    @pytest.mark.parametrize("args", [
        (argparse.Namespace(base64=False, command="export", key_id=KEY_NAME, num_files=5,
                            out_filename=FULL_PATH, png=True, size=512)),
        (argparse.Namespace(base64=True, command="export", key_id=KEY_NAME, num_files=5,
                            out_filename=FULL_PATH, png=False, size=512)),
        (argparse.Namespace(base64=False, command="export", key_id=KEY_NAME, num_files=11,
                            out_filename=FULL_PATH, png=True, size=512)),
        (argparse.Namespace(base64=True, command="export", key_id=KEY_NAME, num_files=11,
                            out_filename=FULL_PATH, png=False, size=512))
    ])
    def test_do_export_odd_num_files(self, args):
        gpg2paper.do_export(args)
        if args.png:
            outfiles = glob.glob("%s*.png" % args.out_filename)
        elif args.base64:
            outfiles = glob.glob("%s*.txt" % args.out_filename)
        else:
            assert False
        assert len(outfiles) == args.num_files


    @pytest.mark.parametrize("args", [
        (argparse.Namespace(base64=False, command="export", key_id=KEY_NAME, num_files=4,
                            out_filename=FULL_PATH, png=True, size=512)),
        (argparse.Namespace(base64=True, command="export", key_id=KEY_NAME, num_files=4,
                            out_filename=FULL_PATH, png=False, size=512)),
        (argparse.Namespace(base64=False, command="export", key_id=KEY_NAME, num_files=8,
                            out_filename=FULL_PATH, png=True, size=512)),
        (argparse.Namespace(base64=True, command="export", key_id=KEY_NAME, num_files=8,
                            out_filename=FULL_PATH, png=False, size=512))
    ])
    def test_do_export_even_num_files(self, args):
        gpg2paper.do_export(args)
        if args.png:
            outfiles = glob.glob("%s*.png" % args.out_filename)
        elif args.base64:
            outfiles = glob.glob("%s*.txt" % args.out_filename)
        else:
            assert False
        assert len(outfiles) == args.num_files
