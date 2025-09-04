#!/bin/bash
set -e

sync && echo 3 > /proc/sys/vm/drop_caches && sleep 1

if [ -z "$TASK" ]; then
    echo "❗错误: 必须设置 TASK 环境变量"
    exit 1
fi

task_name=$TASK  #qat-8970, qat-4xxx, cpu, csd, no-comp
echo "AAAA $task_name"


if [ "$task_name" = "qat-4xxx" ] || [ "$task_name" = "cpu" ]; then
    compression_option="zlib:1"  #no/zlib/zlib:1
    direct_io=0
    ramp_time=0

    if [ "$task_name" == "cpu" ]; then
        # kernel_version="6.5.0-45-generic"
        kernel_version="6.9.0++"
    else
        kernel_version="6.9.0++"
    fi

elif  [ "$task_name" == "csd" ] ||  [ "$task_name" == "no-comp" ]; then
    compression_option="no"  #no/zlib/zlib:1
    #CHANGED
    # direct_io=1
    # ramp_time=0
    direct_io=0
    ramp_time=0
    kernel_version="6.9.0++"
elif [ "$task_name" = "qat-8970" ]; then
    compression_option="zlib:1"
    direct_io=0
    ramp_time=30
    kernel_version="6.9.0-+"
fi

if [ "$kernel_version" == "6.9.0++" ]; then
    base_path="/lib/modules/$kernel_version/kernel/drivers/crypto/intel/qat"
    if [ "$task_name" == "qat-4xxx" ] && [ -f "$base_path/qat_4xxx/qat_4xxx.ko.zst.bak" ]; then
        echo "Switching to qat_4xxx..."
        if [ -f "$base_path/qat_c62x/qat_c62x.ko.zst" ]; then
            mv "$base_path/qat_c62x/qat_c62x.ko.zst" "$base_path/qat_c62x/qat_c62x.ko.zst.bak"
        fi
        if [ -f "$base_path/qat_4xxx/qat_4xxx.ko.zst.bak" ]; then
            mv "$base_path/qat_4xxx/qat_4xxx.ko.zst.bak" "$base_path/qat_4xxx/qat_4xxx.ko.zst"
        fi
        if lsmod | grep -q "^qat_c62x"; then
            echo "卸载模块: qat_c62x"
            sudo rmmod qat_c62x && echo "模块 qat_c62x 已成功卸载" || echo "卸载模块 qat_c62x 失败"
        else
            echo "模块 qat_c62x 未加载，无需操作"
        fi
        sudo depmod -a
        modprobe qat_4xxx
        echo "Operation completed for qat_4xxx."
    elif [ "$task_name" == "qat-8970" ] && [ -f "$base_path/qat_c62x/qat_c62x.ko.zst.bak" ]; then
        echo "Switching to qat_c62x..."
        if [ -f "$base_path/qat_4xxx/qat_4xxx.ko.zst" ]; then
            mv "$base_path/qat_4xxx/qat_4xxx.ko.zst" "$base_path/qat_4xxx/qat_4xxx.ko.zst.bak"
        fi
        if [ -f "$base_path/qat_c62x/qat_c62x.ko.zst.bak" ]; then
            mv "$base_path/qat_c62x/qat_c62x.ko.zst.bak" "$base_path/qat_c62x/qat_c62x.ko.zst"
        fi
        if lsmod | grep -q "^qat_4xxx"; then
            echo "卸载模块: qat_4xxx"
            sudo rmmod qat_4xxx && echo "模块 qat_4xxx 已成功卸载" || echo "卸载模块 qat_4xxx 失败"
        else
            echo "模块 qat_4xxx 未加载，无需操作"
        fi
        sudo depmod -a
        modprobe qat_c62x
        echo "Operation completed for qat_c62x."
    elif [ "$task_name" == "cpu" ]; then
        if [ -f "$base_path/qat_4xxx/qat_4xxx.ko.zst" ]; then
            mv "$base_path/qat_4xxx/qat_4xxx.ko.zst" "$base_path/qat_4xxx/qat_4xxx.ko.zst.bak"
        fi
        if [ -f "$base_path/qat_c62x/qat_c62x.ko.zst" ]; then
            mv "$base_path/qat_c62x/qat_c62x.ko.zst" "$base_path/qat_c62x/qat_c62x.ko.zst.bak"
        fi
        MODULES=("qat_4xxx" "qat_c62x" "intel_qat")

        for module in "${MODULES[@]}"; do
            if lsmod | grep -q "^${module}"; then
                echo "卸载模块: $module"
                sudo rmmod "$module"
                if [ $? -eq 0 ]; then
                    echo "模块 $module 已成功卸载"
                else
                    echo "卸载模块 $module 失败，请检查权限或依赖关系"
                fi
            else
                echo "模块 $module 未加载"
            fi
        done

    fi
elif [ "$kernel_version" == "6.9.0-+" ]; then
    base_path="/lib/modules/$kernel_version/kernel/drivers/crypto/intel/qat"
    if [ "$task_name" == "qat-8970" ] && [ -f "$base_path/qat_c62x/qat_c62x.ko.zst.bak" ]; then
        echo "Switching to qat_c62x..."
        if [ -f "$base_path/qat_4xxx/qat_4xxx.ko.zst" ]; then
            mv "$base_path/qat_4xxx/qat_4xxx.ko.zst" "$base_path/qat_4xxx/qat_4xxx.ko.zst.bak"
        fi
        if [ -f "$base_path/qat_c62x/qat_c62x.ko.zst.bak" ]; then
            mv "$base_path/qat_c62x/qat_c62x.ko.zst.bak" "$base_path/qat_c62x/qat_c62x.ko.zst"
        fi
        if lsmod | grep -q "^qat_4xxx"; then
            echo "卸载模块: qat_4xxx"
            sudo rmmod qat_4xxx && echo "模块 qat_4xxx 已成功卸载" || echo "卸载模块 qat_4xxx 失败"
        else
            echo "模块 qat_4xxx 未加载，无需操作"
        fi
        sudo depmod -a
        modprobe qat_c62x
        echo "Operation completed for qat_c62x."
    fi

fi


timestamp=$(date "+%Y-%m-%d_%H_%M_%S")
dev_name=$(nvme list | grep RS6U04A23B00K6CQ | cut -c 1-12)
# dev_name=$(nvme list | grep SN-8D64763976E5018B | cut -c 1-12)

export task_name # qat-8970, qat-4xxx, cpu, csd, no-comp
export compression_option # no, zlib, zlib:1
export timestamp
export ramp_time # 30, 0
export direct_io # 0, 1
export dev_name
export kernel_version

# ./run_throughput_test.sh $task_name $compression_option $timestamp $ramp_time $direct_io
# ./run_write_lat_test.sh $compression_option $timestamp $task_name
# ./run_read_lat_test.sh $compression_option $timestamp
# ./get_compress_ratio.sh $compression_option $task_name
