FROM centos:7

# Python 2.7.5 is installed with centos7 image
# Add repository for PIP
RUN yum install -y epel-release

# Install pip
RUN yum install -y python-pip texlive-scheme-basic dvipng make

ENTRYPOINT [ "python" ]
