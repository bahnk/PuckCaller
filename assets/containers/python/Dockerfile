
FROM ubuntu:21.04

RUN apt-get update
RUN apt-get --yes upgrade
RUN apt-get install --yes apt-utils

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London
RUN apt-get install --yes tzdata

RUN apt-get install --yes less

RUN apt-get install --yes \
	python3-airr \
	python3-alignlib \
	python3-bcbio \
	python3-biopython \
	python3-biopython-sql \
	python3-biotools \
	python3-bitbucket-api \
	python3-cobra \
	python3-cppy \
	python3-cpuinfo \
	python3-cutadapt \
	python3-dateparser \
	python3-dateutil \
	python3-datrie \
	python3-deeptools \
	python3-deeptoolsintervals \
	python3-distance \
	python3-dmidecode \
	python3-dmidecode-dbg \
	python3-dna-jellyfish \
	python3-dnaio \
	python3-dnapilib \
	python3-edlib \
	python3-et-xmlfile \
	python3-geneimpacts \
	python3-genometools \
	python3-geopandas \
	python3-git \
	python3-git-os-job \
	python3-git-repo-updater \
	python3-gitdb \
	python3-github \
	python3-gitlab \
	python3-gnuplot \
	python3-gnuplotlib \
	python3-google-auth \
	python3-google-auth-httplib2 \
	python3-google-auth-oauthlib \
	python3-google-i18n-address \
	python3-googleapi \
	python3-googleapi-samples \
	python3-h5py \
	python3-h5py-dbg \
	python3-h5py-mpi \
	python3-h5py-mpi-dbg \
	python3-h5py-serial \
	python3-h5py-serial-dbg \
	python3-h5sparse \
	python3-html5-parser \
	python3-html5lib \
	python3-htseq \
	python3-ipy \
	python3-ipykernel \
	python3-ipyparallel \
	python3-ipython \
	python3-ipython-genutils \
	python3-ipywidgets \
	python3-jinja-vanish \
	python3-jinja2 \
	python3-jupyter-client \
	python3-jupyter-console \
	python3-jupyter-core \
	python3-jupyter-server \
	python3-jupyter-sphinx \
	python3-jupyter-sphinx-theme \
	python3-jupyterlab-pygments \
	python3-jupyterlab-server \
	python3-keras \
	python3-keras-applications \
	python3-keras-preprocessing \
	python3-libxml2 \
	python3-louvain \
	python3-lxml \
	python3-nanoget \
	python3-nanostat \
	python3-nb2plots \
	python3-nbclient \
	python3-nbconvert \
	python3-nbformat \
	python3-nbsphinx \
	python3-nbxmpp \
	python3-networkx \
	python3-ngs \
	python3-nmap \
	python3-notebook \
	python3-numpy \
	python3-oauth \
	python3-oauth2client \
	python3-oauthlib \
	python3-octave-kernel \
	python3-opencv \
	python3-opencv-apps \
	python3-opengl \
	python3-openssl \
	python3-osmapi \
	python3-pairtools \
	python3-pairtools-examples \
	python3-pandas \
	python3-pandas-lib \
	python3-pandocfilters \
	python3-pdfkit \
	python3-pdfminer \
	python3-pip \
	python3-pkg-resources \
	python3-pkgconfig \
	python3-pkginfo \
	python3-pybedtools \
	python3-pybigwig \
	python3-pydot \
	python3-pydot-ng \
	python3-pydotplus \
	python3-pyopencl \
	python3-pyopencl-dbg \
	python3-pyopencolorio \
	python3-pyqt5 \
	python3-pysam \
	python3-rna \
	python3-rpy2 \
	python3-rpy2 \
	python3-sbml \
	python3-sbml5 \
	python3-sbml5-doc \
	python3-scapy \
	python3-scikit-fmm \
	python3-scikit-rf \
	python3-scipy \
	python3-scipy-dbg \
	python3-scrapy \
	python3-seaborn \
	python3-simpy \
	python3-simpy3 \
	python3-skimage \
	python3-skimage-lib \
	python3-sklearn \
	python3-sklearn-lib \
	python3-sklearn-pandas \
	python3-termcolor \
	python3-urllib3 \
	python3-virtualenv \
	python3-virtualenv-clone \
	python3-xlrd \
	python3-xlsxwriter \
	python3-xmlschema \
	python3-xmltodict \
	python3-yaml \
	python3-yaml-dbg \
	python3.9-numpy \
	python3.9-samba

RUN apt-get install --yes "ipython3"
RUN apt-get install --yes "jupyter*"
RUN apt-get install --yes "pandoc*"
RUN apt-get install --yes "libtiff*"
RUN apt-get install --yes "opencv*"
RUN apt-get install --yes "libopencv*"
RUN apt-get install --yes "texlive"
RUN apt-get install --yes "snakemake"

RUN apt-get install --yes \
	bowtie \
	bowtie-examples \
	bowtie2 \
	bowtie2-examples \
	bwa \
	clustalo \
	clustalw \
	clustalx \
	cutadapt \
	fastqc \
	igv \
	kallisto \
	kallisto-examples \
	libpicard-java \
	libpicard-java-doc \
	libseqan2-dev \
	libseqan3-dev \
	multiqc \
	picard \
	picard-tools \
	python-htseq \
	python3-cutadapt \
	python3-htseq \
	rna-star \
	rsem \
	salmon \
	samtools \
	seqan-apps \
	seqan3-doc \
	seqtk \
	trimmomatic

RUN pip install upsetplot
RUN pip install umap-learn
RUN pip install leiden
RUN pip install leidenalg
RUN pip install anndata
RUN pip install scanpy
RUN pip install jupyter-book
RUN pip install pyairtable

