# Database APIs

The database APIs are presented as a collection of MATLAB scripts for manipulating the database. 

## Adding data entries

New data entries such as hardness or surface roughness can be added to the database by the `add_entry.m` script. The function is defined as

``` matlab
function db=add_data_entry(db,entry,epath,data,unit)
```
where *db* is the FatigueData-CMA2022 database. *entry* is the name of the entry to be added, in the format of string. *epath* is the path of the entry in a dataset, in the format of string. The *epath* follows the grammar of referring a field in the matlab structural array, with dot '.' connecting different levels of data struct. The *epath* assumes the root is a dataset under the scidata struct and begins with a dot '.'.
*data* is the data to be filled in the new data entry, in the format of cell array. Each line of the *data* is a data record, with the 1st column denoting the id of articles, the 2nd column denoting the id of datasets, and the 3rd column storing the data to be added. *unit* is the unit of the data, in the format of string. The output is a database with the new data entry added.

## Calculating propeties from the raw data

Currently, the script `cal_property.m` includes the function to calculate fatigue strength from *S*-*N* data. The function is defined as

``` matlab
function p=cal_prop(ds,prop,para)
```

where *ds* is a dataset under the scidata struct. *prop* is the property to be calculated, in the format of string. Use 'fs' for *prop* to calculate the fatigue strength. *para* is a cell array to specify the parameters for the calculation. For fatigue strength, the 1st column is the number of cycles at which the fatigue strength is calculated, the 2nd column is the method for fitting the *S*-*N* data ('linear' or 'stromeryer') and the 3rd column specifies how to process run-out data ('exclude all', 'include all','include max'). The output *p* is the calculated property.

## Calculating rating score of datasets

The script `cal_rate_score.m` calculates rating scores for datasets based on the completeness of their data entries. Weights can be defined to adjust the influence of data entries. The function is defined as

``` matlab
function score=cal_rating_score(ds,weight)
```

where *ds* is a dataset under the scidata struct. *weight* is the weight for data entries, in the format of struct the same as the dataset. *weight* can be initialized by the *weight_init* function with a default weight applied to all data entries. And then users can adjust the weight for specific data entries. For example,

``` matlab
default_weight=1;
weight=weight_init(default_weight);
weight.materials.composition=3;
weight.materials.atomic_struct=2;
weight.processing.proc_para=2;
weight.processing.surf_para=2;
```

The output of the function is the *score* of a dataset.

## Unified Language of Fatigue Data (ULFD)

Datasets can be exported following ULFD to XML files by the script `export_ulfd.m`. The function for export is defined as

``` matlab
function ulfd=exportULFD(meta,ds)
```

where *meta* is the metadata of an article and *ds* is a dataset under the scidata struct. The output is an XML Document object and can be written to file by

``` matlab
xmlwrite([path,filename],ulfd);
```

The XML files defined by ULFD can be imported by `import_ulfd.m`. The function is defined as 

``` matlab
function article=importULFD(path,file)
```

where the *path* and *file* specify the location of the XML file. The function returns an *article* struct containing metadata and scidata. `ulfd.xml` can be used as an example.
