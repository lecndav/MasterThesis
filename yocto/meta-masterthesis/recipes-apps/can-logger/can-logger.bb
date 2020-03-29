SUMMARY = "CAN-Logger"
DESCRIPTION = "Inlcudes measured and canmeasured"

SRC_URI = "file://canmeasured \
					 file://canmeasured.service \
					 file://config.yml \
					 file://measured.conf \
					 file://measured.service \
					 file://measured.socket \
					 file://measured \
					 "


S = "${WORKDIR}"

LICENSE = "CLOSED"

inherit systemd

do_install() {
	install -d ${D}/etc/canmeasured
	install -m 0644 ${WORKDIR}/config.yml  ${D}/etc/canmeasured/config.yml

	install -d ${D}/etc
	install -m 0644 ${WORKDIR}/measured.conf  ${D}/etc/measured.conf

	install -d ${D}/lib/systemd/system
	install -m 0644 ${WORKDIR}/canmeasured.service  ${D}/lib/systemd/system/canmeasured.service
	install -m 0644 ${WORKDIR}/measured.service  ${D}/lib/systemd/system/measured.service
	install -m 0644 ${WORKDIR}/measured.socket   ${D}/lib/systemd/system/measured.socket

	install -d ${D}/usr/bin
	install -m 0700 ${WORKDIR}/canmeasured	${D}/usr/bin/canmeasured
	install -m 0700 ${WORKDIR}/measured	${D}/usr/bin/measured
}

INSANE_SKIP_${PN} = "ldflags"

FILES_${PN} += " /etc/canmeasured /usr/bin /lib/systemd /etc/measured.conf"

SYSTEMD_SERVICE_${PN} += "canmeasured.service"
SYSTEMD_SERVICE_${PN} += "measured.service"

SYSTEMD_AUTO_ENABLE_canmeasured = "enable"
SYSTEMD_AUTO_ENABLE_measured = "enable"
