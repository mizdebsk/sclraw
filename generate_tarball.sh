#!/bin/bash

baseurl="https://github.com/sonatype/plexus-compiler"


dname=$(basename ${baseurl})
version=`grep Version: *spec | sed -e 's/Version:\s*\(.*\)/\1/'`
echo $version

git clone "${baseurl}.git"

GIT_DIR="${dname}/.git" git archive --prefix "${dname}-${version}/" \
    ${dname}-${version} | xz > ${dname}-${version}.tar.xz



