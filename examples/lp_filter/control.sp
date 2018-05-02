* Note that inside control block the commands order is relevant

.control
* set variables
set noaskquit
set filetype=ascii ; rawspice.raw (see `write` command) in ascii format
set nobreak ; output.log won't page break data
set noacct

options NOINIT NOMOD

* ac small signal analysis with:
ac LIN 1025 1 100K ; N Fstart Fstop

run ; run the actual simulation

* output data
print V(vin) V(vout) ; irrelevant since we are parsing the raw file, not the log

* raw file path can be specified with -r flag: ngspice -r data.raw
* it defaults to ./rawspice.raw if a path is not specified with -r.
write
quit
.endc
