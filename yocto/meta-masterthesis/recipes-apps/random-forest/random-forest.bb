SUMMARY = "Random Forest Classifier"
DESCRIPTION = "Random Forest Classifier for driver identification"

SRC_URI = "file://config.yml \
           file://random-forest.py \
           file://random-forest.service \
           "

S = "${WORKDIR}"

LICENSE = "CLOSED"

inherit systemd

do_install() {
	install -d ${D}/etc/random-forest
	install -m 0644 ${WORKDIR}/config.yml  ${D}/etc/random-forest/config.yml

	install -d ${D}/lib/systemd/system
	install -m 0644 ${WORKDIR}/random-forest.service  ${D}/lib/systemd/system/random-forest.service

	install -d ${D}/usr/bin
	install -m 0700 ${WORKDIR}/random-forest.py ${D}/usr/bin/random-forest.py
}

INSANE_SKIP_${PN} = "ldflags"

FILES_${PN} += " /etc/random-forest /usr/bin /lib/systemd"

SYSTEMD_SERVICE_${PN} += "random-forest.service"

SYSTEMD_AUTO_ENABLE_random-forest = "enable"
