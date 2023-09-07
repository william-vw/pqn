from enum import Enum
from rdflib import Namespace, Literal, Graph, BNode, RDF
import pandas as pd
import urllib.parse
import time

class RDFLogFormat(Enum):
    LINK_REIFIED = 1
    LINK_PRED = 2

TR = Namespace("http://notation3.org/trace#")
Sepsis = Namespace("http://dutch.hospital.nl/sepsis#")

tr_terms = {
    'Trace': TR['Trace'],
    'in': TR['in'],
    'activity': TR.activity,
    'ts': TR.ts,
    'from': TR['from'],
    'to': TR.to,
    'next': TR.next,
    'nil': TR.nil,
    'lifecycle': TR.lifecycle_transition,
    'group': TR.org_group
}
log_terms = {}

def convert_xes_n3(log, filepath, format, limit=-1):
    start = time.time_ns()
    start_conv = time.time_ns()

    g = Graph()

    for col in log.columns:
        if col not in ( 'time:timestamp', 'concept:name', 'case:concept:name', 'lifecycle:transition', 'org:group' ):
            log_terms[col] = Sepsis[col]

    groups = log.sort_values(by='time:timestamp', ascending=True).groupby('case:concept:name')
    # print(groups.groups)

    total_num = 0
    cur_traces = 0
    for case, df in groups:
        trace = Sepsis[f"trace_{case}"]
        g.add((trace, RDF.type, tr_terms['Trace']))

        prior_evt = False

        for index, row in df.iterrows():
            evt = Sepsis[f"evt_{index}"]

            activ_label=urllib.parse.quote(row['concept:name']).replace("%20", "_")
            activ = Sepsis[activ_label]
            g.add((evt, tr_terms['activity'], activ))

            ts = Literal(row['time:timestamp'])
            g.add((evt, tr_terms['ts'], ts))

            g.add((evt, tr_terms['in'], trace))

            if (row['lifecycle:transition']):
                value = urllib.parse.quote_plus(row['lifecycle:transition'])
                value = Sepsis[value]
                g.add((evt, tr_terms['lifecycle'], value))

            if (row['org:group']):
                value = urllib.parse.quote_plus(row['org:group'])
                value = Sepsis[value]
                g.add((evt, tr_terms['group'], value))

            for col in log_terms:
                if not pd.isna(row[col]):
                    value = Literal(row[col])
                    g.add((evt, log_terms[col], value))

            if prior_evt is not False:
                add_link(prior_evt, evt, trace, g, format)

            prior_evt = evt

        add_link(prior_evt, tr_terms['nil'], trace, g, format)

        total_num += 1
        cur_traces += 1
        if limit != -1 and cur_traces == limit:
            break

    end_conv = time.time_ns()

    print("total number of traces:", total_num)
    print("conversion time (ms):", (end_conv-start_conv)/1000000)

    start_save = time.time_ns()

    g.serialize(destination=filepath)

    end_save = time.time_ns()
    print("save time (ms):", (end_save-start_save)/1000000)

    end = time.time_ns()
    print("total time (ms):", (end-start)/1000000)



def add_link(prior_evt, next_evt, trace, g, format):
    if format == RDFLogFormat.LINK_REIFIED:
        link = BNode()
        g.add((link, tr_terms['in'], trace))
        g.add((link, tr_terms['from'], prior_evt))
        g.add((link, tr_terms['to'], next_evt))
                    
    elif format == RDFLogFormat.LINK_PRED:
        g.add((prior_evt, tr_terms['next'], next_evt))