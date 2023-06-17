clear;
path0='YOUR_PATH';
load([path0,'FatigueData-CMA2022.mat'],'fatiguedata_cma2022')
art=fatiguedata_cma2022.articles;

path='./';
filename='ulfd.xml';
article_id=1;
dataset_id=1;
dn=export(art(article_id).metadata,art(article_id).scidata.datasets(dataset_id));
xmlwrite([path,filename],dn);

function dn=export(meta,ds)
    dn=com.mathworks.xml.XMLUtils.createDocument('ulfd');
    ulfd=dn.getDocumentElement;
    
    mt=dn.createElement('meta');
    ref=dn.createElement('reference');
    ref.appendChild(add_string(dn,'doi',meta.doi));
    ref.appendChild(add_string(dn,'title',meta.title));
    ref.appendChild(add_string(dn,'source',meta.source));
    ref.appendChild(add_num(dn,'year',meta.year));
    ref.appendChild(add_string_cell(dn,'author',meta.author));
    ref.appendChild(add_string_cell(dn,'institution',meta.institution));
    ref.appendChild(add_string_cell(dn,'country_region',meta.country_region));
    ref.appendChild(add_string_cell(dn,'fund',meta.fund));
    mt.appendChild(ref);
    ulfd.appendChild(mt);
    
    mat=dn.createElement('materials');
    mat.appendChild(add_string(dn,'type',ds.materials.mat_type));
    mat.appendChild(add_string(dn,'name',ds.materials.mat_name));
    mat.appendChild(add_string(dn,'percent_type',ds.materials.percent_type));
    mat.appendChild(add_string(dn,'atomic_structure',ds.materials.atomic_struct));
    mat.appendChild(add_composition(dn,'composition',ds.materials.composition));
    ulfd.appendChild(mat);
    
    proc=dn.createElement('processing');
    proc.appendChild(add_processing(dn,'processing_sequence',ds.processing.proc_para,ds.processing.proc_seq));
    proc.appendChild(add_string(dn,'ingot_description',ds.processing.ingot_desc));
    proc.appendChild(add_num_array(dn,'ingot_size',ds.processing.ingot_size));
    proc.appendChild(add_processing(dn,'surface_treatment_sequence',ds.processing.surf_para,ds.processing.surf_seq));
    ulfd.appendChild(proc);
    
    test=dn.createElement('testing');
    test.appendChild(add_string(dn,'fatigue_type',ds.testing.fat_type));
    test.appendChild(add_num_array(dn,'fatigue_temperature',ds.testing.fat_temp));
    test.appendChild(add_num_array(dn,'load_ratio',ds.testing.fat_r));
    test.appendChild(add_num_array(dn,'frequency',ds.testing.frequency));
    test.appendChild(add_string(dn,'fatigue_standard',ds.testing.fat_standard));
    test.appendChild(add_string(dn,'fatigue_environment',ds.testing.fat_env));
    test.appendChild(add_string(dn,'fatigue_machine',ds.testing.fat_machine));
    test.appendChild(add_string(dn,'specimen_description',ds.testing.spec_desc));
    test.appendChild(add_num_array(dn,'specimen_size',ds.testing.spec_size));
    test.appendChild(add_num_array(dn,'specimen_kt',ds.testing.spec_kt));
    test.appendChild(add_string(dn,'load_control',ds.testing.load_ctrl));
    test.appendChild(add_string(dn,'failure_criterion',ds.testing.fail_crt));
    ulfd.appendChild(test);
 
    fati=dn.createElement('fatigue');
    fati.appendChild(add_string(dn,'fatigue_data_type',ds.fatigue.fdata_type));
    fati.appendChild(add_fatigue_data(dn,'fatigue_data',ds.fatigue.fat_data,ds.fatigue.fdata_type));
    ulfd.appendChild(fati);
    
    mech=dn.createElement('mechanical_properties');
    mech.appendChild(add_num_array(dn,'modulus',ds.mech_prop.modulus));
    mech.appendChild(add_num_array(dn,'yield_strength',ds.mech_prop.yield_strength));
    mech.appendChild(add_num_array(dn,'ultimate_strength',ds.mech_prop.ultimate_strength));
    mech.appendChild(add_num_array(dn,'elongation',ds.mech_prop.elongation));
    mech.appendChild(add_num_array(dn,'fracture_toughness',ds.mech_prop.toughness));
    mech.appendChild(add_num_array(dn,'fatigue_crack_growth_rate',ds.mech_prop.kth));
    ulfd.appendChild(mech);    
end

function obj=add_string(dn,name,str)
    obj=dn.createElement(name);
    %obj.setAttribute('type','str');
    obj.appendChild(dn.createTextNode(str));
end

function obj=add_num(dn,name,num,format)
    obj=dn.createElement(name);
    %obj.setAttribute('type','num');
    if nargin>3
        obj.appendChild(dn.createTextNode(num2str(num,format)));
    else
        obj.appendChild(dn.createTextNode(num2str(num)));
    end
end

function obj=add_string_cell(dn,name,cel)
    obj=dn.createElement(name);
    %obj.setAttribute('type','list_str');
    for i=1:numel(cel)
        cn=dn.createElement('item');
        %cn.setAttribute('id',num2str(i));
        cn.appendChild(dn.createTextNode(cel{i}));
        obj.appendChild(cn);
    end
end

function obj=add_composition(dn,name,cel)
    obj=dn.createElement(name);
    %obj.setAttribute('type','list');
    for i=1:size(cel,1)
        cn=dn.createElement('item');
        %cn.setAttribute('id',num2str(i));
        cn.appendChild(add_string(dn,'element',cel{i,1}));
        cn.appendChild(add_num(dn,'atomic_percent',cel{i,2}));
        obj.appendChild(cn);
    end
end

function obj=add_num_array(dn,name,arr)
    obj=dn.createElement(name);
    %obj.setAttribute('type','list_num');
    n=numel(arr);
    if n==0
        obj.appendChild(add_string(dn,'value',''));
    else    
        for i=1:n
            obj.appendChild(add_num(dn,'value',arr(i)));
        end    
    end
end

function obj=add_processing(dn,name,para,seq)
    obj=dn.createElement(name);
    %obj.setAttribute('type','struct');
    for i=1:numel(seq)
        cn=dn.createElement('item');
        %cn.setAttribute('id',num2str(i));
        data=para{seq(i)};
        f=fieldnames(data);
        for j=1:numel(f)
            tmp=getfield(data,f{j});
            if isnumeric(tmp)
                cn.appendChild(add_num_array(dn,f{j},tmp));
            elseif ischar(tmp)        
                cn.appendChild(add_string(dn,f{j},tmp));
            else
                disp(['processing, data type not found for ',f{i}])
            end
        end
        obj.appendChild(cn);        
    end
end

function obj=add_fatigue_data(dn,name,arr,type)
    obj=dn.createElement(name);
    %obj.setAttribute('type','list');
    for i=1:size(arr,1)
        cn=dn.createElement('item');
        %cn.setAttribute('id',num2str(i));
        if strcmp(type,'sn')
            cn.appendChild(add_num(dn,'fatigue_life',arr(i,1)));
            cn.appendChild(add_num(dn,'stress_amplitude',arr(i,2)));
            cn.appendChild(add_num(dn,'runout',arr(i,3)));
        elseif strcmp(type,'en')
            cn.appendChild(add_num(dn,'fatigue_life',arr(i,1)));
            cn.appendChild(add_num(dn,'strain_amplitude',arr(i,2)));
            cn.appendChild(add_num(dn,'runout',arr(i,3))); 
        elseif strcmp(type,'dadn')
            cn.appendChild(add_num(dn,'SIF_range',arr(i,1)));
            cn.appendChild(add_num(dn,'dadN',arr(i,2)));
        end
        obj.appendChild(cn);
    end
end