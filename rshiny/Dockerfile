FROM rocker/shiny-verse:latest
#RUN apt-get update && apt-get --no-install-recommends install -y \
    #sudo \
    #pandoc \
    #pandoc-citeproc \
    #libgdal-dev \
    #libproj-dev \
    #libgeos-dev \
    #libudunits2-dev \
    #netcdf-bin \
    #libssl-dev \
    #libcurl4-gnutls-dev \
    #libcairo2-dev \
    #libxt-dev \
    #libssh2-1-dev \
    #libpng-dev
COPY . /
WORKDIR /
EXPOSE 3838
CMD R -e 'shiny::runApp("global.R", port=3838, host="0.0.0.0")'
