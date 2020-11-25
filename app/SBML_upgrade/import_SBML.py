import argparse, sys, os
import configparser
import subprocess
import rdflib
from processing_functions import *
from Id_mapping import Id_mapping

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="path to the configuration file")
parser.add_argument("--out", help="path to output directory")
parser.add_argument("--meta", help="path to table of metadata")
parser.add_argument("--format", help="format of the SBML RDF files, compatible with RDFlib")
parser.add_argument("--sbml", help="path to sbml file")
parser.add_argument("--version", help="version of the PMID-CID ressource, if none, the date is used")
args = parser.parse_args()

# Intialyze attributes and paths: 

if not os.path.exists(args.config):
    print("Config file : " + args.config + " does not exist")
    sys.exit(3)

try:    
    config = configparser.ConfigParser()
    config.read(args.config)
except configparser.Error as e:
    print(e)
    sys.exit(3)

namespaces = {
    "cito": rdflib.Namespace("http://purl.org/spar/cito/"),
    "compound": rdflib.Namespace("http://rdf.ncbi.nlm.nih.gov/pubchem/compound/"),
    "reference": rdflib.Namespace("http://rdf.ncbi.nlm.nih.gov/pubchem/reference/"),
    "endpoint":	rdflib.Namespace("http://rdf.ncbi.nlm.nih.gov/pubchem/endpoint/"),
    "obo": rdflib.Namespace("http://purl.obolibrary.org/obo/"),
    "dcterms": rdflib.Namespace("http://purl.org/dc/terms/"),
    "fabio": rdflib.Namespace("http://purl.org/spar/fabio/"),
    "mesh": rdflib.Namespace("http://id.nlm.nih.gov/mesh/"),
    "void": rdflib.Namespace("http://rdfs.org/ns/void#"),
    "skos": rdflib.Namespace("http://www.w3.org/2004/02/skos/core#"),
    "owl": rdflib.Namespace("http://www.w3.org/2002/07/owl#")
}

# Global
path_to_dumps = args.out + "/"
meta_table = args.meta
path_to_g_SBML = args.sbml
ftp = config["FTP"].get("ftp")

# SBML
sbml_version = args.version
sbml_rdf_format = config["SBML"].get("format")
gem_path = path_to_dumps + "GEM/" + sbml_version

# URIS
base_uri_SBML = "http://database/ressources/SMBL/"
Intra_eq_base_uri = "http://database/ressources/ressources_id_mapping/Intra/SBML/"

# PROCESSES
uri = base_uri_SBML + sbml_version

print("Try to move SMBL file to Virtuoso shared directory ...")
if not os.path.exists(gem_path):
    os.makedirs(gem_path)
try:
    subprocess.run("cp " + path_to_g_SBML + " " + gem_path + "/", shell = True, stderr=subprocess.STDOUT)
except subprocess.SubprocessError as e:
    print("There was an error when trying to move SBML file : " + e)
    sys.exit(3)

linked_grahs = [Intra_eq_base_uri + sbml_version]

update_f_name = "SBML_update_file.sh"
with open(path_to_dumps + update_f_name, "w") as update_f:
    pass

gem_file = os.path.basename(path_to_g_SBML)
create_update_file_from_ressource(path_to_dumps, "GEM/" + sbml_version + "/", gem_file, uri, update_f_name)

print("Import identifiers from Graph to create SBML URIs intra equivalences")
# Intialyze Object:
map_ids = Id_mapping(sbml_version, namespaces, ftp)
print("Import configuration table", end = '')
map_ids.import_table_infos(meta_table)
map_ids.get_graph_ids_set(gem_path + "/" + gem_file, uri, sbml_rdf_format)
print("Export SBML Uris intra equivalences ")
map_ids.export_intra_eq(path_to_dumps + "Id_mapping/Intra/", "SBML")
print("Try to load SMBL URIs intra equivalences in Virtuoso ...")

create_update_file_from_ressource(path_to_dumps, "Id_mapping/Intra/SBML/" + sbml_version + "/", "*.trig", '', update_f_name)
create_update_file_from_ressource(path_to_dumps, "Id_mapping/Intra/SBML/" + sbml_version + "/", "void.ttl", Intra_eq_base_uri + sbml_version, update_f_name)