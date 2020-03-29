SUMMARY = "HDF Simulator"
DESCRIPTION = "Random Forest Classifier for driver identification"

SRC_URI = "file://config.yml \
           file://hdf-simulator.py \
           file://hdf-simulator.service \
           "

S = "${WORKDIR}"

LICENSE = "CLOSED"

inherit systemd

do_install() {
	install -d ${D}/etc/hdf-simulator
	install -m 0644 ${WORKDIR}/config.yml  ${D}/etc/hdf-simulator/config.yml

	install -d ${D}/lib/systemd/system
	install -m 0644 ${WORKDIR}/hdf-simulator.service  ${D}/lib/systemd/system/hdf-simulator.service

	install -d ${D}/usr/bin
	install -m 0700 ${WORKDIR}/hdf-simulator.py ${D}/usr/bin/hdf-simulator.py
}

INSANE_SKIP_${PN} = "ldflags"

FILES_${PN} += " /etc/hdf-simulator /usr/bin /lib/systemd"

SYSTEMD_SERVICE_${PN} += "hdf-simulator.service"

SYSTEMD_AUTO_ENABLE_hdf-simulator = "enable"
