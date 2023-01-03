function varargout = imex(varargin)
% IMEX MATLAB code for imex.fig
%      IMEX, by itself, creates a new IMEX or raises the existing
%      singleton*.
%
%      H = IMEX returns the handle to a new IMEX or the handle to
%      the existing singleton*.
%
%      IMEX('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in IMEX.M with the given input arguments.
%
%      IMEX('Property','Value',...) creates a new IMEX or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before imex_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to imex_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help imex

% Last Modified by GUIDE v2.5 31-Dec-2022 00:18:12

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @imex_OpeningFcn, ...
                   'gui_OutputFcn',  @imex_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before imex is made visible.
function imex_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to imex (see VARARGIN)

handles=initialization(handles,'init');
% Choose default command line output for imex
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes imex wait for user response (see UIRESUME)
% uiwait(handles.figure1);
%im=imread('D:\Tsinghua\Project\Fatigue Data Framework\search data\AM fatigue\selected pic\01210.jpeg'); 
%imhandle=imshow(im);
%set(imhandle,'ButtonDownFcn',@ImageClickPos);
%handles.a=1;
%handles.b=2;

% --- Outputs from this function are returned to the command line.
function varargout = imex_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

% % Windows

% --- Executes on mouse motion over figure - except title and menu.
function figure1_WindowButtonMotionFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    pos_ax=handles.axes1.Position;
    pos_ms=get(hObject,'currentpoint');
    handles.mousePosition=pos_ms;
    if (pos_ms(1)>=pos_ax(1))&&(pos_ms(1)<=(pos_ax(1)+pos_ax(3)))&&(pos_ms(2)>=pos_ax(2))&&(pos_ms(2)<=(pos_ax(2)+pos_ax(4)))
        handles.inAxes=1;
    else
        handles.inAxes=0;
    end

    if handles.inAxes
        
        if handles.translate
            ax=handles.axes1;
            xrng=ax.XLim;
            yrng=ax.YLim;
            xlen=xrng(2)-xrng(1);
            ylen=yrng(2)-yrng(1);
            apos=ax.Position;   
            dx=handles.mousePosition-handles.mousePosition0;
            handles.axes1.XLim=handles.xlim1-dx(1)/apos(3)*xlen;
            handles.axes1.YLim=handles.ylim1+dx(2)/apos(4)*ylen;
        elseif handles.eraser_on
            mapos=handles.axes1.CurrentPoint(1,1:2);
            handles=plot_eraser(handles,mapos);
            if handles.erasing 
                handles=erase_data(handles,mapos);    
            end
        elseif handles.boxresize.on
            nc=handles.boxselect.current;
            cid=handles.boxresize.cornerid;
            mapos=handles.axes1.CurrentPoint(1,1:2);
            mapos=trimBox(mapos,handles);
            xyrng=handles.boxselect.xyrng(nc,:);
            if cid==1
                mapos0=[xyrng(2),xyrng(4)];
            elseif cid==2
                mapos0=[xyrng(2),xyrng(3)];
            elseif cid==3
                mapos0=[xyrng(1),xyrng(4)];
            elseif cid==4
                mapos0=[xyrng(1),xyrng(3)];
            end
            handles.boxselect.boxhandles{nc}.XData=[mapos0(1),mapos(1),mapos(1),mapos0(1),mapos0(1)];
            handles.boxselect.boxhandles{nc}.YData=[mapos0(2),mapos0(2),mapos(2),mapos(2),mapos0(2)];        
        elseif handles.boxselect.flag||(~isempty(strfind(handles.currentProperty,'series')))
            motionSensitive=0.005;
            if handles.boxselect.on
                ax=handles.axes1;    
                mapos=handles.axes1.CurrentPoint(1,1:2);
                mapos=trimBox(mapos,handles);
                mapos0=handles.boxselect.pos0;
                xdata=[mapos0(1),mapos(1),mapos(1),mapos0(1),mapos0(1)];
                ydata=[mapos0(2),mapos0(2),mapos(2),mapos(2),mapos0(2)];            
                handles.boxselect.tmphandle.XData=xdata;
                handles.boxselect.tmphandle.YData=ydata;
                xlen=max(xdata)-min(xdata);
                ylen=max(ydata)-min(ydata);
                xrng_ax=handles.axes1.XLim;
                yrng_ax=handles.axes1.YLim;
                xlen_ax=xrng_ax(2)-xrng_ax(1);
                ylen_ax=yrng_ax(2)-yrng_ax(1);
                if (xlen>=xlen_ax*motionSensitive)&&(ylen>=ylen_ax*motionSensitive) 
                    handles.boxselect.tmphandle.Color='k';
                else
                    handles.boxselect.tmphandle.Color='none';
                end
            end
        end
        if ~handles.boxselect.flag &&(isempty(strfind(handles.currentProperty,'preselect')))
            ax=handles.axes1;   
            mapos=ax.CurrentPoint(1,1:2);
            handles.axes2.XLim=[mapos(1)-handles.minLen*0.03,mapos(1)+handles.minLen*0.03];
            handles.axes2.YLim=[mapos(2)-handles.minLen*0.03,mapos(2)+handles.minLen*0.03];
            if isfield(handles,'ax2cross')
                handles.ax2cross(1).XData=[mapos(1)-handles.minLen*0.015,mapos(1)+handles.minLen*0.015];
                handles.ax2cross(1).YData=[mapos(2),mapos(2)];
                handles.ax2cross(2).XData=[mapos(1),mapos(1)];
                handles.ax2cross(2).YData=[mapos(2)-handles.minLen*0.015,mapos(2)+handles.minLen*0.015];
            end
        end
        event=detect_mouse_change(hObject,handles);
        if event.boxresize
            handles.boxresize.detect=1;
        else
            handles.boxresize.detect=0;
        end
        if event.detectData
            handles.detectData.detect=1;
            handles.detectData.id=event.dataid;
            if (~isempty(strfind(handles.currentProperty,'Anchor')))
                handles.anchorID=event.dataid;
            end
        else 
            if  ~handles.pickAnchor
               handles.anchorID=event.dataid;
            end            
            handles.detectData.detect=0;
        end
    end
    guidata(hObject, handles);


    
% --- Executes on mouse press over figure background, over a disabled or
% --- inactive control, or over an axes background.
function figure1_WindowButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)sa
    % % not active if the the mouse is out of the axes1
    if ~handles.inAxes
        handles.inAxes0=0;
        return;
    else
        handles.inAxes0=handles.inAxes;
    end
    if strcmp(hObject.SelectionType,'alt')
        handles.mousePosition0=handles.mousePosition;
        handles.translate=1;
        handles.xlim1=handles.axes1.XLim;
        handles.ylim1=handles.axes1.YLim;
    elseif strcmp(hObject.SelectionType,'normal') 
        if handles.detectData.detect
            handles.detectData.select=1;
        elseif handles.eraser_on
            handles.erasing=1;
            ax=handles.axes1;  
            mapos=ax.CurrentPoint(1,1:2);
            handles=erase_data(handles,mapos);
        elseif handles.boxresize.detect
            event=detect_mouse_change(hObject,handles);
            handles.boxresize.on=1;
            handles.boxselect.current=event.boxid;
            handles.boxresize.cornerid=event.cornerid;        
        elseif handles.pickcolor
            % empty
        elseif (handles.boxselect.flag)|| ...
                (~isempty(strfind(handles.currentProperty,'series')))|| ...
                (~isempty(strfind(handles.currentProperty,'Anchor')))
            handles.boxselect.tmphandle=nan;
            handles.boxselect.on=1;
            ax=handles.axes1;   
            mapos=ax.CurrentPoint(1,1:2);
            mapos=trimBox(mapos,handles);
            handles.boxselect.tmphandle=plot(ax,[mapos(1),mapos(1),mapos(1),mapos(1),mapos(1)], ...
                    [mapos(2),mapos(2),mapos(2),mapos(2),mapos(2)],'color','none');
            handles.boxselect.pos0=mapos;
        elseif  (~isempty(strfind(handles.currentProperty,'preselect')))
            handles=boxSelection(handles);
        end
    end
    guidata(hObject, handles);


% --- Executes on mouse press over figure background, over a disabled or
% --- inactive control, or over an axes background.
function figure1_WindowButtonUpFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    if ~handles.inAxes0
        return;
    else
        handles.inAxes0=0;
    end
    ci=handles.currentImg;
    if strcmp(hObject.SelectionType,'alt')
        handles.translate=0;
    elseif strcmp(hObject.SelectionType,'normal')
        motionSensitive=0.005;
        if  handles.eraser_on
            handles.erasing=0;
        elseif ~isempty(strfind(handles.currentProperty,'Anchor')) 
            if handles.anchorID==0
                handles.selection.nsub=0;
                handles.selection.subset=[];
                handles=select_axis_anchor_subset(handles,ci);
            else
                if handles.detectData.select
                    handles.selection.nsub=1;
                    handles.selection.subset=[handles.anchorID];
                    handles=select_axis_anchor_subset(handles,ci);
                    if handles.anchorID<=2                        
                        if handles.pickAnchor                                               
                            handles.data.imLib(ci).axis.xAnchor.pos(handles.anchorID,:)=handles.axes1.CurrentPoint(1,1:2);                      
                            handles=move_data_point(handles);
                        end
                        pos=handles.data.imLib(ci).axis.xAnchor.pos(handles.anchorID,:);
                    else
                        if handles.pickAnchor                                               
                            handles.data.imLib(ci).axis.yAnchor.pos(handles.anchorID-2,:)=handles.axes1.CurrentPoint(1,1:2);                      
                            handles=move_data_point(handles);
                        end
                        pos=handles.data.imLib(ci).axis.yAnchor.pos(handles.anchorID-2,:);
                    end
                    if isnan(pos(1))||isnan(pos(2))
                        pos=handles.axes1.CurrentPoint(1,1:2);       
                    end
                    handles.axes2.XLim=[pos(1)-handles.minLen*0.03,pos(1)+handles.minLen*0.03];
                    handles.axes2.YLim=[pos(2)-handles.minLen*0.03,pos(2)+handles.minLen*0.03];
                    if isfield(handles,'ax2cross')
                        handles.ax2cross(1).XData=[pos(1)-handles.minLen*0.015,pos(1)+handles.minLen*0.015];
                        handles.ax2cross(1).YData=[pos(2),pos(2)];
                        handles.ax2cross(2).XData=[pos(1),pos(1)];
                        handles.ax2cross(2).YData=[pos(2)-handles.minLen*0.015,pos(2)+handles.minLen*0.015];
                    end
                else
                    handles=update_anchor(handles);
                end
            end
        elseif handles.detectData.select
            handles.detectData.select=0;
            id=handles.detectData.id;
            handles.detectData.id=0;
            handles.selection.nsub=1;
            handles.selection.subset=[id];
            if ~isempty(strfind(handles.currentProperty,'series'))
                n=str2num(handles.currentProperty(8:end));
                handles=select_data_series_subset(handles,ci,n);               
            end
        elseif handles.boxresize.on
            handles.boxresize.on=0;
            handles.boxresize.cornerid=0; 
            handles=update_boxselect(handles);    
            handles=storeImageData(handles);  
        elseif handles.pickcolor
            pos=handles.axes1.CurrentPoint(1,1:2);
            pos=round(pos);
            if size(handles.rgb,3)==3 
                R=handles.rgb(pos(2),pos(1),1);
                G=handles.rgb(pos(2),pos(1),2);
                B=handles.rgb(pos(2),pos(1),3);
            else
                R=handles.rgb(pos(2),pos(1),1);
                G=handles.rgb(pos(2),pos(1),1);
                B=handles.rgb(pos(2),pos(1),1);                 
            end
            handles.Text_red.String=['R ',num2str(R)];
            handles.Text_green.String=['G ',num2str(G)];
            handles.Text_blue.String=['B ',num2str(B)];
            handles.currentColor(1,1,1)=R;
            handles.currentColor(1,1,2)=G;
            handles.currentColor(1,1,3)=B;
            imshow(handles.currentColor,'Parent',handles.axes3);
        elseif handles.boxselect.flag
            handles.boxselect.on=0;
            xdata=handles.boxselect.tmphandle.XData;
            ydata=handles.boxselect.tmphandle.YData;
            xlen=max(xdata)-min(xdata);
            ylen=max(ydata)-min(ydata);
            xrng_ax=handles.axes1.XLim;
            yrng_ax=handles.axes1.YLim;
            xlen_ax=xrng_ax(2)-xrng_ax(1);
            ylen_ax=yrng_ax(2)-yrng_ax(1);
            if (xlen>=xlen_ax*motionSensitive)&&(ylen>=ylen_ax*motionSensitive)
                handles.boxselect.n=handles.boxselect.n+1;
                handles.boxselect.current=handles.boxselect.n;
                nc=handles.boxselect.current;
                handles.boxselect.boxhandles{nc}=handles.boxselect.tmphandle;
                handles.boxselect.tmphandle=nan;
                handles=update_boxselect(handles);
            else
                delete(handles.boxselect.tmphandle);
                handles.boxselect.tmphandle=nan;
            end
            handles=storeImageData(handles);
        elseif (~isempty(strfind(handles.currentProperty,'series')))
            n=str2num(handles.currentProperty(8:end));
            handles.boxselect.on=0;
            xdata=handles.boxselect.tmphandle.XData;
            ydata=handles.boxselect.tmphandle.YData;
            xlen=max(xdata)-min(xdata);
            ylen=max(ydata)-min(ydata);
            xmin=min(xdata); xmax=max(xdata);
            ymin=min(ydata); ymax=max(ydata);
            xrng_ax=handles.axes1.XLim;
            yrng_ax=handles.axes1.YLim;
            xlen_ax=xrng_ax(2)-xrng_ax(1);
            ylen_ax=yrng_ax(2)-yrng_ax(1);
            if (xlen>=xlen_ax*motionSensitive)&&(ylen>=ylen_ax*motionSensitive)
                handles.boxselect.n=1;
                handles.boxselect.current=handles.boxselect.n;
                handles.boxselect.xyrng(1,:)=[xmin,xmax,ymin,ymax];
                delete(handles.boxselect.tmphandle);
                handles.boxselect.tmphandle=nan;
                handles=detect_boxselected_objects(handles);
                handles=select_data_series_subset(handles,ci,n);
            else
                if handles.inAxes
                    handles=add_data_point(handles,handles.boxselect.pos0);
                end
            end
            handles=storeImageData(handles);                       
        end
            
    end    
    guidata(hObject, handles);

    
% --- Executes on scroll wheel click while the figure is in focus.
function figure1_WindowScrollWheelFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.FIGURE)
%	VerticalScrollCount: signed integer indicating direction and number of clicks
%	VerticalScrollAmount: number of lines scrolled for each click
% handles    structure with handles and user data (see GUIDATA)
    if handles.inAxes
        scale=1.1;
        ax=handles.axes1;
        xrng=ax.XLim;
        yrng=ax.YLim;
        xlen=xrng(2)-xrng(1);
        ylen=yrng(2)-yrng(1);
        apos=ax.Position;
        mpos=handles.mousePosition;
        mapos=mouse_pos_ax(mpos,apos,xrng(1),yrng(2),xlen,ylen);
        ratio=[(mapos(1)-xrng(1))/xlen,(yrng(2)-mapos(2))/ylen];
        if eventdata.VerticalScrollCount==1
            xlen=xlen*scale;
            ylen=ylen*scale;
        elseif eventdata.VerticalScrollCount==-1
            xlen=xlen/scale;
            ylen=ylen/scale;
        end
        ax.XLim=[mapos(1)-xlen*ratio(1),mapos(1)+xlen*(1-ratio(1))];
        ax.YLim=[mapos(2)-ylen*(1-ratio(2)),mapos(2)+ylen*ratio(2)];
    end
    guidata(hObject, handles);    
    
% --- Executes on key press with focus on figure1 or any of its controls.
function figure1_WindowKeyPressFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.FIGURE)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
    ci=handles.currentImg;
    if strcmp(eventdata.Key,'control')
        handles=func_key_onoff(handles);
    end
    if handles.keyon
        %if strcmp(eventdata.Key,'control')
        %    handles.selection.continuous=~handles.selection.continuous;
        if strcmp(eventdata.Key,'delete')
            handles=func_delete_data(handles);
        elseif strcmp(eventdata.Key,'w') %strcmp(eventdata.Key,'uparrow')||
            handles.movdir='up';
            handles=move_data_point(handles);
        elseif strcmp(eventdata.Key,'s') %strcmp(eventdata.Key,'downarrow')||
            handles.movdir='down';
            handles=move_data_point(handles);
        elseif strcmp(eventdata.Key,'a') %strcmp(eventdata.Key,'leftarrow')||
            handles.movdir='left';
            handles=move_data_point(handles);
        elseif strcmp(eventdata.Key,'d') %strcmp(eventdata.Key,'rightarrow')||
            handles.movdir='right';
            handles=move_data_point(handles);
        elseif strcmp(eventdata.Key,'f')
            %handles=func_add_data_series(handles);
            handles=func_pick_anchor(handles);
        
        % % use for legend selection
%         elseif strcmp(eventdata.Key,'w')
%             handles=func_legend_select(handles);
%         elseif strcmp(eventdata.Key,'d')
%             handles=func_next_image(handles);
%         elseif strcmp(eventdata.Key,'a')
%             handles=func_previous_image(handles);

        % % use for correcting anchor
        elseif strcmp(eventdata.Key,'x')
            handles=func_next_image(handles);
        elseif strcmp(eventdata.Key,'z')
            handles=func_previous_image(handles);
        elseif strcmp(eventdata.Key,'c')
            if strcmp(handles.data.imLib(ci).axis.yScale,'log')
                handles.data.imLib(ci).axis.yScale='linear';
                handles.Table_detailProperty.Data{8,2}='linear';
            elseif strcmp(handles.data.imLib(ci).axis.yScale,'linear')
                handles.data.imLib(ci).axis.yScale='log';
                handles.Table_detailProperty.Data{8,2}='log';
            end
        elseif strcmp(eventdata.Key,'b')
            if strcmp(handles.data.imLib(ci).axis.xScale,'log')
                handles.data.imLib(ci).axis.xScale='linear';
                handles.Table_detailProperty.Data{5,2}='linear';
            elseif strcmp(handles.data.imLib(ci).axis.xScale,'linear')
                handles.data.imLib(ci).axis.xScale='log';
                handles.Table_detailProperty.Data{5,2}='log';
            end  
        % % S-N / E-N
%         elseif strcmp(eventdata.Key,'v')
%             if strcmp(handles.data.imLib(ci).axis.yLabel.data2,'amp')
%                 handles.data.imLib(ci).axis.yLabel.data2='max';
%                 handles.Table_detailProperty.Data{9,2}='max';
%             elseif strcmp(handles.data.imLib(ci).axis.yLabel.data2,'max')
%                 handles.data.imLib(ci).axis.yLabel.data2='range';
%                 handles.Table_detailProperty.Data{9,2}='range';
%             elseif strcmp(handles.data.imLib(ci).axis.yLabel.data2,'range')
%                 handles.data.imLib(ci).axis.yLabel.data2='amp';
%                 handles.Table_detailProperty.Data{9,2}='amp';                
%             end  
%         elseif strcmp(eventdata.Key,'n')
%             if strcmp(handles.data.imLib(ci).axis.xLabel.unit,'cycles')
%                 handles.data.imLib(ci).axis.xLabel.unit='reversals';
%                 handles.Table_detailProperty.Data{7,2}='reversals';
%             elseif strcmp(handles.data.imLib(ci).axis.xLabel.unit,'reversals')
%                 handles.data.imLib(ci).axis.xLabel.unit='cycles';
%                 handles.Table_detailProperty.Data{7,2}='cycles';
%             end  

        % dadn
        elseif strcmp(eventdata.Key,'v')
            if strcmp(handles.data.imLib(ci).axis.yLabel.unit,'m/cycle')
                handles.data.imLib(ci).axis.yLabel.unit='mm/cycle';
                handles.Table_detailProperty.Data{10,2}='mm/cycle';
            elseif strcmp(handles.data.imLib(ci).axis.yLabel.unit,'mm/cycle')
                handles.data.imLib(ci).axis.yLabel.unit='in/cycle';
                handles.Table_detailProperty.Data{10,2}='in/cycle';
            elseif strcmp(handles.data.imLib(ci).axis.yLabel.unit,'in/cycle')
                handles.data.imLib(ci).axis.yLabel.unit='m/cycle';
                handles.Table_detailProperty.Data{10,2}='m/cycle';                
            end  
        elseif strcmp(eventdata.Key,'n')
            if strcmp(handles.data.imLib(ci).axis.xLabel.unit,'MPa_m')
                handles.data.imLib(ci).axis.xLabel.unit='ksi_in';
                handles.Table_detailProperty.Data{7,2}='ksi_in';
            elseif strcmp(handles.data.imLib(ci).axis.xLabel.unit,'ksi_in')
                handles.data.imLib(ci).axis.xLabel.unit='MPa_m';
                handles.Table_detailProperty.Data{7,2}='MPa_m';
            end             
        elseif strcmp(eventdata.Key,'q')
            if handles.anchorID>0            
                handles.anchorID=mod(handles.anchorID,4)+1;
                handles.selection.nsub=1;
                handles.selection.subset=[handles.anchorID];
                handles=select_axis_anchor_subset(handles,ci);            
            end
        end
    end
    guidata(hObject,handles) 
    


% --- Executes on key release with focus on figure1 or any of its controls.
function figure1_WindowKeyReleaseFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.FIGURE)
%	Key: name of the key that was released, in lower case
%	Character: character interpretation of the key(s) that was released
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) released
% handles    structure with handles and user data (see GUIDATA)


function figure1_KeyPressFcn(hObject, eventdata, handles)

function figure1_KeyReleaseFcn(hObject, eventdata, handles)


% % Callback
% --- Executes during object creation, after setting all properties.
function axes2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to axes2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: place code in OpeningFcn to populate axes2
% --- Executes on button press in Button_next.
function Button_next_Callback(hObject, eventdata, handles)
% hObject    handle to Button_next (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_next_image(handles);
    guidata(hObject, handles);

% --- Executes on button press in Button_previous.
function Button_previous_Callback(hObject, eventdata, handles)
% hObject    handle to Button_previous (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_previous_image(handles);
    guidata(hObject, handles);


% --- Executes on button press in Button_resize.
function Button_resize_Callback(hObject, eventdata, handles)
% hObject    handle to Button_resize (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles.axes1.XLim=handles.xlim0;
    handles.axes1.YLim=handles.ylim0;
    guidata(hObject, handles);   


% --- Executes on button press in boxHL.
function boxHL_Callback(hObject, eventdata, handles)
% hObject    handle to boxHL (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of boxHL
    state=get(hObject,'Value');
    nbox=handles.boxselect.n;
    if nbox>0
        if state
            for i=1:nbox
                handles.boxselect.boxhandles{i}.Selected=1;
            end
        else
            for i=1:nbox
                handles.boxselect.boxhandles{i}.Selected=0;
            end
        end
    end
    guidata(hObject,handles)            

% --- Executes on button press in But_legendSelect.
function But_legendSelect_Callback(hObject, eventdata, handles)
% hObject    handle to But_legendSelect (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_legend_select(handles);
    guidata(hObject,handles)
    
% --- Executes during object creation, after setting all properties.
function But_detectAxis_CreateFcn(hObject, eventdata, handles)
% hObject    handle to But_detectAxis (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% --- Executes on button press in But_detectAxis.
function But_detectAxis_Callback(hObject, eventdata, handles)
% hObject    handle to But_detectAxis (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_detect_axis(handles);
    guidata(hObject,handles);

% --- Executes on button press in But_seperateObject.
function But_seperateObject_Callback(hObject, eventdata, handles)
% hObject    handle to But_seperateObject (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_seperate_object(handles);
    guidata(hObject,handles)
    
% --- Executes on button press in But_importImg.
function But_importImg_Callback(hObject, eventdata, handles)
% hObject    handle to But_importImg (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles.data.path = [uigetdir(),'\'];
    handles=initialization(handles,'import');
%     handles.data.imLib=[];
%     handles.data.filelist={};
%     tmp=dir(handles.data.path);
%     nImg=0;
%     imName={};
%     for i=3:numel(tmp)
%         if ~tmp(i).isdir
%             nImg=nImg+1;
%             len=numel(tmp(i).name);
%             for j=len:-1:1
%                 if strcmp(tmp(i).name(j),'.')
%                     break;
%                 end
%             end
%             handles.data.imLib(nImg).fullname=tmp(i).name;
%             handles.data.imLib(nImg).name=tmp(i).name(1:j-1);
%             handles.data.imLib(nImg).suffix=tmp(i).name(j:len);
%             imName{nImg}=tmp(i).name;
%             handles.data.filelist{nImg}=tmp(i).name;
%         end
%     end
%     handles.data.nImg=nImg;
%     handles.currentImg=1;
%     handles=updateFigure(handles);
%     handles=updateCounts(handles);
%     handles.ListImage.String=imName;
    guidata(hObject,handles)



% --- Executes on button press in But_delLegendBox.
function But_delLegendBox_Callback(hObject, eventdata, handles)
% hObject    handle to But_delLegendBox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_del_legend_box(handles);
    guidata(hObject,handles) 
        

% --- Executes on button press in But_segment.
function But_segment_Callback(hObject, eventdata, handles)
% hObject    handle to But_segment (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=segement_pic(handles);
    guidata(hObject,handles) 
    savedata=handles.data;
    save([handles.data.path,'project.mat'],'savedata');


% --- Executes on button press in But_saveProject.
function But_saveProject_Callback(hObject, eventdata, handles)
% hObject    handle to But_saveProject (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=storeImageData(handles);
    if isfield(handles,'data')&&isfield(handles.data,'file')
        [file,path] = uiputfile(handles.data.file);
    else
        [file,path] = uiputfile();
    end
    savedata=handles.data;
    save([path,file],'savedata');
    guidata(hObject,handles)

% --- Executes on button press in But_loadProject.
function But_loadProject_Callback(hObject, eventdata, handles)
% hObject    handle to But_loadProject (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    [file,path] = uigetfile();
    if ~isequal(file,0)
        load([path,file]);
        handles.data.path=path;
        handles.data.file=file;
        handles.data=savedata;
        handles=initialization(handles,'load');
%         handles.nImg=numel(handles.data.imLib);
%         handles.currentImg=1;
%         handles.colorChannel=1;  % 1:rgb; 2:grayscale; 3:black-white     
%         handles.inAxes=0;
%         handles.inAxes0=0;
%         handles.currentProperty='';
%         handles.currentTable='';
%         handles.detectData=struct();
%         handles.detectData.select=0;
%         handles.detectData.detect=0;
%         handles.detectData.id=0;
% 
%         handles.plot.sepobj.active=0; 
% 
%         handles.plot.selection=struct();
%         handles.plot.selection.hd=[];
% 
%         handles=updateFigure(handles);
%         handles=updateColorBut(handles);        
%         handles=updateCounts(handles);
%         handles.translate=0;
%         handles=boxselectInitialize(handles);
%         handles=boxSelectBut_initialize(handles);
%         handles=legendSelectBut_initialize(handles);
%         handles.Text_numBox.String=['nbox: ',num2str(handles.boxselect.n)];
%         handles.Text_name.String=[handles.data.imLib(handles.currentImg).name,handles.data.imLib(handles.currentImg).suffix];
%         handles.Edit_processRange.String=['1 - ',num2str(handles.nImg)];
%         handles.processRange=[1,handles.nImg];
% 
%         handles=display_file_table(handles);
%         handles=selectionInitialize(handles);
%         handles=setting_initialize(handles);
%         handles=datastruct_initialize(handles);
%         handles=data_page_initialization(handles);
        guidata(hObject,handles)
    end

% --- Executes on button press in But_analyseLegend.
function But_analyseLegend_Callback(hObject, eventdata, handles)
% hObject    handle to But_analyseLegend (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    handles=func_analyse_legend(handles);
    guidata(hObject,handles)

    
% --- Executes on button press in But_symbolRecognition.
function But_symbolRecognition_Callback(hObject, eventdata, handles)
% hObject    handle to But_symbolRecognition (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_symbol_recognition(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_colorRecognition.
function But_colorRecognition_Callback(hObject, eventdata, handles)
% hObject    handle to But_colorRecognition (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    handles=func_symbol_recognition_color(handles);
    guidata(hObject,handles)   

% --- Executes on button press in But_addPickedData.
function But_addPickedData_Callback(hObject, eventdata, handles)
% hObject    handle to But_addPickedData (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_add_picked_data(handles);
    guidata(hObject,handles)   

% --- Executes on button press in But_replacePickedData.
function But_replacePickedData_Callback(hObject, eventdata, handles)
% hObject    handle to But_replacePickedData (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_replace_picked_data(handles);
    guidata(hObject,handles)   
    
% --- Executes on button press in But_addDataSeries.
function But_addDataSeries_Callback(hObject, eventdata, handles)
% hObject    handle to But_addDataSeries (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_add_data_series(handles);
    guidata(hObject,handles)

    
% --- Executes on button press in But_deleteData.
function But_deleteData_Callback(hObject, eventdata, handles)
% hObject    handle to But_deleteData (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_delete_data(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_autoAxis.
function But_autoAxis_Callback(hObject, eventdata, handles)
% hObject    handle to But_autoAxis (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    handles=func_auto_axis(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_keyonoff.
function But_keyonoff_Callback(hObject, eventdata, handles)
% hObject    handle to But_keyonoff (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_key_onoff(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_pickColor.
function But_pickColor_Callback(hObject, eventdata, handles)
% hObject    handle to But_pickColor (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    handles=func_pick_color(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_selectColor.
function But_selectColor_Callback(hObject, eventdata, handles)
% hObject    handle to But_selectColor (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_select_color(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_addColor.
function But_addColor_Callback(hObject, eventdata, handles)
% hObject    handle to But_addColor (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    handles=func_add_color(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_resetColor.
function But_resetColor_Callback(hObject, eventdata, handles)
% hObject    handle to But_resetColor (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_reset_color(handles);
    guidata(hObject,handles)    

    
% --- Executes on button press in But_eraser.
function But_eraser_Callback(hObject, eventdata, handles)
% hObject    handle to But_eraser (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_eraser_on(handles);
    guidata(hObject,handles)    

    
% --- Executes on button press in But_shapeOrColorPick.
function But_shapeOrColorPick_Callback(hObject, eventdata, handles)
% hObject    handle to But_shapeOrColorPick (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    handles=func_switch_shape_color_pick(handles);
    guidata(hObject,handles)    
    
% --- Executes on selection change in ListImage.
function ListImage_Callback(hObject, eventdata, handles)
% hObject    handle to ListImage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns ListImage contents as cell array
%        contents{get(hObject,'Value')} returns selected item from ListImage
    contents = cellstr(get(hObject,'String'));
    fileName=contents{get(hObject,'Value')};
    disp(fileName)
    for i=1:handles.data.nImg
        if strcmp(fileName,handles.data.imLib(i).fullname)
            handles.currentImg=i;
            handles=updateFigure(handles);
            handles=updateCounts(handles);
            break;
        end
    end
    guidata(hObject,handles)
    
% --- Executes during object creation, after setting all properties.
function ListImage_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ListImage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: listbox controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double

    string=get(hObject,'String');
    id=find(string=='/');
    if ~isempty(id)
        tmp=str2double(string(1:id(1)-1));
    else
        tmp=str2double(string);
    end
    if ~isnan(tmp)
        int0=round(tmp);
        if (int0<=handles.data.nImg)&&(int0>=1)
            handles.currentImg=tmp;
            handles=updateFigure(handles);   
            ct=handles.currentTable;
            handles.currentProperty='';
            if strcmp(ct,'file')
                handles=display_file_table(handles);
            elseif strcmp(ct,'setting')
                handles=display_setting_table(handles);
            elseif strcmp(ct,'data')
                handles=display_data_table(handles);
            end
            handles=detail_page_initialization(handles);            
        end
    end
    handles=updateCounts(handles);
    guidata(hObject, handles);      

% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end    
  
function Edit_processRange_Callback(hObject, eventdata, handles)
% hObject    handle to Edit_processRange (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Edit_processRange as text
%        str2double(get(hObject,'String')) returns contents of Edit_processRange as a double
    tmp=get(hObject,'String');
    c=strsplit(tmp,'-');
    if numel(c)==2
        r1=str2num(c{1});
        r2=str2num(c{2});
        if numel(r1)==1 && numel(r2)==1
            if r1<=r2
                handles.processRange=[r1,r2];
            end
        end
    end
    hObject.String=[num2str(handles.processRange(1)),' - ',num2str(handles.processRange(2))];
    guidata(hObject,handles)
    

% --- Executes during object creation, after setting all properties.
function Edit_processRange_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Edit_processRange (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Edit_eraseSize_Callback(hObject, eventdata, handles)
% hObject    handle to Edit_eraseSize (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Edit_eraseSize as text
%        str2double(get(hObject,'String')) returns contents of Edit_eraseSize as a double
    tmp=get(hObject,'String');
    s=str2num(tmp);
    if ~isempty(s)
        handles.eraser_size=s;
        hObject.String=num2str(s);
    end
    guidata(hObject,handles)

% --- Executes during object creation, after setting all properties.
function Edit_eraseSize_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Edit_eraseSize (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function Edit_colorTolerance_Callback(hObject, eventdata, handles)
% hObject    handle to Edit_colorTolerance (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Edit_colorTolerance as text
%        str2double(get(hObject,'String')) returns contents of Edit_colorTolerance as a double
    tmp=get(hObject,'String');
    tol=str2num(tmp);
    if ~isempty(tol)
        handles.color_tolerance=tol;
        hObject.String=num2str(tol);
    end
    guidata(hObject,handles)

% --- Executes during object creation, after setting all properties.
function Edit_colorTolerance_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Edit_colorTolerance (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes during object creation, after setting all properties.
function Table_msg_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Table_msg (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called 
    pos=hObject.Position;
    hObject.Data={'Welcome'};
    hObject.ColumnWidth={pos(3)-20};

% --- Executes during object creation, after setting all properties.
function Table_property_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Table_property (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
    pos=hObject.Position;
    hObject.ColumnName={'Name'};
    hObject.Data={};
    hObejct.ColumnEditable=[0];
    hObject.ColumnWidth={pos(3)-18};
    
% --- Executes when selected cell(s) is changed in Table_property.
function Table_property_CellSelectionCallback(hObject, eventdata, handles)
% hObject    handle to Table_property (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.TABLE_PROPERTY)
%	Indices: row and column indices of the cell(s) currently selecteds
% handles    structure with handles and user data (see GUIDATA)
    handles=clear_axes3(handles);
    handles=updateImage2(handles);
    if strcmp(handles.currentTable,'file')
        id=eventdata.Indices;
        if ~isempty(id)             % if selected in setting or data, the function is called when switch back to file and return empty id. 
            fileName=hObject.Data{id(1,1),id(1,2)};
            for i=1:handles.data.nImg
                if strcmp(fileName,handles.data.imLib(i).fullname)
                    handles.currentImg=i;
                    handles=updateFigure(handles);
                    handles=updateCounts(handles);
                    break;
                end
            end
        end
    elseif strcmp(handles.currentTable,'data')
        id=eventdata.Indices;
        handles=data_page_initialization(handles);
        if ~isempty(id)
            item=hObject.Data{id(1,1),1};
            tmp=strsplit(item);
            handles=display_data_detail(handles,tmp{end});
            handles=show_item_box(handles,tmp{end});
        end
    end
    guidata(hObject,handles)
    
% --- Executes when entered data in editable cell(s) in Table_property.
function Table_property_CellEditCallback(hObject, eventdata, handles)
% hObject    handle to Table_property (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.TABLE)
%	Indices: row and column indices of the cell(s) edited
%	PreviousData: previous data for the cell(s) edited
%	EditData: string(s) entered by the user
%	NewData: EditData or its converted form set on the Data property. Empty if Data was not changed
%	Error: error string when failed to convert EditData to appropriate value for Data
% handles    structure with handles and user data (see GUIDATA)
    ct=handles.currentTable;
    stat=0;
    if strcmp(ct,'setting')
        id=eventdata.Indices;
        item=hObject.Data{id(1),1};
        num=str2num(eventdata.EditData);
        n=numel(num);
        if n==1
            [handles,stat]=updateSetting(handles,item,num);
        end
        if stat
            handles=updateDataAfterSetting(handles,item);
            handles=delete_plot_sepobj(handles);
        else
            hObject.Data{id(1),2}=eventdata.PreviousData;
            handles=addMsg(handles,'ERROR: property value. <bw_thre>: [0,1]');
        end
    end
    guidata(hObject,handles)

    
% --- Executes during object creation, after setting all properties.
function Table_detailProperty_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Table_detailProperty (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
    pos=hObject.Position;
    hObject.ColumnName={'term','value'};
    hObject.RowName={};
    hObject.Data={};
    hObject.ColumnEditable=logical([0,1]);
    hObject.ColumnWidth={'auto','auto'};    

    
% --- Executes when selected cell(s) is changed in Table_property.
function Table_detailProperty_CellSelectionCallback(hObject, eventdata, handles)
% hObject    handle to Table_property (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.TABLE_PROPERTY)
%	Indices: row and column indices of the cell(s) currently selecteds
% handles    structure with handles and user data (see GUIDATA)
    
    ci=handles.currentImg;
    if strcmp(handles.currentTable,'data')
        id=eventdata.Indices;
        if ~isempty(id)
            item=hObject.Data{id(1,1),1};
            tmp=strsplit(item);
            id2=str2num(tmp{end});
            n=handles.selection.n;
            if strcmp(handles.currentProperty,'item')
                handles.Text_selectedObject.String=['Legend item ',tmp{end}];
                for i=1:n
                    if (i==id2*2)||(i==id2*2-1)
                        handles.plot.selection.hd(i).Color='b';
                    else
                        handles.plot.selection.hd(i).Color='k';
                    end
                end
                symbox=handles.data.imLib(ci).legend.item(id2).box{1};
                handles=clear_axes3(handles);
                imshow(handles.rgb(symbox(3):symbox(4),symbox(1):symbox(2),:),'Parent',handles.axes3);
            elseif strcmp(handles.currentProperty,'preselect')
                handles.Text_selectedObject.String=['Legend preselect ',tmp{end}];
                n=handles.boxselect.n;
                for i=1:n
                    if i==id2
                        handles.boxselect.boxhandles{i}.Selected='on';
                    else
                        handles.boxselect.boxhandles{i}.Selected='off';
                    end
                end
            elseif  ~isempty(strfind(handles.currentProperty,'series'))
                n=str2num(handles.currentProperty(8:end));
                handles.selection.subset=[id2];
                handles.selection.nsub=1;
                handles=select_data_series_subset(handles,ci,n);
            elseif  ~isempty(strfind(handles.currentProperty,'Anchor'))
                if id(1)==3 && id(2)==2
                    handles.selection.subset=[1];
                    handles.selection.nsub=1;
                    handles.anchorID=1;
                elseif id(1)==3 && id(2)==3
                    handles.selection.subset=[2];
                    handles.selection.nsub=1;
                    handles.anchorID=2;
                elseif id(1)==4 && id(2)==2
                    handles.selection.subset=[3];
                    handles.selection.nsub=1; 
                    handles.anchorID=3;
                elseif id(1)==4 && id(2)==3
                    handles.selection.subset=[4];
                    handles.selection.nsub=1;  
                    handles.anchorID=4;
                else
                    handles.selection.subset=[];
                    handles.selection.nsub=0;                     
                    handles.anchorID=0;
                end
                handles=select_axis_anchor_subset(handles,ci);
            else                
                for i=1:n
                    if i==id2
                        handles.plot.selection.hd(i).Color='b';
                    else
                        handles.plot.selection.hd(i).Color='k';
                    end
                end
            end
        end
    end
    guidata(hObject,handles)
    
% --- Executes when entered data in editable cell(s) in Table_property.
function Table_detailProperty_CellEditCallback(hObject, eventdata, handles)
% hObject    handle to Table_property (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.CONTROL.TABLE)
%	Indices: row and column indices of the cell(s) edited
%	PreviousData: previous data for the cell(s) edited
%	EditData: string(s) entered by the user
%	NewData: EditData or its converted form set on the Data property. Empty if Data was not changed
%	Error: error string when failed to convert EditData to appropriate value for Data
% handles    structure with handles and user data (see GUIDATA)
    ct=handles.currentTable;
    ci=handles.currentImg;
    stat=0;
    if strcmp(ct,'data')
        cp=handles.currentProperty;
        id=eventdata.Indices;
        if ~isempty(strfind(cp,'Anchor'))
            mod=0;
            if (id(1)==1)&&(id(2)>=2)&&(id(2)<=3)
                num=str2num(eventdata.EditData);
                if numel(num)==1
                    mod=1;
                    hObject.Data{id(1),id(2)}=num2str(num,'%3.2e');
                    if id(2)==2
                        handles.data.imLib(ci).axis.xAnchor.data(1)=num;
                    elseif id(2)==3
                        handles.data.imLib(ci).axis.xAnchor.data(2)=num;
                    end
                end
            elseif (id(1)==2)&&(id(2)>=2)&&(id(2)<=3)
                num=str2num(eventdata.EditData);
                if numel(num)==1
                    mod=1;
                    hObject.Data{id(1),id(2)}=num2str(num,'%3.2e');
                    if id(2)==2
                        handles.data.imLib(ci).axis.yAnchor.data(1)=num;
                    elseif id(2)==3
                        handles.data.imLib(ci).axis.yAnchor.data(2)=num;
                    end
                end                
            elseif (id(2)==2)&&((id(1)==5)||(id(1)==8))
                if isequal(eventdata.EditData,'log') || isequal(eventdata.EditData,'linear')
                    mod=1;
                    hObject.Data{id(1),id(2)}=eventdata.EditData;
                elseif isequal(eventdata.EditData,1)
                    mod=1;
                    hObject.Data{id(1),id(2)}='log';
                elseif isequal(eventdata.EditData,2)
                    mod=1;
                    hObject.Data{id(1),id(2)}='linear';
                end  
                if id(1)==5
                    handles.data.imLib(ci).axis.xScale=hObject.Data{id(1),id(2)};
                elseif id(1)==8
                    handles.data.imLib(ci).axis.yScale=hObject.Data{id(1),id(2)};
                end                
            elseif (id(2)==2)&&((id(1)==6)||(id(1)==7)||(id(1)==9)||(id(1)==10))
                mod=1;
                hObject.Data{id(1),id(2)}=eventdata.EditData;
                if id(1)==6
                    handles.data.imLib(ci).axis.xLabel.data2=hObject.Data{id(1),id(2)};
                elseif id(1)==7
                    handles.data.imLib(ci).axis.xLabel.unit=hObject.Data{id(1),id(2)};
                elseif id(1)==9
                    handles.data.imLib(ci).axis.yLabel.data2=hObject.Data{id(1),id(2)};
                elseif id(1)==10
                    handles.data.imLib(ci).axis.yLabel.unit=hObject.Data{id(1),id(2)};
                end
            end
                
            if ~mod
                hObject.Data{id(1),id(2)}=eventdata.PreviousData;
            end        
        elseif id(2)==2
            item=hObject.Data{id(1),1};
            if strcmp(item(1:4),'data')||strcmp(item(1:4),'text')
                if strcmp(cp,'xTicks')||strcmp(cp,'yTicks')
                    num=str2num(eventdata.EditData);
                    n=numel(num);
                    if n==1
                        hObject.Data{id(1),2}=num;
                    else
                        hObject.Data{id(1),2}=eventdata.PreviousData;
                        handles=addMsg(handles,'ERROR: illegal value.');
                    end
                elseif  strcmp(cp,'xLabel')||strcmp(cp,'yLabel')
                    hObject.Data{id(1),2}=eventdata.EditData;
                elseif strcmp(cp,'item')
                    hObject.Data{id(1),2}=eventdata.EditData;
                    handles.data.imLib(ci).legend.item(id(1)).text=eventdata.EditData;
                end
            else
                hObject.Data{id(1),id(2)}=eventdata.PreviousData;
            end
        elseif (id(2)==4)&&(~isempty(strfind(cp,'series')))
            num=str2num(eventdata.EditData);
            n=numel(num);
            ns=str2num(handles.currentProperty(8:end));
            if n==1
                if ~isfield(handles.data.imLib(ci).data.series(ns),'runout')
                    handles.data.imLib(ci).data.series(ns).runout=zeros(1,size(handles.data.imLib(ci).data.series(ns),1));
                end
                if num>0
                    hObject.Data{id(1),id(2)}=1;
                    handles.data.imLib(ci).data.series(ns).runout(id(1))=1;
                else
                    hObject.Data{id(1),id(2)}=0;
                    handles.data.imLib(ci).data.series(ns).runout(id(1))=0;
                end
            end
        else
            hObject.Data{id(1),id(2)}=eventdata.PreviousData;
        end
    end
    guidata(hObject,handles)
    
% --- Executes on button press in But_dispFile.
function But_dispFile_Callback(hObject, eventdata, handles)
% hObject    handle to But_dispFile (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    handles=display_file_table(handles);
    guidata(hObject,handles)
    
% --- Executes on button press in But_dispSetting.
function But_dispSetting_Callback(hObject, eventdata, handles)
% hObject    handle to But_dispSetting (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=display_setting_table(handles);
    guidata(hObject,handles)
    

% --- Executes on button press in But_dispData.
function But_dispData_Callback(hObject, eventdata, handles)
% hObject    handle to But_dispData (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=display_data_table(handles);
    guidata(hObject,handles)

    
% --- Executes on button press in But_autorun.
function But_autorun_Callback(hObject, eventdata, handles)
% hObject    handle to But_autorun (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_autorun(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_autorun2.
function But_autorun2_Callback(hObject, eventdata, handles)
% hObject    handle to But_autorun2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    handles=func_autorun2(handles);
    guidata(hObject,handles)
    
% --- Executes on button press in But_pickAnchor.
function But_pickAnchor_Callback(hObject, eventdata, handles)
% hObject    handle to But_pickAnchor (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_pick_anchor(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_clearData.
function But_clearData_Callback(hObject, eventdata, handles)
% hObject    handle to But_clearData (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles=func_clear_data_seires(handles);
    guidata(hObject,handles)

% --- Executes on button press in But_deleteDataSeries.
function But_deleteDataSeries_Callback(hObject, eventdata, handles)
% hObject    handle to But_deleteDataSeries (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)    
    handles=func_delete_data_seires(handles);
    guidata(hObject,handles)
    
    
% --- Executes on button press in RadBut_rgb.
function RadBut_rgb_Callback(hObject, eventdata, handles)
% hObject    handle to RadBut_rgb (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Hint: get(hObject,'Value') returns toggle state of RadBut_rgb
    if handles.colorChannel~=1
        handles.colorChannel=1;
        handles=updateColorBut(handles);
        guidata(hObject,handles)
    end
    
% --- Executes on button press in RadBut_gray.
function RadBut_gray_Callback(hObject, eventdata, handles)
% hObject    handle to RadBut_gray (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of RadBut_gray
    if handles.colorChannel~=2
        handles.colorChannel=2;
        handles=updateColorBut(handles);
        guidata(hObject,handles)
    end
    
% --- Executes on button press in RadBut_bw.
function RadBut_bw_Callback(hObject, eventdata, handles)
% hObject    handle to RadBut_bw (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of RadBut_bw
    if handles.colorChannel~=3
        handles.colorChannel=3;
        handles=updateColorBut(handles);
        guidata(hObject,handles)    
    end
    
% --- Executes on button press in CBox_axis.
function CBox_axis_Callback(hObject, eventdata, handles)
% hObject    handle to CBox_axis (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of CBox_axis


% --- Executes on button press in CBox_legend.
function CBox_legend_Callback(hObject, eventdata, handles)
% hObject    handle to CBox_legend (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of CBox_legend


% --- Executes on button press in CBox_data.
function CBox_data_Callback(hObject, eventdata, handles)
% hObject    handle to CBox_data (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of CBox_data


% --- Executes on button press in CBox_sepobj.
function CBox_sepobj_Callback(hObject, eventdata, handles)
% hObject    handle to CBox_sepobj (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of CBox_sepobj
    handles.plot.sepobj.active=get(hObject,'Value');
    handles=updatePlot_sepobj(handles);
    guidata(hObject,handles)


% % Initialization

function handles=initialization(handles,type)
    if strcmp(type,'init')
        handles.data.path='';% E:\Data\Literature Data\test dataset\  'E:\Data\Literature Data\AM fatigue 3\figure\EN\'; %'D:\Tsinghua\Project\Fatigue Data Framework\search data\AM fatigue\selected pic\';%;
    end
    fig=handles.figure1;
    fig.Units='pixels';
    ax=handles.axes1;
    ax.Units='pixels';
    ax.FontSize=10;
    ax.FontName='Arial';
    ax2=handles.axes2;
    ax2.XColor=[1,1,1];
    ax2.YColor=[1,1,1];
    ax2.XTick=[];
    ax2.YTick=[];
    handles=clear_axes3(handles);
    imshow([1],'Parent',handles.axes1);
    if strcmp(type,'import')||strcmp(type,'init')
        handles.data.imLib=[];
        handles.data.filelist={};
        handles.data.plot=struct([]);
        handles.imHeight=1;
        handles.imWidth=1;
        handles.minLen=1;
        handles.pickAnchor=0;
        tmp=dir(handles.data.path);
        nImg=0;
        for i=3:numel(tmp)
            if ~tmp(i).isdir
                len=numel(tmp(i).name);
                for j=len:-1:1
                    if strcmp(tmp(i).name(j),'.')
                        break;
                    end
                end
                suffix=tmp(i).name(j:len);
                if strcmp(suffix,'.png') || strcmp(suffix,'.jpeg') || strcmp(suffix,'.jpg') || strcmp(suffix,'.bmp')
                    nImg=nImg+1;
                    handles.data.imLib(nImg).fullname=tmp(i).name;
                    handles.data.imLib(nImg).name=tmp(i).name(1:j-1);
                    handles.data.imLib(nImg).suffix=suffix;
                    handles.data.imLib(nImg).path=handles.data.path;
                    handles.data.filelist{nImg,1}=tmp(i).name;          
                end
            end
        end
        handles.data.nImg=nImg;
        handles=imLib_var_init(handles);
    end
    
    
    
    handles.currentImg=1;
    handles.colorChannel=1;  % 1:rgb; 2:grayscale; 3:black-white     
    handles.inAxes=0;
    handles.inAxes0=0;
    
    handles.currentProperty='';
    handles.currentTable='';
    handles.detectData=struct();
    handles.detectData.select=0;
    handles.detectData.detect=0;
    handles.detectData.id=0;
    
    handles.plot.sepobj.active=0; 
    
    handles.plot.selection=struct();
    handles.plot.selection.hd=[];
    
    handles=updateFigure(handles);
    handles=updateColorBut(handles);        
    handles=updateCounts(handles);
    handles.translate=0;
    handles=boxselectInitialize(handles);
    handles=boxSelectBut_initialize(handles);
    handles=legendSelectBut_initialize(handles);
    handles.Text_numBox.String=['nbox: ',num2str(handles.boxselect.n)];
    handles=eraser_initialize(handles);
    if handles.data.nImg>0
        handles.Text_name.String=[handles.data.imLib(handles.currentImg).name,handles.data.imLib(handles.currentImg).suffix];
        handles.Edit_processRange.String=['1 - ',num2str(handles.data.nImg)];
        handles.processRange=[1,handles.data.nImg];
        handles=display_file_table(handles);
        handles=selectionInitialize(handles);
        handles=setting_initialize(handles);
        handles=datastruct_initialize(handles);
        handles=data_page_initialization(handles);        
    else
        handles.Text_name.String='';
        handles.Edit_processRange.String='';
        handles.processRange=[];
    end
    handles.Text_red.String=['R '];
    handles.Text_green.String=['G '];
    handles.Text_blue.String=['B '];    
    
    handles.color_tolerance=30;
    handles.Edit_colorTolerance.String=num2str(handles.color_tolerance);
    handles.pickcolor=0;
    handles.currentColor=uint8([]);
    handles.pixelRecord=[];
    
    handles.keyon=0;    % will be switch on in the func_key_onoff()
    handles=func_key_onoff(handles);
    
function handles=setting_initialize(handles)
    handles.setting.bw_thre=0.8;
    handles.setting.thre_AxisPercent=0.8;
    handles.setting.thre_charscale=1.5;   % 1
    handles.setting=orderfields(handles.setting);
    fn=fieldnames(handles.setting);
    handles.data.settinglist={};
    n=numel(fn);
    for i=1:n
        handles.data.settinglist{i,1}=fn{i};
        handles.data.settinglist{i,2}=getfield(handles.setting,fn{i});
    end

    
function handles=datastruct_initialize(handles)
    
    datalist= ...
        {'Seperated objects'; ...
         'Axis'; ...         
         '  |-- xLabel'; ...
         '  |-- xAnchor'; ...
         '  |-- xTicks'; ...
         '  |-- xScale'; ...
         '  |-- yLabel'; ...
         '  |-- yAnchor'; ...
         '  |-- yTicks'; ...
         '  |-- yScale'; ...
         'Legend'; ...  
         '  |-- preselect';
         '  |-- item'; ...
         'Data';};
     n=numel(datalist);
     ci=handles.currentImg;
     for i=1:handles.data.imLib(ci).data.nseries
         datalist{i+n}=['  |-- series_',num2str(i)];
     end
     handles.data.datalist=datalist;
     for i=1:size(handles.data.datalist,1)
         handles.data.datalist{i,2}=0;
     end
     
function handles=boxSelectBut_initialize(handles)
% hObject    handle to But_legendSelect (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles.boxselect.flag=0;

    
function handles=legendSelectBut_initialize(handles)
% hObject    handle to But_legendSelect (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    handles.legendselect=0;
    handles.But_legendSelect.BackgroundColor=[0.94,0.94,0.94];
    %handles.But_legendSelect.BackgroundColor=[0.7,0.7,1.0];
    
 function handles=boxselectInitialize(handles)
    if isfield(handles,'boxselect') 
        for i=1:numel(handles.boxselect.boxhandles)
            delete(handles.boxselect.boxhandles{i});
        end
    end
    handles.boxselect.flag=0;
    handles.boxselect.on=0;
    handles.boxselect.n=0;
    handles.boxselect.current=0;
    handles.boxselect.boxhandles={};
    handles.boxselect.xyrng=[];
    handles.boxselect.rcrng=[];
    handles.boxresize.detect=0;
    handles.boxresize.on=0;         
    
function handles=selectionInitialize(handles)
    handles.selection.type='';
    handles.selection.continuous=0;
    handles.selection.n=0;
    handles.selection.id=[];
    handles.selection.nsub=0;
    handles.selection.subset=[];
    
function handles=data_page_initialization(handles)
    handles=axis_property_initialization(handles);
    handles=legend_property_initialization(handles);
    handles=data_property_initialization(handles);
    
function handles=axis_property_initialization(handles)
    
function handles=legend_property_initialization(handles)
    handles.legendselect=0;
    handle.boxselect.flag=0;
    handles.add_data_series=0;
    
function handles=data_property_initialization(handles) 

    
function handles=detail_page_initialization(handles)
    pos=handles.Table_detailProperty.Position;
    handles.Table_detailProperty.ColumnName={'term','value'};
    handles.Table_detailProperty.RowName={};
    handles.Table_detailProperty.Data={};
    handles.Table_detailProperty.ColumnEditable=logical([0,1]);
    handles.Table_detailProperty.ColumnWidth={'auto','auto'}; 
    
% % Functions    
    
function handles=updateFigure(handles)
    % % clear up
    cla(handles.axes1);
    cla(handles.axes2);
    handles.rgb=[];
    handles.gray=[];
    handles.bw=[];   
    handles.currentColor=uint8([]);
    handles.axes1.NextPlot='replace';
    handles.plot.sepobj.hd=[];
    handles.imhandle=struct([]);
    handles.pixelRecord=[];
    if handles.data.nImg==0
        return;
    end
    if isfield(handles.data.imLib(handles.currentImg),'path')
        im=imread([handles.data.imLib(handles.currentImg).path,handles.data.imLib(handles.currentImg).name,handles.data.imLib(handles.currentImg).suffix]); 
    else
        im=imread([handles.data.path,handles.data.imLib(handles.currentImg).name,handles.data.imLib(handles.currentImg).suffix]); 
    end
    dim3=size(im,3);
    if dim3==3
        handles.rgb=im;
    elseif dim3==1
        handles.rgb=im;
        handles.gray=im;
    end
    handles.rgb0=handles.rgb;
    handles.imHeight=size(im,1);
    handles.imWidth=size(im,2);    
    handles=updateImage(handles);
    handles=updateImage2(handles);
    imshow(uint8(zeros(1,1,3)+255),'Parent',handles.axes3);
    handles.minLen=min(handles.imHeight,handles.imWidth);
    handles.movdir='';
    handles.anchorID=0;
    handles.pickAnchor=0;
    handles.movstep=handles.minLen*0.001;
    xdata=handles.imhandle.XData;
    ydata=handles.imhandle.YData;
    xlen=xdata(2)-xdata(1);
    ylen=ydata(2)-ydata(1);
    if xlen>ylen
        delta=xlen-ylen;
        handles.axes1.YLim=[ydata(1)-delta/2,ydata(2)+delta/2];
    else
        delta=ylen-xlen;
        handles.axes1.XLim=[xdata(1)-delta/2,xdata(2)+delta/2];
    end
    handles.axes1.NextPlot='add';
    handles.axes1.DataAspectRatioMode='manual';
    handles.axes1.DataAspectRatio=[1,1,1];
    handles.xlim0=handles.axes1.XLim;
    handles.ylim0=handles.axes1.YLim;
    handles.Text_name.String=[handles.data.imLib(handles.currentImg).name,handles.data.imLib(handles.currentImg).suffix];
    
    handles=updatePlot_sepobj(handles);
    
    %handles.imhandle.Clipping='off';
    %ax=get(handles.imhandle,'parent');
    %ax.Visible='on';
    %ax.Clipping='off';

function handles=updateImage(handles)
    if handles.data.nImg==0
        return;
    end
    if numel(handles.imhandle)>0
        delete(handles.imhandle);
    end
    if handles.colorChannel==1
        handles.imhandle=imshow(handles.rgb,'Parent',handles.axes1);      
    elseif handles.colorChannel==2
        if isempty(handles.gray)
            handles.gray=rgb2gray(handles.rgb);
        end
        handles.imhandle=imshow(handles.gray,'Parent',handles.axes1);
    elseif handles.colorChannel==3
        if isempty(handles.gray)
            handles.gray=rgb2gray(handles.rgb);
        end      
        if isempty(handles.bw)
            handles.bw=imbinarize(handles.gray,handles.setting.bw_thre);
        end                
        handles.imhandle=imshow(handles.bw,'Parent',handles.axes1);
    end    
    
function handles=updateImage2(handles)   
    if handles.data.nImg==0
        return;
    end    
    if handles.colorChannel==1
        imshow(handles.rgb,'Parent',handles.axes2);        
    elseif handles.colorChannel==2
        if isempty(handles.gray)
            handles.gray=rgb2gray(handles.rgb);
        end
        imshow(handles.gray,'Parent',handles.axes2);
    elseif handles.colorChannel==3
        if isempty(handles.gray)
            handles.gray=rgb2gray(handles.rgb);
        end      
        if isempty(handles.bw)
            handles.bw=imbinarize(handles.gray,handles.setting.bw_thre);
        end                
        imshow(handles.bw,'Parent',handles.axes2);
    end    
    handles.axes2.NextPlot='add';
    handles.ax2cross(1)=plot(handles.axes2,[handles.imWidth*1/4,handles.imWidth*3/4],[handles.imHeight/2,handles.imHeight/2],'r');
    handles.ax2cross(2)=plot(handles.axes2,[handles.imWidth/2,handles.imWidth/2],[handles.imHeight*1/4,handles.imHeight*3/4],'r');
    handles.axes2.NextPlot='replace';
    
function handles=updatePreview(handles,rrng,crng)
    cla(handles.axes2)
    handles.imPrehandle=imshow(handles.rgb(rrng(1):rrng(2),crng(1):crng(2),:),'Parent',handles.axes2);
    
function handles=updateCounts(handles)
    set(handles.edit1,'String',[num2str(handles.currentImg),' / ', num2str(handles.data.nImg)]);

function mapos=mouse_pos_ax(mpos,apos,x0,y0,xlen,ylen)
    mapos(1)=(mpos(1)-apos(1))/apos(3)*xlen+x0;
    mapos(2)=y0-(mpos(2)-apos(2))/apos(4)*ylen;


function mapos=trimBox(mapos,handles)
    if mapos(1)<0.5
        mapos(1)=0.5;
    elseif mapos(1)>handles.imWidth+0.5
        mapos(1)=handles.imWidth+0.5;
    end    
    if mapos(2)<0.5
        mapos(2)=0.5;
    elseif mapos(2)>handles.imHeight+0.5
        mapos(2)=handles.imHeight+0.5;
    end        


% % detect if the mouse encounter the corner of box    
function event=detect_mouse_change(hObject,handles)
    event.boxid=0;
    event.cornerid=0;
    event.boxresize=0;
    event.detectData=0;
    event.dataid=0;
    ci=handles.currentImg;
    cp=handles.currentProperty;
    ax=handles.axes1;
    mapos=ax.CurrentPoint(1,1:2);
    if handles.boxselect.flag
        % % detect the box select
        n=handles.boxselect.n;
        if n>0
            id=[0,0];
            min0=inf;
            dist=zeros(n,4);
            for i=1:n
                box=handles.boxselect.xyrng(i,:);
                dist(i,1)=abs(mapos(1)-box(1))+abs(mapos(2)-box(3));    % upper left
                dist(i,2)=abs(mapos(1)-box(1))+abs(mapos(2)-box(4));    % lower left
                dist(i,3)=abs(mapos(1)-box(2))+abs(mapos(2)-box(3));    % upper right
                dist(i,4)=abs(mapos(1)-box(2))+abs(mapos(2)-box(4));    % lower right
                [mtmp,itmp]=min(dist(i,:),[],2);
                if mtmp<min0
                    id=[i,itmp];
                    min0=mtmp;
                end
            end
            xrng=handles.axes1.XLim;
            xlen=xrng(2)-xrng(1);
            if min0<xlen*0.01
                if id(2)==1 || id(2)==4
                    hObject.Pointer='topl';
                else
                    hObject.Pointer='topr';
                end
                event.boxresize=1;
                event.boxid=id(1);
                event.cornerid=id(2);
            else
                hObject.Pointer='arrow';
            end
        end
    elseif ~isempty(strfind(cp,'series'))&&(~handles.eraser_on)
        sid=str2num(cp(8:end));
        n=0;
        if isfield(handles.data.imLib(ci).data.series(sid),'pdata')
            pdata=handles.data.imLib(ci).data.series(sid).pdata;
            n=size(pdata,1);
        end
        if n>0
            id=0;
            min0=inf;
            dist=0;
            for i=1:n
                dist=abs(mapos(1)-pdata(i,1))+abs(mapos(2)-pdata(i,2));    % upper left
                if dist<min0
                    min0=dist;
                    id=i;
                end
            end
            xrng=handles.axes1.XLim;
            xlen=xrng(2)-xrng(1);
            if min0<xlen*0.01
                hObject.Pointer='hand';
                event.detectData=1;
                event.dataid=id;
            else
                hObject.Pointer='arrow';
            end
        end       
    elseif ~isempty(strfind(cp,'Anchor'))
        xpos=handles.data.imLib(ci).axis.xAnchor.pos;
        ypos=handles.data.imLib(ci).axis.yAnchor.pos;
        id=0;
        min0=inf;
        if ~isempty(xpos) ...
            dist=abs(mapos(1)-xpos(1,1))+abs(mapos(2)-xpos(1,2));
            if dist<min0
                id=1;
                min0=dist;
            end
            dist=abs(mapos(1)-xpos(2,1))+abs(mapos(2)-xpos(2,2));
            if dist<min0
                id=2;
                min0=dist;
            end            
        end
        if ~isempty(ypos) ...
            dist=abs(mapos(1)-ypos(1,1))+abs(mapos(2)-ypos(1,2));
            if dist<min0
                id=3;
                min0=dist;
            end
            dist=abs(mapos(1)-ypos(2,1))+abs(mapos(2)-ypos(2,2));
            if dist<min0
                id=4;
                min0=dist;
            end            
        end      
        if  ~isinf(min0)   
            xrng=handles.axes1.XLim;
            xlen=xrng(2)-xrng(1);
            if min0<xlen*0.01
                hObject.Pointer='hand';
                event.detectData=1;
                event.dataid=id;
            else
                event.dataid=0;
                hObject.Pointer='arrow';
            end    
        else
            hObject.Pointer='arrow';
        end
    end    
function handles=update_boxselect(handles)
    nc=handles.boxselect.current;
    ci=handles.currentImg;
    xtmp=handles.boxselect.boxhandles{nc}.XData;
    xmin=min(xtmp); xmax=max(xtmp);
    crng=[round(xmin),round(xmax)];
    crng(1)=max([1,crng(1)]);
    crng(2)=min([handles.imWidth,crng(2)]);
    ytmp=handles.boxselect.boxhandles{nc}.YData;
    ymin=min(ytmp); ymax=max(ytmp);
    rrng=[round(ymin),round(ymax)];  
    rrng(1)=max([1,rrng(1)]);
    rrng(2)=min([handles.imHeight,rrng(2)]);
    updatePreview(handles,rrng,crng);
    handles.boxselect.xyrng(nc,:)=[xmin,xmax,ymin,ymax];
    handles.boxselect.rcrng(nc,:)=[rrng,crng];
    handles.Text_numBox.String=['nbox: ',num2str(handles.boxselect.n)];
    
function handles=storeImageData(handles)
    ci=handles.currentImg;
    %handles.data.imLib(ci).boxselect.nbox=handles.boxselect.n;
    %handles.data.imLib(ci).boxselect.xyrng=handles.boxselect.xyrng;
    %handles.data.imLib(ci).boxselect.rcrng=handles.boxselect.rcrng;
    handles.data.imLib(ci).imHeight=handles.imHeight;
    handles.data.imLib(ci).imWidth=handles.imWidth;
   
function handles=load_legend_preselect(handles)
    ci=handles.currentImg;
    imdata=handles.data.imLib(ci).legend.preselect;
    if isfield(imdata,'nbox')
        nbox=imdata.nbox;
        handles.boxselect.n=nbox;
        ax=handles.axes1;
        ax.NextPlot='add';
        if nbox>0
            for i=1:nbox
                xyrng=imdata.box(i,:);
                rcrng=imdata.rcrng(i,:);
                handles.boxselect.xyrng(i,:)=xyrng;
                handles.boxselect.rcrng(i,:)=imdata.rcrng(i,:);
                handles.boxselect.boxhandles{i}=plot(ax,[rcrng(3),rcrng(4),rcrng(4),rcrng(3),rcrng(3)], ...
                        [rcrng(1),rcrng(1),rcrng(2),rcrng(2),rcrng(1)],'k');
            end
        end
    end
    
function handles=boxSelection(handles,mapos)
    nbox=handles.boxselect.n;
    inbox=0;
    if nbox>0
        ax=handles.axes1;   
        mapos=ax.CurrentPoint(1,1:2);
        for i=nbox:-1:1
            xyrng=handles.boxselect.xyrng(i,:);
            if (mapos(1)>=xyrng(1))&&(mapos(1)<=xyrng(2))&&(mapos(2)>=xyrng(3))&&(mapos(2)<=xyrng(4))
                s=handles.boxselect.boxhandles{i}.Selected;
                if strcmp(s,'on')
                    handles.boxselect.boxhandles{i}.Selected='off';
                else
                    handles.boxselect.boxhandles{i}.Selected='on';
                end
                s=handles.boxselect.boxhandles{i}.Selected;
                if strcmp(s,'on')
                    handles.boxselect.current=i;
                    handles=update_boxselect(handles);
                    handles=updatePreview(handles,handles.boxselect.rcrng(i,1:2),handles.boxselect.rcrng(i,3:4));
                else
                    if ~handles.selection.continuous
                        cla(handles.axes2);
                        handles.boxselect.current=0;
                    end
                end
                inbox=i;
                break;
            end
        end
        if ~handles.selection.continuous
            for i=1:nbox
                if i~=inbox
                    handles.boxselect.boxhandles{i}.Selected='off';
                end
            end
            if inbox==0
                cla(handles.axes2);
                handles.boxselect.current=0;            
            end            
        end
    end
    
function handles=segement_pic(handles)
    ci=handles.currentImg;
    n=handles.boxselect.n;
    imdata=handles.data.imLib(ci);
    if n>0
        for i=1:n
            rcrng=handles.boxselect.rcrng(i,:);
            im0=handles.rgb(rcrng(1):rcrng(2),rcrng(3):rcrng(4),:);
            if ~exist([handles.data.path,'segmentation'])
                mkdir([handles.data.path,'segmentation'])
            end
            if i<10
                imwrite(im0,[handles.data.path,'segmentation\',imdata.name,'_0',num2str(i),imdata.suffix])
            else
                imwrite(im0,[handles.data.path,'segmentation\',imdata.name,'_',num2str(i),imdata.suffix])
            end
        end
        handles.data.imLib(ci).segmented=1;
    end

       
    
function handles=display_setting_table(handles)    
    handles.Table_property.Data=handles.data.settinglist;
    pos=handles.Table_property.Position;
    handles.Table_property.ColumnName={'setting','value'};
    handles.Table_property.RowName={};
    handles.Table_property.ColumnWidth={100,pos(3)-110};
    handles.Table_property.ColumnEditable=logical([0,1]);
    handles.currentTable='setting';
    
    
function handles=display_file_table(handles)    
    mysize=size(handles.data.filelist);
    filelist={};
    if (mysize(2)>1) && (mysize(1)==1)
        for i=1:mysize(2)
            filelist{i,1}=handles.data.filelist{i};
        end
    else
        for i=1:mysize(1)
            filelist{i,1}=handles.data.filelist{i};
        end
    end
    handles.Table_property.Data=filelist;
    pos=handles.Table_property.Position;
    handles.Table_property.ColumnName={'name'};
    handles.Table_property.RowName='numbered';
    handles.Table_property.ColumnWidth={pos(3)-70};
    handles.Table_property.ColumnEditable=logical([0]);
    handles.currentTable='file';

function handles=display_data_table(handles)    
    handles=datastruct_initialize(handles);
    handles.Table_property.Data=handles.data.datalist;
    pos=handles.Table_property.Position;
    handles.Table_property.ColumnName={'name','state'};
    handles.Table_property.RowName={};
    handles.Table_property.ColumnWidth={150,pos(3)-160};
    handles.Table_property.ColumnEditable=logical([0]);
    handles.currentTable='data';    

       
function handles=display_data_detail(handles,term)
    ci=handles.currentImg;
    handles=detail_page_initialization(handles);
    pos=handles.Table_property.Position;
    handles.currentProperty=term;
    if strcmp(term,'xLabel')||strcmp(term,'yLabel')
        h1=getfield(handles.data.imLib(ci).axis,term);
        if h1.exist
            handles.Table_detailProperty.ColumnName={'term','value'};
            handles.Table_detailProperty.ColumnWidth={100,pos(3)-110};
            data{1,1}='state';
            data{1,2}=h1.state;
            data{2,1}='text';
            data{2,2}=h1.text;            
            for i=1:numel(h1.data)
                data{i+2,1}=['data ',num2str(i)];
                data{i+2,2}=strip_char_1(h1.data{i}.Text);
            end
            handles.Table_detailProperty.Data=data;
        end
    elseif strcmp(term,'xTicks')||strcmp(term,'yTicks')
        h1=getfield(handles.data.imLib(ci).axis,term);
        if h1.exist
            handles.Table_detailProperty.ColumnName={'term','value1','value2'};
            handles.Table_detailProperty.ColumnWidth={100,round((pos(3)-110)/2),round((pos(3)-110)/2)};
            data{1,1}='state';
            data{1,2}=h1.state;
            for i=1:numel(h1.data)
                data{i+1,1}=['data ',num2str(i)];
                data{i+1,2}=h1.data(i);
                data{i+1,3}=h1.datastr{i};
            end
            handles.Table_detailProperty.Data=data;
        end   
    elseif strcmp(term,'preselect')
        h1=getfield(handles.data.imLib(ci).legend,term);
        handles.Table_detailProperty.ColumnName={'term','x1','x2','y1','y2'};
        handles.Table_detailProperty.ColumnEditable=logical([0,0,0,0,0]);
        if h1.nbox>0
            for i=1:h1.nbox
                data{i,1}=['box ',num2str(i)];
                data{i,2}=h1.rcrng(i,3);
                data{i,3}=h1.rcrng(i,4);
                data{i,4}=h1.rcrng(i,1);
                data{i,5}=h1.rcrng(i,2);                     
            end  
            handles.Table_detailProperty.Data=data;
        end
    elseif strcmp(term,'item')
        handles.Table_detailProperty.ColumnName={'term','text','R','G','B'};
        handles.Table_detailProperty.ColumnWidth={100,200,100,100,100};
        handles.Table_detailProperty.ColumnEditable=logical([0,1,0,0,0]);
        item=handles.data.imLib(ci).legend.item;
        nitem=handles.data.imLib(ci).legend.nitem;
        if nitem>0
            for i=1:nitem
                data{i,1}=['data ',num2str(i)];
                data{i,2}=item(i).text;
                data{i,3}=item(i).color(1);
                data{i,4}=item(i).color(2);
                data{i,5}=item(i).color(3);                     
            end  
            handles.Table_detailProperty.Data=data;   
        end
    elseif ~isempty(strfind(term,'series'))
        n=str2num(term(8:end));
        handles.Table_detailProperty.ColumnName={'id','x','y','runout'};
        handles.Table_detailProperty.ColumnEditable=logical([0,0,0,1]);
        nr=0;
        if isfield(handles.data.imLib(ci).data.series(n),'pdata')
            pd=handles.data.imLib(ci).data.series(n).pdata;
            nr=size(pd,1);
        end
        if isfield(handles.data.imLib(ci).data.series(n),'runout')
            flag_ro=1;
            ro=handles.data.imLib(ci).data.series(n).runout;
        else
            flag_ro=0;
        end
%         if nr>0
%             for i=1:nr
%                 data{i,1}=['data ',num2str(i)];
%                 data{i,2}=pd(i,1);
%                 data{i,3}=pd(i,2);
%                 if flag_ro==1;
%                     data{i,4}=ro(i);
%                 else
%                     data{i,4}=nan;
%                 end
%             end  
%             handles.Table_detailProperty.Data=data;   
%         end 
    elseif strcmp(term,'xAnchor')||strcmp(term,'yAnchor')
        xdata=handles.data.imLib(ci).axis.xAnchor.data;
        ydata=handles.data.imLib(ci).axis.yAnchor.data;        
        xpos=handles.data.imLib(ci).axis.xAnchor.pos;
        ypos=handles.data.imLib(ci).axis.yAnchor.pos;
        
        handles.Table_detailProperty.ColumnName={'term','value','value'};
        handles.Table_detailProperty.ColumnWidth={80,(pos(3)-110)/2,(pos(3)-110)/2};
        handles.Table_detailProperty.ColumnEditable=logical([0,1,1]);
        data{1,1}='xdata';
        if ~isempty(xdata)
            data{1,2}=num2str(xdata(1),'%3.2e');
            data{1,3}=num2str(xdata(2),'%3.2e');
        end
        data{2,1}='ydata';
        if ~isempty(ydata)
            data{2,2}=ydata(1);
            data{2,3}=ydata(2);
        end   
        data{3,1}='xpos';
        if ~isempty(xpos)
            data{3,2}=xpos(1,1);
            data{3,3}=xpos(2,1);
        end
        data{4,1}='ypos';
        if ~isempty(ypos)
            data{4,2}=ypos(1,2);
            data{4,3}=ypos(2,2);
        end          
        data{5,1}='xScale';
        data{5,2}=handles.data.imLib(ci).axis.xScale;
        data{8,1}='yScale';
        data{8,2}=handles.data.imLib(ci).axis.yScale;  
        data{6,1}='xLabel';
        data{6,2}=handles.data.imLib(ci).axis.xLabel.data2;
        data{9,1}='yLabel';
        data{9,2}=handles.data.imLib(ci).axis.yLabel.data2;        
        data{7,1}='xUnit';
        data{7,2}=handles.data.imLib(ci).axis.xLabel.unit;    
        data{10,1}='yUnit';
        data{10,2}=handles.data.imLib(ci).axis.yLabel.unit;          
        handles.Table_detailProperty.Data=data;      
    else    
        handles.currentProperty='';
    end
    
function handles=show_item_box(handles,term)
    ci=handles.currentImg;
    handles=clean_selection_plot(handles);
    handles=boxselectInitialize(handles);
    if strcmp(term,'xLabel')||strcmp(term,'yLabel')||strcmp(term,'xTicks')||strcmp(term,'yTicks')
        h=handles.data.imLib(ci).axis;
        n=handles.selection.n;
        handle.axes1.NextPlot='add';
        if isfield(h,term)
            h1=getfield(h,term);
            if h1.exist
                handles.selection.type=term;
                for i=1:size(h1.box,1)
                    n=n+1;
                    handles.plot.selection.hd=[handles.plot.selection.hd,plotbox(h1.box(i,:),handles,'k')];
                end
            end
        end
        handles.selection.n=n;
    elseif strcmp(term,'preselect')
        handles=load_legend_preselect(handles);
    elseif strcmp(term,'item')
        h=handles.data.imLib(ci).legend;
        n=handles.selection.n;
        handle.axes1.NextPlot='add';
        if isfield(h,term)
            h1=getfield(h,term);
            if h.exist
                handles.selection.type=term;
                for i=1:h.nitem
                    n=n+1;
                    handles.plot.selection.hd=[handles.plot.selection.hd,plotbox(h1(i).box{1,1},handles,'k')];
                    n=n+1;
                    handles.plot.selection.hd=[handles.plot.selection.hd,plotbox(h1(i).box{1,2},handles,'k')];
                end
            end
        end
        handles.selection.n=n;  
    elseif ~isempty(strfind(term,'series'))
        n=str2num(term(8:end));
        nr=0;
        if isfield(handles.data.imLib(ci).data.series(n),'pdata')
            pd=handles.data.imLib(ci).data.series(n).pdata;
            nr=size(pd,1);    
            handle.axes1.NextPlot='add';
        end
        if nr>0
            if isfield(handles.data.imLib(ci).data,'colorpick') && (handles.data.imLib(ci).data.colorpick==1)
                handles.rgb=handles.rgb0;
                for i=1:size(pd,1)
                    handles.rgb(pd(i,2),pd(i,1),:)=uint8(reshape([255,255,0],[1,1,3]));
                end
                handles=updateImage(handles);
            else
                for i=1:nr
                    p=plot(handles.axes1,pd(i,1),pd(i,2),'o','MarkerSize',4,'MarkerEdgeColor','k','MarkerFaceColor','y','LineWidth',0.75);
                    handles.plot.selection.hd=[handles.plot.selection.hd,p];
                end
                handles.selection.n=nr;
            end
        end
        symbox=handles.data.imLib(ci).legend.item(n).box{1};
        imshow(handles.rgb(symbox(3):symbox(4),symbox(1):symbox(2),:),'Parent',handles.axes3);        
    elseif strcmp(term,'xAnchor') || strcmp(term,'yAnchor')      
        xpos=handles.data.imLib(ci).axis.xAnchor.pos;
        ypos=handles.data.imLib(ci).axis.yAnchor.pos;
        handles.axes1.NextPlot='add';
        if ~isempty(xpos) 
            p=plot(handles.axes1,xpos(1,1),xpos(1,2),'o','MarkerSize',5,'MarkerEdgeColor','w','MarkerFaceColor','b','LineWidth',1.25);
            handles.plot.selection.hd=[handles.plot.selection.hd,p];
            p=plot(handles.axes1,xpos(2,1),xpos(2,2),'o','MarkerSize',5,'MarkerEdgeColor','w','MarkerFaceColor','r','LineWidth',1.25);
            handles.plot.selection.hd=[handles.plot.selection.hd,p];            
        end
        if ~isempty(ypos) 
            p=plot(handles.axes1,ypos(1,1),ypos(1,2),'^','MarkerSize',5,'MarkerEdgeColor','w','MarkerFaceColor','b','LineWidth',1.25);
            handles.plot.selection.hd=[handles.plot.selection.hd,p];
            p=plot(handles.axes1,ypos(2,1),ypos(2,2),'^','MarkerSize',5,'MarkerEdgeColor','w','MarkerFaceColor','r','LineWidth',1.25);
            handles.plot.selection.hd=[handles.plot.selection.hd,p];            
        end        
        handles.selection.n=4;
    end
    
function handles=clean_selection_plot(handles)
    n=handles.selection.n;
    for i=1:n
        delete(handles.plot.selection.hd(i))
    end
    handles.plot.selection.hd=[];
    handles.selection.n=0;
    
function handles=updateColorBut(handles)    
    if handles.colorChannel==1
        handles.RadBut_rgb.Value=1;
        handles.RadBut_gray.Value=0;
        handles.RadBut_bw.Value=0;
    elseif handles.colorChannel==2
        handles.RadBut_rgb.Value=0;
        handles.RadBut_gray.Value=1;
        handles.RadBut_bw.Value=0;
    elseif handles.colorChannel==3
        handles.RadBut_rgb.Value=0;
        handles.RadBut_gray.Value=0;
        handles.RadBut_bw.Value=1;       
    end
    handles=updateImage(handles);
    handles=updateImage2(handles);

function handles=updateDataAfterSetting(handles,item)
    if strcmp(item,'bw_thre')
        handles.bw=[];
        if handles.colorChannel==3
            handles=updateImage(handles);
            handles=updateImage2(handles);
        end
    end
    
function [handles,stat]=updateSetting(handles,item,num)
    stat=0;
    if strcmp(item,'bw_thre')
        if (num>=0)&&(num<=1)
            handles.setting=setfield(handles.setting,item,num);    
            stat=1;
        end
    end

    
    
function handles=addMsg(handles,msg)
    string=flip(handles.Table_msg.Data);
    n=numel(string);
    msg=[num2str(n),'   ',msg];
    string{n+1,1}=msg;
    handles.Table_msg.Data=flip(string);

function handles=updatePlot_sepobj(handles)    
    ci=handles.currentImg;
    if handles.plot.sepobj.active
        if isempty(handles.plot.sepobj.hd)
            if handles.data.imLib(ci).sepobj.exist
                n=handles.data.imLib(ci).sepobj.n;
                ci=handles.currentImg;
                box=handles.data.imLib(ci).sepobj.box;
                for i=1:n
                    handles.plot.sepobj.hd=[handles.plot.sepobj.hd,plotbox(box(i,:),handles)];
                end
            end
        else
            n=numel(handles.plot.sepobj.hd);
            for i=1:n
                handles.plot.sepobj.hd(i).Visible='on';
            end
        end
    else
        if ~isempty(handles.plot.sepobj.hd)
            n=numel(handles.plot.sepobj.hd);
            for i=1:n
                handles.plot.sepobj.hd(i).Visible='off';
            end            
        end
    end

function handles=delete_plot_sepobj(handles)
    if ~isempty(handles.plot.sepobj.hd)
        for i=1:numel(handles.plot.sepobj.hd)
            delete(handles.plot.sepobj.hd(i))
        end
        handles.plot.sepobj.hd=[];
    end
    
function p=plotbox(bx,handles,color)
    if nargin<3
        color='k';
    end
    p=plot(handles.axes1,[bx(1),bx(2),bx(2),bx(1),bx(1)],[bx(3),bx(3),bx(4),bx(4),bx(3)],'color',color,'LineWidth',0.5);
    
function handles=func_next_image(handles)
    handles=storeImageData(handles);
    if handles.currentImg<handles.data.nImg
        handles.currentImg=handles.currentImg+1;
        for i=1:handles.boxselect.n
            delete(handles.boxselect.boxhandles{i});
        end
        handles=updateFigure(handles);
        handles=boxselectInitialize(handles);
        handles=selectionInitialize(handles);
        handles=updateCounts(handles);
        handles=boxSelectBut_initialize(handles);
        handles=legendSelectBut_initialize(handles);
        handles.Text_numBox.String=['nbox: ',num2str(handles.boxselect.n)];
        handles=eraser_initialize(handles);
        handles.Text_numBox.String=num2str(handles.color_tolerance);
        
        ct=handles.currentTable;
        handles.currentProperty='';
        if strcmp(ct,'file')
            handles=display_file_table(handles);
        elseif strcmp(ct,'setting')
            handles=display_setting_table(handles);
        elseif strcmp(ct,'data')
            handles=display_data_table(handles);
        end
        handles=detail_page_initialization(handles);
        
        % % use for correting anchors
        handles.currentProperties='xAnchor';
        handles=display_data_detail(handles,'xAnchor');
        handles=show_item_box(handles,'xAnchor');
        
        % % for quick legend seletion
        %handles=func_legend_select(handles);
    end
    
function handles=func_previous_image(handles)    
    handles=storeImageData(handles);
    if handles.currentImg>1
        handles.currentImg=handles.currentImg-1;
        for i=1:handles.boxselect.n
            delete(handles.boxselect.boxhandles{i});
        end
        handles=updateFigure(handles);
        handles=boxselectInitialize(handles);
        handles=selectionInitialize(handles);
        handles=updateCounts(handles);
        handles=boxSelectBut_initialize(handles);
        handles=legendSelectBut_initialize(handles);
        handles.Text_numBox.String=['nbox: ',num2str(handles.boxselect.n)];
        handles=eraser_initialize(handles);
        handles.Text_numBox.String=num2str(handles.color_tolerance);
        
        ct=handles.currentTable;
        if strcmp(ct,'file')
            handles=display_file_table(handles);
        elseif strcmp(ct,'setting')
            handles=display_setting_table(handles);
        elseif strcmp(ct,'data')
            handles=display_data_table(handles);
        end
        handles=detail_page_initialization(handles); 
        
        % % use for correting anchors
        handles.currentProperties='xAnchor';
        handles=display_data_detail(handles,'xAnchor');
        handles=show_item_box(handles,'xAnchor');
        
    end       
    
function handles=func_seperate_object(handles)    
    handles=addMsg(handles,'EXECUTING seperated_object ...');
    if isempty(handles.gray)
        handles.gray=rgb2gray(handles.rgb);
    end
    if isempty(handles.bw)
        handles.bw=imbinarize(handles.gray,handles.setting.bw_thre);
    end
    ci=handles.currentImg;
    try
        [n_sepobj,row,col,center,box,ob_wh]=seperated_object(handles.bw);
        handles=addMsg(handles,'DONE seperated_object.');
    catch
        handles=addMsg(handles,'ERROR when executing seperated_object.');
    end
    handles.data.imLib(ci).sepobj.exist=1;
    handles.data.imLib(ci).sepobj.n=n_sepobj;
    handles.data.imLib(ci).sepobj.row=row;
    handles.data.imLib(ci).sepobj.col=col;
    handles.data.imLib(ci).sepobj.center=center;
    handles.data.imLib(ci).sepobj.box=box;
    handles.data.imLib(ci).sepobj.ob_wh=ob_wh;
    handles=delete_plot_sepobj(handles);
    handles=updatePlot_sepobj(handles);   

    
function handles=func_detect_axis(handles)   
    ci=handles.currentImg;
    if ~handles.data.imLib(ci).sepobj.exist
        handles=addMsg(handles,'Objects are not seperated, CALL seperate_object.');
        handles=func_seperate_object(handles);
    end
    try
        n_cls=handles.data.imLib(ci).sepobj.n;
        row=handles.data.imLib(ci).sepobj.row;
        col=handles.data.imLib(ci).sepobj.col;
        box=handles.data.imLib(ci).sepobj.box;        
        thre_AxisPercent=handles.setting.thre_AxisPercent;
        handles=addMsg(handles,'EXECUTING detect_coordinate.');
        [xaw,yaw,mark_r,mark_c,pos_xa,pos_ya,coordObid,wf,hf,origin]=detect_coordinate(n_cls,box,row,col,thre_AxisPercent);
        % save data to imLib
        handles=savedata_detect_coordinate(handles,ci,pos_xa,pos_ya,coordObid);
        handles=addMsg(handles,'DONE detect_coordinate.');
    catch ME
        handles=addMsg(handles,'ERROR when executing detect_coordinate.');
        return;
    end    

    try
        center=handles.data.imLib(ci).sepobj.center;
        ob_wh=handles.data.imLib(ci).sepobj.ob_wh;  
        thre_AxisPercent=handles.setting.thre_AxisPercent;
        handles=addMsg(handles,'EXECUTING recognize_axis_character.');
        thre_charscale=handles.setting.thre_charscale;
        [xxlabel,yylabel,xxlabels,yylabels,xlabcl_box,ylabcl_box, ...
         xxtick_num,yytick_num,xxtick_str,yytick_str, ...
         xtlcl_box,ytlcl_box]=recognize_axis_character(n_cls,center,box,ob_wh,pos_xa,pos_ya,row,col,wf,hf,origin,handles.bw,thre_charscale);
        handles=savedata_axis_character(handles,xxlabel,yylabel,xxlabels,yylabels,xlabcl_box,ylabcl_box,xxtick_num,yytick_num,xxtick_str,yytick_str,xtlcl_box,ytlcl_box);
        handles=addMsg(handles,'DONE recognize_axis_character.');
    catch ME
        handles=addMsg(handles,'ERROR when executing recognize_axis_character.');
        return;
    end  
    
    try 
        bw1=imbinarize(handles.gray,0.9);
        [px1,px2,py1,py2,x1,x2,y1,y2]=calibrate_axis(xaw,yaw,mark_r,mark_c,xxtick_num,yytick_num,xtlcl_box,ytlcl_box,bw1);
        handles=savedata_calibrate_axis(handles,px1,px2,py1,py2,x1,x2,y1,y2);
        handles=addMsg(handles,'DONE calibrate_axis.');
    catch ME
        handles=addMsg(handles,'ERROR when executing calibrate_axis.');
        return;
    end
    
function handles=func_analyse_legend(handles)
    ci=handles.currentImg;
    if ~handles.data.imLib(ci).sepobj.exist
        handles=addMsg(handles,'Objects are not seperated, CALL seperate_object.');
        handles=func_seperate_object(handles);
    end    
    handles=imLib_legend_init(handles,ci);
    center=handles.data.imLib(ci).sepobj.center;
    ob_wh=handles.data.imLib(ci).sepobj.ob_wh;
    n_cls=handles.data.imLib(ci).sepobj.n;
    row=handles.data.imLib(ci).sepobj.row;
    col=handles.data.imLib(ci).sepobj.col;
    box=handles.data.imLib(ci).sepobj.box;        
    thre_AxisPercent=handles.setting.thre_AxisPercent;
    handles=addMsg(handles,'EXECUTING analyse_legend.');
    nbox=handles.data.imLib(ci).legend.preselect.nbox;
    bw=handles.bw;
    rgb=handles.rgb;
    for i=1:nbox
        legendbox=handles.data.imLib(ci).legend.preselect.rcrng(i,:);
        try        
            [symbol,word,color,itembox]=process_legend(legendbox,row,col,center,box,ob_wh,bw,rgb);
            % save data to imLib
            handles=savedata_analyse_legend(handles,ci,symbol,word,color,itembox);
            handles=addMsg(handles,['Done analyse_legend ',num2str(i),'/',num2str(nbox)]);
        catch ME
            handles=addMsg(handles,['ERROR when executing analyse_legend ',num2str(i),'/',num2str(nbox)]);
            return;
        end    
    end
    if strcmp(handles.currentTable,'data')&&strcmp(handles.currentProperty,'item')
        handles=display_data_detail(handles,'item');
    end

function handles=func_del_legend_box(handles)
    if strcmp(handles.currentProperty,'preselect')
        n=handles.boxselect.n;
        ct=0;
        deleted=[];
        ndel=0;
        xyrng=handles.boxselect.xyrng;
        rcrng=handles.boxselect.rcrng;
        handles.boxselect.xyrng=[];
        handles.boxselect.rcrng=[];
        bh=handles.boxselect.boxhandles;
        if n>0
            for i=1:n
                s=handles.boxselect.boxhandles{i}.Selected;
                if strcmp(s,'on')
                    delete(handles.boxselect.boxhandles{i});
                    ndel=ndel+1;
                    deleted(ndel)=i;
                end
            end
            handles.boxselect.boxhandles={};
            for i=1:n
                if ~ismember(i,deleted)
                    ct=ct+1;
                    handles.boxselect.boxhandles{ct}=bh{i};
                    handles.boxselect.xyrng(ct,:)=xyrng(i,:);
                    handles.boxselect.rcrng(ct,:)=rcrng(i,:);
                end
            end
        end
        handles.boxselect.n=n-ndel;
        handles.Text_numBox.String=['nbox: ',num2str(handles.boxselect.n)];
        handles.boxselect.current=0; 
        handles=savedata_legend_preselect(handles);
        handles=display_data_detail(handles,'preselect');
    end
    
function handles=func_symbol_recognition(handles)
    ci=handles.currentImg;
    if ~handles.data.imLib(ci).sepobj.exist
        handles=addMsg(handles,'Objects are not seperated, CALL seperate_object.');
        handles=func_seperate_object(handles);
    end    
    if ~handles.data.imLib(ci).legend.exist
        handles=addMsg(handles,'Legend not found.');
        if handles.data.imLib(ci).legend.preselect.exist
            handles=func_analyse_legend(handles);
        else    
            handles=addMsg(handles,'Legend region not found, EXIT.');
        end    
    end  
    handles=imLib_data_init(handles,ci);
    sepobj=handles.data.imLib(ci).sepobj;
    center=sepobj.center;
    ob_wh=sepobj.ob_wh;
    n_cls=sepobj.n;
    row=sepobj.row;
    col=sepobj.col;
    box=sepobj.box;
    pos_xa=0;
    pos_ya=0;
    incbox={};
    excbox={};
    excid=[];
    if handles.data.imLib(ci).axis.pos_xa.exist==1
        pos_xa=handles.data.imLib(ci).axis.pos_xa.data;
    end    
    if handles.data.imLib(ci).axis.pos_ya.exist==1
        pos_ya=handles.data.imLib(ci).axis.pos_ya.data;
    end
    [h,w]=size(handles.bw);
    if ~isnan(pos_xa) && ~isnan(pos_ya) && pos_xa && pos_ya
        incbox={[pos_ya,w,1,pos_xa]};
    else
        incbox={[1,w,1,h]};
    end
    preselect=handles.data.imLib(ci).legend.preselect;
    if preselect.exist
        for i=1:preselect.nbox
            rcrng=preselect.rcrng;
            excbox{i}=[rcrng(3),rcrng(4),rcrng(1),rcrng(2)];
        end
    end
    coordObid=handles.data.imLib(ci).axis.coordObid;
    if ~isnan(coordObid)
        excid=[coordObid];
    end
    lgd=handles.data.imLib(ci).legend;
    symbol={};
    color={};
    for i=1:lgd.nitem
        symbol{i}=(lgd.item(i).symbol-1)*(0-1);
        color{i}=lgd.item(i).color;
    end
    handles=addMsg(handles,'EXECUTING symbol_recognition.');    
    try
        [ifreg,xreg,yreg,type,overlap]=single_shape_reconition(symbol,color,row,col,box,center,ob_wh,handles.bw,incbox,excbox,excid);
        handles=savedata_symbol_recognition(handles,ifreg,xreg,yreg,type,overlap);
        handles=addMsg(handles,'Done symbol_recognition');   
    catch
        handles=addMsg(handles,'ERROR symbol_recognition.');   
        return;
    end
    handles=datastruct_initialize(handles);
    handles=detail_page_initialization(handles);

function handles=func_symbol_recognition_color(handles)
    ci=handles.currentImg;
    if ~handles.data.imLib(ci).sepobj.exist
        handles=addMsg(handles,'Objects are not seperated, CALL seperate_object.');
        handles=func_seperate_object(handles);
    end    
    if ~handles.data.imLib(ci).legend.exist
        handles=addMsg(handles,'Legend not found.');
        if handles.data.imLib(ci).legend.preselect.exist
            handles=func_analyse_legend(handles);
        else    
            handles=addMsg(handles,'Legend region not found, EXIT.');
        end    
    end  
    handles=imLib_data_init(handles,ci);
    sepobj=handles.data.imLib(ci).sepobj;
    center=sepobj.center;
    ob_wh=sepobj.ob_wh;
    n_cls=sepobj.n;
    row=sepobj.row;
    col=sepobj.col;
    box=sepobj.box;
    pos_xa=0;
    pos_ya=0;
    incbox={};
    excbox={};
    excid=[];
    if handles.data.imLib(ci).axis.pos_xa.exist==1
        pos_xa=handles.data.imLib(ci).axis.pos_xa.data;
    end    
    if handles.data.imLib(ci).axis.pos_ya.exist==1
        pos_ya=handles.data.imLib(ci).axis.pos_ya.data;
    end
    [h,w]=size(handles.bw);
    if ~isnan(pos_xa) && ~isnan(pos_ya) && pos_xa && pos_ya
        incbox={[pos_ya,w,1,pos_xa]};
    else
        incbox={[1,w,1,h]};
    end
    preselect=handles.data.imLib(ci).legend.preselect;
    if preselect.exist
        for i=1:preselect.nbox
            rcrng=preselect.rcrng;
            excbox{i}=[rcrng(3),rcrng(4),rcrng(1),rcrng(2)];
        end
    end
    lgd=handles.data.imLib(ci).legend;
    symbol={};
    color={};
    for i=1:lgd.nitem
        symbol{i}=(lgd.item(i).symbol-1)*(0-1);
        color{i}=lgd.item(i).color;
    end
    handles=addMsg(handles,'EXECUTING symbol_recognition.');    
    try
        data=extract_data_by_color(handles.rgb,color,incbox,excbox);
        handles=savedata_symbol_recognition_color(handles,data);
        handles=addMsg(handles,'Done symbol_recognition_color');   
    catch
        handles=addMsg(handles,'ERROR symbol_recognition_color.');   
        return;
    end
    handles=datastruct_initialize(handles);
    handles=detail_page_initialization(handles);    

function handles=func_add_picked_data(handles)
    ci=handles.currentImg;
    cp=handles.currentProperty;
    data=handles.pixelRecord;
    handles.data.imLib(ci).data.exist=1;
    handles.data.imLib(ci).data.state='auto';
    ns=handles.data.imLib(ci).legend.nitem;
    handles.data.imLib(ci).data.nseries=ns;
    handles.data.imLib(ci).data.colorpick=1;
    if ~isempty(strfind(cp,'series'))
        n=str2num(cp(8:end));
    else
        return;
    end
    n1=size(data,1);
    n2=size(handles.data.imLib(ci).data.series(n).pdata,1);
    if n2==0
        handles.data.imLib(ci).data.series(n).pdata=data;
        handles.data.imLib(ci).data.series(n).auto=zeros(n1,1)+1;
        handles.data.imLib(ci).data.series(n).runout=zeros(n1,1);
    else
        handles.data.imLib(ci).data.series(n).pdata(n2+1:n2+n1,1:2)=data;
        handles.data.imLib(ci).data.series(n).auto(n2+1:n2+n1,1)=zeros(n1,1)+1;
        handles.data.imLib(ci).data.series(n).runout(n2+1:n2+n1,1)=zeros(n1,1);        
    end    
    handles=datastruct_initialize(handles);
    handles=detail_page_initialization(handles);        

function handles=func_replace_picked_data(handles)
    ci=handles.currentImg;
    cp=handles.currentProperty;
    data=handles.pixelRecord;
    handles.data.imLib(ci).data.exist=1;
    handles.data.imLib(ci).data.state='auto';
    ns=handles.data.imLib(ci).legend.nitem;
    handles.data.imLib(ci).data.nseries=ns;
    handles.data.imLib(ci).data.colorpick=1;
    if ~isempty(strfind(cp,'series'))
        n=str2num(cp(8:end));
    else
        return;
    end
    n1=size(data,1);
    handles.data.imLib(ci).data.series(i).pdata=data;
    handles.data.imLib(ci).data.series(i).auto=zeros(n1,1)+1;
    handles.data.imLib(ci).data.series(i).runout=zeros(n1,1);
    handles=datastruct_initialize(handles);
    handles=detail_page_initialization(handles);   
    
function handles=func_add_data_series(handles)
    if handles.add_data_series==0
        handles.add_data_series=1;
        handles.boxselect.flag=1;
    else
        handles.boxselect.flag=0;
        handles.add_data_series=0;
        handles=savedata_add_data_series(handles);
        handles=display_data_table(handles); 
        handles=display_data_detail(handles,'item');
        handles=boxselectInitialize(handles);
        handles=selectionInitialize(handles);  
        handles=updateImage2(handles);
    end
    if handles.add_data_series
        handles.But_addDataSeries.BackgroundColor=[0.7,0.7,1.0];
    else
        handles.But_addDataSeries.BackgroundColor=[0.94,0.94,0.94];
    end        

function handles=func_delete_data(handles) 
    ci=handles.currentImg;
    cp=handles.currentProperty;
    if ~isempty(strfind(cp,'series'))
        sid=str2num(cp(8:end));
    else 
        return;
    end
    n=handles.selection.n;
    nsub=handles.selection.nsub;
    subset=handles.selection.subset;
    ct=0;
    pdata=handles.data.imLib(ci).data.series(sid).pdata;
    pd_tmp=[];  % temporary pdata
    hd_tmp=[];  % temporary handles;
    for i=1:n
        delete(handles.plot.selection.hd(i));
        if ~ismember(i,subset)
            ct=ct+1;
            pd_tmp(ct,:)=pdata(i,:);
        end
    end
    handles.data.imLib(ci).data.series(sid).pdata=[];
    handles.data.imLib(ci).data.series(sid).pdata=pd_tmp;
    handles.selection.n=n-nsub;
    handles.selection.nsub=0;
    handles.selection.subset=[];
    handles=display_data_detail(handles,cp);
    handles=show_item_box(handles,cp);
  
function handles=func_autorun(handles)
    rng=handles.processRange;
    ct=0;
    for i=rng(1):rng(2)
        ct=ct+1;
        handles.currentImg=i;
        handles=updateFigure(handles); 
        handles=addMsg(handles,'----------'); 
        handles=addMsg(handles,['Image ',num2str(i),' ',handles.data.imLib(i).name,handles.data.imLib(i).suffix]);  
        handles=updateCounts(handles);
        handles.gray=[];
        handles.bw=[];
        if size(handles.rgb,3)==3
            handles.gray=rgb2gray(handles.rgb);
        else
            handles.gray=handles.rgb;
        end
        handles.bw=imbinarize(handles.gray,handles.setting.bw_thre); 
        
        disp([num2str(i),'seperate object']);
        handles=func_seperate_object(handles);
        disp([num2str(i),'detect_axis'])
        handles=func_detect_axis(handles);
        try
            disp([num2str(i),'analyse_legend'])
            handles=func_analyse_legend(handles);        
%             disp([num2str(i),'symbol_recognition'])
%             handles=func_symbol_recognition(handles);
        end
        handles.data.msg=handles.Table_msg.Data;
        savedata=handles.data;
        if mod(ct,10)==0
            %save(['E:\Data\Literature Data\project.mat'],'savedata');
        end
    end
    %save(['E:\Data\Literature Data\project.mat'],'savedata');

function handles=func_autorun2(handles)
    rng=handles.processRange;
    ct=0;
    for i=rng(1):rng(2)
        ct=ct+1;
        handles.currentImg=i;
        handles=updateFigure(handles); 
        handles=addMsg(handles,'----------'); 
        handles=addMsg(handles,['Image ',num2str(i),' ',handles.data.imLib(i).name,handles.data.imLib(i).suffix]);  
        handles=updateCounts(handles);
        handles.gray=[];
        handles.bw=[];
        if size(handles.rgb,3)==3
            handles.gray=rgb2gray(handles.rgb);
        else
            handles.gray=handles.rgb;
        end
        handles.bw=imbinarize(handles.gray,handles.setting.bw_thre); 
        
        disp([num2str(i),'seperate object']);
        handles=func_seperate_object(handles);
        disp([num2str(i),'detect_axis'])
        handles=func_detect_axis(handles);
        try
            disp([num2str(i),'analyse_legend'])
            handles=func_analyse_legend(handles);        
            disp([num2str(i),'symbol_recognition_color'])
            handles=func_symbol_recognition_color(handles);
        end
        handles.data.msg=handles.Table_msg.Data;
        savedata=handles.data;
        %if mod(ct,10)==0
        %    save(['E:\Data\Literature Data\project.mat'],'savedata');
        %end
    end
    %save(['E:\Data\Literature Data\project.mat'],'savedata');    
    
function handles=func_auto_axis(handles)    
    rng=handles.processRange;
    ct=0;
    for i=rng(1):rng(2)
        ct=ct+1;
        handles.currentImg=i;
        handles=updateFigure(handles);
        handles=updateCounts(handles);
        handles.gray=[];
        handles.bw=[];
        if size(handles.rgb,3)==3
            handles.gray=rgb2gray(handles.rgb);
        else
            handles.gray=handles.rgb;
        end
        handles.bw=imbinarize(handles.gray,handles.setting.bw_thre); 
        disp([num2str(i),' detect_axis'])
        try
            handles=func_detect_axis(handles);
        end
        handles.data.msg=handles.Table_msg.Data;
        savedata=handles.data;
        if mod(ct,10)==0
            save(['E:\Data\Literature Data\project_1-500_axis.mat'],'savedata');
        end        
    end
    save(['E:\Data\Literature Data\project_1-500_axis.mat'],'savedata');
    
function handles=func_legend_select(handles)
    if handles.legendselect==0
        handles.legendselect=1;
        handles.boxselect.flag=1;
    else
        handles.boxselect.flag=0;
        handles.legendselect=0;
        handles=savedata_legend_preselect(handles);
        handles=display_data_detail(handles,'preselect');
        handles=boxselectInitialize(handles);
        handles=selectionInitialize(handles);
        handles=updateImage2(handles);
    end
    if handles.legendselect
        handles.But_legendSelect.BackgroundColor=[0.7,0.7,1.0];
    else
        handles.But_legendSelect.BackgroundColor=[0.94,0.94,0.94];
    end                

function handles=func_key_onoff(handles)
    handles.keyon=~handles.keyon;
    if handles.keyon
        handles.But_keyonoff.BackgroundColor=[0.7,0.7,1.0];
    else
        handles.But_keyonoff.BackgroundColor=[0.94,0.94,0.94];
    end      
    
function handles=func_clear_data_seires(handles)
    ci=handles.currentImg;
    handles.data.imLib(ci).data.colorpick=0;
    for j=1:numel(handles.data.imLib(ci).data.series)
        handles.data.imLib(ci).data.series(j).pdata=[];
        handles.data.imLib(ci).data.series(j).auto=[];
        handles.data.imLib(ci).data.series(j).runout=[];
    end
    handles=display_data_detail(handles,'');

function handles=func_delete_data_seires(handles)
    ci=handles.currentImg;
    cp=handles.currentProperty;
    n=str2num(cp(8:end));    
    handles.data.imLib(ci).data.state='';
    rng=[1:handles.data.imLib(ci).data.nseries];
    rng=rng(~ismember(rng,n));
    handles.data.imLib(ci).data.nseries=handles.data.imLib(ci).data.nseries-1;
    handles.data.imLib(ci).data.series=handles.data.imLib(ci).data.series(rng); 
    handles.data.imLib(ci).legend.nitem=handles.data.imLib(ci).legend.nitem-1;
    handles.data.imLib(ci).legend.state='';
    handles.data.imLib(ci).legend.item=handles.data.imLib(ci).legend.item(rng);
    if handles.data.imLib(ci).data.nseries==0
        handles.data.imLib(ci).data.exist=0;
        handles.data.imLib(ci).data.colorpick=0;
    end
    if handles.data.imLib(ci).legend.nitem==0
        handles.data.imLib(ci).legend.exist=0;
    end    
    handles=display_data_table(handles);
    handles=display_data_detail(handles,'');    
    
function handles=func_pick_anchor(handles)
    handles.pickAnchor=~handles.pickAnchor;
    if handles.pickAnchor
        handles.But_pickAnchor.BackgroundColor=[0.7,0.7,1.0];
    else
        handles.But_pickAnchor.BackgroundColor=[0.94,0.94,0.94];
    end                
 
function handles=func_pick_color(handles)
    if handles.pickcolor==0
        handles.pickcolor=1;
    else
        handles.pickcolor=0;
        handles.Text_red.String='R ';
        handles.Text_green.String='G ';
        handles.Text_blue.String='B ';
        handles.currentColor=uint8([]);
    end
    if handles.pickcolor
        handles.But_pickColor.BackgroundColor=[0.7,0.7,1.0];
    else
        handles.But_pickColor.BackgroundColor=[0.94,0.94,0.94];
    end     

function handles=func_select_color(handles)    
    c=handles.currentColor;
    if isempty(c)
        return
    end
    handles.rgb=handles.rgb0;
    rgb=handles.rgb;
    h=handles.imHeight;
    w=handles.imWidth;
    crit=handles.color_tolerance;
    if ~sum(isnan(c),'all')
        delta=abs(double(rgb)-double(c));
        delr=delta(:,:,1);
        delg=delta(:,:,2);
        delb=delta(:,:,3);
        indr=find(delr<=crit);
        indg=find(delg<=crit);
        indb=find(delb<=crit);
        tmp=intersect(indr,indg);
        candidate=intersect(tmp,indb);
        [I,J]=ind2sub([h,w],candidate);
        for i=1:numel(I)
            handles.rgb(I(i),J(i),:)=uint8(reshape([255,255,0],[1,1,3]));
        end
        handles.pixelRecord=[J,I];
        handles=updateImage(handles);
    end

function handles=func_add_color(handles)    
    c=handles.currentColor;
    if isempty(c)
        return
    end
    rgb=handles.rgb;
    h=handles.imHeight;
    w=handles.imWidth;
    crit=30;
    if ~sum(isnan(c),'all')
        delta=abs(double(rgb)-double(c));
        delr=delta(:,:,1);
        delg=delta(:,:,2);
        delb=delta(:,:,3);
        indr=find(delr<=crit);
        indg=find(delg<=crit);
        indb=find(delb<=crit);
        tmp=intersect(indr,indg);
        candidate=intersect(tmp,indb);
        [I,J]=ind2sub([h,w],candidate);
        n1=numel(I);
        for i=1:n1
            handles.rgb(I(i),J(i),:)=uint8(reshape([255,255,0],[1,1,3]));
        end
        n=size(handles.pixelRecord,1);
        if n==0
            handles.pixelRecord=[J,I];
        else
            handles.pixelRecord(n+1:n+n1,:)=[J,I];
        end
        handles=updateImage(handles);
    end    
    
function handles=func_reset_color(handles)    
    handles.rgb=handles.rgb0;
    handles.pixelRecord=[];
    handles=updateImage(handles);
    
    
function handles=func_eraser_on(handles)
    handles.eraser_on=~handles.eraser_on;
    
    if handles.eraser_on
        handles.But_eraser.BackgroundColor=[0.7,0.7,1.0];
        handles.eraser_handle=plot([]);
    else
        handles.But_eraser.BackgroundColor=[0.94,0.94,0.94];
        if isfield(handles,'eraser_handle') 
            delete(handles.eraser_handle); 
        end
        handles=display_data_detail(handles,handles.currentProperty);
    end    

function handles=func_switch_shape_color_pick(handles)    
    ci=handles.currentImg;
    if isfield(handles.data.imLib(ci).data,'colorpick')
        handles.data.imLib(ci).data.colorpick=~handles.data.imLib(ci).data.colorpick;
    else
        handles.data.imLib(ci).data.colorpick=0;
    end

function handles=add_data_point(handles,pos0)
    cp=handles.currentProperty;
    ci=handles.currentImg;
    n=str2num(cp(8:end));
    if ~isfield(handles.data.imLib(ci).data.series(n),'pdata')
        handles.data.imLib(ci).data.series(n).pdata=[];
    end
    nr=size(handles.data.imLib(ci).data.series(n).pdata,1);
    nr=nr+1;
    handles.data.imLib(ci).data.series(n).pdata(nr,:)=pos0;
    handles.data.imLib(ci).data.series(n).auto(nr,:)=0;
    handles.data.imLib(ci).data.series(n).runout(nr)=0;
    handles=display_data_detail(handles,cp);
    handles=show_item_box(handles,cp);
    handles.selection.subset=[nr];
    handles.selection.nsub=1;
    handles=select_data_series_subset(handles,ci,n);   
    
function handles=savedata_detect_coordinate(handles,ci,pos_xa,pos_ya,coordObid)
    % pos_xa
    if handles.data.imLib(ci).axis.pos_xa.exist==1
        handles.data.imLib(ci).axis.pos_xa.n_mod=handles.data.imLib(ci).axis.pos_xa.n_mod+1;
        handles.data.imLib(ci).axis.pos_xa.mod(handles.data.imLib(ci).axis.pos_xa.n_mod)=handles.data.imLib(ci).axis.pos_xa.data;
    end 
    handles.data.imLib(ci).axis.pos_xa.exist=1;
    handles.data.imLib(ci).axis.pos_xa.state='auto';
    handles.data.imLib(ci).axis.pos_xa.data=pos_xa;
    % pos_ya
    if handles.data.imLib(ci).axis.pos_ya.exist==1
        handles.data.imLib(ci).axis.pos_ya.n_mod=handles.data.imLib(ci).axis.pos_ya.n_mod+1;
        handles.data.imLib(ci).axis.pos_ya.mod(handles.data.imLib(ci).axis.pos_ya.n_mod)=handles.data.imLib(ci).axis.pos_ya.data;
    end 
    handles.data.imLib(ci).axis.pos_ya.exist=1;
    handles.data.imLib(ci).axis.pos_ya.state='auto';
    handles.data.imLib(ci).axis.pos_ya.data=pos_ya;    
    % coordObid, the object id of the coordinate system
    handles.data.imLib(ci).axis.coordObid=coordObid;
    
    
function handles=savedata_axis_character(handles,xxlabel,yylabel,xxlabels,yylabels,xlabcl_box,ylabcl_box,xxtick_num,yytick_num,xxtick_str,yytick_str,xtlcl_box,ytlcl_box)
    % % xlabel
    ci=handles.currentImg;
%     if handles.data.imLib(ci).axis.xLabel.exist==1
%         handles.data.imLib(ci).axis.xLabel.n_mod=handles.data.imLib(ci).axis.xLabel.n_mod+1;
%         handles.data.imLib(ci).axis.xLabel.mod(handles.data.imLib(ci).axis.xLabel.n_mod)=handles.data.imLib(ci).axis.xLabel.data;
%     end    
    handles.data.imLib(ci).axis.xLabel.exist=1;
    handles.data.imLib(ci).axis.xLabel.state='auto';
    handles.data.imLib(ci).axis.xLabel.text=xxlabel;
    handles.data.imLib(ci).axis.xLabel.data=xxlabels;
    handles.data.imLib(ci).axis.xLabel.box=xlabcl_box;
    
    % % ylabel
%     if handles.data.imLib(ci).axis.yLabel.exist==1
%         handles.data.imLib(ci).axis.yLabel.n_mod=handles.data.imLib(ci).axis.yLabel.n_mod+1;
%         handles.data.imLib(ci).axis.yLabel.mod(handles.data.imLib(ci).axis.yLabel.n_mod)=handles.data.imLib(ci).axis.yLabel.data;
%     end    
    handles.data.imLib(ci).axis.yLabel.exist=1;
    handles.data.imLib(ci).axis.yLabel.state='auto';
    handles.data.imLib(ci).axis.yLabel.text=yylabel;
    handles.data.imLib(ci).axis.yLabel.data=yylabels;
    handles.data.imLib(ci).axis.yLabel.box=ylabcl_box;
    
    % % xticks
%     if handles.data.imLib(ci).axis.xTicks.exist==1
%         handles.data.imLib(ci).axis.xTicks.n_mod=handles.data.imLib(ci).axis.xTicks.n_mod+1;
%         handles.data.imLib(ci).axis.xTicks.mod(handles.data.imLib(ci).axis.xTicks.n_mod)=handles.data.imLib(ci).axis.xTicks.data;
%     end    
    handles.data.imLib(ci).axis.xTicks.exist=1;
    handles.data.imLib(ci).axis.xTicks.state='auto';
    handles.data.imLib(ci).axis.xTicks.box=xtlcl_box;
    handles.data.imLib(ci).axis.xTicks.data=xxtick_num;
    handles.data.imLib(ci).axis.xTicks.datastr=xxtick_str;
    
    % % yticks
%     if handles.data.imLib(ci).axis.yTicks.exist==1
%         handles.data.imLib(ci).axis.yTicks.n_mod=handles.data.imLib(ci).axis.yTicks.n_mod+1;
%         handles.data.imLib(ci).axis.yTicks.mod(handles.data.imLib(ci).axis.yTicks.n_mod)=handles.data.imLib(ci).axis.yTicks.data;
%     end      
    handles.data.imLib(ci).axis.yTicks.exist=1;
    handles.data.imLib(ci).axis.yTicks.state='auto';
    handles.data.imLib(ci).axis.yTicks.box=ytlcl_box;
    handles.data.imLib(ci).axis.yTicks.data=yytick_num;
    handles.data.imLib(ci).axis.yTicks.datastr=yytick_str;

function handles=savedata_calibrate_axis(handles,px1,px2,py1,py2,x1,x2,y1,y2)    
    ci=handles.currentImg;
    handles.data.imLib(ci).axis.xAnchor.exist=1;
    handles.data.imLib(ci).axis.yAnchor.exist=1;
    handles.data.imLib(ci).axis.xAnchor.pos(1,1)=px1;
    handles.data.imLib(ci).axis.xAnchor.pos(2,1)=px2;
    if handles.data.imLib(ci).axis.pos_xa.exist
        handles.data.imLib(ci).axis.xAnchor.pos(1,2)=handles.data.imLib(ci).axis.pos_xa.data;
        handles.data.imLib(ci).axis.xAnchor.pos(2,2)=handles.data.imLib(ci).axis.pos_xa.data;
    else
        handles.data.imLib(ci).axis.xAnchor.pos(1,2)=handles.data.imLib(ci).imHeight;
        handles.data.imLib(ci).axis.xAnchor.pos(2,2)=handles.data.imLib(ci).imHeight;
    end
    handles.data.imLib(ci).axis.xAnchor.data=[x1,x2];
    
    handles.data.imLib(ci).axis.yAnchor.pos(1,2)=py1;
    handles.data.imLib(ci).axis.yAnchor.pos(2,2)=py2;    
    if handles.data.imLib(ci).axis.pos_ya.exist
        handles.data.imLib(ci).axis.yAnchor.pos(1,1)=handles.data.imLib(ci).axis.pos_ya.data-5;
        handles.data.imLib(ci).axis.yAnchor.pos(2,1)=handles.data.imLib(ci).axis.pos_ya.data-5;
    else
        handles.data.imLib(ci).axis.yAnchor.pos(1,1)=1;
        handles.data.imLib(ci).axis.yAnchor.pos(2,1)=1;        
    end    
    handles.data.imLib(ci).axis.yAnchor.data=[y1,y2];    

    
function handles=savedata_legend_preselect(handles)
    ci=handles.currentImg;
    handles.data.imLib(ci).legend.preselect.exist=1;
    handles.data.imLib(ci).legend.preselect.nbox=handles.boxselect.n;
    handles.data.imLib(ci).legend.preselect.box=handles.boxselect.xyrng;
    handles.data.imLib(ci).legend.preselect.rcrng=handles.boxselect.rcrng;
   
    
function handles=savedata_symbol_recognition(handles,ifreg,xreg,yreg,type,overlap)
    ci=handles.currentImg;
    handles.data.imLib(ci).data.exist=1;
    handles.data.imLib(ci).data.state='auto';
    ns=handles.data.imLib(ci).legend.nitem;
    handles.data.imLib(ci).data.nseries=ns;
    if ~isfield(handles.data.imLib(ci).data,'series')
        handles.data.imLib(ci).data.series(1)=struct();
    end
    for i=1:ns
        handles.data.imLib(ci).data.series(i).text=handles.data.imLib(ci).legend.item(i).text;
    end
    nob=numel(ifreg);
    count=zeros(1,handles.data.imLib(ci).data.nseries);
    for i=1:nob
        if type(i)>0
            count(type(i))=count(type(i))+1;
            handles.data.imLib(ci).data.series(type(i)).pdata(count(type(i)),:)=[xreg(i),yreg(i)];
            handles.data.imLib(ci).data.series(type(i)).auto(count(type(i)),:)=1;
            handles.data.imLib(ci).data.series(type(i)).runout(count(type(i)),:)=0;
        end
    end
    
function handles=savedata_symbol_recognition_color(handles,data)
    ci=handles.currentImg;
    handles.data.imLib(ci).data.exist=1;
    handles.data.imLib(ci).data.state='auto';
    ns=handles.data.imLib(ci).legend.nitem;
    handles.data.imLib(ci).data.nseries=ns;
    handles.data.imLib(ci).data.colorpick=1;
    if ~isfield(handles.data.imLib(ci).data,'series')
        handles.data.imLib(ci).data.series(1)=struct();
    end
    for i=1:ns
        handles.data.imLib(ci).data.series(i).text=handles.data.imLib(ci).legend.item(i).text;
    end
    nob=numel(data);
    count=zeros(1,handles.data.imLib(ci).data.nseries);
    for i=1:nob
        handles.data.imLib(ci).data.series(i).pdata=data{i};
        nrow=size(data{i},1);
        handles.data.imLib(ci).data.series(i).auto=zeros(nrow,1)+1;
        handles.data.imLib(ci).data.series(i).runout=zeros(nrow,1);
    end
    
function   handles=imLib_var_init(handles) 
    n=numel(handles.data.imLib);
    for i=1:n
        handles.data.imLib(i).sepobj.exist=0;
        % % Axis
        % pos_xa
        handles.data.imLib(i).axis.pos_xa.exist=0;
        handles.data.imLib(i).axis.pos_xa.state='';
        handles.data.imLib(i).axis.pos_xa.data=nan;
        handles.data.imLib(i).axis.pos_xa.n_mod=0;
        handles.data.imLib(i).axis.pos_xa.mod=[];
        % pos_ya
        handles.data.imLib(i).axis.pos_ya.exist=0;
        handles.data.imLib(i).axis.pos_ya.state='';
        handles.data.imLib(i).axis.pos_ya.data=nan;
        handles.data.imLib(i).axis.pos_ya.n_mod=0;
        handles.data.imLib(i).axis.pos_ya.mod=[];    
        %
        handles.data.imLib(i).axis.coordObid=nan;
        % xLabel, yLabel, xTicks, yTicks
        handles.data.imLib(i).axis.xLabel=struct();
        handles.data.imLib(i).axis.yLabel=struct();
        handles.data.imLib(i).axis.xTicks=struct();
        handles.data.imLib(i).axis.yTicks=struct();
        handles.data.imLib(i).axis.xLabel.exist=0;
        handles.data.imLib(i).axis.yLabel.exist=0;
        handles.data.imLib(i).axis.xTicks.exist=0;
        handles.data.imLib(i).axis.yTicks.exist=0;  
        handles.data.imLib(i).axis.xLabel.data2='life';
        handles.data.imLib(i).axis.yLabel.data2='amp';
        handles.data.imLib(i).axis.xLabel.unit='cycles';
        handles.data.imLib(i).axis.yLabel.unit='MPa';        
        % xScale, yScale
        handles.data.imLib(i).axis.xScale='log';
        handles.data.imLib(i).axis.yScale='linear';
        % xAnchor,yAnchor
        handles.data.imLib(i).axis.xAnchor=struct();
        handles.data.imLib(i).axis.xAnchor.pos=[nan,nan;nan,nan];
        handles.data.imLib(i).axis.xAnchor.data=[];
        handles.data.imLib(i).axis.yAnchor=struct();
        handles.data.imLib(i).axis.yAnchor.pos=[nan,nan;nan,nan];
        handles.data.imLib(i).axis.yAnchor.data=[];        
        
        % % Legend
        handles.data.imLib(i).legend.preselect.exist=0;
        handles.data.imLib(i).legend.preselect.box=[];
        handles.data.imLib(i).legend.preselect.rcrng=[]; 
        handles.data.imLib(i).legend.preselect.nbox=0;
        handles=imLib_legend_init(handles,i);
        
        % % Data
        handles=imLib_data_init(handles,i);
    end

    
function handles=imLib_legend_init(handles,i)
    handles.data.imLib(i).legend.nitem=0;
    handles.data.imLib(i).legend.item=struct([]);
    handles.data.imLib(i).legend.exist=0;
    handles.data.imLib(i).legend.state='';

function handles=imLib_data_init(handles,i)
    handles.data.imLib(i).data.nseries=0;
    handles.data.imLib(i).data.series=struct([]);
    handles.data.imLib(i).data.exist=0;
    handles.data.imLib(i).data.state='';    
    
    
function handles=savedata_analyse_legend(handles,ci,symbol,word,color,box)
    ci=handles.currentImg;
    n=numel(symbol);
    handles.data.imLib(ci).legend.exist=1;
    ni=handles.data.imLib(ci).legend.nitem;
    for i=ni+1:ni+n
        handles.data.imLib(ci).legend.item(i).symbol=symbol{i-ni};
        handles.data.imLib(ci).legend.item(i).text=word{i-ni};
        handles.data.imLib(ci).legend.item(i).color=color{i-ni};
        handles.data.imLib(ci).legend.item(i).box=box{i-ni};
    end
    handles.data.imLib(ci).legend.nitem=ni+n;   

function handles=savedata_add_data_series(handles)    
    ci=handles.currentImg;
    if handles.boxselect.n>0
        n=handles.data.imLib(ci).legend.nitem;
        n=n+1;
        handles.data.imLib(ci).legend.nitem=n;
        if n==1 && (numel(fieldnames(handles.data.imLib(ci).legend.item))==0)
            handles.data.imLib(ci).legend.item(n)=struct();
        end
        handles.data.imLib(ci).legend.exist=1;
        handles.data.imLib(ci).legend.data.exist=1;
        bx=handles.boxselect.rcrng(end,:);
        handles.data.imLib(ci).legend.item(n).box={[bx(3),bx(4),bx(1),bx(2)],[nan,nan,nan,nan]};
        if isempty(handles.gray)
            handles.gray=rgb2gray(handles.rgb);
        end        
        if isempty(handles.bw)
            handles.bw=imbinarize(handles.gray,handles.setting.bw_thre);
        end   
        handles.data.imLib(ci).legend.item(n).symbol=handles.bw(bx(1):bx(2),bx(3):bx(4));
        handles.data.imLib(ci).legend.item(n).text='';
        handles.data.imLib(ci).legend.item(n).color=[nan,nan,nan];
        
        handles.data.imLib(ci).data.nseries=n;
        if n==1 && (numel(fieldnames(handles.data.imLib(ci).data.series))==0)
            handles.data.imLib(ci).data.series(n)=struct();
        end
        handles.data.imLib(ci).data.series(n).type=n;
        handles.data.imLib(ci).data.series(n).pdata=[];
    end

    
function handles=detect_boxselected_objects(handles)    
    ci=handles.currentImg;
    cp=handles.currentProperty;
    n=str2num(cp(8:end));
    data=handles.data.imLib(ci).data.series(n).pdata;
    nr=size(data,1);
    bx=handles.boxselect.xyrng(1,:);
    handles.selection.subset=[];
    nsub=0;
    for i=1:nr
        if inbox1(data(i,:),bx)
            nsub=nsub+1;
            handles.selection.subset(nsub)=i;
        end
    end
    handles.selection.nsub=nsub;
  
function handles=select_data_series_subset(handles,ci,n)
    id=handles.selection.subset;
    nr=size(handles.data.imLib(ci).data.series(n).pdata,1);
    if numel(id)==1
        handles.Text_selectedObject.String=['Data s ',num2str(n),' d ',num2str(id)];
    else
        handles.Text_selectedObject.String=['Data s ',num2str(n),' d multi.'];
    end
    for i=1:nr
        if ismember(i,id)
            handles.plot.selection.hd(i).Marker='+';
            handles.plot.selection.hd(i).MarkerEdgeColor='y';
        else
            handles.plot.selection.hd(i).Marker='o';
            handles.plot.selection.hd(i).MarkerEdgeColor='k';
        end
    end

function handles=select_axis_anchor_subset(handles,ci)
    id=handles.selection.subset;
    if id==1
        handles.Text_selectedObject.String=['xAnchor low'];
    elseif id==2
        handles.Text_selectedObject.String=['xAnchor high'];
    elseif id==3
        handles.Text_selectedObject.String=['yAnchor low'];
    elseif id==4
        handles.Text_selectedObject.String=['yAnchor high'];        
    else
        handles.Text_selectedObject.String=[''];
    end
    for i=1:4
        if ismember(i,id)
            handles.plot.selection.hd(i).MarkerEdgeColor='y';
        else
            handles.plot.selection.hd(i).MarkerEdgeColor='w';
        end
    end    
    
function handles=move_data_point(handles)    
    ci=handles.currentImg;
    cp=handles.currentProperty;
    if ~isempty(strfind(cp,'series'))
        sid=str2num(cp(8:end));
        if handles.selection.nsub==1
            id=handles.selection.subset(1);
            if strcmp(handles.movdir,'up')
                handles.data.imLib(ci).data.series(sid).pdata(id,2)=handles.data.imLib(ci).data.series(sid).pdata(id,2)-handles.movstep;
            elseif strcmp(handles.movdir,'down')
                handles.data.imLib(ci).data.series(sid).pdata(id,2)=handles.data.imLib(ci).data.series(sid).pdata(id,2)+handles.movstep;
            elseif strcmp(handles.movdir,'left')
                handles.data.imLib(ci).data.series(sid).pdata(id,1)=handles.data.imLib(ci).data.series(sid).pdata(id,1)-handles.movstep;
            elseif strcmp(handles.movdir,'right')
                handles.data.imLib(ci).data.series(sid).pdata(id,1)=handles.data.imLib(ci).data.series(sid).pdata(id,1)+handles.movstep; 
            end
        end
        handles=display_data_detail(handles,cp);
        handles=show_item_box(handles,cp);

        pos=handles.data.imLib(ci).data.series(sid).pdata(id,:);
        handles.axes2.XLim=[pos(1)-handles.minLen*0.03,pos(1)+handles.minLen*0.03];
        handles.axes2.YLim=[pos(2)-handles.minLen*0.03,pos(2)+handles.minLen*0.03];
        handles.ax2cross(1).XData=[pos(1)-handles.minLen*0.015,pos(1)+handles.minLen*0.015];
        handles.ax2cross(1).YData=[pos(2),pos(2)];
        handles.ax2cross(2).XData=[pos(1),pos(1)];
        handles.ax2cross(2).YData=[pos(2)-handles.minLen*0.015,pos(2)+handles.minLen*0.015];
        
    elseif ~isempty(strfind(cp,'Anchor'))
        if handles.selection.nsub==1
            id=handles.selection.subset(1);
            if id<=2
                id2=id;
                if strcmp(handles.movdir,'left')
                    handles.data.imLib(ci).axis.xAnchor.pos(id2,1)=handles.data.imLib(ci).axis.xAnchor.pos(id2,1)-handles.movstep;
                elseif strcmp(handles.movdir,'right')
                    handles.data.imLib(ci).axis.xAnchor.pos(id2,1)=handles.data.imLib(ci).axis.xAnchor.pos(id2,1)+handles.movstep; 
                elseif strcmp(handles.movdir,'up')
                    handles.data.imLib(ci).axis.xAnchor.pos(id2,2)=handles.data.imLib(ci).axis.xAnchor.pos(id2,2)-handles.movstep;
                elseif strcmp(handles.movdir,'down')
                    handles.data.imLib(ci).axis.xAnchor.pos(id2,2)=handles.data.imLib(ci).axis.xAnchor.pos(id2,2)+handles.movstep; 
                end
                pos=handles.data.imLib(ci).axis.xAnchor.pos(id2,:);
            else
                id2=id-2;
                if strcmp(handles.movdir,'left')
                    handles.data.imLib(ci).axis.yAnchor.pos(id2,1)=handles.data.imLib(ci).axis.yAnchor.pos(id2,1)-handles.movstep;
                elseif strcmp(handles.movdir,'right')
                    handles.data.imLib(ci).axis.yAnchor.pos(id2,1)=handles.data.imLib(ci).axis.yAnchor.pos(id2,1)+handles.movstep;                
                elseif strcmp(handles.movdir,'up')
                    handles.data.imLib(ci).axis.yAnchor.pos(id2,2)=handles.data.imLib(ci).axis.yAnchor.pos(id2,2)-handles.movstep;
                elseif strcmp(handles.movdir,'down')
                    handles.data.imLib(ci).axis.yAnchor.pos(id2,2)=handles.data.imLib(ci).axis.yAnchor.pos(id2,2)+handles.movstep;
                end
                pos=handles.data.imLib(ci).axis.yAnchor.pos(id2,:);
            end
        end
        handles=display_data_detail(handles,cp);
        handles=show_item_box(handles,cp);
        handles.axes2.XLim=[pos(1)-handles.minLen*0.03,pos(1)+handles.minLen*0.03];
        handles.axes2.YLim=[pos(2)-handles.minLen*0.03,pos(2)+handles.minLen*0.03];
        handles.ax2cross(1).XData=[pos(1)-handles.minLen*0.015,pos(1)+handles.minLen*0.015];
        handles.ax2cross(1).YData=[pos(2),pos(2)];
        handles.ax2cross(2).XData=[pos(1),pos(1)];
        handles.ax2cross(2).YData=[pos(2)-handles.minLen*0.015,pos(2)+handles.minLen*0.015];        
    end
   
function handles=update_anchor(handles)   
    ci=handles.currentImg;
    id=handles.anchorID;
    mapos=handles.axes1.CurrentPoint(1,1:2);
    if id==1
        handles.data.imLib(ci).axis.xAnchor.pos(1,:)=mapos;
    elseif id==2
        handles.data.imLib(ci).axis.xAnchor.pos(2,:)=mapos;
    elseif id==3
        handles.data.imLib(ci).axis.yAnchor.pos(1,:)=mapos;
    elseif id==4
        handles.data.imLib(ci).axis.yAnchor.pos(2,:)=mapos;
    end
    handles.movdir='';
    handles=move_data_point(handles);
    
function handles=clear_axes3(handles)
    cla(handles.axes3);
    imshow([1],'Parent',handles.axes3);

function string=strip_char_1(string0)
    string='';
    for i=1:numel(string0)
        if (~strcmp(string0(i),'\n'))&&abs(string0(i))~=8629  % 8629: the ascii of 
            string=[string,string0(i)];
        end
    end
    
function handles=eraser_initialize(handles)
    handles.eraser_on=0;
    handles.erasing=0;
    handles.eraser_size=round(0.05*min(handles.imWidth,handles.imHeight));
    handles.Edit_eraseSize.String=num2str(handles.eraser_size);
    handles.eraser_handle=plot([]);
    
function handles=erase_data(handles,pos)
    cp=handles.currentProperty;
	if ~isempty(strfind(cp,'series'))
        n=str2num(cp(8:end));    
        ci=handles.currentImg;
        pd=handles.data.imLib(ci).data.series(n).pdata;
        delta=sum(abs(pd-pos),2);
        id=find(delta>=handles.eraser_size);
        handles.data.imLib(ci).data.series(n).pdata=handles.data.imLib(ci).data.series(n).pdata(id,:);
        pd=handles.data.imLib(ci).data.series(n).pdata;
        nd=size(pd,1);
%         id=sub2ind([handles.imHeight,handles.imWidth,3],pd(:,1),pd(:,2),zeros(nd,1)+1);
%         handles.axes1.Children(end).CData(id)=handles.rgb0(id);
%         id=sub2ind([handles.imHeight,handles.imWidth,3],pd(:,1),pd(:,2),zeros(nd,1)+2);
%         handles.axes1.Children(end).CData(id)=handles.rgb0(id);    
%         id=sub2ind([handles.imHeight,handles.imWidth,3],pd(:,1),pd(:,2),zeros(nd,1)+3);
%         handles.axes1.Children(end).CData(id)=handles.rgb0(id);             
        handles=show_item_box(handles,cp);
        handles=display_data_detail(handles,cp);
    end    

function handles=plot_eraser(handles,pos)
    s=handles.eraser_size;
    if size(handles.eraser_handle,1)==1
        handles.eraser_handle.XData=[pos(1),pos(1)+s,pos(1),pos(1)-s,pos(1)];
        handles.eraser_handle.YData=[pos(2)+s,pos(2),pos(2)-s,pos(2),pos(2)+s];
    else
        %handles.axes1.NextPlot='add';
        handles.eraser_handle=plot(handles.axes1,[pos(1),pos(1)+s,pos(1),pos(1)-s,pos(1)],[pos(2)+s,pos(2),pos(2)-s,pos(2),pos(2)+s],'color','k','LineWidth',0.5);
        %handles.axes1.NextPlot='replace';
    end
