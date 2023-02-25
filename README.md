# _ShabbyPages 2023_

Document denoising and binarization are fundamental problems in the document processing space, but current datasets are often too small and lack sufficient complexity to effectively train and benchmark modern data-driven machine learning models.  To fill this gap, we introduce *ShabbyPages*, a new document image dataset designed for training and benchmarking document denoisers and binarizers.

*ShabbyPages* contains over 6,000 clean "born digital" images with synthetically-noised counterparts ("shabby pages") that were augmented using the *Augraphy* document augmentation tool to appear as if they have been printed and faxed, photocopied, or otherwise altered through physical processes.

In [our paper](https://github.com/sparkfish/shabby-pages/blob/dev/paper/paper.pdf), we discuss the creation process of *ShabbyPages* and demonstrate the utility of *ShabbyPages* by training convolutional denoisers which remove real noise features with a high degree of human-perceptible fidelity, establishing baseline performance for a new *ShabbyPages* benchmark.

# What is _ShabbyPages_

To see the _ShabbyPages_ in action, [check out this notebook](https://github.com/sparkfish/shabby-pages/blob/dev/example_shabby_pipeline_generation.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1nvVIuD_G0M1fMVXDeYK2_q5-t6n-m4pA?usp=sharing) that uses the pipeline built with [Augraphy](https://github.com/sparkfish/augraphy).

_ShabbyPages_ is a corpus of born-digital document images with both ground truth and distorted versions appropriate for supervised learning use in training models to reverse distortions and recover the original clean documents. This state-of-the-art dataset with synthetically-generated real-world representations can be used to improve document layout detection, text extraction and OCR processes that depend on denoising and binarization preprocessing models.

Often, training data is not accompanied by clean ground truth sources, which leads to inaccurate training and severely-limited volumes of available training data.  This dataset was created using the latest version of **Augraphy** (8.1.0) to produce a synthetic yet realistic dataset based on ground truth documents.

| ![ShabbyPages Logo](images/Article_Hero_Picture_Shadow.png?raw=true) |
|-|

This repository contains the following scripts for producing the dataset:

1. `letterfit.py`, which defines a class that can fit images to a 8.5"x11" Letter page, similar to a document scanner.
2. `shabbypipeline.py`, which contains a parametrized default Shabby Pages pipeline.
3. `generate_kaggle_set.py`, which produces the full dataset for the Kaggle competition.
4. `remove_blank_pages.py`, which removes images with >99% white pixels from the competition set.
5. `make_submission.py`, which produces the submission file for the Kaggle competition.
6. `daily_build.py`, which produces a small test set every day.
7. `tweet.py`, which tweets an example image from the daily build.
8. `azure_file_service.py`, which manages connections to Azure Files.
9. `example_shabby_pipeline_generation.ipynb`, which is an example to generate shabby image from Augraphy and shabby pipeline using single input image.

# Distortion Pipeline

An **Augraphy** pipeline was applied to ground truth documents to generate _printed, scanned, copied_ and _faxed_ versions of documents encountered in the real world.  In order to preserve a pixel-level mapping between ground truth and distorted versions of documents, geometric transformations that skew or warp document images were avoided.

<p align="center">
    <img src="images/Shabby_Pipeline_Visualization.png?raw=true" title="Shabby Pipeline Visualization">
</p>


# _ShabbyPage-of-the-Day_
[Follow @AugraphyProject](https://twitter.com/AugraphyProject) to check out the each day's randomly generated shabby page.  The _ShabbyPages_ pipeline is used with the latest version of Augraphy each day to generate a _ShabbyPage-of-the-Day_ image posted on Twitter like the following:

<p align="center">
    <img src="images/Twitter_Example.png?raw=true" title="Shabby Page of the Day">
</p>

# Credits / Prior Art
Below are related datasets that offer either real-world scanned documents or a combination of ground-truth and distorted versions.


## Real-World Datasets

* **RVL-CDIP** dataset consists of 400,000 B/W low-resolution (~100 DPI) images in 16 classes, with 25,000 images per class
https://www.cs.cmu.edu/~aharley/rvl-cdip/

* **Tobacco3482** dataset from Kaggle offers 10 different classes of forms, letters, reports, etc.
https://www.kaggle.com/patrickaudriaz/tobacco3482jpg

* **FUNSD (Form Understanding Noisy Scanned Documents)** dataset on Kaggle comprises 199 real, fully annotated, scanned forms that are noisy and vary widely in appearance.
https://www.kaggle.com/sharmaharsh/form-understanding-noisy-scanned-documentsfunsd


## Synthetic Datasets

* **NoisyOffice** dataset from University of California, Irvine contains noisy grayscale printed text images and their corresponding ground truth for both real and simulated documents with 4 types of noise: folded sheets, wrinkled sheets, coffee stains, and footprints.  For each type of font, one type of Noise: 17 files * 4 types of noise = 72 images.
https://archive.ics.uci.edu/ml/datasets/NoisyOffice

* **DDI-100 (Distorted Document Images)** is a synthetic dataset by Ilia Zharikov et al based on 7000 real unique document pages and consists of more than 100000 augmented images. Ground truth comprises text and stamp masks, text and characters bounding boxes with relevant annotations.
https://arxiv.org/abs/1912.11658

* **NIST-SFRS (Structured Forms Reference Set)** consists of 5,590 pages of binary, black-and-white images of synthesized documents from 12 different tax forms from the IRS 1040 Package X for the year 1988. These include Forms 1040, 2106, 2441, 4562, and 6251 together with Schedules A, B, C, D, E, F, and SE.
https://www.nist.gov/srd/nist-special-database-2


## The Augraphy Project
The synthetic distortions in this dataset were generated by [The Augraphy Project](https://github.com/sparkfish/augraphy) using a custom Augraphy pipeline to create realistic old and noisy documents from "born digital" sources.  This simulation of realistic paper-oriented process distortions creates large amounts of training data for AI/ML processes to learn how to remove those distortions.

Augraphy is a Python library that creates multiple copies of original documents though an augmentation pipeline that randomly distorts each copy -- degrading the clean version into dirty and realistic copies rendered through synthetic paper printing, faxing, scanning and copy machine processes.

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# Citations
If you used _ShabbyPages_ in your research, please cite the project's dataset.

BibTeX:
```
@data{ShabbyPages2023,
  author = {The Augraphy Project},
  title = {ShabbyPages: A Reproducible Document Denoising and Binarization Dataset},
  year = {2023},
  url = {https://github.com/sparkfish/shabby-pages},
  version = {2023}
}
```

# License
Copyright 2023 Sparkfish LLC

_ShabbyPages_ is a free and open-source dataset and software recipe distributed under the terms of the [**MIT**](https://github.com/sparkfish/shabby-pages/blob/dev/LICENSE) license.
