# JupyterAsciidocTemplate

Template for converting Jupyter notebooks to an asciidoc book.

1) Put the notebooks in the notebooks folder.

2) Install `nbmake` and `fastdoc`

https://semaphoreci.com/blog/test-jupyter-notebooks-with-pytest-and-nbmake
https://fastai.github.io/fastdoc/

```
pip install nbmake
pip install fastdoc
```

3) `cd` into `fd` and `git clone` your Atlas repo.

4) Review `prep_notebooks.py` and `post_process.py` to see if there's anything you need to adjust.

5) Run

```
sh build.sh
```

to copy over the notebooks, run the notebooks using nbmake, prep the notebooks, convert them, postprocess the asciidoc, and copy the files into the Atlas repo.

Note that `utils.py` configures Matplotlib to generate figures with high enough resolution for print. You can also configure it to generate other formats, etc.
