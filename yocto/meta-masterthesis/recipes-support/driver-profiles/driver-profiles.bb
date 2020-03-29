SUMMARY = "Install Driver Profiles"
DESCRIPTION = "Install Driver Profiles"

SRC_URI = "file://*.hdf"

S = "${WORKDIR}"

LICENSE = "CLOSED"

do_install() {
	install -d ${D}/data/profiles
	install -m 0644 ${WORKDIR}/*.hdf  ${D}/data/profiles/
}

FILES_${PN} += " /data/profiles"
