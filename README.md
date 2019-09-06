# Master thesis

Content ...

## asammdf good 2 know

Good to know snippets for `asammdf`.

### get signals from mf4 file

```python
signals = mdf_file.iter_channels(skip_master=False)
for signal in signals:
  print(signal.name)
```

## Start jupyther

`docker run -it --rm -p 8888:8888 -v ${PWD}/Testdata_mf4:/Testdata_mf4 -v ${PWD}/trips:/trips -v ${PWD}/jupyter/:/home/jovyan/work/ -v ${PWD}/Testdata_csv:/Testdata_csv my_jupyter`
