# remove the old figures
rm -f atlas_repo/*_files/*

# copy the notebooks
cp ../notebooks/chap*.ipynb .

# test the notebooks (which also makes the figures)
pytest --nbmake --overwrite chap*.ipynb

# prepare the notebooks
python prep_notebooks.py

# build the asciidoc version
fastdoc_convert_all --path . --dest_path convert_book

# clean up the asciidoc
for CHAPTER in convert_book/chap*.asciidoc
do
    echo "Postprocessing $CHAPTER"
    python postprocess.py $CHAPTER
done

# push it to Atlas
cp -r convert_book/* atlas_repo
cp preface.asciidoc atlas_repo
#cd atlas_repo
#git add *
#git commit -m "Automated push to atlas"
#git push
