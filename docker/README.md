This docker image contains pre-compiled Recorder and VerifyIO tools, and can be used to reproduce our IPDPS paper result.
Please see the document here: [https://verifyio.readthedocs.io/en/latest/ipdps.html](https://verifyio.readthedocs.io/en/latest/ipdps.html)

**Ingredients:**
- MPICH
- Python 3.11
- HDF5
- [Recorder](https://github.com/uiuc-hpc/Recorder)
- [VerifyIO](https://github.com/wangvsa/VerifyIO)

**Launch the container interactively.**

Example:
```bash
docker run --rm -v ./:/ipdps -it wangvsa/verifyio /bin/bash
```


From the bash prompt you should then be able to use the Recorder and VerifyIO tools.
```bash
root@933cb4b115cb:/ipdps# ls /source
Recorder  VerifyIO
root@933cb4b115cb:/ipdps# echo $RECORDER_INSTALL_PATH/
/source/Recorder/install/
root@933cb4b115cb:/ipdps# echo $VERIFYIO_INSTALL_PATH/
/source/VerifyIO/
```

Developer Notes:

Building a new image with tag v0.2:
```bash
docker build -t verifyio:v0.2 ./
```
