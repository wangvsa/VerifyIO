## VerifyIO

High-performance computing (HPC) applications generate and consume substantial amounts of data, typically managed by parallel file systems. These applications access file systems either through the POSIX interface or by using high-level I/O libraries, such as HDF5 and NetCDF.
While the POSIX consistency model remains dominant in HPC, emerging file systems and popular I/O libraries increasingly adopt alternative consistency models that relax semantics in various ways, creating significant challenges for correctness and portability. VerifyIO is designed to address these issues.
VerifyIO is a trace-driven I/O consistency verification workflow, consisting of four steps.
VerifyIO collects execution traces, detects data conflicts, and verifies proper synchronization against specified consistency models.

![verifyio-workflow](./_static/verifyio-workflow.png)
