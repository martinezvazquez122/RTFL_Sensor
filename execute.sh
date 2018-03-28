while true
do 
    echo ===============================================
    cd /home/pi/Desktop/RTFL_Sensor
    sudo ./lora_sender
    echo ===============================================
    echo
    sleep 10
done
