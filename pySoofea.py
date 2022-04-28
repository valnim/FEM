#! /usr/bin/env python
""" ------------------------------------------------------------------
This file is part of SOOFEA Python.

SOOFEA - Software for Object Oriented Finite Element Analysis

SOOFEA is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
------------------------------------------------------------------ """

import sys, os, imp
from argparse import ArgumentParser

src_path = str(os.path.join(os.path.abspath(sys.path[0]), "src"))
if src_path not in sys.path:
    sys.path.append(src_path)

VTKOutputHandler = None
try:
    from soofea.io.output_handler import VTKOutputHandler
except ImportError:
    pass


def main():
    parser = ArgumentParser(description="SOOFEA - Software for Object Oriented Finite Element Analysis")
    parser.add_argument('-i', '--input_file', help="Open SOOFEA python INPUT_FILE as mesh input file",
                        metavar="INPUT_FILE", required=True)
    parser.add_argument('-o', '--output_file', help="Output VTK OUTPUT_FILE to write results", metavar="OUTPUT_FILE",
                        required=True)
    parser.add_argument('-f', '--force', dest='force_overwrite',
                        action="store_const", const=True, default=False,
                        help="Overwrite given output file without asking")
    args = parser.parse_args()
    input_file_name = args.input_file
    output_file_name = args.output_file
    force_overwrite = args.force_overwrite

    sys.path.append(os.path.split(input_file_name)[0])
    input_script_name = os.path.splitext(os.path.basename(input_file_name))[0]
    fp, pathname, description = imp.find_module(input_script_name)
    module = imp.load_module(input_script_name, fp, pathname, description)

    print('Creating Model ...')
    model, analysis = module.read()

    if VTKOutputHandler is not None:
        output_handler = VTKOutputHandler(output_file_name, model.dimension, force_overwrite=force_overwrite)
    else:
        output_handler = None

    print('Start Analysis ...')
    if analysis:
        analysis.run(output_handler)
    elif output_handler is not None:
        print('No analysis provided! Writing only initial model data to the outputfile!')
        output_handler.write(model)
    print('... done')


if __name__ == "__main__":
    main()
