# Classfication models

Two models were trained for the binary classification of abstracts (`class_abstract/`) and paragraphs (`class_paragraph/`), respectively, using the NLP library Simple Transformers ([https://simpletransformers.ai/](https://simpletransformers.ai/)). 
The Robustly Optimized BERT Pretraining Approach (RoBERTa) is employed.


## Usage

Model input: text organized as a list of string, each of which is an abstract or paragraph.

Model output: a list of class labels and raw model output for each text. Class label '1' stands for the AM fatigue abstract or the Method paragraph, whereas '0' stands for Non-AM-fatigue or Non-method.  

``` python
from simpletransformers.classification import ClassificationModel

# abstract classification
abstracts=['$ABSTRACT_1','$ABSTRACT_2','$ABSTRACT_...']
model = ClassificationModel("roberta", "$PATH/class_abstract/")
predictions, raw_outputs=model.predict(abstracts)

# paragraph classification
paragraphs=['$PARAGRAPH_1','$PARAGRAPH_2','$PARAGRAPH_...']
model = ClassificationModel("roberta", "$PATH/class_paragraph/")
predictions, raw_outputs=model.predict(paragraphs)
```

Please change '\$ABSTRACT_n' and '\$PARAGRAPH_n' to your target text and '\$PATH' to your local path where models locate.

For more details on the classification model, please refer to the web site of [Simple Transformers](https://simpletransformers.ai/)
