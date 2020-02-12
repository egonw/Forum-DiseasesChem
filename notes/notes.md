## Notes du développement de la base

* 10/02/2020 : 
  Inspiration de Metab2MeSH (**Metab2MeSH: annotating compounds with medical subject headings** doi:10.1093/bioinformatics/bts156) de 2012.
  Dans leur papier, la méthodo utilisée pour faire le lien entre métabolites et termes MeSH passe par un matching des substances. A partir de PubChem, pour chaque composé, ils extraient la liste des synonymes assoociés à ce composé, qu'ils matchent ensuite par rapport à la liste des PubMed subtances. La liste Pubmed substances est construite en extrayant l'index "substances" associée à chaque abstract des article PubMed présent de la base NLM PubMed. Ils disposent donc d'une liste de substances PubMed pour lesquelles ils sont un ensemble d'article associés 
  En matchant les synonymes, ils créent ainsi des liens entre les PubChem Compound et les PubMed Substances. Ainsi, chaque PubMed Substances ayant une liste de publications associées, ils ont pour chaque composées pubmed, en fonction du matching des synonymes associées par rapport aux substances PubMed un liste d'article. A partir des articles ils extraient les meSH associés aux catégories : Diseases, Anatomy, Chemicals and Drugs, Phenomena and Processes, Organisms, Psychiatry and Psychology, Anthropology, Education, Sociology and Social Phenomena, Technology, Industry, and Agriculture. ensuite, ils font des tests d'enrichissement pour tester la signficativité de chaque associées PubChem Compounds <-> MeSH term.

  Mais en 2016 est sorti un article de la base PubChem (**Literature information in PubChem: associations between PubChem records and scientific articles** DOI 10.1186/s13321-016-0142-6) :

  Dans cet article ils explique que désormais la base PubChem fournit des associaions PubChem compounds - litterature. En gros, il y a 4 types de sources d'association PuchChem CID - PMID : 
  	- **Depositor-provided corss-references :**
	  Ex:  IBM Almaden Research Center, CTD, ChemDB, etc ...
	  Ce sont des providers externes qui fournissent des associations CID - PMID, à partir d'algo de Text-Mining par e'xemple des papieres qui metionnent la molécule (IBM), ou de la base CTD par exemple qui fournit des anntotations curées et inférées. Ainsi, certaines des références sont issues de curations manuelles et d'autres d'algo de text-mining, certains ce focalise par exemple sur des domaines particuliers (ex: IEDB spécialisé en Immunologie epitope ) ce qui explique la disproportion des cross-reference fournies par les différents providers. Voila ce que j'ai pu trouver sur les annotation fournit par IBM - Almaden : "The IBM BAO strategic IP insight platform (SIIP) aggregates patent and scientific literature data and offers powerful search and analytics capabilities to comb intellectual property for new insights. It uses a computer-driven method for curating and analyzing massive amounts of patents, scientific content and molecular data, automatically extracting chemical entities from textual content as well as from images and symbols."

	- **Bioactivity data extracted from scientific articles :**
	  Certaines autres base de données telles que *ChemBL*, fournisse des informations sur des expériences dans lesquelles est impliquée la molécule. Ainsi, à cette molécule est associée un ensemble de papiers décrivant des expérieences (assay) avec donc des informations sur les méthodes de détections utilisés, les protocoles expérimentaux, les maladies associées, etc ...Il s'agit donc d'article parlant d'expérience dans lesquelles serait impliqué la molécule. *ChemBL* permet également d'enrichir la table BioAssay de pubChem. *IUPHAR* et *BPS* fournissent des références bibliographique sur l'activité des ligand sur des cibles thérapeutique. *PDBBind* litterature associées aux interaction Proteine (ou complexe Proteiques) - Ligand. *BindingDB* fournit des références sur l'affinité des liaisons entre des ligand et des proteines considérés comme des cibles thérapeutiques. *GLIDA* founie des informations sur les intéraction entre ligand et GPCR (récepteurs couplés à des protéines G). Enfin, certaines associations sont diretectment rensignés par les auteurs en indiquant leur publication dans la catégorie BioAssay de PubChem.       
	- **Chemical information provided by journal publishers :** 
	  Plusieurs publishers fournissent également des associations PubChem-PubMed, lorsque l'article est publié certains journaux (ex; Nature Chemical Biology) certains journaux lie directement leur article aux molécules PubChem identifiées dans l'étude.
	- **Automated annotations of PubChem records with PubMed articles via MeSH** :
	  C'est en gros ce que faisait Metab2MeSH. Mais tout les noms (synonymes) associés à un PubChem compound ne sont pas utilsé, les noms chimiques sont filtrés par rapport à la cohérence des associations chemical_name/structures des synonymes, par exemple en regroupant sous un même termes différentes formes de la molécule à différents états de charge par exemple. Ainsi, pour chaque PubChem compound, on obtient une liste de "filtered synonyms"   Les PubChem chemical Names sont matchés contre les concepts MeSH, par le biais des synonymes, permettant de créer l'association PubChem - MeSH qui permettent de liers les PMID associés au MeSH au composé Pubmed. On a ainsi : CID -> Name -> MeSH -> PMID).

Ces infos peuvent être trouvées à plusieurs endroits sur le DocSums, quand on fait une recherche sur le NCBI PubChem compounds, on peut sélectionner des compounds associées à jotre recherche et ensuite, Find l'onglet "Find Related Data", on peut trouver les papiers associées, en filtrant si on le souhaite par sources: providers, MeSH annot ou Publisher.
On a aussi ces infos dans l'onglet litterature de la page pubChem associée au composé, ou pareil, on a par sources *Depositor Provided Citations* pour les références Depositor-provided, *NLM Curated PubMed Citations* pour les associations faîtes par le biais de l'annotation MeSH, et enfin *xxx References* pour celles fournies par les Publishers.
Pour les stats un peu plus descriptives, regarder la partie *Discussion* de l'article. Ainsi : 
	- Très peu d'association sont fournies par les Publishers visiblement.
	- La plupart des PubChem Compound n'ont pas plus de 10 PMIDS associées (95% depositors provided et 70% MeSH auto-annotation).
	- Ils s'interressent ensuite à l'overlap que l'on peut trouver entre les associations CID-PMID fournies par les *Depositor-provided* et celle de *MeSH-annotation*. Ainsi, sur les 39.2 Millions d'association 4% sont communes entre les deux sources -> annotation *orthogonales*, vraiment des points de vue différentes -> complémentarité !
	- Dans cet ensemble des 4% de paires CID-PMID les CID impliqués représente 10% et les PMID 19% de tout ceux qui sont trouvés des les paires CID-PMID
   	- Il y a beaucoup moins de liens CID - PMID issues des *Depositor-provided* que ceux issus des annot meSH, **MAIS**, il y a beaucoup de CID annotés avec une association vers un PMID à partir des *Depositor-provided* Cela s'explique par le fait seul des composés assez connus et étudiés sont annotés dans les MeSH. En effet, les associations générés par les MeSH peuvent ignorer la spécificité, l'identité, du produit chimique pour annoter des termes MeSh qui représentent plutôt des "familles chimiques", à moins que le terme MeSH soit suffisament connu pour être une feuille a par entière du thésaurus MeSH. Ainsi des associations *Depositor-provided* ne souffre pas de ce problème et peuvent permettre d'annoter beaucoup plus de molécules.	  
	- Par contre les faut indiquer que PubChem ne fournie aucun contrôle supplémentaire sur les association fournies par les providers et que la qualité de ces annotations dépend uniquement des contrôles fait par les providers.	       
  
* * *

Alors, on sait que l'on peut récupérer les associations CID - SID - PMID - MeSH à partir du RDF de PubChem. Je pense qu'une première étape pour faciliter le travail ultérieur serait de créer directement dans le RDF les associations CID - PMID, par le même pricnipe que les associations au SID, Compound:CIDxxx cito:isDiscussedBy reference:PIMDyyy

Mais comme on a pu le constater, les associations avec la litterature que l'on peut récupérer avec le RDF sont celle qui sont *Depositor provided* c a d à partir de IBM, la CTD etc ... E
En fait, les associations sont initialement inidiqué à l'échelle des substances et pour le composé l'ensemble des références bibliogrpahiques sont mergées. Le seul inconvénient c'est que ces associations ne constituent pas toutes les associations à la litterature possible. Dans certains cas on observera beaucoup plus d'association *Depositor provided* que NLM Curated, ex de l'acteone avec respectivement 14580 items 7642. Mais des fois c'est l'inverse, par exemple pour le Galactose ou autre où on a beaucoup plus d'associations avec LNM curated. 

Ce que fait PubChem en fait lorsqu'il fait les NLM Curated, c'est donc qui cherche les publications pour lesquelles un MeSH correspondant à la molécule a été annoté, c'est en gros le principe de metabToMeSH. En fait, il renvoie vers une requête PubMed en utilisant comme query "meSh term"[type de MeSH]. Par exemple pour "Kdo2-lipid A" la requête va être "Kdo2-lipid A"[NM], qui est l'abbréviation de Suypplementary concept et pour le Galactose, on a "Galactose"[Mesh Terms:noexp] où c'est un 'Mesh Terms' et on demmande de ne pas étendre la requête a ces termes enfant (:noexp)

Ainsi ce qu'il nous faiut c'est le nom du terme meSh et le type de terme MeSH pour pouvoir lancé la requête avec l'outil E-utils E-search qui me renvoie direct une liste de PMID.
Je sais que : depuis le REST PubChem VIEW, on peut récupérer une vue en JSON de la page associé à un compound et dans la catégorie "Names and Identifiers" -> "Synonyms" -> "MeSH Entry Terms" en suivant la référence on peut retrouver l'identifiant UID du MeSH associé (ex : 68005690). L'identifié UID c'est l'identifiant unique dans la base de données NCBI pour représenter les MeSH. Mais pour pouvoir correctement aire des recherche autour du terme MeSH j'ai l'impression qu'il me faut le MeSH unique id (ex: C004521). Grâce a ce MeSH unique ID, on peut récupérer toutes les infos dont on a besoin sur le MeSH dans le RDF associé, son nom, son type etc ... Et ainsi on pourra construire efficacement la requête.
Donc de sur :
	- Il me faut le RDF MeSH pour avoir les noms et les types associées.
	- Il me faut le meSH unique ID. A savoir si en télécharger le bulk de PubChem, cet identifiant ne serait pas direct annoté, ou au moins le uid car par requête ça risque d'être trèèès long... Donc peut être aussi enviager de télécharger tout MeSH pour faire facilement les liens uid - MeSH unique ID. 



il y a d'autre moyens de chercher à regarder les associations entre molécule et PMID en utilisant les autres, en utilsant d'autres méthodes E-utils mais elles ne sont pas très efficace... J'ai testé : 
ELink (https://dataguide.nlm.nih.gov/eutilities/utilities.html#einfo). D'après la doc c'est : 
ELink (elink.fcgi) est un utilitaire très flexible et puissant qui prend une liste d'identifiants uniques (UID) d'une base de données et renvoie, pour chacun des UID listés :

    une liste d'UID pour des enregistrements similaires, liés ou autrement connectés dans la même base de données,
    une liste d'UID pour les enregistrements liés dans une autre base de données Entrez, ou
    une liste d'URL et d'attributs LinkOut pour les ressources connexes non-Entrez.

En raison de la puissance et de la souplesse de cet utilitaire, et parce qu'il implique des liens entre bases de données (et entre bases de données et ressources externes), il peut être difficile d'utiliser certaines de ses fonctionnalités les plus avancées. Il est conseillé aux nouveaux utilisateurs de faire preuve de patience.
A partir d'un uid on peut donc lancer une requête Elink, en paramétrant les base de données *From* et *To*, on eput faire : 
https://eutils.ncbi.nlm.nih.gov/entrez/query/static/entrezlinks.html
	- *pccompound_pubmed*: PubChem Compound to PubMed -> Très peu de résultats
	- *pccompound_pubmed_mesh* : Related PubMed via MeSH -> Peu de résultats aussi
Le mieux semble être 
	- mesh to pubmed avec *mesh_pubmed_major* : mais les résultats s'arrêtes aux publi de 2010 ... on loupe 10 ans de publi LOL MDR !

Dans tout les cas je pense que le mieux et le plus robuste est de faire exactement ce que fait PubChem !:) En reconstruisant la bonne requêe avec le nom du terme MeSH et son type

**Ce que je me dis :**
Si on a récupérer le RDF de meSH pour faire ce travail, il sera interressant de le raccorder direct au RDf de pubChem.
Si dans une étape ultérieure, on a crée des liens CID - PMID (Compound:CIDxxx cito:isDiscussedBy reference:PIMDyyy), je pense qu'il serait très utile pour que les **nouveaux** liens que l'on a pu créer avec les requêtes PubMed à la manière *NLM Curated*, de construire également des triplets pour enrichir notre RDF Compound:CIDxxx cito:isDiscussedBy reference:NewPMIDFromQueryPubMed
Et encore plus : de créer des éléments correspondant à ces PMID dans le RDF store référence c'est a dire que comme pour ce qui a été fait avec les *Depositor provided*. Donc on créer les incomming et les outgoing links, avec les prdicat *date*, *bibliographicCitation*, *http://purl.org/spar/fabio/hasSubjectTerm*, enfin exactement comme pour les PMID déjà ref (ex: https://pubchem.ncbi.nlm.nih.gov/rest/rdf/reference/PMID10395478.html)

Et on aurait un super RDF !! :)
