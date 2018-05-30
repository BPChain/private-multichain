FROM debian:9-slim
RUN apt-get -y update
RUN apt-get install wget python3-pip git -y
RUN cd /tmp && wget https://www.multichain.com/download/multichain-1.0.4.tar.gz
RUN cd /tmp && tar -xvzf multichain-1.0.4.tar.gz
RUN cd /tmp/multichain-1.0.4 && mv multichaind multichain-cli multichain-util /usr/local/bin
RUN rm -rf /tmp/multichain*
COPY requirements.txt /
RUN pip3 install git+git://github.com/BPChain/scenario-orchestration-service.git@v0.8
RUN pip3 install git+git://github.com/BPChain/blockchain_statistics_readout.git@v1.0
RUN pip3 install -r /requirements.txt
COPY python_sources /python_sources
RUN cd /usr/local/bin && chmod +x multichaind multichain-cli multichain-util
COPY shell_scripts/masterEntry.sh /
RUN chmod +x masterEntry.sh
COPY shell_scripts/slaveEntry.sh /
RUN chmod +x slaveEntry.sh
COPY multichain.conf /root/.multichain/multichain.conf





