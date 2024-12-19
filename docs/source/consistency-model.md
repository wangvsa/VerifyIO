# Consistency Model

A consistency model defines the contract between the programmer and the system, specifying the rules under which shared data remains consistent. Adherence to the model ensures that the outcomes of read, write, and update operations are predictable and correct.
While POSIX consistency is the dominant model in HPC, other consistency models are also used in real-world I/O libraries and file systems.

Currently, VerifyIO supports four consistency models, which cover most of the widely used parallel file systems.

**POSIX Consistency:**

The [POSIX standard](https://pubs.opengroup.org/onlinepubs/9699919799.2018edition/) defines a strong consistency model that requires all writes to be immediately visible to all subsequent reads. While this model is simple to maintain in single-node environments, it is expensive to implement at scale. Nevertheless, major parallel file systems such as Lustre, GPFS, and BeeGF continue to support POSIX consistency due to its compatibility and widespread adoption.

**Commit Consistency:**

Commit consistency offers a relaxed model often used in user-level parallel file systems, such as [UnifyFS](https://github.com/llnl/unifyfs) and [SymphonyFS](https://www.osti.gov/servlets/purl/1619016). Here, synchronization is explicitly performed by issuing `commit` operations, typically by writers, to ensure data becomes globally visible. The data written prior to a commit is only visible after the commit operation completes. In practice, file systems using commit consistency may map a commit to an existing POSIX call; for example, UnifyFS uses the `fsync` call to signal a commit.

**Session Consistency:**

Session consistency, also known as close-to-open consistency, is another relaxed model that synchronizes data between processes when one process closes a file and another subsequently opens it. This model addresses cases where global visibility (ensured by commit consistency) is unnecessary, such as when only a subset of processes perform reads. Session consistency uses `close` and `open` operations to control visibility between processes.


**MPI-IO Consistency:**

MPI-IO, a part of the [MPI standard](https://www.mpi-forum.org/docs/), specifies MPI's I/O functionalities. MPI-IO's relaxed model ensures sequential consistency for conflicting accesses through a *sync-barrier-sync* construct. In this pattern, `MPI_File_open`, `MPI_File_close`, and `MPI_File_sync` serve as synchronization points for flushing or retrieving data, while barriers (e.g., `MPI_Barrier`, or point-to-point communications like `MPI_Send/MPI_Recv`) ensure proper ordering.
