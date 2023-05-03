# TEXTract

Data extraction from text involves the following steps:

1. **Text acquisition**. The text are obtained from xml/html files, see `parser/` for details.

2. **Text classification**. Method and Non-method paragraphs are classified, which helps to get rid of irrelevant data in subsequent processes. See `classification/` for details

3. **Sentence splitting**. The ChemDataExtractor v2 ([http://chemdataextractor2.org/](http://chemdataextractor2.org/)) is used to split sentence, since it specializes in scientific text. 

4. **Regular expression**. Data are extracted by regular expression (RE) designed for AM fatigue, see `RE_AMfatigue/` for details.
