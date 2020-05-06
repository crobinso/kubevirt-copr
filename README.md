Helper script for building [kubevirt](https://github.com/kubevirt/kubevirt)
[copr](https://copr.fedorainfracloud.org/) repos, as seen here:

https://copr.fedorainfracloud.org/groups/g/kubevirt/coprs/

The consumer here is kubevirt's [libvirt image](https://github.com/kubevirt/libvirt) which feeds their CI and distributed project. The main goals for these copr repos are:

* Provide new enough libvirt+qemu for kubevirt's needs. This occasionally means newer than what is what is in Fedora stable repos, similar to what [virt-preview](https://copr.fedorainfracloud.org/coprs/g/virtmaint-sig/virt-preview/) provides.
* Provide builds for as long as needed, so CI can reproduce building the container. This means a single copr repo is not acceptable, as it drops old build versions when a new version is submitted.
* Provide new libvirt + qemu builds before kubevirt wants to consume them. kubevirt doesn't want to test bleeding edge virt, but when they want to test a newish feature, they want the build available yesterday so they can do the work to incorporate it into their CI.

The way this script works:

* Runs nightly via cron on my local machine
* Checks [Fedora koji](https://koji.fedoraproject.org/koji/) build system for any new libvirt and qemu builds completed against rawhide.
* Rebuilds each build into its own copr project, using all stable Fedora releases as the target chroots

All new builds are made available for multiple Fedora stable releases, and kubevirt devs are free to mix and match qemu+libvirt version match as needed, via the individual copr projects.
