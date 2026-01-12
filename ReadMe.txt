This README explains how to reproduce the entire workflow of Project 2 using the exact files included in this submission.
The project consists of:
Web crawling → PDF collection → Text extraction → Indexing → Query results → Building My-collection → Clustering experiments.

1. Environment Setup

1.1 Create a virtual environment
python3 -m venv ir_env
source ir_env/bin/activate

1.2 Install required packages

pip install scrapy==2.11.0          # https://docs.scrapy.org/en/latest/
pip install pdfminer.six==20221105  # https://pdfminersix.readthedocs.io/
pip install nltk==3.8.1             # https://www.nltk.org/
pip install scikit-learn==1.4.1     # https://scikit-learn.org/
pip install beautifulsoup4==4.12.3  # https://www.crummy.com/software/BeautifulSoup/
pip install numpy pandas

2. Run the Web Crawler

Your crawler is composed of:
runSpider.py → the file you run (interactive)
spectrumSpider.py → actual Scrapy spider

2.1 Move into the project folder

cd spectrum_crawler/

2.2 Run the spider (interactive prompt)

python runSpider.py

The script will ask:
How many PDFs do you want to download?
Enter a number, for example:
300
T
his runs the spider programmatically using the Scrapy API
(ref: https://docs.scrapy.org/en/latest/topics/api.html).

Output:
A JSON file containing all collected PDF URLs
(e.g., spectrum_pdfs_300.json
).

3. Build the Inverted Index

The indexer file is:

InvertedIndex.py

Make sure your extracted text files are placed in the folder your script expects.
Run:

python InvertedIndex.py

Output:
spectrum_index.json — your full inverted index.

4. Run Queries and Create Query-Based Collections

Your query engine is:
buildQueries.py

Run:
python buildQueries.py

This script:
Loads spectrum_index.json
Runs the required queries:
✔ “sustainability”
✔ “waste”
Saves separate results
Merges them into my_collection.json (included: 
spectrum_index
)

5. MY-COLLECTION
The file my_collection.json contains:
All documents containing “sustainability”
All documents containing “waste”
No duplicates
This is the input to clustering.

6. Run Clustering Experiments
Your clustering program is:
ExperimentClustring.py
Run:
python ExperimentClustring.py
This script:
Loads my_collection.json
Builds TF or TF-IDF document-term matrix
Performs K-Means for k = 2, 10, 20
Prints good vs. bad clusters
Generates cluster summaries and vector-space behavior

7. Output Files Produced
File	Description
spectrum_pdfs_300.json	300 crawled PDF links from Spectrum 

spectrum_index.json	Final inverted index
my_collection.json	Combined results for sustainability + waste 
spectrum_index
K-Means output prints	Created by ExperimentClustring.py

8. Package References (Inline Code Documentation)
All scripts include comments pointing to:
Scrapy documentation
pdfminer documentation
BeautifulSoup docs
NLTK resources
Scikit-learn KMeans and TF-IDF vectorizer
This satisfies the project requirement for including package URLs in code comments.

9. Re-running the Entire Pipeline
You can reproduce the project with this exact order:
1. python runSpider.py
2. python InvertedIndex.py
3. python buildQueries.py
4. python ExperimentClustring.py

Note:
I will also give you the output for ExperimentClustring.py

Output:

==============================
 Running GLOBAL DF 
==============================

Loaded index with 92449 terms.
Global docs in index: 998
Docs in My-collection: 164

============================
   QUERY STATISTICS
============================
Sustainability docs       : 134
Waste docs               : 43
Docs returned by both    : 13
My-collection (union)    : 164
my_collection.json size  : 164
============================

Building TF–IDF matrix using df_mode='global' ...
Vocabulary size (terms that appear in My-collection): 38613
[INFO] k=2 -> inertia=141.9693
[INFO] k=10 -> inertia=130.1558
[INFO] k=20 -> inertia=118.5210

============================
   SUMMARY FOR k = 2
============================

----------------------------------------
Cluster 1  |  size = 96
----------------------------------------
Top terms (by TF–IDF weight):
sustain, person, commun, offer, question, social, learn, engag, peopl, servic, opportun, beyond, benefit, way, issu, futur, individu, need, focu, resourc

Example documents in this cluster:
  doc_id=  0  |  Azzizi_MCompSC_F2025.pdf
  doc_id= 18  |  Table%20I%20Grief%20Leadership.pdf
  doc_id= 20  |  Upcycling%20comparative%20analysis_dataset.pdf

----------------------------------------
Cluster 0  |  size = 68
----------------------------------------
Top terms (by TF–IDF weight):
sustain, ga, ratio, mm, energi, paramet, temperatur, diamet, condit, carri, c, variat, acknowledg, laboratori, locat, industri, figur, size, fig, averag

Example documents in this cluster:
  doc_id=421  |  Zerges_JCB1998.pdf
  doc_id=428  |  Bachewich_JCS1998.pdf
  doc_id=497  |  dayanandan-2016-Ecology_and_Evolution.pdf

============================
   SUMMARY FOR k = 10
============================

----------------------------------------
Cluster 3  |  size = 65
----------------------------------------
Top terms (by TF–IDF weight):
sustain, offer, commun, way, make, futur, issu, better, opportun, person, busi, resourc, servic, learn, continu, individu, qualiti, object, benefit, environ

Example documents in this cluster:
  doc_id=  0  |  Azzizi_MCompSC_F2025.pdf
  doc_id= 20  |  Upcycling%20comparative%20analysis_dataset.pdf
  doc_id=382  |  An-Introduction-to-Database-Systems-Bipin-C.DESAI.pdf

----------------------------------------
Cluster 1  |  size = 23
----------------------------------------
Top terms (by TF–IDF weight):
voic, sustain, stori, talk, inquiri, bring, live, oak, ethic, articul, listen, peopl, came, educ, lincoln, leadership, struggl, engag, cultur, felt

Example documents in this cluster:
  doc_id= 18  |  Table%20I%20Grief%20Leadership.pdf
  doc_id=482  |  KruzynskiNQF2005.pdf
  doc_id=487  |  Jarl-Vol3Article11.pdf

----------------------------------------
Cluster 4  |  size = 9
----------------------------------------
Top terms (by TF–IDF weight):
psycholog, moder, sustain, questionnair, hypothesi, distress, women, confound, hypothes, promot, score, engag, correl, campaign, reliabl, social, mood, extent, item, altern

Example documents in this cluster:
  doc_id=378  |  ENHJEU_-_Overview_%28FQRSC%29.pdf
  doc_id=527  |  dang-vu-neuralplasticity-2016.pdf
  doc_id=533  |  Bodur-Tofighi-Grohmann%20JR%202016.pdf

----------------------------------------
Cluster 7  |  size = 15
----------------------------------------
Top terms (by TF–IDF weight):
plant, abund, km, biolog, dna, genet, habitat, ecol, gene, site, biol, migrat, wild, aquat, speci, land, mol, genotyp, terrestri, pool

Example documents in this cluster:
  doc_id=420  |  Grant_CJFAS1998.pdf
  doc_id=421  |  Zerges_JCB1998.pdf
  doc_id=428  |  Bachewich_JCS1998.pdf

----------------------------------------
Cluster 9  |  size = 12
----------------------------------------
Top terms (by TF–IDF weight):
pharmacolog, prefront, neurobiolog, nucleu, dopamin, eur, receptor, rat, neurosci, hippocampu, accumben, drug, cortex, pharmacol, ventral, frq, striatum, sucros, medial, neuron

Example documents in this cluster:
  doc_id=509  |  Amir-f1000R-2016.pdf
  doc_id=559  |  fnbeh-10-00238.pdf
  doc_id=578  |  chapman-pone-2015.pdf

----------------------------------------
Cluster 8  |  size = 16
----------------------------------------
Top terms (by TF–IDF weight):
cfd, stathopoulo, turbul, veloc, ashra, tunnel, rooftop, wind, aerodynam, rough, roof, heat, intak, refriger, friction, emiss, ga, atlanta, air, fluid

Example documents in this cluster:
  doc_id=513  |  Ten%20Questions%20Concerning%20Modeling%20of%20Near-Field%20Pollutant%20Dispersion%20in%20the%20Built%20Environment.pdf
  doc_id=522  |  SE-D-16-00202R2.pdf
  doc_id=528  |  HE-D-16-00340R1.pdf

----------------------------------------
Cluster 2  |  size = 13
----------------------------------------
Top terms (by TF–IDF weight):
deton, flame, kpa, stoichiometr, hoi, ignit, combust, cj, unstabl, instabl, transduc, shock, dick, irregular, knystauta, inst, radulescu, cellular, spark, undilut

Example documents in this cluster:
  doc_id=516  |  hydrogen_gao.pdf
  doc_id=589  |  POF.pdf
  doc_id=591  |  paper_porous_hd.pdf

----------------------------------------
Cluster 5  |  size = 6
----------------------------------------
Top terms (by TF–IDF weight):
disaggreg, censu, metro, zahabi, kreider, apparicio, vmt, brodeur, bettex, manaugh, dummi, geographi, mobarak, vinha, cropper, dmti, métropolitain, cervero, kockelman, riva

Example documents in this cluster:
  doc_id=549  |  MS-Economic%20Botany-Atiqur.pdf
  doc_id=603  |  Auger%2C%20Cloutier%20%26%20Morency%20%282015%29%2015-4619.pdf
  doc_id=784  |  hardingpattersonmirandzahabi2011.pdf

----------------------------------------
Cluster 0  |  size = 1
----------------------------------------
Top terms (by TF–IDF weight):
cessac, belerlein, mij, mjt, adasdi, hetk, latora, martineri, cybern, approximatin, aihara, seigelbaum, ozaki, microst, hideaki, amari, sonj, grun, accomp, rmidabl

Example documents in this cluster:
  doc_id=747  |  InterneuronDynamics-IJBC2.pdf

----------------------------------------
Cluster 6  |  size = 4
----------------------------------------
Top terms (by TF–IDF weight):
reactanc, stator, pillay, rotor, torqu, aspal, kueck, dynamomet, wenp, arbi, siraki, vll, nema, windag, olszewski, gharakhani, pfw, shetagar, kodad, cunka

Example documents in this cluster:
  doc_id=768  |  Pillay2013b.pdf
  doc_id=800  |  pillay2012b.pdf
  doc_id=889  |  Pillay2012e.pdf

============================
   SUMMARY FOR k = 20
============================

----------------------------------------
Cluster 3  |  size = 46
----------------------------------------
Top terms (by TF–IDF weight):
sustain, person, offer, commun, beyond, creation, learn, engag, profession, focu, benefit, commit, servic, social, perceiv, futur, issu, question, field, resourc

Example documents in this cluster:
  doc_id=  0  |  Azzizi_MCompSC_F2025.pdf
  doc_id=382  |  An-Introduction-to-Database-Systems-Bipin-C.DESAI.pdf
  doc_id=405  |  Ideal-Real-Links.pdf

----------------------------------------
Cluster 1  |  size = 21
----------------------------------------
Top terms (by TF–IDF weight):
voic, sustain, stori, inquiri, talk, ethic, bring, live, peopl, oak, came, articul, felt, listen, educ, thousand, emot, awar, engag, comfort

Example documents in this cluster:
  doc_id= 18  |  Table%20I%20Grief%20Leadership.pdf
  doc_id=487  |  Jarl-Vol3Article11.pdf
  doc_id=506  |  2016.Vaillancourt.CMTJ22.1.MTinMT..pdf

----------------------------------------
Cluster 17  |  size = 11
----------------------------------------
Top terms (by TF–IDF weight):
wast, auction, expens, sell, invest, price, integ, decid, busi, custom, machin, cost, multi, suppli, usag, manufactur, whole, simul, co, implement

Example documents in this cluster:
  doc_id= 20  |  Upcycling%20comparative%20analysis_dataset.pdf
  doc_id=574  |  bhuiyan-globaljournal-2015.pdf
  doc_id=711  |  35418-123952-1-PB.pdf

----------------------------------------
Cluster 4  |  size = 8
----------------------------------------
Top terms (by TF–IDF weight):
psycholog, questionnair, distress, moder, sustain, confound, promot, hypothesi, women, campaign, hypothes, mood, score, correl, engag, social, item, reliabl, advertis, experienc

Example documents in this cluster:
  doc_id=378  |  ENHJEU_-_Overview_%28FQRSC%29.pdf
  doc_id=533  |  Bodur-Tofighi-Grohmann%20JR%202016.pdf
  doc_id=566  |  doucerain-frontiers-2015.pdf

----------------------------------------
Cluster 7  |  size = 7
----------------------------------------
Top terms (by TF–IDF weight):
aquat, ecol, freshwat, climat, habitat, lake, biol, km, watersh, hutch, geolog, river, basin, anim, ecosystem, abund, resour, dispers, speci, land

Example documents in this cluster:
  doc_id=420  |  Grant_CJFAS1998.pdf
  doc_id=497  |  dayanandan-2016-Ecology_and_Evolution.pdf
  doc_id=504  |  fraser-pone-2016.pdf

----------------------------------------
Cluster 14  |  size = 12
----------------------------------------
Top terms (by TF–IDF weight):
membran, liquid, chemic, min, temperatur, concentr, nitrogen, molecul, surfac, surfact, ion, acid, nm, salt, cell, carbon, plate, densiti, transport, mm

Example documents in this cluster:
  doc_id=421  |  Zerges_JCB1998.pdf
  doc_id=428  |  Bachewich_JCS1998.pdf
  doc_id=537  |  packirisamy-scientific-reports-2016.pdf

----------------------------------------
Cluster 12  |  size = 2
----------------------------------------
Top terms (by TF–IDF weight):
dessu, tenté, grandissant, parvenu, défend, répandu, construit, pièc, inhérent, attendr, venait, paysag, contrair, préservat, soumiss, commencé, passant, recour, ordinair, garder

Example documents in this cluster:
  doc_id=482  |  KruzynskiNQF2005.pdf
  doc_id=811  |  Une%20enqu%C3%AAte%20plus%20approfondie%20sur%20l%27impression%203D.pdf

----------------------------------------
Cluster 18  |  size = 5
----------------------------------------
Top terms (by TF–IDF weight):
ladi, lover, feminin, woman, emin, qualifi, confess, ambival, marketplac, admir, impress, husband, discours, femin, fiction, narr, mari, seventeenth, qtd, sister

Example documents in this cluster:
  doc_id=488  |  Lady%20Mary_s%20Imperfect%20Employment.pdf
  doc_id=491  |  bobker.pdf
  doc_id=512  |  Tittler-BAJ-XVII-1-2016.pdf

----------------------------------------
Cluster 9  |  size = 10
----------------------------------------
Top terms (by TF–IDF weight):
prefront, neurobiolog, pharmacolog, dopamin, hippocampu, accumben, nucleu, cortex, receptor, rat, neurosci, ventral, frq, striatum, eur, drug, medial, pharmacol, brain, neuropsychopharmacolog

Example documents in this cluster:
  doc_id=509  |  Amir-f1000R-2016.pdf
  doc_id=559  |  fnbeh-10-00238.pdf
  doc_id=578  |  chapman-pone-2015.pdf

----------------------------------------
Cluster 13  |  size = 4
----------------------------------------
Top terms (by TF–IDF weight):
celik, rng, lateb, leitl, schatzmann, carissimo, hensen, meroney, heijst, gousseau, hellsten, nozu, tominaga, mochida, yoshi, yoshikawa, blocken, carmeliet, kataoka, aij

Example documents in this cluster:
  doc_id=513  |  Ten%20Questions%20Concerning%20Modeling%20of%20Near-Field%20Pollutant%20Dispersion%20in%20the%20Built%20Environment.pdf
  doc_id=545  |  Blocken%20B%2C%20Stathopoulos%20T%2C%20Van%20Beeck%20J%20P%20A%20J.%20%282016%29.%20Pedestrian-level%20Wind%20Conditions%20around%20Buildings.pdf
  doc_id=652  |  Lateb2014_Accepted_Version.pdf

----------------------------------------
Cluster 11  |  size = 12
----------------------------------------
Top terms (by TF–IDF weight):
deton, flame, kpa, hoi, stoichiometr, combust, ignit, cj, unstabl, instabl, shock, transduc, argon, dick, irregular, inst, knystauta, exotherm, cellular, astronaut

Example documents in this cluster:
  doc_id=516  |  hydrogen_gao.pdf
  doc_id=589  |  POF.pdf
  doc_id=591  |  paper_porous_hd.pdf

----------------------------------------
Cluster 8  |  size = 4
----------------------------------------
Top terms (by TF–IDF weight):
vasan, unglaz, cfd, transpir, aerodynam, collector, turbul, stathopoulo, weather, tall, oncom, friction, schemat, expon, roof, dymond, vloc, kutscher, bambara, faill

Example documents in this cluster:
  doc_id=522  |  SE-D-16-00202R2.pdf
  doc_id=556  |  pagination_INDAER_3215.pdf
  doc_id=664  |  1.%20Experimental%20Study%20of%20Wind%20Effects%20on%20Unglazed%20Transpired%20Collectors.pdf

----------------------------------------
Cluster 16  |  size = 1
----------------------------------------
Top terms (by TF–IDF weight):
beforeandafterrespiratoryev, especiallyinoldermen, surroundingsleeponset, whilehornyaket, largerportionsofnremandremsleepwithorwithoutleg, insteadofpoorsleepinrlsresultingfromattenu, areaforfuturestudi, parasomniasar, sleepwalkingandsleepterror, orremsleep, ordangerousandofteninvolvebehavioursthatmightappear, xbe, shoutingandthrash, andphysiologicalhyperarous, thattypicallyoccurduringswsinthefirstthirdofthenight, onerecruitedparticip, attributedtohowferriet, parasomniaswillbereviewedsecond, espaet, usedbothanautomaticspindledetectorandameasur

Example documents in this cluster:
  doc_id=527  |  dang-vu-neuralplasticity-2016.pdf

----------------------------------------
Cluster 19  |  size = 5
----------------------------------------
Top terms (by TF–IDF weight):
ackerman, fabri, downwash, epa, plume, downwind, gupta, irsst, saathoff, taller, sécurité, ashra, refriger, momentum, expon, rooftop, upwind, atlanta, sampler, buoyanc

Example documents in this cluster:
  doc_id=528  |  HE-D-16-00340R1.pdf
  doc_id=665  |  Performance%20of%20ASHRAE%20models%20in%20assessing%20pollutant%20dispersion%20from%20rooftop%20emissions.pdf
  doc_id=850  |  Evaluation%20of%20ASHRAE%20Dilution%20Models%20to%20Estimate%20Dilution%20from%20Rooftop%20Exhausts.pdf

----------------------------------------
Cluster 15  |  size = 4
----------------------------------------
Top terms (by TF–IDF weight):
assam, himalayan, botani, dayanandan, nei, crop, mizoram, tropic, ethidium, india, leaf, habitat, indica, kess, bawa, deforest, shrub, eastern, delhi, bromid

Example documents in this cluster:
  doc_id=547  |  Barbhuiya_et_al-2016-Ecology_and_Evolution.pdf
  doc_id=549  |  MS-Economic%20Botany-Atiqur.pdf
  doc_id=650  |  dayanandan.plosone.2014.pdf

----------------------------------------
Cluster 10  |  size = 3
----------------------------------------
Top terms (by TF–IDF weight):
ipcc, zickfeld, intergovernment, aerosol, clim, stocker, geophi, damon, anthropogen, dioxid, proportion, greenhous, solomon, trenberth, matthew, gase, eickhout, neumay, cdiac, elzenet

Example documents in this cluster:
  doc_id=585  |  GignacMatthews2015_ERL.pdf
  doc_id=645  |  Matthews_2014_Environ_Res_Lett.pdf
  doc_id=976  |  Rossetal2012_Tellus.pdf

----------------------------------------
Cluster 5  |  size = 4
----------------------------------------
Top terms (by TF–IDF weight):
disaggreg, metro, kreider, bettex, brodeur, zahabi, apparicio, vmt, manaugh, dummi, dmti, cropper, métropolitain, riva, cervero, mobarak, kockelman, vinha, trip, downtown

Example documents in this cluster:
  doc_id=603  |  Auger%2C%20Cloutier%20%26%20Morency%20%282015%29%2015-4619.pdf
  doc_id=784  |  hardingpattersonmirandzahabi2011.pdf
  doc_id=879  |  GHGs_paper_-_Paris_2012_submitted.pdf

----------------------------------------
Cluster 2  |  size = 1
----------------------------------------
Top terms (by TF–IDF weight):
niﬁe, piezotron, tyurin, pogrebnjak, crothrust, micromech, croeng, phylippov, dushin, nerchenko, guendugov, kharlamov, dalian, stochiometr, drocarbon, microreactor, subson, tronautica, suoka, microcapillari

Example documents in this cluster:
  doc_id=663  |  SHOC-D-13-00069%5B1%5D.pdf

----------------------------------------
Cluster 0  |  size = 1
----------------------------------------
Top terms (by TF–IDF weight):
cessac, belerlein, mij, mjt, adasdi, hetk, latora, martineri, cybern, approximatin, aihara, seigelbaum, ozaki, microst, hideaki, amari, sonj, grun, accomp, rmidabl

Example documents in this cluster:
  doc_id=747  |  InterneuronDynamics-IJBC2.pdf

----------------------------------------
Cluster 6  |  size = 3
----------------------------------------
Top terms (by TF–IDF weight):
tolbert, windag, kodad, phumiphak, cunka, gharakhani, habetl, otaduy, casada, kueck, wenp, olszewski, vll, aspal, pout, pfw, shetagar, arbi, siraki, dynamomet

Example documents in this cluster:
  doc_id=768  |  Pillay2013b.pdf
  doc_id=889  |  Pillay2012e.pdf
  doc_id=890  |  Pillay2012d.pdf


==============================
 Running LOCAL DF  
==============================

Loaded index with 92449 terms.
Global docs in index: 998
Docs in My-collection: 164

============================
   QUERY STATISTICS
============================
Sustainability docs       : 134
Waste docs               : 43
Docs returned by both    : 13
My-collection (union)    : 164
my_collection.json size  : 164
============================

Building TF–IDF matrix using df_mode='local' ...
Vocabulary size (terms that appear in My-collection): 38613
[INFO] k=2 -> inertia=144.3684
[INFO] k=10 -> inertia=132.4088
[INFO] k=20 -> inertia=120.8484

============================
   SUMMARY FOR k = 2
============================

----------------------------------------
Cluster 1  |  size = 95
----------------------------------------
Top terms (by TF–IDF weight):
person, commun, question, social, servic, offer, engag, peopl, context, learn, particip, other, focu, way, involv, educ, issu, beyond, sens, benefit

Example documents in this cluster:
  doc_id=  0  |  Azzizi_MCompSC_F2025.pdf
  doc_id= 18  |  Table%20I%20Grief%20Leadership.pdf
  doc_id= 20  |  Upcycling%20comparative%20analysis_dataset.pdf

----------------------------------------
Cluster 0  |  size = 69
----------------------------------------
Top terms (by TF–IDF weight):
ga, mm, fig, ratio, temperatur, diamet, paramet, variat, veloc, experiment, shown, calcul, length, energi, laboratori, engin, mixtur, densiti, simul, constant

Example documents in this cluster:
  doc_id=421  |  Zerges_JCB1998.pdf
  doc_id=428  |  Bachewich_JCS1998.pdf
  doc_id=497  |  dayanandan-2016-Ecology_and_Evolution.pdf

============================
   SUMMARY FOR k = 10
============================

----------------------------------------
Cluster 8  |  size = 48
----------------------------------------
Top terms (by TF–IDF weight):
econom, cost, servic, busi, framework, industri, issu, decis, countri, goal, benefit, invest, expect, market, unit, better, particular, improv, propos, find

Example documents in this cluster:
  doc_id=  0  |  Azzizi_MCompSC_F2025.pdf
  doc_id= 20  |  Upcycling%20comparative%20analysis_dataset.pdf
  doc_id=382  |  An-Introduction-to-Database-Systems-Bipin-C.DESAI.pdf

----------------------------------------
Cluster 3  |  size = 14
----------------------------------------
Top terms (by TF–IDF weight):
librarian, scholarli, platform, librarianship, librari, debat, commit, onlin, reader, dissemin, topic, june, profession, write, disciplinari, regularli, juli, scholarship, hope, scholar

Example documents in this cluster:
  doc_id= 18  |  Table%20I%20Grief%20Leadership.pdf
  doc_id=491  |  bobker.pdf
  doc_id=512  |  Tittler-BAJ-XVII-1-2016.pdf

----------------------------------------
Cluster 6  |  size = 31
----------------------------------------
Top terms (by TF–IDF weight):
want, stori, thing, friend, live, happen, routledg, young, experienc, psycholog, someth, never, voic, educ, think, bring, feel, say, awar, youth

Example documents in this cluster:
  doc_id=378  |  ENHJEU_-_Overview_%28FQRSC%29.pdf
  doc_id=407  |  Social-Development.pdf
  doc_id=487  |  Jarl-Vol3Article11.pdf

----------------------------------------
Cluster 9  |  size = 13
----------------------------------------
Top terms (by TF–IDF weight):
membran, molecul, chemic, temperatur, salt, ion, liquid, iv, acid, nitrogen, bulk, morpholog, electron, surfac, mg, carbon, chemistri, concentr, cell, acta

Example documents in this cluster:
  doc_id=421  |  Zerges_JCB1998.pdf
  doc_id=428  |  Bachewich_JCS1998.pdf
  doc_id=537  |  packirisamy-scientific-reports-2016.pdf

----------------------------------------
Cluster 5  |  size = 3
----------------------------------------
Top terms (by TF–IDF weight):
peut, seul, deux, ainsi, nou, lien, avec, commenc, aujourd, pour, une, au, saisir, relativ, université, grand, par, femm, radical, lutt

Example documents in this cluster:
  doc_id=482  |  KruzynskiNQF2005.pdf
  doc_id=639  |  Jeppesenetal_ephemera2014.pdf
  doc_id=811  |  Une%20enqu%C3%AAte%20plus%20approfondie%20sur%20l%27impression%203D.pdf

----------------------------------------
Cluster 2  |  size = 9
----------------------------------------
Top terms (by TF–IDF weight):
habitat, genotyp, leaf, pcr, trait, polymorph, wild, km, ecol, microsatellit, crop, genet, bayesian, biodivers, allel, tropic, dna, plant, primer, dayanandan

Example documents in this cluster:
  doc_id=497  |  dayanandan-2016-Ecology_and_Evolution.pdf
  doc_id=504  |  fraser-pone-2016.pdf
  doc_id=547  |  Barbhuiya_et_al-2016-Ecology_and_Evolution.pdf

----------------------------------------
Cluster 7  |  size = 11
----------------------------------------
Top terms (by TF–IDF weight):
neurosci, cortex, neurobiolog, prefront, dopamin, pharmacolog, nucleu, rat, neural, accumben, receptor, brain, ventral, eur, hippocampu, pharmacol, medial, striatum, frq, cortic

Example documents in this cluster:
  doc_id=509  |  Amir-f1000R-2016.pdf
  doc_id=559  |  fnbeh-10-00238.pdf
  doc_id=578  |  chapman-pone-2015.pdf

----------------------------------------
Cluster 1  |  size = 15
----------------------------------------
Top terms (by TF–IDF weight):
stathopoulo, cfd, roof, tunnel, wind, aerodynam, rooftop, ashra, turbul, expon, height, rough, plume, meteorolog, recircul, intak, veloc, refriger, atlanta, upstream

Example documents in this cluster:
  doc_id=513  |  Ten%20Questions%20Concerning%20Modeling%20of%20Near-Field%20Pollutant%20Dispersion%20in%20the%20Built%20Environment.pdf
  doc_id=522  |  SE-D-16-00202R2.pdf
  doc_id=528  |  HE-D-16-00340R1.pdf

----------------------------------------
Cluster 4  |  size = 13
----------------------------------------
Top terms (by TF–IDF weight):
deton, hoi, flame, stoichiometr, cj, shock, ignit, kpa, inst, transduc, combust, dick, irregular, instabl, radulescu, argon, knystauta, unstabl, propag, gaseou

Example documents in this cluster:
  doc_id=516  |  hydrogen_gao.pdf
  doc_id=589  |  POF.pdf
  doc_id=591  |  paper_porous_hd.pdf

----------------------------------------
Cluster 0  |  size = 7
----------------------------------------
Top terms (by TF–IDF weight):
covari, questionnair, score, advertis, item, symptom, subscal, recruit, consent, hypothes, psychosoci, distress, footnot, mood, abnorm, feel, multivari, depress, fs, confound

Example documents in this cluster:
  doc_id=527  |  dang-vu-neuralplasticity-2016.pdf
  doc_id=533  |  Bodur-Tofighi-Grohmann%20JR%202016.pdf
  doc_id=566  |  doucerain-frontiers-2015.pdf

============================
   SUMMARY FOR k = 20
============================

----------------------------------------
Cluster 3  |  size = 45
----------------------------------------
Top terms (by TF–IDF weight):
person, profession, commun, offer, creation, perceiv, question, engag, focu, servic, social, purpos, learn, beyond, issu, commit, context, percept, evid, sens

Example documents in this cluster:
  doc_id=  0  |  Azzizi_MCompSC_F2025.pdf
  doc_id=382  |  An-Introduction-to-Database-Systems-Bipin-C.DESAI.pdf
  doc_id=405  |  Ideal-Real-Links.pdf

----------------------------------------
Cluster 1  |  size = 21
----------------------------------------
Top terms (by TF–IDF weight):
voic, talk, listen, stori, came, inquiri, ethic, live, child, ask, felt, emot, educ, particip, bring, articul, friend, awar, lincoln, teacher

Example documents in this cluster:
  doc_id= 18  |  Table%20I%20Grief%20Leadership.pdf
  doc_id=487  |  Jarl-Vol3Article11.pdf
  doc_id=506  |  2016.Vaillancourt.CMTJ22.1.MTinMT..pdf

----------------------------------------
Cluster 17  |  size = 10
----------------------------------------
Top terms (by TF–IDF weight):
auction, integ, su, expens, custom, wast, op, sell, machin, inventori, choos, price, multimedia, decid, slot, co, manufactur, sequenc, maxim, ot

Example documents in this cluster:
  doc_id= 20  |  Upcycling%20comparative%20analysis_dataset.pdf
  doc_id=574  |  bhuiyan-globaljournal-2015.pdf
  doc_id=711  |  35418-123952-1-PB.pdf

----------------------------------------
Cluster 4  |  size = 8
----------------------------------------
Top terms (by TF–IDF weight):
distress, questionnair, confound, item, mood, hypothesi, hypothes, score, campaign, psycholog, women, advertis, correl, moder, reliabl, sd, subscal, anxieti, unrel, adult

Example documents in this cluster:
  doc_id=378  |  ENHJEU_-_Overview_%28FQRSC%29.pdf
  doc_id=533  |  Bodur-Tofighi-Grohmann%20JR%202016.pdf
  doc_id=566  |  doucerain-frontiers-2015.pdf

----------------------------------------
Cluster 7  |  size = 7
----------------------------------------
Top terms (by TF–IDF weight):
aquat, ecol, freshwat, lake, habitat, biol, climat, geolog, fish, zool, hutch, salmonid, salmon, quinn, trout, arctic, appl, speci, fisheri, spawn

Example documents in this cluster:
  doc_id=420  |  Grant_CJFAS1998.pdf
  doc_id=497  |  dayanandan-2016-Ecology_and_Evolution.pdf
  doc_id=504  |  fraser-pone-2016.pdf

----------------------------------------
Cluster 14  |  size = 12
----------------------------------------
Top terms (by TF–IDF weight):
liquid, molecul, membran, acid, nitrogen, chemic, min, nm, temperatur, carbon, ion, plate, salt, surfac, solvent, surfact, cell, sodium, protein, wash

Example documents in this cluster:
  doc_id=421  |  Zerges_JCB1998.pdf
  doc_id=428  |  Bachewich_JCS1998.pdf
  doc_id=537  |  packirisamy-scientific-reports-2016.pdf

----------------------------------------
Cluster 12  |  size = 2
----------------------------------------
Top terms (by TF–IDF weight):
quatr, grandissant, partag, conséquent, tou, commencé, largement, détaillé, atteint, recour, remerci, aucun, défini, autr, nombreux, intéress, voir, dernier, niveau, limité

Example documents in this cluster:
  doc_id=482  |  KruzynskiNQF2005.pdf
  doc_id=811  |  Une%20enqu%C3%AAte%20plus%20approfondie%20sur%20l%27impression%203D.pdf

----------------------------------------
Cluster 18  |  size = 6
----------------------------------------
Top terms (by TF–IDF weight):
woman, literari, ladi, obscur, admir, lover, narrat, narr, essay, ambival, cloth, nobl, emin, peter, scene, mari, gender, men, mysteri, confess

Example documents in this cluster:
  doc_id=488  |  Lady%20Mary_s%20Imperfect%20Employment.pdf
  doc_id=491  |  bobker.pdf
  doc_id=512  |  Tittler-BAJ-XVII-1-2016.pdf

----------------------------------------
Cluster 9  |  size = 10
----------------------------------------
Top terms (by TF–IDF weight):
neurobiolog, prefront, dopamin, pharmacolog, nucleu, rat, accumben, neurosci, receptor, cortex, ventral, eur, hippocampu, neural, pharmacol, medial, striatum, brain, frq, drug

Example documents in this cluster:
  doc_id=509  |  Amir-f1000R-2016.pdf
  doc_id=559  |  fnbeh-10-00238.pdf
  doc_id=578  |  chapman-pone-2015.pdf

----------------------------------------
Cluster 13  |  size = 5
----------------------------------------
Top terms (by TF–IDF weight):
mochida, carissimo, heijst, tominaga, gousseau, blocken, hellsten, cubic, carmeliet, eddi, shear, ooka, streamwis, horsesho, unsteadi, plume, advect, recircul, convect, vortex

Example documents in this cluster:
  doc_id=513  |  Ten%20Questions%20Concerning%20Modeling%20of%20Near-Field%20Pollutant%20Dispersion%20in%20the%20Built%20Environment.pdf
  doc_id=545  |  Blocken%20B%2C%20Stathopoulos%20T%2C%20Van%20Beeck%20J%20P%20A%20J.%20%282016%29.%20Pedestrian-level%20Wind%20Conditions%20around%20Buildings.pdf
  doc_id=652  |  Lateb2014_Accepted_Version.pdf

----------------------------------------
Cluster 11  |  size = 12
----------------------------------------
Top terms (by TF–IDF weight):
deton, hoi, flame, cj, stoichiometr, shock, ignit, argon, kpa, inst, combust, dick, transduc, irregular, instabl, exotherm, unstabl, transvers, radulescu, knystauta

Example documents in this cluster:
  doc_id=516  |  hydrogen_gao.pdf
  doc_id=589  |  POF.pdf
  doc_id=591  |  paper_porous_hd.pdf

----------------------------------------
Cluster 8  |  size = 3
----------------------------------------
Top terms (by TF–IDF weight):
perpendicular, duct, clad, athien, faill, vloc, kutscher, bambara, dymond, aerodynam, cfd, intak, laminar, utc, suction, preheat, unglaz, vasan, outlet, improperli

Example documents in this cluster:
  doc_id=522  |  SE-D-16-00202R2.pdf
  doc_id=664  |  1.%20Experimental%20Study%20of%20Wind%20Effects%20on%20Unglazed%20Transpired%20Collectors.pdf
  doc_id=962  |  paper_final.pdf

----------------------------------------
Cluster 16  |  size = 1
----------------------------------------
Top terms (by TF–IDF weight):
chirp, nonsleepwalk, especiallywithlargersampl, andmethodolog, diagnosticgroup, althoughsampl, reportednogroupdifferencesinsigmapowerversuscontrol, drawameaningfulcomparisonbetweenthetwostudi, werefoundbetweensleepwalk, unreport, afterisolatedtreatmentofanunderli, nonoverweight, toaberrantswadynamicsbysuggestingthata, pasubjectshad, andahigheroccurrenceofarous, decayedmor, iscertainlyrequir, tounderstandtheroleofspindleactivityinpa, onestudi, failedtoreporttheir

Example documents in this cluster:
  doc_id=527  |  dang-vu-neuralplasticity-2016.pdf

----------------------------------------
Cluster 19  |  size = 6
----------------------------------------
Top terms (by TF–IDF weight):
expon, saathoff, irsst, roof, wind, meteorolog, rooftop, tunnel, buoyanc, stathopoulo, tracer, aerodynam, friction, tavg, uncap, cimor, brode, venkatram, hd, entrain

Example documents in this cluster:
  doc_id=528  |  HE-D-16-00340R1.pdf
  doc_id=556  |  pagination_INDAER_3215.pdf
  doc_id=665  |  Performance%20of%20ASHRAE%20models%20in%20assessing%20pollutant%20dispersion%20from%20rooftop%20emissions.pdf

----------------------------------------
Cluster 15  |  size = 4
----------------------------------------
Top terms (by TF–IDF weight):
assam, himalayan, nei, dayanandan, botani, crop, leaf, mizoram, tropic, seed, shrub, indica, bawa, ethidium, cycler, seedl, habitat, harvest, eastern, botan

Example documents in this cluster:
  doc_id=547  |  Barbhuiya_et_al-2016-Ecology_and_Evolution.pdf
  doc_id=549  |  MS-Economic%20Botany-Atiqur.pdf
  doc_id=650  |  dayanandan.plosone.2014.pdf

----------------------------------------
Cluster 10  |  size = 3
----------------------------------------
Top terms (by TF–IDF weight):
damon, zickfeld, ipcc, clim, intergovernment, geophi, aerosol, stocker, proportion, dioxid, anthropogen, solomon, greenhous, matthew, tellu, mahowald, trenberth, ebi, uvic, millenni

Example documents in this cluster:
  doc_id=585  |  GignacMatthews2015_ERL.pdf
  doc_id=645  |  Matthews_2014_Environ_Res_Lett.pdf
  doc_id=976  |  Rossetal2012_Tellus.pdf

----------------------------------------
Cluster 5  |  size = 4
----------------------------------------
Top terms (by TF–IDF weight):
elast, disaggreg, dummi, metro, downtown, trip, automobil, cervero, brodeur, kockelman, ewe, vinha, mobarak, gauvin, amt, apparicio, kreider, zahabi, dmti, vmt

Example documents in this cluster:
  doc_id=603  |  Auger%2C%20Cloutier%20%26%20Morency%20%282015%29%2015-4619.pdf
  doc_id=784  |  hardingpattersonmirandzahabi2011.pdf
  doc_id=879  |  GHGs_paper_-_Paris_2012_submitted.pdf

----------------------------------------
Cluster 2  |  size = 1
----------------------------------------
Top terms (by TF–IDF weight):
croeng, phylippov, nerchenko, sadahira, nikitin, kitawaki, inaba, dushin, johzaki, stochiometr, microreactor, micromech, crothrust, piezotron, pogrebnjak, tyurin, kharlamov, niﬁe, dustrial, hieronymu

Example documents in this cluster:
  doc_id=663  |  SHOC-D-13-00069%5B1%5D.pdf

----------------------------------------
Cluster 0  |  size = 1
----------------------------------------
Top terms (by TF–IDF weight):
seigelbau, hestrin, urthermor, latora, martineri, escrib, tatori, exci, galarreta, ramework, byelectr, rakic, architec, pgora, boyar, bifur, presynaps, friston, shimazaki, cessac

Example documents in this cluster:
  doc_id=747  |  InterneuronDynamics-IJBC2.pdf

----------------------------------------
Cluster 6  |  size = 3
----------------------------------------
Top terms (by TF–IDF weight):
otaduy, casada, wenp, polyphas, namepl, tolbert, vll, pout, phumiphak, pfw, durban, aspal, shetagar, kodad, cunka, azad, windag, habetl, olszewski, nema

Example documents in this cluster:
  doc_id=768  |  Pillay2013b.pdf
  doc_id=889  |  Pillay2012e.pdf
  doc_id=890  |  Pillay2012d.pdf