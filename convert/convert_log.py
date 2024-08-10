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
    'lifecycle': TR.lifecycle,
    'group': TR.org_group,
    
    'resource': TR.resource,
    'Event': TR['Event'],
    'Object': TR['Object'],
    'E2O': TR['E2O'],
    'O2O': TR['O2O'],
    'OAVal': TR['OAVal'],
    'event': TR['event'],
    'object': TR['object'],
    'object2': TR['object2'],
    'qualifier': TR['qualifier'],
    'attribute': TR['attribute'],
    
    'case_obj': TR['case_obj']
}
log_terms = {}

def convert_xes_rdf(log, save_to, ns, format, limit=-1):
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

            activ = str_to_uri(row['concept:name'], ns, QuoteOptions.CUSTOM)
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

def convert_ocel2_rdf(log, save_to, ns, case_obj_type=None, limit=-1):
    start = time.time_ns()
    start_conv = time.time_ns()
    
    g = Graph()
    
    events = []; count = 0
    for _, row in log.events.iterrows():
        events.append(row['ocel:eid'])
        evt = str_to_uri(row['ocel:eid'], ns, QuoteOptions.CUSTOM)
        g.add((evt, RDF.type, tr_terms['Event']))
        g.add((evt, tr_terms['activity'], Literal(row['ocel:activity'])))
        g.add((evt, tr_terms['ts'], Literal(row['ocel:timestamp'])))
        g.add((evt, tr_terms['lifecycle'], Literal(row['lifecycle'])))
        g.add((evt, tr_terms['resource'], Literal(row['resource'])))
        
        if count != -1:
            count += 1
            if count == limit:
                break
    
    objects = []
    for _, row in log.relations.loc[log.relations['ocel:eid'].isin(events),].iterrows():
    # for _, row in log.relations.iterrows():
        objects.append(row['ocel:oid'])
        rel = BNode()
        g.add((rel, RDF.type, tr_terms['E2O']))
        g.add((rel, tr_terms['event'], str_to_uri(row['ocel:eid'], ns, QuoteOptions.CUSTOM)))
        g.add((rel, tr_terms['object'], str_to_uri(row['ocel:oid'], ns, QuoteOptions.CUSTOM)))
        g.add((rel, tr_terms['qualifier'], Literal(row['ocel:qualifier'])))
        
    for _, row in log.objects.loc[log.objects['ocel:oid'].isin(objects),].iterrows():
        obj = str_to_uri(row['ocel:oid'], ns, QuoteOptions.CUSTOM)
        g.add((obj, RDF.type, tr_terms['Object']))
        g.add((obj, RDF.type, str_to_uri(row['ocel:type'], ns, QuoteOptions.CUSTOM)))  
        
    # for _, row in log.objects.iterrows():
    #     obj = str_to_uri(row['ocel:oid'], ns, QuoteOptions.CUSTOM)
    #     g.add((obj, RDF.type, tr_terms['Object']))
    #     g.add((obj, RDF.type, str_to_uri(row['ocel:type'], ns, QuoteOptions.CUSTOM)))
    
    for _, row in log.o2o.loc[log.o2o['ocel:oid'].isin(objects),].iterrows():
    # for _, row in log.o2o.iterrows():
        rel = BNode()
        g.add((rel, RDF.type, tr_terms['O2O']))
        g.add((rel, tr_terms['object'], str_to_uri(row['ocel:oid'], ns, QuoteOptions.CUSTOM)))
        g.add((rel, tr_terms['object2'], str_to_uri(row['ocel:oid_2'], ns, QuoteOptions.CUSTOM)))
        g.add((rel, tr_terms['qualifier'], Literal(row['ocel:qualifier'])))

    # for _, row in log.object_changes.iterrows():
    #     val = BNode()
    #     field = row['ocel:field']
    #     value = row[field]
    #     if value == "None" or pd.isna(value) or pd.isnull(value):
    #         continue
        
    #     g.add((val, RDF.type, tr_terms['OAVal']))
    #     g.add((val, tr_terms['object'], str_to_uri(row['ocel:oid'], ns, QuoteOptions.CUSTOM)))
    #     g.add((val, tr_terms['attribute'], Literal(field)))
    #     g.add((val, tr_terms['ts'], Literal(row['ocel:timestamp'])))
    #     g.add((val, RDF.value, Literal(row[field])))

    # if case_obj_type is not None:
    #     cases = log.relations.loc[log.relations['ocel:type']==case_obj_type,]
    #     groups = cases.sort_values(by='ocel:timestamp').groupby('ocel:oid')
        
    #     for case, df in groups:
    #         case_uri = str_to_uri(case, ns, QuoteOptions.CUSTOM)
                   
    #         trace = str_to_uri(f"trace_{case}", ns, QuoteOptions.CUSTOM)
    #         g.add((trace, RDF.type, tr_terms['Trace']))
            
    #         prior_evt = False
    #         for _, row in df.iterrows():
                
    #             evt = str_to_uri(row['ocel:eid'], ns, QuoteOptions.CUSTOM)
    #             if prior_evt is not False:
    #                 add_link_case(prior_evt, evt, trace, g, case_uri)

    #             prior_evt = evt

    #         add_link_case(prior_evt, tr_terms['nil'], trace, g, case_uri)

    end_conv = time.time_ns()

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
        return link
                    
    elif format == RdfRepresent.LINK_PRED:
        g.add((prior_evt, tr_terms['next'], next_evt))
        

def add_link_case(prior_evt, next_evt, trace, g, case):
    link = add_link(prior_evt, next_evt, trace, g, RdfRepresent.LINK_REIFIED)
    g.add((link, tr_terms['case_obj'], case))