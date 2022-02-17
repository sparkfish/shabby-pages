`build/` contains scripts for producing an Augraphy dataset.

The following files are here:
1. `samplegenerator.py`, which defines a class that can fit images to a 8.5"x11" Letter page, similar to a document scanner.
2. `fit.py`, which uses the stuff in `samplegenerator.py` to fit/crop all the images in a directory.
3. `shabbypipeline.py`, which contains a parametrized default Augraphy pipeline.
4. `grayscale.py`, which removes color from all images in a directory.
5. `build_single.py`, which uses a process pool to render many images concurrently, for a single resolution.
5. `build_multi.py`, which can be used for multiple-resolution builds and testing.
