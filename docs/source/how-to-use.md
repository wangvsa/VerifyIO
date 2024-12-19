# How to use VerifyIO

## Installation

### Prerequisites:

- Recorder: Please follow the Recorder [document](https://recorder.readthedocs.io) to install Recorder.
- Python packages: networkx and numpy


## Usage:

Case 1: You want to study your own applications. You need to run the applicatin with Recorder to generate the execution trace, then run VerifyIO on the trace file to perform the verification.
Again, please follow the Recorder document for installing Recorder and tracing.

If you just want to try out VerifyIO and don't want to trace any application, you can download some of the traces I uploaded here. Those are the traces I used for my IPDPS paper. You are also welcome to read the reproducibility page, which provides instuctions to reproduce the results presented in the IPDPS paper.


## Features

- Trace Collection: VerifyIO relines on Recorder to capture the detailed execution trace, which including calls from POSIX, MPI and high-level I/O libraryes. The Recorder trace can also be used for other analysis.
- Conflict Detection: Identifies conflicting I/O operations between processes.
- Synchronization Verification: Verifies proper synchronization according to specified consistency models. We currently support four widely-used consistency models: POSIX, Commit, Session, and MPI-IO.
- Consistency Issue Reporting: Provides call-chain information for improperly synchronized conflicts to aid debugging.
