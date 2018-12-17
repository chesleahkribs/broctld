# broctld

Joint project with @KiraJ42 @RobertMinter
December 2018 - Concurrent Parallel and Distributive Programming 
Term Project 

broctld is a future project listed on the Bro website: https://www.bro.org/development/projects/broctld.html

The suggested design of broctld is defined as follows:

"We divide the broctld service into two parts that run in two separate processes. Most of the logic resides inside the “Main Process”; that one implements configuration, API, logging, inter-node communication., and almost everything else. The one thing that the Main Process doesn’t do is the supervision of the Bro processes: that’s performed by a separate “Supervisor Process”, which the Main Process controls.

When the broctld service starts up, the Main Process receives control first. Initially, no Supervisor Process will be running yet. The Main Process then spawns up a Supervisor Process and sets up communication between the two. A freshly started Supervisor Process will initially not yet be controlling any Bro processes. To start them, the Main Process instructs the Supervisor Process to spawn them; the supervisor Process then keeps the Bro processes running until the Main Process explicitly signals to stop some, or all.

The Main Process can shutdown its operation without stopping the Supervisor Process process, allowing for example to upgrade configuration or code without impacting the Bro processes. Once the Main Process starts up again, it will notice that a Supervisor Process is already running and will connect to it through the communication channel already established by the previous instance.

When the broctld system service gets shuts down through the OS, that means both broctld and the Bro processes need to terminate. The Main Process first instructs the Supervisor Process to stop the Bro processes. It then terminate the Supervisor Process, and finally shuts itself down."

This project implements the basic structure of broctld, i.e. the main and supervisor processes. Simple node programs (node.py) represent a running Bro process on a particular node. The supervisor process maintains those nodes, controlling and restarting them if necessary. The main process (broctld.py) communicates to the user with a simple shell interface and, while running, maintains control of the supervisor process and relays any relevants user commands to the nodes through the supervisor. 

However, should the main process be taken down for any reason including not only system errors but also maintenence or updates the supervisor process and the connected nodes with running Bro instances will continue to run with no interruption. Once the main program has been brought back online it will begin communicating with the supervisor process as soon as possible after restart. 

#Execution

python broctld.py       -- runs the broctld shell
python node.py          -- runs a "bro instance" on another terminal
