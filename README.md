# ShabbyPages 2022

<p align="center">
    <img src="images/Article_Hero_Picture_Shadow.png?raw=true" title="Shabby Pages Logo">
</p>

ShabbyPages is a corpus of born-digital document images with both ground truth and distorted versions appropriate for use in training models to reverse distortions and recover to original denoised documents.  This state-of-the-art dataset with synthetically-generated real-world representations can be used to improve document layout detection, text extraction and OCR processes that depend on denoising and binarization preprocessing models.

Often, training data is not accompanied by clean ground truth sources, which leads to inaccurate training and severely-limited volumes of available training data.  This dataset was created using **Augraphy** to produce a synthetic yet realistic dataset based on ground truth documents.

This repository contains the following scripts for producing the dataset:

1. `letterfit.py`, which defines a class that can fit images to a 8.5"x11" Letter page, similar to a document scanner.
2. `shabbypipeline.py`, which contains a parametrized default Augraphy pipeline.
3. `daily_pipeline.py`, similar to 2 but with modifications for the Shabby Pages set.
4. `generate_kaggle_set.py`, which produces the full dataset for the Kaggle competition.
5. `remove_blank_pages.py`, which removes images with >99% white pixels from the competition set.
6. `make_submission.py`, which produces the submission file for the Kaggle competition.
7. `daily_build.py`, which produces a small test set every day.
8. `tweet.py`, which tweets an example image from the daily build.
9. `azure_file_service.py`, which manages connections to Azure Files.

# Distortion Pipeline

An **Augraphy** pipeline was applied to ground truth documents to generate _printed, scanned, copied_ and _faxed_ versions of documents encountered in the real world.  In order to preserve a pixel-level mapping between ground truth and distorted versions of documents, geometric transformations that skew or warp document images were avoided.

```
   .
   .
   .
pipeline details or visual
   .
   .
   .
```


# Credits / Prior Art
Below are related datasets that offer either real-world scanned documents or a combination of ground-truth and distorted versions.


## Real-World Datasets

* **RVL-CDIP** dataset consists of 400,000 B/W low-resolution (~100 DPI) images in 16 classes, with 25,000 images per class
https://www.cs.cmu.edu/~aharley/rvl-cdip/

* **Tobacco3482** dataset from Kaggle offers 10 different classes of forms, letters, reports, etc.
https://www.kaggle.com/patrickaudriaz/tobacco3482jpg

* **FUNSD (Form Understanding Noisy Scanned Documents)** dataset on Kaggle comprises 199 real, fully annotated, scanned forms that are noisy and vary widely in appearance.
https://www.kaggle.com/sharmaharsh/form-understanding-noisy-scanned-documentsfunsd


## Synthentic Datasets

* **NoisyOffice** dataset from University of California, Irvine contains noisy grayscale printed text images and their corresponding ground truth for both real and simulated documents with 4 types of noise: folded sheets, wrinkled sheets, coffee stains, and footprints.  For each type of font, one type of Noise: 17 files * 4 types of noise = 72 images.
https://archive.ics.uci.edu/ml/datasets/NoisyOffice

* **DDI-100 (Distorted Document Images)** is a synthetic dataset by Ilia Zharikov et al based on 7000 real unique document pages and consists of more than 100000 augmented images. Ground truth comprises text and stamp masks, text and characters bounding boxes with relevant annotations.
https://arxiv.org/abs/1912.11658

* **NIST-SFRS (Structured Forms Reference Set)** consists of 5,590 pages of binary, black-and-white images of synthesized documents from 12 different tax forms from the IRS 1040 Package X for the year 1988. These include Forms 1040, 2106, 2441, 4562, and 6251 together with Schedules A, B, C, D, E, F, and SE.
https://www.nist.gov/srd/nist-special-database-2


## The Augraphy Project
The synthetic distortions in this dataset were generated by [The Augraphy Project](https://github.com/sparkfish/augraphy) using a custom Augraphy pipeline to create realistic old and noisy documents from "born digital" sources.  This simulation of realistic paper-oriented process distortions creates large amounts of training data for AI/ML processes to learn how to remove those distortions.

Augraphy is a Python library that creates multiple copies of original documents though an augmentation pipeline that randomly distorts each copy -- degrading the clean version into dirty and realistic copies rendered through synthetic paper printing, faxing, scanning and copy machine processes.
