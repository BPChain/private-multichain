FROM debian:stable-slim
RUN apt-get update -y
RUN apt-get install wget -y
RUN cd /tmp && wget https://www.multichain.com/download/multichain-1.0.3.tar.gz
RUN cd /tmp && tar -xvzf multichain-1.0.3.tar.gz
RUN cd /tmp/multichain-1.0.3 && mv multichaind multichain-cli multichain-util /usr/local/bin
COPY masterEntry.sh /
RUN chmod +x masterEntry.sh
COPY slaveEntry.sh /
RUN chmod +x slaveEntry.sh
COPY multichain.conf /root/.multichain/multichain.conf
RUN cd /usr/local/bin && chmod +x multichaind multichain-cli multichain-util
RUN rm -rf /tmp/multichain*

