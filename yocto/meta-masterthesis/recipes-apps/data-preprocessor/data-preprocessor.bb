SUMMARY = "Data-Preprocessor"
DESCRIPTION = "Preprocesses MDF files and stores it in HDF5 files"

SRC_URI = "file://config.yml \
           file://data-preprocessor.py \
					 file://data-preprocessor.service \
					 "

S = "${WORKDIR}"

LICENSE = "CLOSED"

inherit systemd

do_install() {
	install -d ${D}/etc/data-preprocessor
	install -m 0644 ${WORKDIR}/config.yml  ${D}/etc/data-preprocessor/config.yml

	install -d ${D}/lib/systemd/system
	install -m 0644 ${WORKDIR}/data-preprocessor.service  ${D}/lib/systemd/system/data-preprocessor.service

	install -d ${D}/usr/bin
	install -m 0700 ${WORKDIR}/data-preprocessor.py ${D}/usr/bin/data-preprocessor.py
}

INSANE_SKIP_${PN} = "ldflags"

FILES_${PN} += " /etc/data-preprocessor /usr/bin /lib/systemd"

SYSTEMD_SERVICE_${PN} += "data-preprocessor.service"

SYSTEMD_AUTO_ENABLE_data-preprocessor = "enable"
