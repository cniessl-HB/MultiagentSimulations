# Distributed sorted table.

A distributed table similar to the distributed chord table, but with alternative characteristics.

## Goals

A distributed simulation maintains a large number of individual agents running on multiple networked computers
This can be abstracted to multiple resource keys located across multiple nodes.

Each node needs to be able to find any resource keys in the minimal steps possible.
A distributed chord table is able to do this via the finger table, dynamically updating in the background as nodes enter and exit the distributed system.

However, the design goal was intended for the torrent protocol to quickly find and update resource tables.
Our own application has different design assumptions, and thus may find improved performance when accomodating those assumptions. 

## Assumptions

Nodes will all be known to eachother and are intended to run in a trusted/non-anonymous network.

The total number of resources may change over time, increasing or decreasing as a simulation runs.

Nodes should be as balanced as possible with the amount of resources they are responsible for running.

Overhead for maintaining the table should aim for best scalable performance. O(log(n)) as opposed to O(n) if possible.

## Design

Since resources are given an index or ID in numerical order, assigning resources to nodes becomes trivial via modulo calculation and assignment.

The bottleneck for performance then becomes maintaining a list of peer connections for each node, and finding the next available ID for a resource creation operation.
