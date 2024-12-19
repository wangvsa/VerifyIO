VerifyIO 
========

High-performance computing (HPC) applications generate and consume substantial amounts of data, typically managed by parallel file systems. These applications access file systems either through the POSIX interface or by using high-level I/O libraries, such as HDF5 and NetCDF.
While the POSIX consistency model remains dominant in HPC, emerging file systems and popular I/O libraries increasingly adopt alternative consistency models that relax semantics in various ways, creating significant challenges for correctness and portability. For example, this paper lists a dozen of recent parallel file systems and their relaxec consistency models. 


Talk about the IPDPS paper, its result, findings and how to cite.

.. toctree::
   :maxdepth: 1
   :hidden:

   workflow
   how-to-use
   consistency-model
   ipdps


