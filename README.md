# doomharvest
![logo](doomharvest_name.png)

## Description

This is a package for using chatgpt to gather natural history data.

## An example

Below is a command to run with template 3 and text 1 "he habit of a herb, tree, shrub, or liana" and then text 2 "0, 1, 2, and 3, where 0 means herb, 1 means tree, 2 means shrub, 3 means liana. The terms ‘herbaceous’ and ‘epiphytic’ mean ‘herb’. The term ‘arborescent’ means tree. The term ‘suffrutescent’ means shrub. The phrase ‘woody vine’ means liana." See the templates below for "d3". 

```python
python doomharvest.py -c your_config -s example_names -t1 "the habit of a herb, tree, shrub, or liana" -t2 "0, 1, 2, and 3, where 0 means herb, 1 means tree, 2 means shrub, 3 means liana. The terms ‘herbaceous’ and ‘epiphytic’ mean ‘herb’. The term ‘arborescent’ means tree. The term ‘suffrutescent’ means shrub. The phrase ‘woody vine’ means liana." -te d3
```

The output is listed below. 

```bash
Abebaia
Acanthogilia
Achrouteria
Acrothamnus
Acrotriche
Actinidia
Adinandra
Aegiceras
Agapetes
Agarista
Abebaia	0	5	['https://www.plantsoftheworldonline.org', 'https://www.gbif.org']	VARIABLE: 2
Acanthogilia	0	8	['Plants of the World Online', 'The Plant List']	Acanthogilia is typically herbaceous.
Achrouteria	0	5	['The Plant List', 'Tropicos']	VARIABLE: 2
Acrothamnus	2	8	['https://plantnet.rbgsyd.nsw.gov.au', 'https://powo.science.kew.org']	VARIABLE: 0
Acrotriche	2	8	['https://www.anbg.gov.au/gnp/gnp12/acrotriche.html', 'https://vicflora.rbg.vic.gov.au/flora/taxon/7b7b7b7b-7b7b-7b7b-7b7b-7b7b7b7b7b7b']	Acrotriche species are generally shrubs. VARIABLE: Some species may exhibit a more herbaceous form.
Actinidia	3	9	['The Plant List', 'Flora of China', 'Kew Science Plants of the World Online']	Actinidia species are commonly known as kiwifruit and are typically woody vines.
Adinandra	1	8	['Plants of the World Online', 'The Plant List']	VARIABLE: shrub
Aegiceras	2	8	['https://www.plantsoftheworldonline.org', 'https://www.gbif.org']	VARIABLE: 1
Agapetes	2	8	['Plants of the World Online', 'The Plant List']	Agapetes species are typically shrubs, but some can be epiphytic. VARIABLE: 0
Agarista	2	8	['The Plant List', 'Flora of North America']	VARIABLE: 1
```

## Templates

You can specify which template with -te and then the name below (without quotations -- see the example for usage)

 - "d1" = f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to floral morphology, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, report the most common state and then in the annotations put VARIABLE: and then the alternative state. ",
 - "c1" = f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. In regard to floral morphology, I need you to tell me the number of INSERTTEXT1 that the taxon that the user provides has in a JSON dictionary like this: {{'taxon_name': {{'value_min', ‘value_max’, 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, put VARIABLE in the annotations. ",
 - "d2" = f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to floral morphology, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list the sources or references used for obtaining this data. If you did not find a source, set the confidence to -1. The best sources are these websites: “https://www.delta-intkey.com/angio/index.htm”, and “http://floranorthamerica.org/”. Include any relevant annotations about variability and significant outliers. ",
 - "d3" = f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to habit and leaf form, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, report the most common state and then in the annotations put VARIABLE: and then the alternative state. ",
 - "c2" = f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to habit and leaf form, I need you to tell me the number of INSERTTEXT1 that the taxon that the user provides has in a JSON dictionary like this: {{'taxon_name': {{'value_min', ‘value_max’, 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, put VARIABLE in the annotations. ",
 - "d4" = f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to fruit morphology, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, report the most common state and then in the annotations put VARIABLE: and then the alternative state. ",
 - "d5" = f"I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. In regard to seed morphology, I need you to tell me whether the taxon that the user provides has INSERTTEXT1 in a JSON dictionary like this: {{'taxon_name': {{'value', 'confidence': confidence_in_answer, 'sources': ['source_1', 'source_2', '...'],'annotations': 'annotation'}}}}. Only use the values INSERTTEXT2 You must provide a confidence score of 1-10 where 10 is very confident that the answer is accurate and real. Return only the JSON dictionary with no explanation. If you don't know the answer, set the confidence to -1. Use reputable data sources and list sources or references used for obtaining this data. Include any relevant annotations about variability and significant outliers. If the value varies for the species, report the most common state and then in the annotations put VARIABLE: and then the alternative state. ",
 - "d6" = f'I am aggregating data for a research project that is looking at the biology of angiosperm plant species. You are an specialist in botanical taxonomy. Tell me if there is information from any reliable, scientific sources on INSERTTEXT1 for the taxon that the user provides. Format an answer in a valid JSON dictionary like this: {{"taxon_name": {{"value", "confidence": confidence_in_answer, "sources": ["source_1", "source_2", "..."],"annotations": "annotation"}}}}. Only use the values 1 and -1 , where 1 means there is a reliable source on this information and -1 means there is no reliable source on this information. Only report a source if you can find a reliable source.'
