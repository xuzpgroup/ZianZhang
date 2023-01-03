function varargout = datacorrect(varargin)
% DATACORRECT MATLAB code for datacorrect.fig
%      DATACORRECT, by itself, creates a new DATACORRECT or raises the existing
%      singleton*.
%
%      H = DATACORRECT returns the handle to a new DATACORRECT or the handle to
%      the existing singleton*.
%
%      DATACORRECT('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in DATACORRECT.M with the given input arguments.
%
%      DATACORRECT('Property','Value',...) creates a new DATACORRECT or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before datacorrect_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to datacorrect_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help datacorrect

% Last Modified by GUIDE v2.5 06-Jul-2022 12:10:05

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @datacorrect_OpeningFcn, ...
                   'gui_OutputFcn',  @datacorrect_OutputFcn, ...
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


% --- Executes just before datacorrect is made visible.
function datacorrect_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to datacorrect (see VARARGIN)

% Choose default command line output for datacorrect
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes datacorrect wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = datacorrect_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;
