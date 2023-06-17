clear
path='YOUR_PATH';
file='ulfd.xml';
data=importULFD(path,file);

function data=importULFD(path,file)
    xdoc=xmlread([path,file]);
    xroot=xdoc.getDocumentElement;

    data=data_init();
    meta=xroot.getElementsByTagName('meta').item(0);
    ref=meta.getElementsByTagName('reference').item(0);
    m=data.metadata;
    m.doi=extract_string(ref,'doi');
    m.title=extract_string(ref,'title');
    m.source=extract_string(ref,'source');
    m.year=uint8(extract_num(ref,'year'));
    m.author=extract_string_cell(ref,'author');
    m.institution=extract_string_cell(ref,'institution');
    m.country_region=extract_string_cell(ref,'country_region');
    m.fund=extract_string_cell(ref,'fund');
    data.metadata=m;

    ds=data.scidata.datasets(1);

    fati=xroot.getElementsByTagName('fatigue').item(0);
    ds.fatigue.fdata_type=extract_string(fati,'fatigue_data_type');
    ds.fatigue.fat_data=extract_fatigue(fati,'fatigue_data',ds.fatigue.fdata_type);

    mat=xroot.getElementsByTagName('materials').item(0);
    ds.materials.mat_type=extract_string(mat,'type');
    ds.materials.mat_name=extract_string(mat,'name');
    ds.materials.percent_type=extract_string(mat,'percent_type');
    ds.materials.atomic_struct=extract_string(mat,'atomic_structure');
    ds.materials.composition=extract_composition(mat,'composition');

    proc=xroot.getElementsByTagName('processing').item(0);
    ds.processing.proc_para=extract_processing(proc,'processing_sequence');
    ds.processing.proc_seq=[1:numel(ds.processing.proc_para)];
    ds.processing.ingot_desc=extract_string(proc,'ingot_description');
    ds.processing.ingot_size=extract_num_array(proc,'ingot_size');
    ds.processing.surf_para=extract_processing(proc,'surface_treatment_sequence');
    ds.processing.surf_seq=[1:numel(ds.processing.surf_para)];

    test=xroot.getElementsByTagName('testing').item(0);
    ds.testing.fat_type=extract_string(test,'fatigue_type');
    ds.testing.fat_temp=extract_num_array(test,'fatigue_temperature');
    ds.testing.fat_r=extract_num_array(test,'load_ratio');
    ds.testing.frequency=extract_num_array(test,'frequency');
    ds.testing.fat_standard=extract_string(test,'fatigue_standard');
    ds.testing.fat_env=extract_string(test,'fatigue_environment');
    ds.testing.fat_machine=extract_string(test,'fatigue_machine');
    ds.testing.spec_desc=extract_string(test,'specimen_description');
    ds.testing.spec_size=extract_num_array(test,'specimen_size');
    ds.testing.spec_kt=extract_num_array(test,'specimen_kt');
    ds.testing.load_ctrl=extract_string(test,'load_control');
    ds.testing.fail_crt=extract_string(test,'failure_criterion');

    mech=xroot.getElementsByTagName('mechanical_properties').item(0);
    ds.mech_prop.modulus=extract_num_array(mech,'modulus');
    ds.mech_prop.yield_strength=extract_num_array(mech,'yield_strength');
    ds.mech_prop.ultimate_strength=extract_num_array(mech,'ultimate_strength');
    ds.mech_prop.elongation=extract_num_array(mech,'elongation');
    ds.mech_prop.toughness=extract_num_array(mech,'fracture_toughness');
    ds.mech_prop.kth=extract_num_array(mech,'fatigue_crack_growth_rate');
    
    data.scidata.datasets=ds;
end

function data=extract_fatigue(obj,tag,type)
    eles=obj.getElementsByTagName(tag).item(0).getElementsByTagName('item');
    n=eles.getLength;
    data=[];
    ct=0;
    if strcmp(type,'sn')
        for i=1:n
            data(i,1)=extract_num(eles.item(i-1),'fatigue_life');
            data(i,2)=extract_num(eles.item(i-1),'stress_amplitude');
            data(i,3)=extract_num(eles.item(i-1),'runout');
        end
    elseif strcmp(type,'en')
        for i=1:n
            data(i,1)=extract_num(eles.item(i-1),'fatigue_life');
            data(i,2)=extract_num(eles.item(i-1),'strain_amplitude');
            data(i,3)=extract_num(eles.item(i-1),'runout');
        end    
    elseif strcmp(type,'dadn')
        for i=1:n
            data(i,1)=extract_num(eles.item(i-1),'SIF_range');
            data(i,2)=extract_num(eles.item(i-1),'dadN');
        end 
    end
end

function data=extract_num_array(obj,tag)
    eles=obj.getElementsByTagName(tag).item(0).getElementsByTagName('value');
    n=eles.getLength;
    data=[];
    ct=0;
    for i=1:n
        tmp=eles.item(i-1);
        if tmp.hasChildNodes
            tmp2=tmp.getFirstChild.getData;
            if numel(tmp2)>0
                ct=ct+1;
                data(ct)=str2num(tmp2);
            end
        end
    end
end

function proc=extract_processing(obj,tag)
    obj1=obj.getElementsByTagName(tag).item(0);
    items=obj1.getElementsByTagName('item');
    proc={};
    for i=0:items.getLength-1
       ele=items.item(i);
       tmp=struct();
       cn=ele.getChildNodes;
       nc=cn.getLength;
       for j=1:nc
           child=cn.item(j-1);
           if ismember('getTagName',methods(child))
               ctag=char(child.getTagName);
               data=extract_string_num(child);
               tmp=setfield(tmp,ctag,data);
           end    
       end 
       proc{i+1}=tmp;
    end
end
   
function data=extract_string_num(obj)
    eles=obj.getElementsByTagName('value');
    n=eles.getLength;
    if n>0
        data=[];
        ct=0;
        for i=1:n
            tmp=char(eles.item(i-1).getFirstChild.getData);
            if numel(tmp)>0
                ct=ct+1;
                data(ct)=str2num(tmp);
            end
        end
    else
        data=char(obj.getFirstChild.getData);
    end
end

function str=extract_string(obj,tag)
    tmp=obj.getElementsByTagName(tag).item(0);
    if tmp.hasChildNodes
        str=char(obj.getElementsByTagName(tag).item(0).getFirstChild.getData);
    else
        str='';
    end
end

function num=extract_num(obj,tag)
    num=str2num(obj.getElementsByTagName(tag).item(0).getFirstChild.getData);
end

function cel=extract_string_cell(obj,tag)
    obj1=obj.getElementsByTagName(tag).item(0);
    items=obj1.getElementsByTagName('item');
    cel={};
    for k=0:items.getLength-1
       ele=items.item(k);
       cel{k+1}=char(ele.getFirstChild.getData);    
    end
end

function comp=extract_composition(obj,tag)
    comp={};
    obj1=obj.getElementsByTagName(tag).item(0);
    items=obj1.getElementsByTagName('item');
    cel={};
    for k=0:items.getLength-1
       ele=items.item(k).getElementsByTagName('element').item(0);
       comp{k+1,1}=char(ele.getFirstChild.getData);   
       ap=items.item(k).getElementsByTagName('atomic_percent').item(0);
       comp{k+1,2}=str2num(ap.getFirstChild.getData);   
    end    

end

function data=data_init()
    data.metadata=struct();
    data.metadata.doi='';
    data.metadata.title='';
    data.metadata.source='';
    data.metadata.year=0;
    data.metadata.author={};
    data.metadata.institution={};
    data.metadata.country_region={};
    data.metadata.fund={};
    
    data.scidata=struct();
    ds=struct(); 
    ds.fatigue=struct();
    ds.materials=struct();
    ds.processing=struct();
    ds.testing=struct();
    ds.mech_prop=struct();        
    ds.fatigue.fat_data=[];
    ds.fatigue.fdata_type='';
    ds.fatigue.extract_method='';
    ds.materials.mat_type='';
    ds.materials.mat_name='';
    ds.materials.percent_type='';
    ds.materials.atomic_struct='';
    ds.materials.mat_name2='';
    %ds.materials.trade_name='';
    ds.materials.composition={};
    ds.processing.proc_para={};
    ds.processing.proc_seq=[];
    ds.processing.ingot_desc='';
    ds.processing.ingot_size='';
    ds.processing.surf_para={};
    ds.processing.surf_seq=[];
    ds.testing.fat_type='';
    ds.testing.fat_temp=[];
    ds.testing.fat_env='';
    ds.testing.fat_r=[];
    ds.testing.fat_machine='';
    ds.testing.fat_standard='';
    ds.testing.spec_desc='';
    ds.testing.spec_size=[];
    ds.testing.spec_kt=1;
    ds.testing.frequency=[];
    ds.testing.load_ctrl='';
    ds.testing.fail_crt='';    
    %ds.testing.load_direction=''; 
    ds.mech_prop.modulus=[];
    ds.mech_prop.yield_strength=[];
    ds.mech_prop.ultimate_strength=[];
    ds.mech_prop.elongation=[];
    ds.mech_prop.toughness=[];
    ds.mech_prop.kth=[];  
    
    data.scidata.datasets(1)=ds;
end