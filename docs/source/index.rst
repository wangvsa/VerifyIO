VerifyIO 
========

HPC applications, such as scientific simulations and AI training, generate and process vast amounts of data, imposing significant demands on I/O systems to ensure efficient and correct data handling. These I/O demands are typically supported by parallel file systems. To ensure portability and compatibility, most widely deployed parallel file systems, such as Lustre and GPFS, conform to th `POSIX standard <https://pubs.opengroup.org/onlinepubs/9699919799.2018edition/>`_, providing both the POSIX interface and its associated consistency semantics.

HPC applications access these parallel file systems either directly through POSIX APIs or via higher-level I/O libraries (e.g., PnetCDF and HDF5). These libraries offer more user-friendly interfaces and implement various parallel I/O optimizations. While these libraries may eventually invoke POSIX APIs for portability, they often adopt relaxed consistency models (weaker than POSIX) for better performance. For instance, HDF5 and PnetCDF, both built on MPI-IO, use MPI-IO’s relaxed consistency model, which diverges from the strict guarantees of POSIX.

On the storage side, though many HPC systems continue to use POSIX-compliant file systems, recent trends show that emerging file systems such as BurstFS, UnifyFS, and GfarmBB---are choosing to relax POSIX consistency semantics while maintaining the POSIX interface. (Our HPDC `paper <https://dl.acm.org/doi/abs/10.1145/3431379.3460637>`_ studies many recent parallel file systems and their consistency models).
By keeping the POSIX interface, they support legacy applications while relaxing consistency semantics to improve performance. However, this trade-off introduces new risks related to portability and correctness, especially when applications assume stricter POSIX guarantees.

A key question is: How can we ensure that applications behave correctly on systems with different consistency models? Even if an application and its associated I/O libraries are programmed using POSIX APIs, how can we verify that they adhere to the specific consistency rules of the underlying system---especially when those rules deviate from POSIX? Furthermore, if a program violates these semantics, how can we diagnose the cause of a violation, e.g., whether it is caused by the application or the underlying I/O library?

There are several challenges in answering these questions. First, verifying correctness requires formal specifications of the target consistency model, as well as a rigorously designed verification algorithm.
Second, different I/O systems may relax POSIX semantics in different ways, making it difficult to design a generic verification algorithm that can account for all possible variations.
Third, as the I/O software stack deepens, HPC applications may involve multiple libraries and middleware, making it difficult to trace the root cause of semantics violations.
Lastly, the solution must be insightful, easy-to-use, and capable of helping both application developers and I/O system designers identify and resolve consistency issues. This requires significant designing and engineering efforts.

To tackle these challenges, we propose a trace-driven four-step verification workflow that systematically collects execution traces and verifies their adherence to specific consistency models. We use the framework from our previous `work <https://ieeexplore.ieee.org/abstract/document/10504997>`_ to specify I/O consistency models in a unified way. This aids in the design of a generic verification algorithm that can handle different consistency models. Further, we extend the framework to define the concept of a properly-synchronized execution, where no data conflicts occur, or all conflicts are properly synchronized according to the specified consistency model. For any execution, our algorithm examines the traces to verify whether it is properly synchronized, i.e., whether it follows the rules of the specified consistency model.
Although a properly synchronized execution does not guarantee that the entire application is synchronized correctly, because applications may follow different I/O execution paths. In our experience, this is rare though, most HPC applications tend to have a few if not one I/O path. More importantly, when an execution is found to be improperly synchronized, it indicates the presence of data races, suggesting potential consistency issues or implementation bugs in either the application or the I/O library.

The `VerifyIO <https://github.com/wangvsa/VerifyIO>`_ project is an open-source project that implements the above-mentioned verification workflow. VerifyIO contains four components, one for each step of the workflow:
(1) *a tracing tool* that collects execution traces with sufficient information for later steps
(2) *a conflict detection tool* that identifies data conflicts within the execution traces
(3) *an MPI matching tool* that matches MPI calls to establish the temporal order between all conflicting operations
(4) *a verification tool* that checks whether identified conflicts are properly synchronized according to the target consistency model.


.. toctree::
   :maxdepth: 1
   :hidden:

   workflow
   how-to-use
   consistency-model
   ipdps


