FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append_alen-iot-gateway-can-hw1-2 += " \
            file://disabling-onboard-CAN.patch \
"