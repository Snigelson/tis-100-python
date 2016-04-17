## File formats and such

### Definition file

Defines the machine. Contains information about the model, nodes, and
connected inputs and outputs.

#### Node types

The following numbers are from the manual except for VISUALIZATION MODULE
which has no identifier in the manual, and FILE.

* T20 - RESERVED
* T21 - EXECUTION NODE
* T30 - STACK MEMORY
* T31 - RANDOM ACCESS MEMORY
* T40 - VISUALIZATION MODULE
* T50 - FILE

The code for T21 blocks are read from a file. If the name of a node is "FOO",
the code will be read from "FOO.T21".
