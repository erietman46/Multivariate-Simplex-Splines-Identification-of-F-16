%F16_IOmapping.m
%
%   Description:
%       This file shows how load and plot the IO mapping of the F16 aerodynamic coefficient C_m.
%
%   Construction date:  17-06-2009
%   Last updated:       17-03-2024
%
%   C.C. de Visser
%   TUDelft, Faculty of Aerospace Engineering, Division of Control &
%   Simulation


%%   Clearing workspace
clear all
close all
clc

printfigs = 1; % 1: print figures to disk as PNG
figpath = ''; % set the path where the figures will be printed

warning('WARNING: This file was written for Matlab R2020B, some functions may not be compatible in later versions');

%%   Loading data
dataname = 'F16traindata_CMabV_2026';
valdataname = 'F16validationdata_2026';
% measurement dataset
load(dataname, 'Cm', 'Z_k', 'U_k')
% special validation dataset
load(valdataname, 'Cm_val', 'alpha_val', 'beta_val')

% measurements Z_k = Z(t) + v(t)
alpha_m = Z_k(:,1); % measured angle of attack
beta_m = Z_k(:,2);  % measured angle of sideslip
Vtot = Z_k(:,3);    % measured velocity

% input to Kalman filter
Au = U_k(:,1); % perfect accelerometer du/dt data
Av = U_k(:,2); % perfect accelerometer dv/dt data
Aw = U_k(:,3); % perfect accelerometer dw/dt data


%%   Plotting results
close all;
%---------------------------------------------------------
% creating triangulation (only used for plotting here)
TRIeval = delaunayn(Z_k(:, [1 2]));

%   viewing angles
az = 140;
el = 36;

% create figures

plotID = 101;
figure(plotID);
set(plotID, 'Position', [0 100 900 500], 'defaultaxesfontsize', 10, 'defaulttextfontsize', 10, 'color', [1 1 1], 'PaperPositionMode', 'auto');
% plot data points
plot3(alpha_m, beta_m, Cm, '.k'); % note that alpha_m = alpha, beta_m = beta, y = Cm
view(0, 90); 
ylabel('beta [rad]');
xlabel('alpha [rad]');
zlabel('C_m [-]');
title('F16 CM(\alpha_m, \beta_m) raw measurements only');
% print results to disk if printfigs = 1
if (printfigs == 1)
    fpath = sprintf('fig_F16data3D');
    savefname = strcat(figpath, fpath);
    print(plotID, '-dpng', '-r300', savefname);
end



plotID = 1001;
figure(plotID);
set(plotID, 'Position', [800 100 900 500], 'defaultaxesfontsize', 10, 'defaulttextfontsize', 10, 'color', [1 1 1], 'PaperPositionMode', 'auto');
trisurf(TRIeval, alpha_m, beta_m, Cm, 'EdgeColor', 'none'); 
grid on;
hold on;
% plot data points
plot3(alpha_m, beta_m, Cm, '.k'); % note that alpha_m = alpha, beta_m = beta, y = Cm
view(az, el);
ylabel('beta [rad]');
xlabel('alpha [rad]');
zlabel('C_m [-]');
title('F16 CM(\alpha_m, \beta_m) raw interpolation');
% set fancy options for plotting 
set(gcf,'Renderer','OpenGL');
hold on;
poslight = light('Position',[0.5 .5 15],'Style','local');
hlight = camlight('headlight');
material([.3 .8 .9 25]);
minz = min(Cm);
shading interp;
lighting phong;
drawnow();
% print results to disk if printfigs = 1
if (printfigs == 1)
    fpath = sprintf('fig_F16data3DSurf');
    savefname = strcat(figpath, fpath);
    print(plotID, '-dpng', '-r300', savefname);
end

% if the Cm_val matrix exists, then a special validation set is used in this year's assigment
if (exist('Cm_val'))
    plotID = 2001;
    figure(plotID);
    set(plotID, 'Position', [0 400 500 500], 'defaultaxesfontsize', 10, 'defaulttextfontsize', 10, 'color', [1 1 1], 'PaperPositionMode', 'auto');
    grid on;
    hold on;
    % plot data points
    plot3(alpha_val, beta_val, Cm_val, 'ro'); % note that alpha_m = alpha, beta_m = beta, y = Cm
    view(az, el);
    ylabel('validation beta [rad]');
    xlabel('validation alpha [rad]');
    zlabel('validation C_m_{val} [-]');
    title('F16 CM(\alpha_{val}, \beta_{val}) validation set');
    % set fancy options for plotting 
    % print results to disk if printfigs = 1
    if (printfigs == 1)
        fpath = sprintf('fig_F16valdata3D');
        savefname = strcat(figpath, fpath);
        print(plotID, '-dpng', '-r300', savefname);
    end
    
    plotID = 2002;
    figure(plotID);
    set(plotID, 'Position', [400 400 500 500], 'defaultaxesfontsize', 10, 'defaulttextfontsize', 10, 'color', [1 1 1], 'PaperPositionMode', 'auto');
    grid on;
    hold on;
    % plot data points
    plot(alpha_val, beta_val, 'ro'); % note that alpha_m = alpha, beta_m = beta, y = Cm
    ylabel('validation beta [rad]');
    xlabel('validation alpha [rad]');
    title('F16 (\alpha_{val}, \beta_{val}) special validation set');
    % set fancy options for plotting 
    % print results to disk if printfigs = 1
    if (printfigs == 1)
        fpath = sprintf('fig_F16valdata');
        savefname = strcat(figpath, fpath);
        print(plotID, '-dpng', '-r300', savefname);
    end
end



