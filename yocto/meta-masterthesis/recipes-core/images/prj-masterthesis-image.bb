SUMMARY = "Image for my masterhesis - driver identification based on driver behaviour"

require recipes-core/images/iot-eval-image.bb

EXTRA_IMAGE_FEATURES = " package-management tools-sdk tools-debug"
# tools-sdk tools-debug

DEPENDS += " go-cross-armv7vet2hf-neon go-dep"

IMAGE_ROOTFS_MAXSIZE = "1500000"
MENDER_DATA_PART_SIZE_MB = "150"
MENDER_STORAGE_TOTAL_SIZE_MB = "3072"

IMAGE_INSTALL += "\
            python3 python3-pip python3-pandas python3-numpy \
			can-logger \
			data-preprocessor \
			random-forest \
            hdf-simulator \
			dbc \
            driver-profiles \
            git git-perltools findutils libgfortran gfortran gfortran-symlinks libgfortran-dev \
	    "
# peak-linux-driver
# python3-scikit-build-native
#

IMAGE_INSTALL_remove += " opkg partclone minicom speedtest gpsd gps-utils htop nmap gsm-component uim wl18xx-bluetooth gdb gdbm ppp unzip wpa-supplicant bluez5 gnome-desktop-testing gtk-doc"

EXTRA_USERS_PARAMS = "usermod -P root root;"
