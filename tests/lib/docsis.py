# Copyright (c) 2015
#
# All rights reserved.
#
# This file is distributed under the Clear BSD license.
# The full text can be found in LICENSE in the root directory.
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os, config
from common import cmd_exists
import Tkinter

class docsis:
    """
    Name: docsis module
    Purpose: docsis operating.
    Input: Absolute path of text file
    Fuction:
        decode():
            return output file name(.txt)
        encode(output_type='cm_cfg')
            return output file name(.cfg or .bin)
    """
    def __init__(self, file_path):
        self.file_path=file_path
        self.dir_path=os.path.split(file_path)[0]
        self.file=os.path.split(file_path)[1]
        assert cmd_exists('docsis')
        assert cmd_exists('tclsh')
        tclsh = Tkinter.Tcl()
        assert tclsh.eval("package require sha1"), "please run apt-get install tcllib first"

    def decode(self):
        if '.cfg' in self.file:
            os.system("docsis -d %s > %s" %(self.file_path, self.file_path.replace('.cfg', '.txt')))
            assert os.path.exists(self.file.replace('.cfg', '.txt'))

            return  self.file.replace('.cfg', '.txt')

    def encode(self, output_type='cm_cfg'):
        if '.txt' in self.file and output_type=='cm_cfg':
            cmcfg_name=self.file.replace('.txt', '.cfg')
            cmcfg_path=os.path.join(self.dir_path, cmcfg_name)
            os.system("docsis -e %s /dev/null %s" % (self.file_path, cmcfg_path))
            assert os.path.exists(cmcfg_path)

            return  os.path.join(config.board['station'], cmcfg_name)
        elif '.txt' in self.file and output_type=='mta_cfg':
            mtacfg_name=self.file.replace('.txt', '.bin')
            mtacfg_path=os.path.join(self.dir_path, mtacfg_name)
            cmd = "tclsh %s/mta_conf.tcl" % os.path.dirname(__file__)
            os.system("%s %s -e -hash eu -out %s" % (cmd, self.file_path, mtacfg_path))
            assert os.path.exists(mtacfg_path)

            return  os.path.join(config.board['station'], mtacfg_name)
