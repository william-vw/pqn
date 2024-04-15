from convert_base import str_to_uri, RdfRepresent, QuoteOptions
from rdflib import Namespace, Literal, Graph, BNode, RDF, RDFS
import pandas as pd
from enum import Enum
import time

DFG = Namespace("http://rdf.org/dfg#")

class DFGSource(Enum):
    NORMATIVE = 1
    DISCOVERED = 2

dfg_terms = {
    'Activity': DFG.Activity,
    # 'Link': DFG.Link,
    'activity': DFG.activity,
    'source': DFG.source,
    'freq': DFG.freq,
    'from': DFG['from'],
    'to': DFG.to,
    'next': DFG.next,
    'nil': DFG.nil,
    
    DFGSource.NORMATIVE: DFG.normative,
    DFGSource.DISCOVERED: DFG.discovered,
}


def convert_dfg_rdf(dfg, save_to, ns, source):
    start = time.time_ns()
    start_conv = time.time_ns()

    g = Graph()
    
    # use to determine if activity is endpoint or not
    df = pd.DataFrame(
        [ [ src, tgt, freq ] for ((src, tgt), freq) in dfg.items() ],
        columns=[ 'src', 'tgt', 'freq' ]
    )
    
    for ((src, tgt), freq) in dfg.items():
        src_activ = str_to_uri(src, ns, QuoteOptions.REMOVE_SPECIAL)
        tgt_activ = str_to_uri(tgt, ns, QuoteOptions.REMOVE_SPECIAL)
        
        add_link(src_activ, tgt_activ, source, g, freq=freq)
        
        if tgt not in df['src']:
            add_link(tgt_activ, dfg_terms['nil'], source, g)
    
    end_conv = time.time_ns()
    print("conversion time (ms):", (end_conv-start_conv)/1000000)

    start_save = time.time_ns()

    g.serialize(destination=save_to)

    end_save = time.time_ns()
    print("save time (ms):", (end_save-start_save)/1000000)

    end = time.time_ns()
    print("total time (ms):", (end-start)/1000000)
    
# def add_activ(label, ns, source, g):
#     activ = BNode()
#     g.add((activ, RDF.type, dfg_terms['Activity']))
    
#     g.add((activ, RDFS.label, label))
#     uri = str_to_uri(label, ns, QuoteOptions.REMOVE_SPECIAL)
#     g.add((activ, dfg_terms['activity'], uri))
#     g.add((activ, dfg_terms['source'], dfg_terms[source]))
    
        
def add_link(prior_activ, next_activ, source, g, freq=False):
    link = BNode()
    # g.add((link, RDF.type, dfg_terms['Link']))
    g.add((link, dfg_terms['from'], prior_activ))
    g.add((link, dfg_terms['to'], next_activ))
    g.add((link, dfg_terms['source'], dfg_terms[source]))
    if freq:
        g.add((link, dfg_terms['freq'], Literal(freq)))