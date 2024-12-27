# IPDPS'25 Reproducibility Effort

To ensure reproducibility, a Docker environment containing the required source code and traces has been provided. Since the standard test cases of the corresponding high-level I/O libraries were analyzed using VerifyIO for the IPDPS paper, a script was developed and adapted to automate this process. This enables the verification to be performed in batches for multiple traces. The following steps outline the process for handling multiple traces more efficiently:

## 1. Install and Run Docker

### Prerequisites

- Docker installed on your local system
- Ensure that you have the correct Docker image available locally. If not, pull the image from a Docker registry using:

### Pull our docker image

```bash
docker pull verifyio-image:v1
```

### Run the verifyio docker image

First, let's create a local directory to save the result.

```
mkdir ~/ipdps-verifyio-result
```

Then run the docker iamge.
```bash
docker run --rm -it -v ~/ipdps-verifyio-result:/ipdps --verifyio-image:v1 /bin/bash
```

Notes:
- With the `--rm` paramter, the docker container will be deleted after exit
- The `-v` options mounts your local directory to the docker directory `/ipdps`, so the data saved
  in the docker image's `/ipdps` will persit even after the docker container has been deleted.


### 2. Reproduce the IPDPS result:

Now the docker container should have started, and you should be at the `/ipdps` directory.

```bash
root@933cb4b115cb:/ipdps# pwd
/ipdps
```

Our IPDPS paper presents two tools: Recorder and VerifyIO, both has been installed under the `/source` directory.

```bash
root@933cb4b115cb:/ipdps# ls /source
Recorder  VerifyIO
root@933cb4b115cb:/ipdps# echo $RECORDER_INSTALL_PATH/
/source/Recorder/install/
root@933cb4b115cb:/ipdps# echo $VERIFYIO_INSTALL_PATH/
/source/VerifyIO/
```

### Download dataset

We have provided several scripts to easily reproduce the results. Next, we will work you through them.
Our paper studies the consistency compliance of 91 built-in tests from three high-level I/O libraries, we have uploaded
all trace files on [Zenodo](https://doi.org/10.5281/zenodo.14553174).

Run the following command to download those trace files.
```bash
$VERIFYIO_INSTALL_PATH/ipdps/00-download-dataset.sh
```

The script will download and decompress all trace files under `./dataset` directory.

```bash
root@933cb4b115cb:/ipdps# ls ./dataset/*
dataset/hdf5-1.14.4-3-recorder-traces:
2Gio   cache		 init_term  pflush2	 pread	   pshutdown	   shapesame  vfd
bigio  filters_parallel  mpi	    pmulti_dset  prestart  select_io_dset  testphdf5

dataset/netcdf-4.9.2-recorder-traces:
h_par		mpi_parallel  parallel	 parallel3  parallel5  parallel_compress  quantize_par
h_par_compress	nc4perf       parallel2  parallel4  parallel6  parallel_zlib	  simplerw_coll_r

dataset/pnetcdf-1.13.0-recorder-traces:
add_var		  flexible	  ivarn			  put_all_kinds       test_vard_rec	tst_redefine
alignment_test	  flexible2	  large_var_cdf5	  put_parameter       test_vardf	tst_symlink
attrf		  flexible_api	  last_large_var	  record	      test_vardf90	tst_vars_fill
buftype_free	  flexible_var	  mix_collectives	  redef1	      test_varm		tst_version
buftype_freef	  flexible_varm   modes			  scalar	      tst_def_var_fill	varn_contig
check_striping	  inq_num_vars	  ncmpi_vars_null_stride  test_erange	      tst_del_attr	varn_int
check_type	  inq_num_varsf   noclobber		  test_fillvalue      tst_dimsizes	varn_intf
collective_error  inq_recsize	  nonblocking		  test_get_varn       tst_free_comm	varn_real
erange_fill	  inq_recsizef	  null_args		  test_vard	      tst_info		vectors
error_precedence  iput_all_kinds  one_record		  test_vard_multiple  tst_max_var_dims
```

### Conflict detection:

The [`auto_detect.sh`](https://github.com/wangvsa/VerifyIO/blob/main/ipdps/auto_detect.sh) script can be used to process multiple traces and detect conflicts. The script requires the path to the directory containing the traces as an argument. Please adjust the configuartion for resource manager accordingly. 

```bash
$VERIFYIO_INSTALL_PATH/ipdps/01-detect-conflicts.sh ./dataset/pnetcdf-1.13.0-recorder-traces
```

### Semantic verification

The [`auto_verify.sh`](https://github.com/wangvsa/VerifyIO/blob/main/ipdps/auto_verify.sh) script can be used for verification. This script requires the path to the directory containing the traces, and the path to verifyio as arguments. By default, it verifies all supported semantics, i.e., POSIX, MPI-IO, Commit, Session with Vector clock algorithm.

```bash
$VERIFYIO_INSTALL_PATH/ipdps/02-perform-verification.sh ./dataset/pnetcdf-1.13.0-recorder-traces
```

## Step 3. Post-Processing and Visualization:

### Heatmap Plot

For visualizing up to three CSV files in a single heatmap, use the following argument:

```bash
python verifyio_plot_heatmap.py --files="/path/to/output1.csv" "/path/to/output2.csv" "/path/to/output3.csv"
```

Finally, exit the container once you are done.

```bash
exit
```
