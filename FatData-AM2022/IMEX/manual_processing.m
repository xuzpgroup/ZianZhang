
% % clear data series
% for id=6:20
%     savedata.imLib(id).data.colorpick=0;
%     for j=1:numel(savedata.imLib(id).data.series)
%         savedata.imLib(id).data.series(j).pdata=[];
%         savedata.imLib(id).data.series(j).auto=[];
%         savedata.imLib(id).data.series(j).runout=[];
%     end
% end

% % delete data series
% for id=1:numel(savedata.imLib)
%     %savedata.imLib(id).data.colorpick=0;
%     savedata.imLib(id).data.state='';
%     savedata.imLib(id).data.nseries=0;
%     savedata.imLib(id).data.series=struct(); 
%     savedata.imLib(id).legend.nitem=0;
%     savedata.imLib(id).legend.state='';
%     savedata.imLib(id).legend.item=struct();
%     savedata.imLib(id).data.exist=0;
%     savedata.imLib(id).legend.exist=0;   
% end

% % ---------------------------------------------
% % separate dataset into pieces
path='E:\Data\Literature Data\project data\dadn\';
filename='project_am3_processed';%'project_preprocess2'
outname='project_am3_processed';
suffix='.mat';
% % step=100;
% rng=[101,151,171,191,211,231;150,170,190,210,230,252];
rng=[41;60];

% % separate according to defined range
for i=1:size(rng,2)
    load([path,filename,'_',num2str(rng(1,i)),'-',num2str(rng(2,i)),suffix]);
    for j=1:numel(savedata.imLib)
        savedata.imLib(j).axis.xScale='log';
        savedata.imLib(j).axis.yScale='log';
        savedata.imLib(j).axis.xLabel.unit='MPa_m';
        savedata.imLib(j).axis.xLabel.data2='dK';
        savedata.imLib(j).axis.yLabel.unit='m/cycle';
        savedata.imLib(j).axis.yLabel.data2='da/dN';
    end
    %save([path,'project_am3_processed_',num2str(rng(1,i)),'-',num2str(rng(2,i)),suffix],'savedata')
    %save([path,outname,'_',num2str(rng(1,i)),'-',num2str(rng(2,i)),suffix],'savedata')
    clear savedata
end
