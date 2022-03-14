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
FROM registry.gitlab.eox.at/vs/harvester:release-2.1.6

LABEL name="EOEPCA harvester" \
      vendor="EOX IT Services GmbH <https://eox.at>" \
      license="MIT Copyright (C) 2021 EOX IT Services GmbH <https://eox.at>" \
      type="EOEPCA harvester" \
      version="0.9.0"


RUN pip3 install \
    https://github.com/stactools-packages/sentinel2/archive/b6a7fbe01c72085f789dc7d33ab6de706d0ff5b4.tar.gz \
    pyyaml \
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
