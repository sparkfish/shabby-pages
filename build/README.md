`build/` contains scripts for producing an Augraphy dataset.

The following files are here:
1. `generate-kaggle-set.py`, which, given 150dpi document images in `/images/150dpi` will produce a dataset suitable for a Kaggle competition.
2. `shabbypipeline.py`, which contains a parametrized default Augraphy pipeline.
3. `grayscale.py`, which removes color from all images in a directory.
4. `letterfit.py`, which defines a class that can fit images to a 8.5"x11" Letter page, similar to a document scanner.
5. `gen_evaluation.py`, which produces an evaluation CSV from images in the `/images/cropped/test_cleaned` directory.

