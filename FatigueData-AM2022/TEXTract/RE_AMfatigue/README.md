# RE_AMfatigue

The code is used to extract additive manufacturing (AM) fatigue data by regular expression (RE).

<table>
    <tr>
        <td><b>Category</b></td>
        <td><b>Parameter</b></td>
        <td><b>description</b></td>
        <td><b>Category</b></td>
        <td><b>Parameter</b></td>
        <td><b>description</b></td>        
    </tr>
    <tr>
        <td>Materials</td>
        <td>mat_name</td>
        <td>Name of the material</td> 
        <td rowspan="2">Processing</td>  
        <td>heat_treat</td>
        <td>Heat treatment</td>        
    </tr>
    <tr>
        <td rowspan="17">AM</td>
        <td>am_type</td>
        <td>Types of AM</td>
        <td>surf_treat</td>
        <td>Surface treatment</td>                    
    </tr>    
    <tr>
        <td>am_machine</td>
        <td>AM machine</td>
        <td rowspan="9">Testing</td>
        <td>fat_type</td>
        <td>Types of fatigue tests</td>          
    </tr>    
    <tr>
        <td>direction</td>
        <td>Direction of specimen</td>
        <td>fat_temp</td>
        <td>Fatigue temperature</td>          
    </tr>        
    <tr>
        <td>scan_speed</td>
        <td>Scan speed</td>
        <td>fat_env</td>
        <td>Fatigue environment</td>          
    </tr>      
    <tr>
        <td>hatch_space</td>
        <td>Hatch space</td>
        <td>fat_r</td>
        <td>Load ratio</td>         
    </tr>      
    <tr>
        <td>layer_thickness</td>
        <td>Layer_thickness</td>
        <td>frequency</td>
        <td>Frequency of loading</td>         
    </tr>      
    <tr>
        <td>preheat</td>
        <td>Preheat temperature of the AM platform</td>
        <td>fat_machine</td>
        <td>Fatigue machine</td> 
    </tr>      
    <tr>
        <td>am_env</td>
        <td>AM environment</td>
        <td>fat_standard</td>
        <td>Fatigue standard</td>         
    </tr>      
    <tr>
        <td>layer_rot</td>
        <td>Layer scan rotation</td>
        <td>spec_desc</td>
        <td>Specimen description</td>         
    </tr>  
    <tr>
        <td>scan_pattern</td>
        <td>Scan pattern</td>
        <td>load_ctrl</td>
        <td>Load control</td>         
    </tr>  
    <tr>
        <td>fdstock_size</td>
        <td>Size of feedstock</td>
        <td rowspan="4">Static<br>mechanical<br>properties</td>
        <td>modulus</td>
        <td>Young's modulus</td>               
    </tr>     
    <tr>
        <td>power</td>
        <td>power of the heat source</td>
        <td>yield_strength</td>
        <td>Yield strength</td>      
    </tr>           
    <tr>
        <td>voltage</td>
        <td>Voltage of the heat source</td>
        <td>tensile_strength</td>
        <td>Tensile strength</td>  
    </tr>      
    <tr>
        <td>current</td>
        <td>Current of the heat source</td>
        <td>Elongation</td>
        <td>elongation</td>          
    </tr>     
    <tr>
        <td>speed_func</td>
        <td>Speed function of the heat source</td>
        <td> </td>
        <td> </td>     
        <td> </td>     
    </tr>        
    <tr>
        <td>pfeed_rate</td>
        <td>Powder feed rate</td>
        <td> </td>
        <td> </td> 
        <td> </td>           
    </tr>        
    <tr>
        <td>wfeed_rate</td>
        <td>Wire feed rate</td>
        <td> </td>
        <td> </td> 
        <td> </td>           
    </tr>            
</table>    



## Usage

Download the `regular_expr.py` file and import the function `extract_data`.

INPUT

`extract_data` includes 2 function arguments, *doc* and *parameter*.
*doc* is a list of string and each string is a sentence.
*parameter* is the target parameter to extract, as listed in the above table.

OUTPUT

`extract_data` returns a dictionary including *value*, *unit* and *source*, each of which is a list.
*source* records the sentence where the data extracted from.

An example for the `parser` is given below:

``` python
from regular_expr import extract_data

doc=['$SENTENCE_1','$SENTENCE_2','$SENTENCE_...']
para='am_type'
data=extract_data(doc,para)
```

Please change '\$SENTENCE_n' to your target text.
