clear;
path0='YOUR_PATH';
load([path0,'FatigueData-CMA2022.mat'],'fatiguedata_cma2022')
art=fatiguedata_cma2022.articles;

path='./';
filename='ulfd.xml';
article_id=1;
dataset_id=1;
ulfd=exportULFD(art(article_id).metadata,art(article_id).scidata.datasets(dataset_id));
xmlwrite([path,filename],ulfd);

function ulfd=exportULFD(meta,ds)
    ulfd=com.mathworks.xml.XMLUtils.createDocument('ulfd');
    ulfd=ulfd.getDocumentElement;
    
    mt=ulfd.createElement('meta');
    ref=ulfd.createElement('reference');
    ref.appendChild(add_string(ulfd,'doi',meta.doi));
    ref.appendChild(add_string(ulfd,'title',meta.title));
    ref.appendChild(add_string(ulfd,'source',meta.source));
    ref.appendChild(add_num(ulfd,'year',meta.year));
    ref.appendChild(add_string_cell(ulfd,'author',meta.author));
    ref.appendChild(add_string_cell(ulfd,'institution',meta.institution));
    ref.appendChild(add_string_cell(ulfd,'country_region',meta.country_region));
    ref.appendChild(add_string_cell(ulfd,'fund',meta.fund));
    mt.appendChild(ref);
    ulfd.appendChild(mt);
    
    mat=ulfd.createElement('materials');
    mat.appendChild(add_string(ulfd,'type',ds.materials.mat_type));
    mat.appendChild(add_string(ulfd,'name',ds.materials.mat_name));
    mat.appendChild(add_string(ulfd,'ratio_type',ds.materials.ratio_type));
    mat.appendChild(add_string(ulfd,'atomic_structure',ds.materials.atomic_struct));
    mat.appendChild(add_composition(ulfd,'composition',ds.materials.composition));
    ulfd.appendChild(mat);
    
    proc=ulfd.createElement('processing');
    proc.appendChild(add_processing(ulfd,'processing_sequence',ds.processing.proc_para,ds.processing.proc_seq));
    proc.appendChild(add_string(ulfd,'ingot_description',ds.processing.ingot_desc));
    proc.appendChild(add_num_array(ulfd,'ingot_size',ds.processing.ingot_size));
    proc.appendChild(add_processing(ulfd,'surface_treatment_sequence',ds.processing.surf_para,ds.processing.surf_seq));
    ulfd.appendChild(proc);
    
    test=ulfd.createElement('testing');
    test.appendChild(add_string(ulfd,'fatigue_type',ds.testing.fat_type));
    test.appendChild(add_num_array(ulfd,'fatigue_temperature',ds.testing.fat_temp));
    test.appendChild(add_num_array(ulfd,'load_ratio',ds.testing.fat_r));
    test.appendChild(add_num_array(ulfd,'frequency',ds.testing.frequency));
    test.appendChild(add_string(ulfd,'fatigue_standard',ds.testing.fat_standard));
    test.appendChild(add_string(ulfd,'fatigue_environment',ds.testing.fat_env));
    test.appendChild(add_string(ulfd,'fatigue_machine',ds.testing.fat_machine));
    test.appendChild(add_string(ulfd,'specimen_description',ds.testing.spec_desc));
    test.appendChild(add_num_array(ulfd,'specimen_size',ds.testing.spec_size));
    test.appendChild(add_num_array(ulfd,'specimen_kt',ds.testing.spec_kt));
    test.appendChild(add_string(ulfd,'load_control',ds.testing.load_ctrl));
    test.appendChild(add_string(ulfd,'failure_criterion',ds.testing.fail_crt));
    ulfd.appendChild(test);
 
    fati=ulfd.createElement('fatigue');
    fati.appendChild(add_string(ulfd,'fatigue_data_type',ds.fatigue.fdata_type));
    fati.appendChild(add_fatigue_data(ulfd,'fatigue_data',ds.fatigue.fat_data,ds.fatigue.fdata_type));
    ulfd.appendChild(fati);
    
    mech=ulfd.createElement('mechanical_properties');
    mech.appendChild(add_num_array(ulfd,'modulus',ds.mech_prop.modulus));
    mech.appendChild(add_num_array(ulfd,'yield_strength',ds.mech_prop.yield_strength));
    mech.appendChild(add_num_array(ulfd,'ultimate_strength',ds.mech_prop.ultimate_strength));
    mech.appendChild(add_num_array(ulfd,'elongation',ds.mech_prop.elongation));
    mech.appendChild(add_num_array(ulfd,'fracture_toughness',ds.mech_prop.toughness));
    mech.appendChild(add_num_array(ulfd,'fatigue_crack_growth_rate',ds.mech_prop.kth));
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