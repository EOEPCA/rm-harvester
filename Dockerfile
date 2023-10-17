#------------------------------------------------------------------------------
#
# Project: prism view server
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
#------------------------------------------------------------------------------
# Copyright (C) 2021 EOX IT Services GmbH <https://eox.at>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#-----------------------------------------------------------------------------

# TODO: make this from a specific release, once released
FROM registry.gitlab.eox.at/vs/vs/harvester:release-4.1.3

LABEL name="EOEPCA harvester" \
      vendor="EOX IT Services GmbH <https://eox.at>" \
      license="MIT Copyright (C) 2021 EOX IT Services GmbH <https://eox.at>" \
      type="EOEPCA harvester" \
      version="0.9.0"


RUN pip3 install \
    stactools-sentinel2==0.3.0 \
    stactools-sentinel3==0.4.0 \
    stactools-landsat==0.4.1 \
    stactools-sentinel1==0.7.1 \
    https://github.com/stactools-packages/sentinel1/archive/ef8ae78c1573f3cf2ea5c7e4051798bbb56d84d9.tar.gz \
    pyyaml \
    boto3 \
    s3fs

RUN mkdir /harvester_eoepca
ADD harvester_eoepca/ \
    /harvester_eoepca/harvester_eoepca
ADD setup.py setup.cfg \
    /harvester_eoepca/
ADD MANIFEST.in \
    /harvester_eoepca
RUN cd /harvester_eoepca && \
    pip3 install .
