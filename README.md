# Mini Workshop on OpenMC

This two-hour workshop hosted at the first Symposium on Advanced
Sensors and Modeling Techniques for Nuclear Reactor Safety aims
to introduce some basics of the [OpenMC Monte Carlo code](https://openmc.readthedocs.io/en/stable/). 


OpenMC is an open-source code originally written by Paul Romano at MIT to
provide a test bench for massively parallel computing while retaining a
realistic representation of physics.  Development continues at MIT 
in the [Computational Reactor Physics Group](https://crpg.mit.edu/) and other
organizations.  OpenMC is equipped with a rich Python API, which makes it
fun to use, and its connection to a variety of nuclear data makes it
reasonably fast to set up.

## Prerequisites

Attendees should have a working knowledge of the Linux command line and Python.
For attendees without such experience, there is an [earlier workshop on
Software Carpentry](https://katyhuff.github.io/2018-12-15-mumbai/) that 
attendees are **strongly encouraged** to attend;
register [here](https://goo.gl/forms/OCjAryhRSBTS0HaT2)!

Attendees should also have a basic understanding of reactor physics.
 
## Access to OpenMC

For this workshop, attendees can use OpenMC on their own machines or via
remote access to an off-site cluster. Log-in information will be provided 
prior to the workshop for registered participants.

For those who use the [Anaconda package manager]() on Linux or OS X, OpenMC 
can be installed via

```bash
robertsj@sampo ~/ $ conda config --add channels conda-forge
robertsj@sampo ~/ $ conda install openmc
```

For other ways to install OpenMC, please 
see the [Quick Install Guide](https://openmc.readthedocs.io/en/stable/quickinstall.html).

Note, installation on Windows is not well supported at this time, and 
folks without Linux or OS X are encouraged to install a suitable
interface for remotely connecting to the off-site cluster.  One such
interface is the `bash` environment 
provided by [Git for Windows](https://git-scm.com/downloads), which
is described as part of the preparation for the
[morning workshop](https://katyhuff.github.io/2018-12-15-mumbai/).  Other
interfaces include [Putty](https://www.putty.org/) 
and [MobaXterm](https://mobaxterm.mobatek.net/)

The sample inputs and other materials we'll use in the workshop can 
be obtained by cloning this repository via

```
git clone https://github.com/corps-g/asemot_openmc.git
```


## Schedule

The workshop is scheduled to begin at 1:30 pm.  The following is 
a coarse breakdown of topics

| Topic               | Duration |
|---------------------|----------|
| Overview of OpenMC (key features) | 15 min   |
| A basic pin cell (materials, geometries, settings, and statepoints)    | 30 min   |
| A basic assembly (universes, lattices, and tallies)   | 45 min   |
| Multigroup data  (cross-section generation and multigroup mode)   | 30 min   |




