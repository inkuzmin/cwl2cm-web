# cwl2cm-web
Web tool to convert CWL to ConceptMaps developed during the [BioHackathon 2018 Paris](https://bh2018paris.info/).

# Development
```bash
$ docker build . -t cwl2cm-web
$ docker run -d -p 80:80 cwl2cm-web
```

# Acknowledgements

## CWL
Amstutz, Peter; Andeer, Robin; Chapman, Brad; Chilton, John; Crusoe, Michael R.; Valls Guimerà, Roman; Carrasco Hernandez, Guillermo; Ivkovic, Sinisa; Kartashov, Andrey; Kern, John; Leehr, Dan; Ménager, Hervé; Mikheev, Maxim; Pierce, Tim; Randall, Josh; Soiland-Reyes, Stian; Stojanovic, Luka; Tijanić, Nebojša (2016): Common Workflow Language, draft 3. figshare.
https://dx.doi.org/10.6084/m9.figshare.3115156.v1

## EDAM
Ison, J., Kalaš, M., Jonassen, I., Bolser, D., Uludag, M., McWilliam, H., Malone, J., Lopez, R., Pettifer, S. and Rice, P. (2013). [EDAM: an ontology of bioinformatics operations, types of data and identifiers, topics and formats](http://bioinformatics.oxfordjournals.org/content/29/10/1325.full). _Bioinformatics_, **29**(10): 1325-1332.
[![10.1093/bioinformatics/btt113](https://zenodo.org/badge/DOI/10.1093/bioinformatics/btt113.svg)](https://doi.org/10.1093/bioinformatics/btt113) PMID: [23479348](http://www.ncbi.nlm.nih.gov/pubmed/23479348) _Open Access_

## gxformat2.py
The `gxformat2.py` is a patched version of `export.py` from https://github.com/jmchilton/gxformat2
