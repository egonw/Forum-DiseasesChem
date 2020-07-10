# Enrichment analysis to RDF graph

### Processes

The goal of this analysis is to convert significant associations from enrichment analysis in RDF triples.

The main source is an enrichment result table, created from the knowledge graph (See metab2mesh Section of this repository for more information), which can be found at *ftp adress*. For each enrichment result table, a metadata.txt file is associated to, indicating sources graphs and other parameters

Several graphs can be created from the same enrichment table using differents parameters.

Each created graph is linked to the configuration file used to create it, indicating source files and parameters, always placed in the description attribute of the associated void.ttl

### Config files

All used configuration files are stored in the *config* directory.

- [INPUT_TABLE]
  - path: path to the enrichment result file (eg. data/metab2mesh/with_Mesh_Thesaurus/2020-07-07/final_table_greater.csv) (TODO: Later must be a ftp adress !!!)
- [METADATA]
  - ressource: The name of the association ressource (eg. EnrichmentAnalysis/CID_MESH) 
  - version = The version of this ressource
  - targets = URIs of graphs targeted by this analysis (eg. PubChem and MESH graph URIs)
  - path_to_git_config = The path to the associated configuration file in the Git architecture from thr root (eg. app/Analyzes/.../.../config.ini)
- [PARSER] 
  - chunk_size: The chunk size used to read the enrichment result file (eg. 1000000)
  - padj_threshold = The adjusted p-value threshold (eg. 0.000001)
- [NAMESPACE]
  - ns: A list of URI namespaces (eg. *http://rdf.ncbi.nlm.nih.gov/pubchem/compound/*)
  - name = A list of prefix associated to namespaces, in the same order as in *ns* (eg. *compound*)
- [SUBJECTS]
  - name: The column name in the enrichment result file corresponding to desired triple subjects (eg. CID)
  - namespace = The namespace prefix of subjects, see NAMESPACE section (eg. compound)
  - prefix = A prefix which can be added before the content of the subject column (eg. CID)
- [PREDICATES]
  - name = The predicate (eg. related)
  - namespace = The namespace prefix of the predicate, see NAMESPACE section (eg. skos)
- [OBJECTS]
  - name = The column name in the enrichment result file corresponding to desired triple objects (eg. MESH)
  - namespace = The namespace prefix of subjects, see NAMESPACE section
  - prefix = A prefix which can be added before the content of the subject column.
- [OUT]
  - path_to_dumps: A path to the Docker Virtuoso share directory
  - file_prefix = Output file names

### Run

```bash
python3 app/Analyzes/Enrichment_to_graph/convert_association_table_to_triples.py --config="path/to/config.ini"
```

All triples will be exported in the Docker Virtuoso share directory. A file named *upload_Enrichment.sh* can then be used to load triples into Virtuoso.