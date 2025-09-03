#!/bin/bash
set -e 


QAT_8970_HOME=/home/user/Programs/peak_test/qat_8970
export ICP_ROOT=$QAT_8970_HOME/QAT-driver-8970

######## install QAT-8970-driver
# if [ -d "$ICP_ROOT" ]; then
#     cd $ICP_ROOT && make uninstall && make clean
#     rm -rf $ICP_ROOT
# fi

# mkdir -p $ICP_ROOT
# tar -zxof /home/user/Downloads/QAT.L.4.22.0-00001.tar.gz -C $ICP_ROOT


cd $ICP_ROOT 
############### ./configure --prefix=$QAT_8970_HOME/qat_8970_install
# ./configure --prefix=$QAT_8970_HOME/qat_8970_install --enable-uio=proxy
# make clean
# sudo make -j install 
sudo make samples-install LATENCY_CODE=1 SAMPLE_CODE_CORPUS_PATH=/home/user/DataFiles/silesia_data/silesia.tar # 运行时需要加参数 ./cpa_sample_code runTests=32 getLatency=1
export LD_LIBRARY_PATH=$QAT_8970_HOME/qat_8970_install/bin:$PATH
ldconfig
systemctl restart qat