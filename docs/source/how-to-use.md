# How to use VerifyIO

The workflow for VerifyIO can generally be divided into three independent steps (Step 1 - Step 3). These steps require [Recorder](https://github.com/uiuc-hpc/Recorder/tree/dev) and [VerifyIO](https://github.com/uiuc-hpc/Recorder/tree/dev/tools/verifyio).
Additional scripts are available for exporting results as CSV files and visualizing them (Step 4 and Step 5).

### Prerequisite:


Recorder is the tracing tool we use to collect the execution trace of the targeted application. Please follow Recorder's [document](https://recorder.readthedocs.io) to install it. Once installed, make sure to set `$RECORDER_INSTALL_PATH` to the location of Recorder. 

VerifyIO is written in Python, so no installation is required. Ensure that the dependent python packages are installed. These include numpy and networkx.

### Usage:

- Case 1: You want to study your own applications. You need to run the applicatin with Recorder to generate the execution trace, then run VerifyIO on the trace file to perform the verification. For this use case, start from step 1.
- Case 2: If you just want to try out VerifyIO and don't want to trace any application, you can download some of the existing traces we uploaded on [Zenodo](https://doi.org/10.5281/zenodo.14553174). Once you have the trace saved locally, you can start from step 2. Those traces are used in our IPDPS paper. You are also welcome to read the reproducibility page, which provides instuctions to reproduce the results presented in the IPDPS paper.


#### Step 1:  Run the application with Recorder to collect the execution trace.
```bash
mpirun -np N -env LD_PRELOAD $RECORDER_INSTALL_PATH/lib/librecorder.so ./your-app

# On HPC systems, you may need to use srun or
# other job schedulers to replace mpirun, e.g.,
srun -n4 -N1 --overlap --export=ALL,LD_PRELOAD=$RECORDER_INSTALL_PATH/lib/librecorder.so ./your-app
flux run -n 4 --env LD_PRELOAD=$RECORDER_INSTALL_PATH/lib/librecorder.so ./your-app
```
For more information on the Recorder and guidance on its usage, please refer to its [document](https://recorder.readthedocs.io/latest/overview.html).

#### Step 2: Conflict detection

Run the conflict detector to report conflicting I/O accesses. A conflict pair involves two I/O operations that access an overlapping range of the same file and at least one is a write.
To detect conflicts, use the `conflict-detector` tool from Recorder:

```bash
$RECORDER_INSTALL_PATH/bin/conflict-detector /path/to/trace-folder
```
This command will write all detected conflicts to the file `/path/to/trace-folder/conflicts.dat`. Note this `conflits.dat` file is not human-readable, but is required for the next step.

#### Step 3: Semantic verification

The next step is to run the semantic verification using `verifyio.py`. It checks if the detected conflicting accesses are properly synchronzied. By default, MPI-IO semantics and the vector clock algorithm are used for verification.


```bash
# By default, it verifies the MPI-IO semantics
python ./verifyio.py /path/to/trace-folder

# Example 1: verifying POSIX consistsency:
python ./verifyio.py /path/to/trace-folder --semantics=POSIX

# Example 2: verifying Commit consistsency:
python ./verifyio.py /path/to/trace-folder --semantics=Commit
```

Available arguments:
* --semantics: Specifies the I/O semantics to verify. Choices are: POSIX, MPI-IO (default), Commit, Session, Custom.
* --algorithm: Specifies the algorithm for verification. Choices are: 1: Graph reachability, 2: Transitive closure, 3: Vector clock (default), 4: On-the-fly algorithm. (See our IPDPS paper for the discussion on different algoritms)
* --semantic_string: A custom semantic string for verification. Default is: "c1:+1[MPI_File_close, MPI_File_sync] & c2:-1[MPI_File_open, MPI_File_sync]""
* --show_details: Displays details of the conflicts.
* --show_summary: Displays a summary of the conflicts.
* --show_full_chain: Displays the call chain of the conflicts.

**Some techniqual notes :**

The verification code first matches all MPI calls to build a happens-before graph representing the happens-before order. Each node in the graph represents either an MPI call or an I/O call. If there exists a path from node A to node B, then A must happens-before B. 

Given a conflicing I/O pair of accesses *(op1, op2)*. With the help of the happens-before graph, we can figure out if op1 happens-before op2. If so, they are properly synchronzied. This works well for the POSIX semantics. For example, consider this path: 
> op1(by rank1) -> send(by rank1) -> recv(by rank2) -> op2(by rank2). 

This path tells us op1 and op2 are properly synchronized according to the POSIX semantics.
   
However, things are a little different with other consistency models. 
Take MPI-IO consistency as an example here, the MPI standard requires the use of the `sync-barrier-sync` construct to guarnatee sequencial consistency. In other words, the MPI-IO semantics (nonatomic mode) requires a `sync-barrier-sync` in between two conflicting operations for them to be considered properly synchronized. Here, the `barrier` can be replaced by a send-recv or a collective call. The `sync` is one of `MPI_File_open`, `MPI_File_close`, or `MPI_File_sync`.

Note that, according to the MPI standard, not all collective calls guarantee the temporal order (i.e., the `barrier` in the `sync-barrier-sync` construct) between the involved processes. The MPI standard explictly says the following collectives are guaranteed to impose the temporal order:

| ----------------------------------------- |
| - MPI_Barrier                             |
| - MPI_Allgather                           |
| - MPI_Alltoall and their V and W variants |
| - MPI_Allreduce                           |
| - MPI_Reduce_scatter                      |
| - MPI_Reduce_scatter_block                |
| ----------------------------------------- |

#### Step 4: Export Results to CSV

**Dependencies for step 4 & 5:**

Ensure the following dependencies are installed:

Python Libraries:

- **argparse**: For parsing command-line arguments.
- **pandas**: For data manipulation and analysis. Install using `pip install pandas`.
- **seaborn**: For advanced data visualization. Install using `pip install seaborn`.
- **matplotlib**: For creating static, animated, and interactive plots. Install using `pip install matplotlib`.
- **numpy**: For numerical computations. Install using `pip install numpy`.

VerifyIO results can be exported to a CSV format for further analysis by using [`verifyio_to_csv.py `](https://github.com/lalilalalalu/verifyio_scripts/blob/main/verifyio_to_csv.py). Use the following command, providing the output file (usually stdout from VerifyIO execution) as an argument:

```bash
python verifyio_to_csv.py /path/to/verifyio/output /path/to/output.csv
```
Optional arguments:
* --dir_prefix="/prefix/to/remove": Removes a specified prefix from the paths in the output.
* --group_by_api: Groups the output by API calls.

#### Step 5: Heatmap Visualization

To visualize the results from VerifyIO, use the [`verifyio_plot_heatmap.py`](https://github.com/lalilalalalu/verifyio_scripts/blob/main/verifyio_plot_violation_heatmap.py) script:

```bash
python verifyio_plot_heatmap.py --file=/path/to/output.csv
```
