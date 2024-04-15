from convert_base import str_to_uri, RdfRepresent, QuoteOptions
from rdflib import Namespace, Literal, Graph, BNode, RDF
import pandas as pd
import time

TR = Namespace("http://rdf.org/trace#")

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

def convert_log_rdf(log, save_to, ns, format, limit=-1):
    start = time.time_ns()
    start_conv = time.time_ns()

    g = Graph()

    for col in log.columns:
        if col not in ( 'time:timestamp', 'concept:name', 'case:concept:name', 'lifecycle:transition', 'org:group' ):
            log_terms[col] = ns[col]

    groups = log.sort_values(by='time:timestamp', ascending=True).groupby('case:concept:name')
    # print(groups.groups)

    total_num = 0
    cur_traces = 0
    for case, df in groups:
        trace = ns[f"trace_{case}"]
        g.add((trace, RDF.type, tr_terms['Trace']))

        prior_evt = False

        for index, row in df.iterrows():
            evt = ns[f"evt_{index}"]

            activ = str_to_uri(row['concept:name'], ns, QuoteOptions.SPACE_UNDERSCORE)
            g.add((evt, tr_terms['activity'], activ))

            ts = Literal(row['time:timestamp'])
            g.add((evt, tr_terms['ts'], ts))

            g.add((evt, tr_terms['in'], trace))

            if ('lifecycle:transition' in row):
                value = str_to_uri(row['lifecycle:transition'], ns)
                g.add((evt, tr_terms['lifecycle'], value))

            if ('org:group' in row):
                value = str_to_uri(row['org:group'], ns)
                g.add((evt, tr_terms['group'], value))

            for col in log_terms:
                if col in row and not pd.isna(row[col]):
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

    g.serialize(destination=save_to)

    end_save = time.time_ns()
    print("save time (ms):", (end_save-start_save)/1000000)

    end = time.time_ns()
    print("total time (ms):", (end-start)/1000000)



def add_link(prior_evt, next_evt, trace, g, format):
    if format == RdfRepresent.LINK_REIFIED:
        link = BNode()
        g.add((link, tr_terms['in'], trace))
        g.add((link, tr_terms['from'], prior_evt))
        g.add((link, tr_terms['to'], next_evt))
                    
    elif format == RdfRepresent.LINK_PRED:
        g.add((prior_evt, tr_terms['next'], next_evt))