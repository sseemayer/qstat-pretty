# qstat-pretty

NOTE: This fork is for use with the Torque Resource Manager, not GridEngine

qstat-pretty is a parser and pretty-printer for the output of the Grid Engine `qstat` program. It will parse the XML output produced by `qstat -x` and display it in a table.


![pstat screenshot](http://i.imgur.com/WkYaAyt.png)

Some nice features:

  * Table automatically grows with the size of the columns
  * Minimalistic tables
  * Can query local and remote grid status using SSH
  * Will auto-detect and parse Torque Resource Manager (defaults to original GridEngine parser)
 
## Getting started

qstat-pretty requires Python 2.6 or later (Python 3 supported!) and no additional modules.

To use locally:
  1. Check out qstat-pretty somewhere
  2. Run `python setup.py build` as non-root
  3. Link the pstat executable to your bin directory `ln -s "$(pwd)/pstat" ~/local/bin/`
  4. You can now use the `pstat` command.

qstat-pretty is still in very early development, so give me a message if you have problems getting things to run.

## Basic Usage

    $ pstat

## Advanced Usage

pstat supports getting job data from three sources: 

  * The local system (by running a `qstat` command) (default!)
  * Another host (by running `qstat` via `ssh`) (use the `-S [hostname]` option)
  * An XML file (use the `-X [xmlfile]` option)

All other parameters passed to pstat will be passed on to the qstat command. Examples:

  * Show my job status on the current system:

        $ pstat

  * Show my job status on the cluster head node reachable by `ssh clustmaster`:

        $ pstat -S clustmaster

  * Show job status for all users on clustmaster:

        $ pstat -S clustmaster -u "*"

  * Show job status on clustmaster for user jdoe:

        $ pstat -S clustmaster -u jdoe
