FROM ubuntu:xenial

RUN apt-get -y update 

# Install wine and related packages
RUN dpkg --add-architecture i386 
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates sudo software-properties-common

RUN add-apt-repository ppa:ubuntu-wine/ppa && apt-get update \
    && apt-get install -y wine1.8

COPY ./ /kolibri

SHELL ["/bin/bash", "-c"]

# Build kolibri windows installer.
RUN mkdir /installer/
RUN cd /kolibri/kolibri-installers/windows \
    && WHL_FILE=$(find ./ -name \*.whl) \
    && WHL_FILE=$(basename $WHL_FILE) \
    && WHL_FILE=${WHL_FILE:8} \
    && WHL_FILE_VERSION=${WHL_FILE:0:(${#WHL_FILEs}-21)} \
    && export KOLIBRI_BUILD_VERSION=$WHL_FILE_VERSION \
    && wine inno-compiler/ISCC.exe installer-source/KolibriSetupScript.iss

CMD cp /kolibri/kolibri-installers/windows/*.exe /installer/