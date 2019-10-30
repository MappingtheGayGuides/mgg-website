#!/bin/sh
USER=mapping6
HOST=mappingthegayguides.org
DIR=/public_html/

hugo && rsync -avz public/ ${USER}@${HOST}:~/${DIR}

exit 0
