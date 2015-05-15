#SERIAL 201505111300

# Base the name of the software on the spec file
PACKAGE := $(shell basename *.spec .spec)
# Override this arch if the software is arch specific
ARCH = noarch

# Variables for clean build directory tree under repository
BUILDDIR = ./build
ARTIFACTDIR = ./artifacts
SDISTDIR = ${ARTIFACTDIR}/sdist
RPMBUILDDIR = ${BUILDDIR}/rpm-build
RPMDIR = ${ARTIFACTDIR}/rpms
DEBBUILDDIR = ${BUILDDIR}/deb-build
DEBDIR = ${ARTIFACTDIR}/debs

# base rpmbuild command that utilizes the local buildroot
# not using the above variables on purpose.
# if you can make it work, PRs are welcome!
RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
    --define "_sourcedir  %(pwd)/artifacts/sdist" \
    --define "_builddir %{_topdir}/rpm-build" \
    --define "_srcrpmdir %{_rpmdir}" \
    --define "_rpmdir %(pwd)/artifacts/rpms"

INSTALLDIR = /var/lib/zabbixsrv/alertscripts/
CONFIGDIR = /etc/zabbix/alertscripts/
DATADIR = /usr/share/${PACKAGE}

all: rpms

clean:
	rm -rf ${BUILDDIR}/ *~ ${PACKAGE}/

clean_all: clean
	rm -rf ${ARTIFACTDIR}/

install:
	mkdir -p ${DESTDIR}${INSTALLDIR}
	mkdir -p ${DESTDIR}${CONFIGDIR}
	mkdir -p ${DESTDIR}${DATADIR}
	cp -pr scripts/maintenance-mode ${DESTDIR}${INSTALLDIR}
	cp -pr config/maintmode.conf ${DESTDIR}${CONFIGDIR}
	cp -pr templates/*.xml ${DESTDIR}${DATADIR}


install_rpms: rpms
	yum install ${RPMDIR}/${ARCH}/${PACKAGE}*.${ARCH}.rpm

reinstall: uninstall install

uninstall: clean
	rm -f ${DESTDIR}${INSTALLDIR}/maintenance-mode
	rm -f ${DESTDIR}${CONFIGDIR}/maintmode.conf
	rm -rf ${DESTDIR}${DATADIR}

uninstall_rpms: clean
	rpm -e ${PACKAGE}

sdist:
	mkdir -p ${SDISTDIR}
	mkdir ${PACKAGE}
	cp -pr * ${PACKAGE}/ ||:
	tar -czf ${SDISTDIR}/${PACKAGE}.tar.gz \
		--exclude ".git" --exclude "*.log" \
		--exclude "build" \
		${PACKAGE}
	rm -rf ${PACKAGE}

prep_rpmbuild: sdist
	mkdir -p ${RPMBUILDDIR}
	mkdir -p ${RPMDIR}
	cp ${SDISTDIR}/${PACKAGE}.tar.gz ${RPMBUILDDIR}/

rpms: prep_rpmbuild
	${RPMBUILD} -ba ${PACKAGE}.spec

srpm: prep_rpmbuild
	${RPMBUILD} -bs ${PACKAGE}.spec
