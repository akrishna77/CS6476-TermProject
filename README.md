# CS6476-TermProject

## Project Website
  https://akrishna77.github.io/visual-relationships/

## Contents

Here is a list of the functionality of each notebook in this repo:

* DataExploration.ipynb - Exploring the dataset, and code to generate tailored dataset for limited predicates.
* VisRel + All Pairs Detection.ipynb - Object Detection using Faster-RCNN and returning all possible BBox pairs.
* BBoxMaskClassifier.ipynb  - CNN classifier on top of bounding box masks.
* TripletLossNN.ipynb - Model using Triplet Loss + BBox Mask + Glove embeddings.
* BBoxWordEmbeddingModel.ipynb  - Model using BBox Mask + Glove embeddings + AlexNet latent vector.

* new_json_dataset - Tailored dataset for our 4 predicates, extracted from the VRD dataset.
* triplets_dataset - <anchor, positive, negative> triplets mined for our triplet-based approach.
* models - Contains our best models from the appraoches we tried.

  Our best model can be found at : [](https://tinyurl.com/r9pldad)
  
## Misc

  If you're having trouble viewing the notebook, copy the link to the `.ipynb` file into [Jupyter Notebook Viewer](https://nbviewer.jupyter.org/)!
