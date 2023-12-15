from rdflib import Graph, Namespace, Literal, BNode, URIRef
from rdflib.namespace import RDF, FOAF,  XSD, split_uri
from SPARQLWrapper import SPARQLWrapper, JSON

import os
import pandas as pd
from datetime import datetime, timedelta

#Code Pikeln
def pickeln_data_from_wikidata():
    cache_file = 'data_cache.csv'
    cache_duration = timedelta(days=7)  # Daten alle 7 Tage aktualisieren

    # Überprüfen, ob eine zwischengespeicherte Datei existiert und aktuell ist
    if os.path.exists(cache_file):
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.now() - file_mod_time < cache_duration:
            return pd.read_csv(cache_file)

    # SPARQL-Abfrage an Wikidata
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery('''
        SELECT DISTINCT ?school ?label_school ?location ?label_location ?location_coordinates ?website
        WHERE {
          SERVICE <https://query.wikidata.org/sparql> {
            ?school wdt:P31 wd:Q15850083;     	# is a university of applied science
                    rdfs:label ?label_school;       	 
                    wdt:P625 ?location_coordinates;
                    wdt:P131 ?location;
                    wdt:P856 ?website.
            ?location rdfs:label ?label_location.



            OPTIONAL {?school wdt:P1813 ?shortname;   	 
                            wdt:P1366 ?school_replace.  	 
                    ?school_replace rdfs:label ?label_replace.}
            OPTIONAL {?location wdt:P625 ?location_coordinates.}

            FILTER (LANG(?label_school) = "en" &&      	# Englisch sind mehr verfügbar als in Deutsch
                    LANG(?label_location) = "en")
            }
          }
        ORDER BY ASC (?label_school)
    ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Verarbeiten der Ergebnisse
    data = []
    for result in results["results"]["bindings"]:
        entry = {
            'school': result["school"]["value"],
            'label_school': result["label_school"]["value"],
            'location': result["location"]["value"],
            'label_location': result["label_location"]["value"],
            'website': result["website"]["value"]
        }
        if 'location_coordinates' in result:
            entry['location_coordinates'] = result["location_coordinates"]["value"]
        else:
            entry['location_coordinates'] = None

        data.append(entry)

    df = pd.DataFrame(data)
    # Speichern in einer CSV-Datei
    df.to_csv(cache_file, index=False)

    return df

def generate_graph(df):
    g = Graph()
    # Definieren eines eigenen Namespace für die Fachhochschulen
    fh_ns = Namespace("http://www.example.org/fh/")

    for index, row in df.iterrows():
            # Erstellen eines URIRef-Node für jede Schule
            school_node = URIRef(row['school'])
            location_node = URIRef(row['location'])
            # Hinzufügen von Informationen zur Schule
            g.add((school_node, RDF.type, fh_ns.UniversityOfAppliedSciences))
            g.add((school_node, FOAF.name, Literal(row['label_school'])))
            g.add((school_node, FOAF.based_near, URIRef(row['location'])))
            g.add((school_node, FOAF.page, URIRef(row['website'])))
            g.add((school_node, fh_ns.locationName, Literal(row['label_location'])))
            # # Koordinaten als Literal hinzufügen
            if pd.notna(row['location_coordinates']):
                 g.add((location_node, fh_ns.coordinates, Literal(row['location_coordinates'], datatype=XSD.string)))

    return g

data1 = pickeln_data_from_wikidata()
graph = generate_graph(data1.head(1))


#Visualisierung
import matplotlib.pyplot as plt
import networkx as nx
from rdflib import Graph

def convert_rdflib_graph_to_networkx(graph):
    G = nx.Graph()

    for subj, pred, obj in graph:
        _, pred_local_name = split_uri(pred)
        G.add_edge(subj, obj, label=pred_local_name)

    return G

def visualize_graph(G):
    pos = nx.spring_layout(G)  # Layout für den Graphen
    edge_labels = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', linewidths=0.45, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.show()

# Umwandeln des rdflib-Graphen in einen networkx-Graphen
nx_graph = convert_rdflib_graph_to_networkx(graph)

visualize_graph(nx_graph)




