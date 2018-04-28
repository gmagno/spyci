* Note that inside control block the commands order is relevant

.control
* set variables
set noaskquit
set filetype=ascii ; rawspice.raw (see `write` command) in ascii format
set nobreak ; output.log won't page break data
set noacct

options NOINIT NOMOD

* transient analysis with:
*   - suggested time step: 10us
*   - duration of 10ms
*   - start time at 0s
*   - max time step: 10us
tran 10e−6 1e-2 0 10e-6

run ; run the actual simulation

* Output data
print V(vin) V(vout) ; irrelevant since we are parsing the raw file, not the log

* raw file path can be specified with -r flag: ngspice -r data.raw
* it defaults to ./rawspice.raw if a path is not specified with -r.
write
quit
.endc
