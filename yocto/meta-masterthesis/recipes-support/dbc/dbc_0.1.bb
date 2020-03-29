SUMMARY = "Install DBC files"
DESCRIPTION = "Install DBC files"

SRC_URI = "file://*.dbc"

S = "${WORKDIR}"

LICENSE = "CLOSED"

do_install() {
	install -d ${D}/etc/dbc
	install -m 0644 ${WORKDIR}/*.dbc  ${D}/etc/dbc/
}

FILES_${PN} += " /etc/dbc"
