# Copyright (c) 2012, Renato Florentino Garcia <fgarcia.renato@gmail.com>
#                     Stefano Pellegrini <stefpell@ee.ethz.ch>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the authors nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHORS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pysigset, signal
pysigset.suspended_signals(signal.SIGCHLD)
from builtins import str as text
from builtins import range

import gdb
#import matplotlib
#matplotlib.use('TKAgg')
#import matplotlib.pyplot as pl

import numpy as np
import struct
from functools import *


def get_blob_info(val):
    shape_size = val['shape_']['_M_impl']['_M_finish'] - val['shape_']['_M_impl']['_M_start']
    shape = []
    for s in range(0,int(shape_size)):
        shape.append(int((val['shape_']['_M_impl']['_M_start']+s).dereference()))

    data_address = val['data_']['px'].dereference()['cpu_ptr_']
    diff_address = val['diff_']['px'].dereference()['cpu_ptr_']

    return (shape , data_address , diff_address)


def get_blob_vals(shape, data_address, diff_address):
    """ Copies the image data to a PIL image and shows it.

    Args:
        width: The image width, in pixels.
        height: The image height, in pixels.
        n_channel: The number of channels in image.
        line_step: The offset to change to pixel (i+1, j) being
            in pixel (i, j), in bytes.
        data_address: The address of image data in memory.
        data_symbol: Python struct module code to the image data type.
    """

    data_size = reduce(lambda x, y: x*y, shape, 1)

    infe = gdb.inferiors()
    # Calculate the memory padding to change to the next image line.
    # Either due to memory alignment or a ROI.

    # Format memory data to load into the image.
    partition = shape[len(shape)-1]
    fmt = "".join(["f" for f in range(0,partition)])

    data = None
    diff = None
    if int(data_address):
        memory_data = infe[0].read_memory(data_address, data_size*4)
        data = np.array([struct.unpack(fmt, memory_data[4*partition*s:4*partition*(s+1)])
                         for s in range(0, int(data_size/partition))])
        data = data.reshape(tuple(shape))

    if int(diff_address):
        memory_diff = infe[0].read_memory(diff_address, data_size*4)
        diff = np.array([struct.unpack(fmt, memory_diff[4*partition*s:4*partition*(s+1)])
                         for s in range(0, int(data_size/partition))])
        diff = diff.reshape(tuple(shape))

    return data , diff

def blobget(arg):
    """Diplays the content of an opencv image"""


    # Access the variable from gdb.
    args = gdb.string_to_argv(arg)
    val = gdb.parse_and_eval(args[0])
    with pysigset.suspended_signals(signal.SIGCHLD):

        blob_info = get_blob_info(val)
        return get_blob_vals(*blob_info)





