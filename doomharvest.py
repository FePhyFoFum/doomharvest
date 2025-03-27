import sys
import json
import math
import argparse as ap
import numpy as np
from langchain_openai import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser

# These are example templates

TEMPLATES = {"d1":	f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to floral morphology, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, report the most common state and then in the annotations put VARIABLE: and then the alternative state. ",
             "c1":	f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. In regard to floral morphology, I need you to tell me the number of INSERTTEXT1 that the taxon that the user provides has in a JSON dictionary like this: {{'taxon_name': {{'value_min', ‘value_max’, 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, put VARIABLE in the annotations. ",
             "d2":	f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to floral morphology, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list the sources or references used for obtaining this data. If you did not find a source, set the confidence to -1. The best sources are these websites: “https://www.delta-intkey.com/angio/index.htm”, and “http://floranorthamerica.org/”. Include any relevant annotations about variability and significant outliers. ",
             "d3":	f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to habit and leaf form, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, report the most common state and then in the annotations put VARIABLE: and then the alternative state. ",
             "c2":	f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to habit and leaf form, I need you to tell me the number of INSERTTEXT1 that the taxon that the user provides has in a JSON dictionary like this: {{'taxon_name': {{'value_min', ‘value_max’, 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, put VARIABLE in the annotations. ",
             "d4":f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to fruit morphology, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, report the most common state and then in the annotations put VARIABLE: and then the alternative state. ",
             "d5":	f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to seed morphology, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, report the most common state and then in the annotations put VARIABLE: and then the alternative state. ",
             "d6": f'I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. Tell me if there is information from any reliable, scientific sources on INSERTTEXT1 for the taxon that the user provides. Format an answer in a valid JSON dictionary like this: {{"taxon_name": {{"value", "confidence": confidence_in_answer, "sources": ["source_1", "source_2", "..."],"annotations": "annotation"}}}}. Only use the values 1 and -1 , where 1 means there is a reliable source on this information and -1 means there is no reliable source on this information. Only report a source if you can find a reliable source.'}


"""
read the configuration file
should be in the format 
AZURE_API_VERSION VERSION
AZURE_API_BASE https://azure-openai-apiADDRESS
AZURE_API_KEY_AZURE KEY
AZURE_API_TYPE TYPE
AZURE_ORGANIZATION ORGIFREQUIRED
"""
def read_config(fl):
    data = {}
    f = open(fl,"r")
    for i in f:
        i=i.strip()
        if len(i) > 1:
            spls = i.split(" ")
            data[spls[0]] = spls[1]
    f.close()
    return data


def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    They weights are in effect first normalized so that they 
    sum to 1 (and so they must not all be 0).

    values, weights -- NumPy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)
    return (average, math.sqrt(variance))

class SpeciesDataAggregator:
    def __init__(self, configfile, model_name="gpt-4o"):
        data = read_config(configfile)
        self.model_name = model_name
        self.llm = AzureChatOpenAI(
                    deployment_name = 'gpt-4o',
                    openai_api_version = data['AZURE_API_VERSION'],
                    openai_api_key = data['AZURE_API_KEY_AZURE'],
                    azure_endpoint = data['AZURE_API_BASE'],
                    openai_organization = data['AZURE_ORGANIZATION'],
                    temperature = 1.0,
                    max_tokens = 256,
                    top_p = 0,
                    frequency_penalty = 0,
                    presence_penalty = 0
                )
        self.parser = JsonOutputParser()
    
    def run_discrete_TEMPLATE_query(self,species,template_text):
        system_message = SystemMessage(content=template_text)
        user_message = HumanMessage(content=species)

        messages = [system_message, user_message]
        try:
            response = self.llm.invoke(messages)
        except:
            return species, "ERROR content warning"
        content = response.content
        try:
            parsed_content = self.parser.parse(content)
            taxon_name = list(parsed_content.keys())[0]
            value = parsed_content[taxon_name]['value']
            conf = parsed_content[taxon_name]['confidence']
            sourc = parsed_content[taxon_name]['sources']
            annot = parsed_content[taxon_name]['annotations']
            return taxon_name, value, conf, sourc,annot
        except Exception as e:
            print(e,file=sys.stderr)
            print(f"ERROR: {content}", file=sys.stderr)
            return species, "ERROR"

    def aggregate_template_answer_data(self, species_list, reps,template_text):
        results = []
        for species in species_list:
            print(species,file=sys.stderr)
            if reps == 1:
                result = self.run_discrete_TEMPLATE_query(species,template_text)
                results.append(result)
            elif reps > 1:
                sp = None
                answer = []
                confs = []
                sources = set([])
                annotations = set([])
                err = False
                for i in range(reps):
                    result = self.run_discrete_TEMPLATE_query(species,template_text)
                    sp = result[0]
                    if "ERROR" in result[-1]:
                        results.append(result)
                        err = True
                        break
                    answer.append(result[1])
                    confs.append(result[2])
                    for j in result[3]:
                        sources.add(j)
                    annotations.add(result[4])
                if err:
                    continue
                try:
                    x1,x1s = weighted_avg_and_std(answer,confs)
                    result = (sp,x1,x1s,sum(confs)/len(confs),",".join(list(sources)),",".join(list(annotations)))
                except:
                    result = (sp,str(answer[0]),"0",str(confs[0]),"0",list(sources)[0],list(annotations)[0],"(ERROR IN AVG STD)")
                results.append(result)
        return results

    def aggregate_template_answer_data_check(self, species_list, reps,template_text):
        results = []
        for species in species_list:
            print(species,file=sys.stderr)
            result = self.run_discrete_TEMPLATE_query(species,template_text)
            results.append(result)
        return results

def main(args):
    taxa_list = []
    with open(args.taxa, "r") as sf:
        for line in sf:
            if len(line.strip()) > 2:
                taxa_list.append(line.strip())

    aggregator = SpeciesDataAggregator(args.configfile)
    if args.te != "d6":
        template_text = TEMPLATES[args.te].replace("INSERTTEXT1",args.t1).replace("INSERTTEXT2",args.t2) 
        results = aggregator.aggregate_template_answer_data(taxa_list,args.reps,template_text)
    else:
        template_text = TEMPLATES[args.te].replace("INSERTTEXT1",args.t1)
        results = aggregator.aggregate_template_answer_data_check(taxa_list,1,template_text)
    

    if args.outfile:
        with open(args.outfile, "w") as outf:
            for result in results:
                outf.write(",".join(result) + "\n")
    else:
        for result in results:
            print("\t".join([str(i) for i in result]))

if __name__ == "__main__":
    parser = ap.ArgumentParser(prog="doomharvest",
        formatter_class=ap.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", "--outfile", type=str, required=False,
        help="Output file.")
    parser.add_argument('-s', "--taxa", type=str, required=True,
                        help="file with one species on each line")
    parser.add_argument('-r',"--reps",type=int,required=False,
                        help="how many reps do you want?",default = 1)
    parser.add_argument('-c',"--configfile",type=str,required=True,
                        help="the config file with info in it.", default="um_config")
    parser.add_argument('-t1',"--t1",type=str,required=True,help="the replace for text1")
    parser.add_argument('-t2',"--t2",type=str,required=False,help="the replace for text2")
    parser.add_argument('-te',"--te",type=str,required=True,help="the template (d1,c1,...)")
    if len(sys.argv) == 0:
        sys.argv.append("-h")
    args = parser.parse_args()

    main(args)