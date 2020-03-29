SUMMARY = "Image for my masterhesis - driver identification based on driver behaviour"

require recipes-core/images/iot-eval-image.bb

EXTRA_IMAGE_FEATURES = " package-management"

IMAGE_INSTALL += " \
            python3 python3-pip python3-pandas python3-h5py python3-numpy python3-dateutil python3-pyyaml \
			can-logger \
			data-preprocessor \
			random-forest \
            hdf-simulator \
			dbc \
            driver-profiles \
	    "
# peak-linux-driver
# python3-scikit-build-native
#

IMAGE_INSTALL_remove += " opkg partclone"

EXTRA_USERS_PARAMS = "usermod -P root root;"
