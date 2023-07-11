clear;
path='D:\Tsinghua\Project\Fatigue Data Framework\search data\wos\20220917\matlab_data\BMG_HEA\20230603_v1\';
file='FatigueData-CMA2022.mat';
load([path,file]);

% % weight definition
default_weight=1;
weight=weight_init(default_weight);
weight.materials.composition=3;
weight.materials.atomic_struct=2;
weight.processing.proc_para=2;
weight.processing.surf_para=2;

% % calculate rating score
art=fatiguedata_cma2022.articles;
na=numel(art);
for i=1:na
    ds=art(i).scidata.datasets;
    nd=numel(ds);
    for j=1:nd
        fatiguedata_cma2022.articles(i).scidata.datasets(j).score=cal_rating_score(fatiguedata_cma2022.articles(i).scidata.datasets(j),weight);
    end
end    

function score=cal_rating_score(ds,weight)
    tot=0;
    fill=0;
    
    [t,f]=fill_rate_field(ds.fatigue,weight.fatigue);
    tot=tot+t;
    fill=fill+f;
    
    [t,f]=fill_rate_field(ds.materials,weight.materials);
    tot=tot+t;
    fill=fill+f;    
   

    [t,f]=fill_rate_field(ds.processing,weight.processing);
    tot=tot+t;
    fill=fill+f;     
    
    [t,f]=fill_rate_field(ds.testing,weight.testing);
    tot=tot+t;
    fill=fill+f;   
    
    [t,f]=fill_rate_field(ds.mech_prop,weight.mech_prop);
    tot=tot+t;
    fill=fill+f;  

    score=fill/tot;
end

function [tot,fill]=fill_rate_field(field,weight)
    tot=0;
    fill=0;
    fn=fieldnames(field);
    for i=1:numel(fn)
        w=0;
        f=getfield(field,fn{i});
        if isfield(weight,fn{i})
            w=getfield(weight,fn{i});
        end
        tot=tot+w;        
        if ~isempty(f)
            fill=fill+w;
        end
    end
end

function w=weight_init(default)
    w.fatigue.fat_data=default;
    w.fatigue.fdata_type=default;
    w.fatigue.extract_method=default;
    w.materials.mat_type=default;
    w.materials.mat_name=default;
    w.materials.percent_type=default;
    w.materials.atomic_struct=default;
    w.materials.mat_name2=default;
    w.materials.composition=default;
    w.materials.glass_tran=default;
    w.materials.grain_size=default;
    w.materials.ratio_type=default;
    w.processing.proc_para=default;
    w.processing.proc_seq=default;
    w.processing.ingot_desc=default;
    w.processing.ingot_size=default;
    w.processing.surf_para=default;
    w.processing.surf_seq=default;
    w.testing.fat_type=default;
    w.testing.fat_temp=default;
    w.testing.fat_env=default;
    w.testing.fat_r=default;
    w.testing.fat_machine=default;
    w.testing.fat_standard=default;
    w.testing.spec_desc=default;
    w.testing.spec_size=default;
    w.testing.spec_kt=default;
    w.testing.ktconvert=default;
    w.testing.frequency=default;
    w.testing.load_ctrl=default;
    w.testing.fail_crt=default;   
    w.mech_prop.modulus=default;
    w.mech_prop.yield_strength=default;
    w.mech_prop.ultimate_strength=default;
    w.mech_prop.elongation=default;
    w.mech_prop.toughness=default;
    w.mech_prop.kth=default;    
end